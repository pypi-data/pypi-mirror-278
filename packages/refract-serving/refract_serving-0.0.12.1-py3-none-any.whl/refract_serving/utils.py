# -*- coding: utf-8 -*-
import json
import logging
import sys
from datetime import datetime
import pickle
import os
from werkzeug.datastructures import FileStorage
import time
from mosaicml_serving.constants import Database
from uuid import uuid4
from mosaicml_serving.schema import MLModelRequestLogSchema
from mosaicml_serving.middlewares import close_db_connection
from mosaic_utils.ai.file_utils import pickle_loads, create_model_tar, save_model_data
import requests
import tempfile
import shutil
import platform
from mosaic_utils.ai.flavours import (
    keras,
    pytorch,
    sklearn,
    tensorflow,
    pyspark,
    spacy,
    pmml,
    xgboost,
)
from mosaic_utils.ai.file_utils import extract_tar, pickle_loads
from mosaicml_serving.constants import (
    Environment,
    Flavour,
    Headers,
    Model,
    MosaicBackend,
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


def retry_with_backoff(max_retries, sleep_seconds):
    """Create a retry decorator with backoff.

    This function returns a decorator that can be applied to other functions to add retry functionality.
    The decorator will retry the wrapped function a specified number of times with a backoff period
    between each attempt.

    Args:
        max_retries (int): The maximum number of times the wrapped function will be retried.
        sleep_seconds (float): The duration in seconds to wait between retry attempts.

    Returns:
        function: A decorator that can be applied to other functions to add retry functionality.

    Example:
        @retry_with_backoff(max_retries=3, sleep_seconds=2)
        def my_function():
            # Perform some operations that might fail
            # ...

    In the example above, `my_function` will be retried up to 3 times if it raises an exception.
    There will be a 2-second sleep between each retry attempt.
    """
    def decorator_retry(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Error occurred: {str(e)}")
                    retries += 1
                    if retries < max_retries:
                        logger.error(f"Retrying in {sleep_seconds} seconds...")
                        time.sleep(sleep_seconds)
                    else:
                        logger.error(f"Maximum retries reached. Giving up.")
                        raise
        return wrapper
    return decorator_retry


def get_loader(flavour):
    if flavour == Flavour.keras:
        return keras.load_model
    if flavour == Flavour.sklearn:
        return sklearn.load_model
    if flavour == Flavour.pytorch:
        return pytorch.load_model
    if flavour == Flavour.tensorflow:
        return tensorflow.load_model
    if flavour == Flavour.pyspark:
        return pyspark.load_model
    if flavour == Flavour.spacy:
        return spacy.load_model
    if flavour == Flavour.r:
        # R import specifically moved below as it will give error of rpy2 while deploying otherwise
        from mosaic_utils.ai.flavours import r

        return r.load_model
    if flavour == Flavour.pmml:
        return pmml.load_model
    if flavour == Flavour.xgboost:
        return xgboost.load_model


def uuid_generator():
    _uuid = uuid4()
    return str(_uuid)


def read_jwt():
    token = os.getenv(Environment.token_path) or os.path.expanduser("~/.token")
    with open(token) as f:
        jwt = f.read().strip("\n")
        return jwt


def get_headers():
    jwt = read_jwt()
    return {
        Headers.authorization: f"Token {jwt}",
        Headers.x_project_id: os.environ.get("PROJECT_ID"),
    }


def get_swagger_def_and_model_info(source):
    deployment_data = os.environ[Model.deployment_data]
    model_id, version_id = eval(deployment_data)["model_id"], eval(deployment_data)["version_id"]

    mosaic_model = get_model_info(model_id, version_id)

    # Create swagger_spec
    with open(
        os.getenv(
            Environment.mosaic_ai_serving_swagger,
            (os.path.join(os.path.dirname(__file__), "swagger_template.json")),
        ),
        "r",
    ) as f:
        swagger_spec_str = f.read()
    swagger_spec_str = (
        swagger_spec_str.replace("$SERVICE_NAME$", mosaic_model["name"])
        .replace("$SERVICE_VERSION$", version_id)
        .replace("$BASE_URL$", os.environ[Environment.base_url])
    )
    swagger_spec = json.loads(swagger_spec_str)

    try:
        schema = get_model_version_schema(model_id, version_id)
        swagger_spec["definitions"]["ServiceOutput"] = schema.get("output", {}).get(
            "output", {}
        )
        swagger_spec["definitions"]["ServiceInput"] = schema.get("input", {}).get(
            "input", {}
        )
    except Exception as ex:
        print(ex)
    finally:
        return swagger_spec, mosaic_model


# Add retry mechanism to the existing function
@retry_with_backoff(max_retries=5, sleep_seconds=60)
def get_model_info(model_id, version_id):

    url = MosaicBackend.server + MosaicBackend.model_info.format(ml_model_id=model_id)

    response = requests.get(url, headers=get_headers())
    mosaicml_model = response.json()
    version = {"version_id": version_id}
    model_info = {
        k: v
        for k, v in mosaicml_model.items()
        if k in ("id", "name", "flavour", "created_on", "created_by")
    }
    model_info.update(version)
    return model_info


# Add retry mechanism to the existing function
@retry_with_backoff(max_retries=5, sleep_seconds=60)
def get_model_version_schema(model_id, version_id):

    url = MosaicBackend.server + MosaicBackend.version_info.format(
        ml_model_id=model_id, version_id=version_id
    )
    response = requests.get(url, headers=get_headers())

    version = response.json()
    if version["schema"] is None:
        version["schema"] = {}

    return version["schema"]


def nlg_for_lime(lime_data):
    lime_feature = lime_data["list"]
    codelines = nlg_for_lime_shap_fi(feature_data=lime_feature)
    return codelines


def nlg_for_shap(shap_feature, mode):
    shap_feature_data = shap_feature["data"]
    predicted_value = shap_feature["predicted_value"]
    if mode == "classification":
        shap_feature_data = shap_feature_data[predicted_value]
        codelines = nlg_for_lime_shap_fi(feature_data=shap_feature_data)
    else:
        shap_feature_data = shap_feature_data[0]
        codelines = nlg_for_lime_shap_fi(feature_data=shap_feature_data)
    return codelines


def nlg_for_lime_shap_fi(feature_data):
    positive = []
    negative = []
    positive_contribution = dict((k, v) for k, v in feature_data.items() if v >= 0)
    if len(positive_contribution) > 0:
        positive.append("Top positively contributing features are :")
        for keys, value in dict(
            sorted(positive_contribution.items(), key=lambda i: i[1], reverse=True)
        ).items():
            positive.append("\u2022 {} has an impact of {:.4f}".format(keys, value))
    else:
        positive.append("No positively contributing features for this prediction")
    negative_contribution = dict((k, v) for k, v in feature_data.items() if v < 0)
    if len(negative_contribution) > 0:
        negative.append("\nTop negatively contributing features:\n")
        for keys, value in dict(
            sorted(negative_contribution.items(), key=lambda i: i[1])
        ).items():
            negative.append("\u2022 {} has an impact of {:.4f}".format(keys, value))
    else:
        negative.append("No negatively contributing features for this prediction")
    sum_of_coefficents = 0
    for keys, value in feature_data.items():
        sum_of_coefficents += value
    final_nlg = {
        "nlg": {
            "positive": positive,
            "negative": negative,
            "sum_of_coefficents": sum_of_coefficents,
        }
    }
    return final_nlg


def ensemble_model_list(dependent_model):
    """method to prepare the dependent models of ensemble model"""
    try:
        dep_model_id = dependent_model["model_id"]
        dep_version_id = dependent_model["version_id"]
        previous_dep_model_id = dependent_model["previous_model_id"]
        previous_dep_version_id = dependent_model["previous_version_id"]
        dep_model_name = dependent_model["name"]
        dep_flavour = dependent_model["flavour"]
        model_dir = download_dep_model(dep_model_id, dep_version_id)
        dep_model_dict = load_dep_model(
            model_dir,
            previous_dep_model_id,
            previous_dep_version_id,
            dep_model_name,
            dep_flavour,
        )
        return dep_model_dict
    except Exception as ex:
        print(ex)


def download_dep_model(model_id, version_id):
    """Download the dependent model from storage"""
    # download model from object storage server
    try:
        file_path = f"{os.getenv(Environment.mount_path)}/{model_id}/{version_id}/{'ml_model.tar.gz'}"
        model_data = FileStorage(open(file_path, "rb"))
        # write model to tar file
        temp_dir = tempfile.mkdtemp()
        tar_path = os.path.join(temp_dir, "ml_model.tar.gz")
        model_data.save(tar_path)
        # extract model file
        extract_tar(tar_path, temp_dir)
        # remove tar file
        os.unlink(tar_path)
        return temp_dir
    except Exception as ex:
        raise ex




def load_dep_model(model_dir, model_id, version_id, model_name, flavour):
    """load the dependent model"""
    final_dict = {}
    x_train = None
    loader = get_loader(flavour)
    model_file = os.path.join(model_dir, Model.model_file)
    scoring_func_file = os.path.join(model_dir, Model.scoring_func_file)
    x_train_func_file = os.path.join(model_dir, Model.x_train_func_file)
    model = loader(model_file)
    score = pickle_loads(scoring_func_file)
    if os.path.exists(x_train_func_file):
        x_train = pickle_loads(x_train_func_file)
        final_dict[version_id] = {
            "model_object": model,
            "score_object": score,
            "x_train": x_train,
        }
    else:
        final_dict[version_id] = {"model_object": model, "score_object": score}
    return final_dict


def get_model_metadata(ml_model_id, ml_version_id):
    headers = get_headers()
    url = MosaicBackend.server + MosaicBackend.version_info.format(
        ml_model_id=ml_model_id, version_id=ml_version_id
    )
    response = requests.get(url, headers=get_headers())
    if response.status_code != 200:
        raise Exception(response.json())
    model_info = json.loads(response.text)["model_info"]
    return model_info


# Add retry mechanism to the existing function
@retry_with_backoff(max_retries=5, sleep_seconds=60)
def update_deployment_status(
    deployment_id, deployment_status, deployment_strategy, deployment_data
):
    # changes to update the deployment status in ai backend
    url = MosaicBackend.server + MosaicBackend.deploy_status.format(
        deployment_id=eval(deployment_data)["deployment_id"]
    )
    data = {
        "deployment_status": deployment_status,
        "deployment_strategy": deployment_strategy,
        "deployment_data": deployment_data,
    }
    deploy_response_status = requests.get(url, headers=get_headers())
    url = MosaicBackend.server + MosaicBackend.deploy_status.format(
        deployment_id=deployment_id
    )
    requests.post(url, json=data, headers=get_headers())

def uuid_generator():
    """Method to generate uuid"""
    _uuid = uuid4()
    return str(_uuid)


def get_db_type():
    """Method to get db type"""
    url = Database.url
    db_type = url.split("+")[0]
    return db_type




def create_json_file(input_type, json_data, temp_dir):
    """Method to create json file"""
    with open(f"{temp_dir}/{input_type}.json", "w") as outfile:
        json.dump(json_data, outfile)
    return f"{temp_dir}/{input_type}.json"


def create_pickle_file(name, to_pickle_data, temp_dir):
    """Method to create pickle file"""
    with open(f"{temp_dir}/{name}.pkl", "wb") as outfile:
        pickle.dump(to_pickle_data, outfile)
    return f"{temp_dir}/{name}.pkl"


def upload_db_minio(
    ep,
    status,
    temp_dir,
    req_json,
    req_file,
    req_form,
    response_data,
    upload_logging_data,
    file_path,
    db_session,
):
    # support variables required
    deployment_data = os.environ[Model.deployment_data]
    model_id, version_id = (
        eval(deployment_data)["model_id"],
        eval(deployment_data)["version_id"],
    )
    score_api_hit_logger(
        response_data["request_id"], datetime.now(), "request_logging_nas", start=True
    )
    version_dir_file_path = os.getenv(Environment.mount_path) + "/" + f"{model_id}/{version_id}"

    # Creating files based on request_type
    if req_json is not None:
        request_data = req_json
        request_file_name = f"{response_data['request_id']}_request_data"
        request_data_file = create_json_file(request_file_name, request_data, temp_dir)
        obj_key_req = save_model_data(version_dir_file_path, request_data_file)

    if req_form != {}:
        request_file_name = f"{response_data['request_id']}_request_data"
        request_data_file = create_json_file(request_file_name, req_form, temp_dir)
        obj_key_req = save_model_data(version_dir_file_path, request_data_file)

    if req_file is not None:
        response_tar_file_name = f"{response_data['request_id']}_request_file"
        tar_path = create_model_tar(temp_dir, response_tar_file_name, file_path)
        obj_key_file = save_model_data(version_dir_file_path, tar_path)

    # Saving response data in form of file
    response_file_name = f"{response_data['request_id']}_response_data"
    response_data_file = create_json_file(response_file_name, response_data, temp_dir)
    obj_key_resp = save_model_data(version_dir_file_path, response_data_file)

    score_api_hit_logger(
        response_data["request_id"], datetime.now(), "request_logging_nas", end=True
    )

    # adding model info to database
    ml_schema = MLModelRequestLogSchema(strict=True)
    data, errors = ml_schema.load(upload_logging_data)
    from mosaicml_serving.models import MLModelRequestLog

    score_api_hit_logger(
        response_data["request_id"], datetime.now(), "request_logging_db", start=True
    )
    ml_model_request_log = MLModelRequestLog(**data)
    db_session.add(ml_model_request_log)
    db_session.commit()
    close_db_connection(db_session)
    score_api_hit_logger(
        response_data["request_id"], datetime.now(), "request_logging_db", end=True
    )


def convert_array_to_list_le(obj):
    import numpy as np

    if isinstance(obj, list):
        return obj
    elif isinstance(obj, np.ndarray):
        obj = obj.tolist()
        return obj
    else:
        return obj


def model_score_logger():
    logger.info("Model loaded for deployment")
    logger.info("Score function loaded for deployment")


def score_api_hit_logger(request_id, time, function, start=False, end=False):
    if start:
        if function == "score":
            logger.debug(
                "DEBUG- Score api hit for " + request_id + " Started : " + str(time)
            )
        if function == "request_logging_nas":
            logger.debug(
                "DEBUG- Request Logging - Dumping into nas location for "
                + request_id
                + " Started : "
                + str(time)
            )
        if function == "request_logging_db":
            logger.debug(
                "DEBUG- Request Logging - Database operation for storing request for "
                + request_id
                + " Started : "
                + str(time)
            )
    if end:
        if function == "score":
            logger.debug(
                "DEBUG- Score api hit for "
                + request_id
                + " ended successfully: "
                + str(time)
            )
        if function == "request_logging_nas":
            logger.debug(
                "DEBUG- Request Logging - Dumping into nas location for "
                + request_id
                + " ended : "
                + str(time)
            )
        if function == "request_logging_db":
            logger.debug(
                "DEBUG- Request Logging - Database operation for storing request for "
                + request_id
                + " ended : "
                + str(time)
            )


def uwsgi_workers_threads():
    cpu_limit = eval(os.environ[Model.deployment_data].replace("null", "None"))[
        "replica_cpu_limit"
    ]
    if cpu_limit[-1:] == "m":
        cpu_core = int(eval(cpu_limit[:-1]) / 1000)
    else:
        cpu_core = int(cpu_limit)
    workers = 2 * cpu_core + 1
    if os.environ[Model.flavour] == Flavour.pytorch and platform.python_version().startswith('3.8'):
        threads = 2 * int(os.cpu_count())
        workers = 1
    elif os.environ[Model.flavour] not in [Flavour.keras, Flavour.tensorflow, Flavour.r, Flavour.sas, Flavour.pytorch]:
        threads = 3
    else:
        threads = 1
    return workers, threads
def get_model_data():
    """Get model data from NAS volume"""
    try:
        file_path = f"{os.getenv(Environment.mount_path)}/{os.getenv(Model.download_url)}"
        model_data = FileStorage(open(file_path, "rb"))
        return model_data
    except Exception as ex:
        logger.exception(ex)
        raise ex

def trigger_cleanup():
    "cleanup tmp dir"
    try:
        logging.info("#Cleaning up the temparory data")
        tmpdir = os.getenv('TMPDIR', None)
        if tmpdir :
            root_dir = os.path.dirname(tmpdir)
            if (os.path.basename(os.path.dirname(root_dir))) == "user_temp":
                logging.info("deleting tmp dir : ")
                logging.info(tmpdir)
                shutil.rmtree(tmpdir)
                if len(os.listdir(root_dir)) == 0:
                    shutil.rmtree(root_dir)
    except Exception as ex:
        logging.info(ex)
        pass
