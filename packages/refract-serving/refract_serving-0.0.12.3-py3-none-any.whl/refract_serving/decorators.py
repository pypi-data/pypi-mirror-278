# -*- coding: utf-8 -*-
import os
from datetime import datetime
import logging
import tempfile
from flask import jsonify, request
from mosaicml_serving.utils import create_pickle_file
from mosaicml_serving.constants import Environment, Model
from mosaicml_serving.utils import uuid_generator
from mosaic_utils.ai.score.exceptions import MosaicException
from mosaic_utils.ai.file_utils import save_model_data

logger = logging.getLogger("mosaic_serving")


def feedback_request_logger(func):
    """
    function to generate request id and log data of every request for scoring function
    Args:
        func:
    Returns:

    """
    deployment_data = os.environ[Model.deployment_data]
    model_id, version_id = (
        eval(deployment_data)["model_id"],
        eval(deployment_data)["version_id"],
    )

    def feedback_logger():
        # calculating time and request id
        status_code = 200
        status = "Failure"
        request_id = uuid_generator()
        start_time = datetime.utcnow()
        try:
            response = func(request_id)
            if isinstance(response, tuple):
                response_score_pickled, response = response
                if response_score_pickled:
                    score_response_file = create_pickle_file(
                        request_id, response_score_pickled, tempfile.mkdtemp()
                    )
                    file_path = (
                        os.getenv(Environment.mount_path)
                        + "/"
                        + f"{model_id}/{version_id}"
                    )
                    save_model_data(file_path, score_response_file)

            response_data = response.get_json()
            status = "Success" if response else "Failure"
        except MosaicException as e:
            status_code = e.code
            response_data = e.message
        except Exception as e:
            status_code = 500
            response_data = str(e)
        end_time = datetime.utcnow()

        # creating upload logging data payload
        upload_logging_data = {
            "response_data": response_data,
            "model_id": model_id,
            "version_id": version_id,
            "request_id": request_id,
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "status": status,
            "feedback": "",
            "status_code": status_code,
        }
        return jsonify(
            {
                "data": response_data,
                "request_id": request_id,
                "upload_logging_data": upload_logging_data,
            }
        )

    return feedback_logger
