# -*- coding: utf-8 -*-
import os


class Environment:
    base_url = "BASE_URL"
    token_path = "TOKEN_PATH"
    mosaic_ai_server = "MOSAIC_AI_SERVER"
    mosaic_ai_serving_swagger = "MOSAIC_AI_SERVING_SWAGGER"
    ld_library_path = "LD_LIBRARY_PATH"
    r_home = "R_HOME"
    tz = "TZ"
    home = "HOME"
    uwsgi_workers = "WORKERS"
    uwsgi_threads = "THREADS"
    mount_path = "MOUNT_PATH"
    tmpdir = 'TMPDIR'





class Model:
    flavour = "MODEL_FLAVOUR"
    directory = "MODEL_DIRECTORY"
    download_url = "MODEL_DOWNLOAD_URL"
    init_script = "MODEL_INIT_SCRIPT"
    model_file = "ml_model"
    r_model_file = "model.rds"
    scoring_func_file = "scoring_func"
    r_scoring_func_file = "score.rds"
    input_type = "INPUT_TYPE"
    x_train_func_file = "x_train"
    model_list_file = "model_list"
    deployment_strategy = "DEPLOYMENT_STRATEGY"
    deployment_id = "DEPLOYMENT_ID"
    deployment_data = "DEPLOYMENT_DATA"
    scoring_func_file_sas = "score_func.sas"
    custom_predict_file = "custom_score"
    source = "SOURCE"


class Flavour:
    keras = "keras"
    sklearn = "sklearn"
    pytorch = "pytorch"
    tensorflow = "tensorflow"
    pyspark = "pyspark"
    spacy = "spacy"
    r = "r"
    pmml = "pmml"
    ensemble = "ensemble"
    sas = "sas"
    xgboost = "xgboost"

class ModelSource:
    mlflow = "mlflow"

class Database:
    url = "DATABASE_URL"
    use_connection_pooling = "DATABASE_USE_CONNECTION_POOLING"
    pool_size = "DATABASE_POOL_SIZE"
    pool_timeout = "DATABASE_POOL_TIMEOUT"
    pool_recycle = "DATABASE_POOL_RECYCLE"
    connect_args = "DATABASE_CONNECT_ARGS"
    pool_pre_ping = "DATABASE_POOL_PRE_PING"


class MosaicBackend:
    server = os.getenv(
        Environment.mosaic_ai_server, "http://localhost:5000/registry/api"
    )
    feedback_post_request = "/v1/feedback"
    feedback = "/v1/feedback/{request_id}"
    model_info = "/v1/ml-model/{ml_model_id}"
    version_info = "/v1/ml-model/{ml_model_id}/version/{version_id}"
    request_logger = "/v1/request-logger"
    request_metric = "/v1/{request_id}/add-request-metric"
    deploy_status = "/v1/ml-model/deploy/{deployment_id}"


class Headers:
    authorization = "Authorization"
    x_auth_userid = "X-Auth-Userid"
    x_auth_username = "X-Auth-Username"
    x_auth_email = "X-Auth-Email"
    x_auth_given_name = "X-Auth-Given-Name"
    x_auth_family_name = "X-Auth-Family-Name"
    x_project_id = "X-Project-Id"
    PROJECT_ID = "PROJECT_ID"


class CRANPackageList:
    pre_installed_packages = [
        "base",
        "boot",
        "class",
        "cluster",
        "codetools",
        "compiler",
        "datasets",
        "evaluate",
        "foreign",
        "graphics",
        "grDevices",
        "grid",
        "IRkernel",
        "KernSmooth",
        "lattice",
        "MASS",
        "Matrix",
        "methods",
        "mgcv",
        "mosaicrml",
        "nlme",
        "nnet",
        "parallel",
        "pbdZMQ",
        "compareDF",
        "rlang",
        "rpart",
        "spatial",
        "splines",
        "stats",
        "stats4",
        "survival",
        "tcltk",
        "tools",
        "utils",
    ]


class ExplainableAIMode:
    classification = "classification"
    regression = "regression"


class DeploymentStatus:
    """ml model deployment status"""

    Deploying = "DEPLOYING"
    Deployed = "DEPLOYED"
    Failed = "FAILED"


class ModelSAS:
    """SAS moswl deployments"""

    model_path = "/notebooks/notebooks/"
    libname = "mosaic"
    request_obj = "request_obj"
    request_csv = "request_obj.csv"
    predicted_obj = "predicted_data"
    predicted_csv = "predicted_data.csv"
    sas_format = ".sas7bdat"
    score_obj = "scoring_obj"
    regex_to_fetch_errors = r"(^REFRACTERROR).*?((\n|END))"
