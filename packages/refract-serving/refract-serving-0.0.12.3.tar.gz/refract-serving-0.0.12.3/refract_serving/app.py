# -*- coding: utf-8 -*-
import copy
import json
import inspect
import os
import traceback
import shutil
import logging
import numpy as np
import requests
import tempfile
import re
from flasgger import Swagger
from flask import Flask, Response, jsonify, request, send_from_directory
from mosaic_utils.ai.file_utils import pickle_loads, create_model_tar
from mosaic_utils.ai.score.encoder import ScoreResponseEncoder
from mosaicml_serving.middlewares import create_db_connection
from mosaicml_serving.utils import (
    uuid_generator,
    get_model_metadata,
    upload_db_minio,
    model_score_logger,
    score_api_hit_logger,
)
from werkzeug.exceptions import UnsupportedMediaType
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from mosaicml_serving.constants import (
    Environment,
    Model,
    MosaicBackend,
    CRANPackageList,
    Flavour,
    DeploymentStatus,
    ModelSAS,
    ModelSource
)
from mosaicml_serving.decorators import feedback_request_logger
from mosaicml_serving.schema import FeedbackSchema
from mosaicml_serving.utils import (
    get_headers,
    get_loader,
    get_swagger_def_and_model_info,
    nlg_for_lime,
    nlg_for_shap,
    ensemble_model_list,
    update_deployment_status,
    convert_array_to_list_le,
)
from mosaic_utils.ai.score.exceptions import MosaicException
import sys
import matplotlib
from datetime import datetime

# define flask app
application = Flask(__name__)


# default handler
def simple(env, resp):
    return [b"Invalid Url"]


application.wsgi_app = DispatcherMiddleware(
    simple, {os.environ[Environment.base_url]: application.wsgi_app}
)

LOG_LEVEL = os.environ["LOG_LEVEL"]
# define stream handler
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(LOG_LEVEL)

logger = logging.getLogger("mosaic_serving")
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream_handler)
extra = {"project_id": None, "request_id": None}
logger = logging.LoggerAdapter(logger, extra)


@application.route("/", methods=["GET"])
def index():
    return Response(json.dumps(model_info), status=200, mimetype="application/json")


@application.route("/ping")
def ping():
    """health check api"""
    return "Service is up!"


@application.after_request
def response_processor(response):
    """Function automatically called after every request used for request log"""

    ep = request.endpoint
    status = response.status_code
    content_type = request.headers.get('Content-Type', '')
    # check for score function endpoint
    if ep == "feedback_logger":
        # storing local variables here as context is lost in call on close
        # local variables for file, formdata, json
        temp_dir = tempfile.mkdtemp()

        req_file = request.files.get("file1")
        file_path = None
        if req_file:
            req_file.stream.seek(0)
            file_path = temp_dir + "/" + req_file.filename
            req_file.save(file_path)
            req_json = None
        elif 'application/json' in content_type:
            req_json = request.get_json()
        req_form = request.form.to_dict()
        response_data = response.get_json()

        upload_logging_data = response_data["upload_logging_data"]
        response.json.pop("upload_logging_data")

        # altering response to for failure and removing excess upload data
        if upload_logging_data["status"] == "Failure":
            response = Response(
                upload_logging_data["response_data"], upload_logging_data["status_code"]
            )
        else:
            res = copy.deepcopy(response_data)
            del res["upload_logging_data"]
            response.set_data(json.dumps(res))

        deployment_data = eval(os.getenv(Model.deployment_data))
        retention_policy = deployment_data.get("retention_policy")
        if retention_policy is None:
            retention_policy = "true"
        if retention_policy.lower() == "true":
            # uploading file to minio and storing records in DB
            upload_db_minio(
                ep,
                status,
                temp_dir,
                req_json,
                req_file,
                req_form,
                response_data,
                upload_logging_data,
                file_path,
                create_db_connection(),
            )
        shutil.rmtree(temp_dir)

    return response


@application.route("/score", methods=["POST"])
@feedback_request_logger
def score(request_id):
    """scoring api"""
    try:
        score_api_hit_logger(request_id, datetime.now(), "score", start=True)

        if flavour == "r":
            # R import specifically moved below as it will give error of rpy2 while deploying otherwise
            from mosaic_utils.ai.flavours.r import load_r_json
            from rpy2.robjects import r

            input_type = os.environ[Model.input_type]
            response_temp = tempfile.mkdtemp() + "/"
            file_temp = response_temp + uuid_generator() + ".txt"
            if input_type == "json":
                logger.debug(request.json)
                response = scoring(model, load_r_json(request.json))
                logger.debug(response)
                r.write(response, file=file_temp)
            elif input_type == "file":
                file = request.files.get("file1")
                temp_file = tempfile.mkdtemp()
                file.save(os.path.join(temp_file, file.filename))
                tmp_file_path = os.path.join(temp_file, file.filename)
                logger.debug(tmp_file_path)
                response = scoring(model, tmp_file_path)
                logger.debug(response)
                shutil.rmtree(temp_file)
                r.write(response, file=file_temp)
            with open(file_temp) as f:
                final_response = f.read()
            shutil.rmtree(response_temp)

            score_api_hit_logger(request_id, datetime.now(), "score", end=True)

            return jsonify(final_response)
        elif flavour == Flavour.ensemble:
            if use_score_v2:
                score_response_object = scoring_ensemble.score(
                    model_dict, request, dry_run=False
                )
                response_serialized = json.loads(
                    json.dumps(score_response_object, cls=ScoreResponseEncoder)
                )

                score_api_hit_logger(request_id, datetime.now(), "score", end=True)
                return score_response_object, jsonify(response_serialized)
            else:
                response = scoring_ensemble(model_dict, request)

                score_api_hit_logger(request_id, datetime.now(), "score", end=True)
                return jsonify(response)

        elif flavour == Flavour.sas:
            response = scoring_sas(request)
            score_api_hit_logger(request_id, datetime.now(), "score", end=True)

            return jsonify(response)
        else:
            if use_score_v2:
                score_response_object = scoring_func.score(
                    model, request, dry_run=False
                )
                response_serialized = json.loads(
                    json.dumps(score_response_object, cls=ScoreResponseEncoder)
                )

                score_api_hit_logger(request_id, datetime.now(), "score", end=True)
                return score_response_object, jsonify(response_serialized)
            else:
                response = scoring_func(model, request)
                score_api_hit_logger(request_id, datetime.now(), "score", end=True)
                return jsonify(response)
        return jsonify(response)
    # exception handling
    except UnsupportedMediaType as error:
        logger.exception((str(type(error)) + traceback.format_exc()))
        logger.debug((str(type(error)) + traceback.format_exc()))
        raise Exception(f"Invalid Payload. Input must be a json object or a file : {str(error)}")
    except MosaicException as error:
        raise error
    except Exception as error:
        a = []
        a = str(traceback.format_exc()).split("\n")
        logger.info("Score api hit for " + request_id + " failed")
        logger.debug("Score api hit for " + request_id + " failed")
        logger.exception((str(type(error)) + traceback.format_exc()))
        logger.debug((str(type(error)) + traceback.format_exc()))
        raise Exception(
            "Invalid Payload"
            + "\n\nDetails:\n"
            + str(type(error))
            + "\nError in Line\n"
            + traceback.format_exc()
        )


def if_whatif_and_request(request_data, temp_dir):
    from mosaicml_serving.explainableai import local_interpretation

    model_id, version_id, _ = os.environ["MODEL_DOWNLOAD_URL"].split("/")
    if not model_metadata:
        model_info = get_model_metadata(model_id, version_id)
    else:
        model_info = model_metadata
    if "data" not in model_info:
        model_info["data"] = x_train
    if "whatif" in request_data.keys():
        model_info["model"] = model
        model_info["input"] = request_data["whatif"]
        model_info["custom_score"] = request_data["custom_score"]
        expai_graphs = local_interpretation.LocalInterpretation(model_info)
        lime_data = expai_graphs.get_lime_data()
        try:
            nlg = nlg_for_lime(lime_data)
            lime_data.update(nlg)
        except Exception as e:
            lime_data.update(
                {"nlg": {"positive": [], "negative": [], "sum_of_coefficents": ""}}
            )
        return lime_data
    else:
        request_data["request_id"] = request_data["request"]
        request_data.update(model_info)
        request_data["temp_dir"] = temp_dir
        return request_data


@application.route("/explainable-ai", methods=["POST"])
def expi():
    """
    Method to plot LOCAL INTERPRETATION graphs
    :return: Tar file of graphs
    """
    from mosaicml_serving.explainableai import local_interpretation

    try:
        # Creating temporary directory
        temp_dir = tempfile.mkdtemp()
        # Fetching JSON data
        request_data = request.get_json()
        if isinstance(x_train, np.ndarray) or isinstance(x_train, list):
            request_data.update({"model": model, "temp_dir": temp_dir, "data": x_train})
        else:
            request_data.update({"model": model, "temp_dir": temp_dir})

        request_data.update({"custom_score": custom_predict})

        if "whatif" in request_data.keys():
            return if_whatif_and_request(request_data, temp_dir)

        if "request" in request_data.keys():
            request_data = if_whatif_and_request(request_data, temp_dir)

        # Plotting LOCAL INTERPRETATION graphs
        request_data["data"] = x_train
        request_data["feature_names"] = x_train.columns.tolist()
        expai_graphs = local_interpretation.LocalInterpretation(request_data)
        expai_graphs.lime_plots()
        expai_graphs.shap_plots()
        lime_data = expai_graphs.get_lime_data()
        try:
            nlg = nlg_for_lime(lime_data)
            lime_data.update(nlg)
        except Exception as e:
            lime_data.update(
                {"nlg": {"positive": [], "negative": [], "sum_of_coefficents": ""}}
            )
        shap_data = expai_graphs.get_shap_data()
        try:
            shap_feature = shap_data["feature"]
            nlg_shap = nlg_for_shap(shap_feature, request_data["mode"])
            shap_feature.update(nlg_shap)
        except Exception as e:
            shap_feature = shap_data["feature"]
            shap_feature.update(
                {"nlg": {"positive": [], "negative": [], "sum_of_coefficents": ""}}
            )
        exp_data = {}
        exp_data.update({"lime": lime_data})
        exp_data.update({"shap_feature": shap_data["feature"]})
        exp_data.update({"shap_decision": shap_data["decision"]})
        exp_data["shap_feature"]["expected_value"] = convert_array_to_list_le(
            exp_data["shap_feature"]["expected_value"]
        )
        exp_data["shap_feature"]["predicted_value"] = convert_array_to_list_le(
            exp_data["shap_feature"]["predicted_value"]
        )
        for key, value in exp_data["shap_decision"]["data"][0].items():
            exp_data["shap_decision"]["data"][0][key] = convert_array_to_list_le(value)
        exp_data["shap_decision"]["expected_value"] = convert_array_to_list_le(
            exp_data["shap_decision"]["expected_value"]
        )
        exp_data["shap_decision"]["predicted_value"] = convert_array_to_list_le(
            exp_data["shap_decision"]["predicted_value"]
        )
        # Creating tar
        create_model_tar(
            temp_dir,
            "ml_model",
            f"{temp_dir}/shap_plot.png",
            f"{temp_dir}/lime_plot.png",
        )
        # Creating Payload for storing images in database
        payload = {
            "request_id": request_data["request_id"],
            "exp_data": json.dumps(exp_data),
        }
        multipart_form_data = {"expai_tar": open(f"{temp_dir}/ml_model.tar.gz", "rb")}

        url = MosaicBackend.server + MosaicBackend.request_metric.format(
            request_id=request_data["request_id"]
        )
        requests.post(
            url, data=payload, files=multipart_form_data, headers=get_headers()
        )

        return send_from_directory(temp_dir, "ml_model.tar.gz", as_attachment=True)
    except Exception as error:
        logger.exception((str(type(error)) + traceback.format_exc()))
        logger.debug((str(type(error)) + traceback.format_exc()))
        raise Exception(error)


@application.errorhandler(Exception)
def error_handler(error):
    """Custom error handler"""
    error = str(error)
    return Response(error, status=500)


# @application.errorhandler(InternalServerError)
# def error_handler(error):
#     """ 500 error handler """
#     error = str(error)
#     return Response(error, status=500)


def scoring_sas(request):
    import pandas as pd
    from pandas.io.json import json_normalize
    import saspy
    import glob

    if request.json:
        request_data = request.json
        if "payload" not in request_data.keys() or len(request_data["payload"]) == 0:
            raise MosaicException("Invalid or empty request data", 400)
        df = json_normalize(request_data["payload"])
    if request.files:
        tar_file = request.files.get("file1")
        if not tar_file.filename.endswith(".csv"):
            raise MosaicException("Invalid file type. Please provide a CSV file", 400)

        tar_file.save(os.path.join(ModelSAS.model_path, tar_file.filename))
        df = pd.read_csv(os.path.join(ModelSAS.model_path, tar_file.filename))
    try:
        path = os.path.join(ModelSAS.model_path, uuid_generator()) + "/"
        os.makedirs(path)
        sas_session.saslib(ModelSAS.libname, path=path)
        sas_session.df2sd(df, ModelSAS.request_obj, ModelSAS.libname)
        score_func_file = glob.glob(ModelSAS.model_path + ModelSAS.score_obj + "*")
        shutil.copy(score_func_file[0], path)
        code = open(scoring_func).read()
        ps = sas_session.submit(code)
        prediction_df = sas_session.sd2df(ModelSAS.predicted_obj, ModelSAS.libname)
        if prediction_df is None:
            logger.debug("THE PRIDICTION DICT IS EMPTY : ")
            logger.debug("SAS LOGS : ")
            logger.debug(ps["LOG"])
            matches = re.finditer(
                ModelSAS.regex_to_fetch_errors,
                str(ps.get("LOG", "")),
                re.MULTILINE | re.IGNORECASE,
            )
            for matchNum, match in enumerate(matches, start=1):
                message_raw = match.group()
                if message_raw:
                    shutil.rmtree(path)
                    message_splits = message_raw.replace("REFRACTERROR", "").split("|")
                    if len(message_splits) == 2:
                        custom_exception_message = str(message_splits[1])
                        raise MosaicException(
                            custom_exception_message, message_splits[0]
                        )
                    else:
                        raise MosaicException(message_raw, 400)
            raise MosaicException("Internal Server Error : " + str(ps["LOG"]), 400)

        prediction_df = prediction_df.where(prediction_df.notnull(), None)
        prediction = prediction_df.to_dict("r")
        shutil.rmtree(path)
        logger.debug("\n ## SAS Execution Logs : ")
        logger.debug(ps.get("LOG", ""))
        return prediction
    except MosaicException as e:
        raise e
    except Exception as e:
        raise Exception(
            "Some issue with processing the request."
            "Please check your score function or your payload format"
        )


@application.route("/feedback", methods=["PUT"])
def feedback():
    """feedback api"""
    try:
        _schema = FeedbackSchema(strict=True)
        data, _ = _schema.load(request.json)
        if data["feedback"].lower() not in ("yes", "no"):
            return Response("Please provide feedback as YES or NO", status=412)
        url = MosaicBackend.server + MosaicBackend.feedback.format(
            request_id=data["request_id"]
        )
        try:
            response = requests.put(
                url, json={"feedback": data["feedback"].lower()}, headers=get_headers()
            )
            response.raise_for_status()
        except Exception as e:
            return jsonify(response.json()), 400
        return Response("Feedback Captured", status=200)
    except Exception as error:
        return Response(str(error), status=400)
