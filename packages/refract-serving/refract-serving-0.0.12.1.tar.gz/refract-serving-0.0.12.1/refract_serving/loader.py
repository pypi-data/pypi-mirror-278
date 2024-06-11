import os

# placeholders for model and scoring_fun
global model, scoring_func, model_info, application, scoring, x_train, model_dict, scoring_ensemble, model_metadata, use_score_v2, sas_session, flavour
model = None
scoring_func = None
scoring = None
model_info = {}
x_train = None
model_dict = {}
scoring_ensemble = None
model_metadata = None
use_score_v2 = False
sas_session = None
flavour = os.environ[Model.flavour]
# global var custom_predict
custom_predict = None
matplotlib.use("agg")

try:
    if flavour == "pyspark":
        os.environ["PYSPARK_PYTHON"] = "/opt/conda/bin/python"
        os.environ["PYSPARK_DRIVER_PYTHON"] = "/opt/conda/bin/python"
        from pyspark.sql import SparkSession

        spark = SparkSession.builder.appName(__name__).getOrCreate()
    loader = get_loader(flavour) if flavour != Flavour.ensemble else ""
    model_dir = os.environ[Model.directory]
    if flavour == "r":
        # R import specifically moved below as it will give error of rpy2 while deploying otherwise
        from mosaic_utils.ai.flavours.r import (
            load_model,
            get_r_packages,
            load_r_packages,
            check_pre_installed_packages,
        )

        model_file = os.path.join(model_dir, Model.r_model_file)
        scoring_func_file = os.path.join(model_dir, Model.r_scoring_func_file)
        model = loader(model_file)
        scoring = loader(scoring_func_file)
        package_list, version_list = get_r_packages()
        cran_package_list = CRANPackageList.pre_installed_packages
        pkg_list = check_pre_installed_packages(
            package_list, version_list, cran_package_list
        )
        p_list = [package["name"] for package in pkg_list]
        logger.info("Starting - loading of packages")
        load_r_packages(p_list)
        logger.info("Packages loaded successfully")

    elif flavour == Flavour.ensemble:
        model_file = os.path.join(model_dir, Model.model_file)
        scoring_func_file = os.path.join(model_dir, Model.scoring_func_file)
        model_list_file = os.path.join(model_dir, Model.model_list_file)
        model = pickle_loads(model_file)
        scoring_ensemble = pickle_loads(scoring_func_file)
        if scoring_func and inspect.isclass(scoring_func):
            use_score_v2, scoring_ensemble = True, scoring_ensemble()
        model_dict = {}
        if os.path.exists(model_list_file):
            model_list = pickle_loads(model_list_file)
        if model_list and len(model_list) > 0:
            for dependent_model in model_list:
                dep_model_dict = ensemble_model_list(dependent_model)
                model_dict.update(dep_model_dict)
    elif flavour == Flavour.sas:
        import saspy

        scoring_func = os.path.join(model_dir, Model.scoring_func_file_sas)
        sas_session = saspy.SASsession(results="HTML")
    else:

        if os.environ["SOURCE"] == ModelSource.mlflow:
            model_file = os.path.join(model_dir, "model.pkl")
            scoring_func_dir = os.path.dirname(model_dir)
            scoring_func_file = os.path.join(scoring_func_dir, "scoring_func")
            model = loader(model_file)
            scoring_func = pickle_loads(scoring_func_file)
        else:
            model_file = os.path.join(model_dir, Model.model_file)
            scoring_func_file = os.path.join(model_dir, Model.scoring_func_file)
            x_train_func_file = os.path.join(model_dir, Model.x_train_func_file)
            if os.path.exists(x_train_func_file):
                x_train = pickle_loads(x_train_func_file)
                model_id, version_id, _ = os.environ["MODEL_DOWNLOAD_URL"].split("/")
            if model is None:
                model = loader(model_file)
                scoring_func = pickle_loads(scoring_func_file)
            if scoring_func and inspect.isclass(scoring_func):
                use_score_v2, scoring_func = True, scoring_func()
    model_score_logger()

    swagger_schema, model_info = get_swagger_def_and_model_info(os.environ["SOURCE"])
    application.config["SWAGGER"] = swagger_schema
    swagger = Swagger(application)
    # changes to update the deployment status in ai backend

    update_deployment_status(
        os.environ[Model.deployment_id],
        DeploymentStatus.Deployed,
        os.environ[Model.deployment_strategy],
        os.environ[Model.deployment_data],
    )
    logger.debug("Current Deployment Status " + DeploymentStatus.Deployed)
    logger.info("Current Deployment Status " + DeploymentStatus.Deployed)

except Exception as error:
    # changes to update the deployment status in ai-backend
    update_deployment_status(
        os.environ[Model.deployment_id],
        DeploymentStatus.Failed,
        os.environ[Model.deployment_strategy],
        os.environ[Model.deployment_data],
    )
    logger.info("Current Deployment Status " + DeploymentStatus.Failed)
    logger.debug("Current Deployment Status " + DeploymentStatus.Failed)
    logger.exception((str(type(error)) + traceback.format_exc()))
    logger.debug((str(type(error)) + traceback.format_exc()))
