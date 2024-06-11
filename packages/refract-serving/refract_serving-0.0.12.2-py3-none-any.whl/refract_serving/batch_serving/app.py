# -*- coding: utf-8 -*-
import os
import pandas as pd
from datetime import datetime
import requests
from snowflake.snowpark.session import Session
from mosaic_utils.ai.file_utils import pickle_loads
from constants import ModelConstants, Flavour, Model, CRANPackageList, ModelSource
from utils import download_model, get_loader


def main():
    global model, scoring_func, model_info, application, scoring, model_dict, scoring_ensemble, use_score_v2, flavour
    model = None
    scoring_func = None
    scoring = None
    model_info = {}
    model_dict = {}
    scoring_ensemble = None
    use_score_v2 = False
    sas_session = None

    flavour = os.getenv(Model.flavour)
    input_file = "/data/" + os.getenv("reference_data_path")
    # output_path = "/data/" + os.getenv("output_data_path", "prediction.csv")
    output_path = os.getenv("output_path")
    data_source = os.getenv("data_source")
    write_strategy = os.getenv("write_strategy")
    # flavour = "sklearn"
    # input_file = "models/fifa.csv"
    # output_path = "models/fifa_1.csv"

    model_tar_path = ModelConstants.MODELS_PATH
    print("******************")
    print("model_path", model_tar_path)
    print("model_flavour", flavour)
    print("input_file", input_file)
    print("output_path", output_path)
    print("data_source", data_source)
    print("write_strategy - ", write_strategy)
    print("******************")

    model_source = os.getenv("source")
    print("model_source", model_source)

    run_id = os.getenv("run_id")
    print("run_id", run_id)



    try:
        if model_source == "mlflow":
            print('inside mlflow code for batch deployment')

            loader = get_loader(flavour) if flavour != Flavour.ensemble else ""
            model_dir = model_tar_path
            print('inside mlflow code for batch deployment')
            model_file = os.path.join(model_tar_path, "model.pkl")
            scoring_func_dir = os.path.dirname(model_dir)
            scoring_func_file = os.path.join(scoring_func_dir, "scoring_func")
            model = loader(model_file)
            scoring_func = pickle_loads(scoring_func_file)
            print('model file and score file loaded')
        else:
            model_dir = download_model(model_tar_path)

            # model_file = os.path.join(model_path, ModelConstants.MODEL_FILE)
            # scoring_func_file = os.path.join(model_path, ModelConstants.SCORING_FUN)

            loader = get_loader(flavour) if flavour != Flavour.ensemble else ""

            # model = loader(model_file)
            # scoring_func = pickle_loads(scoring_func_file)

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
                load_r_packages(p_list)

            elif flavour == Flavour.sas:
                import saspy

                scoring_func = os.path.join(model_dir, Model.scoring_func_file_sas)
                sas_session = saspy.SASsession(results="HTML")
            else:
                if os.getenv("SOURCE") == ModelSource.mlflow:
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
                        # model_id, version_id, _ = os.environ["MODEL_DOWNLOAD_URL"].split("/")
                    if model is None:
                        model = loader(model_file)
                        # scoring_func = pickle_loads(scoring_func_file)
                    # if scoring_func and inspect.isclass(scoring_func):
                    #     use_score_v2, scoring_func = True, scoring_func()

    except Exception as error:
        print("Error occurred ", error)

    if data_source.lower() == 'local data files':
        data, result = file_prediction(model, input_file)
        write_result_file(data, result, write_strategy, input_file, output_path)
    if data_source.lower() == 'refract datasets':
        data, result = db_prediction(model, scoring_func)
        # write_result_db("not availble in refracio")
        write_strategy = 'New table' if write_strategy == 'Same table' else write_strategy
        write_result_db(data, result, write_strategy, input_file, output_path)

    # send notification send notification send notification send notification


def file_prediction(model, input_file):
    import joblib

    # Step 1: Read the CSV file
    data = pd.read_csv(input_file)

    # Step 2: Load the pre-trained model
    model = model

    # Step 3: Create an empty list to store predictions
    predictions = []

    # Step 4: Iterate through each row and make predictions
    # for index, row in data.iterrows():
    #     # Assuming 'features' is the name of the input features used for prediction
    #     features = row[column_names].values  # Replace with your feature names
    #     prediction = model.predict(features[-16:])
    #     predictions.append(prediction[0])  # Append the prediction to the list

    # OR Step 4: make predictions
    # print("csv data:- ", data)
    print("model object:- ", model)
    predictions = model.predict(data)

    print("predictions", predictions)
    print("predictions type", type(predictions))
    print("data, predictions -", data, predictions)

    return data, predictions


def write_result_file(data, predictions, write_strategy, input_file, output_path):
    print("Inside write_result:", write_strategy, output_path)
    print("data in write_result_file - ", data)
    # Step 5: Create a new DataFrame with the predictions

    run_id = output_path.split("/")[-1]
    data['Prediction'] = predictions
    data['Run_id'] = run_id

    try:
        if write_strategy == 'Same table':
            path = input_file
            write_data = data
        elif write_strategy == 'New table':
            path = os.path.join(output_path, f"prediction_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
            write_data = data
        elif write_strategy == 'New prediction table':
            path = os.path.join(output_path, f"prediction_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
            write_data = pd.DataFrame({'Prediction': predictions, 'Run_id': run_id})
        else:
            path = input_file
            write_data = pd.DataFrame([])
        print("Final write_data - ", write_data)
        print("Final path - ", path)
        write_data.to_csv(path, index=False)
    except Exception as error:
        print("Error from write_data block", error)


def db_prediction(model, scoring_func):
    # read db_configs
    # conect to db
    # read data
    # run predictions
    # write predictions to db
    # send notification
    # from refractio import get_dataframe
    from refractio import snowflake

    # To get snowflake connection object with a default snowflake connection created by the user, if available.
    # snowflake.get_connection()

    # To read a specific dataset published from a snowflake connection
    data = snowflake.get_dataframe(os.getenv('reference_data_path').upper())
    print(data)

    # Step 2: Load the pre-trained model
    model = model

    # Step 3: Create an empty list to store predictions
    predictions = []

    # Step 4: Iterate through each row and make predictions
    # print("csv data:- ", data)
    print("model object:- ", model)
    predictions = model.predict(data)

    print("predictions", predictions)
    print("predictions type", type(predictions))
    print("data, predictions -", data, predictions)

    return data, predictions


def write_result_db(data, predictions, write_strategy, input_file, output_path):
    print("Inside write_result:", write_strategy, output_path)
    print("data in write_result_file - ", data)

    run_id = output_path.split("/")[-1]
    data['Prediction'] = predictions
    data['Run_id'] = run_id

    try:
        url = f"http://fdc-project-manager:80/project-manager/connections/api/External/v2/external/getConnConfig/" \
              f"{os.getenv('reference_data_path')}/refract_user/{os.getenv('PROJECT_ID')}"

        connection_details = requests.get(url, verify=False).json()

        connection_parameters = dict(user=connection_details["params"]["READER"].get("user"),
                                     password=connection_details["params"]["READER"].get("password"),
                                     account=connection_details["params"]["READER"].get("accountId"),
                                     database=connection_details["params"]["READER"].get("database"),
                                     role=connection_details["params"]["READER"]["role"],
                                     cloudPlatform=connection_details["params"]["READER"]["cloudPlatform"],
                                     schema=connection_details["params"]["READER"].get("schema"),
                                     wareHouse=connection_details["params"]["READER"]["wareHouse"],
                                     region=connection_details["params"]["READER"]["region"] + ".gcp")

        session = Session.builder.configs(connection_parameters).create()

        if write_strategy == 'New table':
            write_data = data
        elif write_strategy == 'New prediction table':
            write_data = pd.DataFrame({'Prediction': predictions, "Run_id": run_id})
        else:
            write_data = data

        new_table_name = f"prediction_{run_id}"
        session.write_pandas(write_data, new_table_name, auto_create_table=True, overwrite=True)
        print("New table created - ", new_table_name)
    except Exception as error:
        print("Error from write db block", error)


if __name__ == "__main__":
    main()
