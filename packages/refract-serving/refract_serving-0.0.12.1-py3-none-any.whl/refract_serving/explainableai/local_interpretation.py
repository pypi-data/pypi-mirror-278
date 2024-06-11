# -*- coding: utf-8 -*-

import shap
from skater.core.local_interpretation.lime.lime_tabular import LimeTabularExplainer
from collections import OrderedDict
import numpy as np
from mosaicml_serving.constants import ExplainableAIMode


class LocalInterpretation:
    def __init__(self, expai_data):
        self.expai_data = expai_data

    def custom_regressor(self, x_test):
        predictions = self.expai_data["model"].predict(x_test)
        return predictions.reshape(1, -1)[0]

    def predict_function(self, mode, deep_learning=False):
        if mode == "regressor":
            mode = "regression"
        elif mode == "classifier":
            mode = "classification"

        if self.expai_data["custom_score"] is not None:
            return self.expai_data["custom_score"]

        elif mode == ExplainableAIMode.classification:
            try:
                if self.expai_data["model"].predict_proba:
                    predict_fn = self.expai_data["model"].predict_proba
            except:
                predict_fn = self.expai_data["model"].decision_function
            return predict_fn
        elif mode == ExplainableAIMode.regression:
            if deep_learning is True:
                return self.custom_regressor
            else:
                return self.expai_data["model"].predict
        else:
            return "Invalid mode"

    def get_explainer(self):
        """
        Method to create explainer
        :return:
        """
        x_test_array = np.array(self.expai_data["data"])
        if isinstance(self.expai_data["input"], list):
            self.expai_data["input"] = np.array(self.expai_data["input"])
        explainer = LimeTabularExplainer(
            x_test_array,
            feature_names=self.expai_data["feature_names"],
            class_names=self.expai_data["target_names"],
            verbose=True,
            mode=self.expai_data["mode"],
        )
        return explainer, x_test_array

    def lime_plots(self):
        """
        Method to plot LIME graphs
        :return:
        """
        explainer, x_test_array = self.get_explainer()
        explainer.explain_instance(
            self.expai_data["input"],
            self.predict_function(
                self.expai_data["mode"], self.expai_data["deep_learning_model"]
            ),
            num_features=self.expai_data["number_of_features"],
        ).as_pyplot_figure().savefig(f"{self.expai_data['temp_dir']}/lime_plot.png")
        return "Graphs plotted successfully"

    def converter_tuple(self, tuple_list):
        tuple_dict = {}
        for field, value in tuple_list:
            tuple_dict.update({field: value})
        return tuple_dict

    def get_lime_data(self):
        """
        Method to fetch lime data
        :return:
        """
        explainer, x_test_array = self.get_explainer()
        exp = explainer.explain_instance(
            self.expai_data["input"],
            self.predict_function(
                self.expai_data["mode"], self.expai_data["deep_learning_model"]
            ),
            num_features=self.expai_data["number_of_features"],
            labels=self.expai_data["target_names"],
            top_labels=len(self.expai_data["target_names"]),
        )
        lime_data = {}
        lime_data.update({"class": exp.class_names})
        if self.expai_data["mode"] == "regression":
            lime_data.update({"list": self.converter_tuple(exp.as_list())})
            lime_data.update({"predicted_value": self.check_numpy(exp.predicted_value)})
            lime_data.update({"min_value": self.check_numpy(exp.min_value)})
            lime_data.update({"max_value": self.check_numpy(exp.max_value)})
            tuple_list = exp.as_map()[1]
            intercept = exp.intercept
            intercept[1] = float(intercept[1])
            lime_data.update({"intercept": intercept})
        else:
            pred_class = exp.predict_proba.argmax()
            lime_data.update(
                {"list": self.converter_tuple(exp.as_list(label=pred_class))}
            )
            temp = {}
            for i, j in zip(exp.class_names, exp.predict_proba.tolist()):
                temp.update({i: j})
            lime_data.update({"predicted_value": temp})
            tuple_list = exp.as_map()[pred_class]
            intercept = exp.intercept
            intercept[1] = float(intercept[1])
            lime_data.update({"intercept": {1: intercept[1]}})
        line_series = []
        tuple_list.sort(key=lambda x: x[0])
        for i, j, k in zip(
            self.expai_data["input"], self.expai_data["feature_names"], tuple_list
        ):
            if k[1] < 0:
                val = "negative"
            else:
                val = "positive"
            temp_list = [float(i), j, val]
            line_series.append(temp_list)
        lime_data.update({"feature_values": line_series})
        lime_data.update({"model": self.expai_data["mode"]})
        return lime_data

    def shap_plots(self):
        """
        Method to plot SHAP graphs
        :return:
        """
        x_test_array = np.array(self.expai_data["data"])
        if len(x_test_array) > 500:
            indices = np.random.choice(x_test_array.shape[0], 500, replace=False)
            x_test_array = x_test_array[indices]
        shap_data = self.fetch_shap_data(
            self.expai_data["mode"],
            x_test_array,
            self.expai_data["deep_learning_model"],
        )
        if self.expai_data["deep_learning_model"] is True:
            shap.force_plot(
                shap_data["expected_value"],
                shap_data["shap_values"],
                shap_data["data"],
                feature_names=self.expai_data["feature_names"],
                show=False,
                matplotlib=True,
            ).savefig(f"{self.expai_data['temp_dir']}/shap_plot.png")
            return "Graphs plotted successfully"
        key = shap_data["predicted_value"]
        if self.expai_data["mode"] == ExplainableAIMode.classification:
            shap_expect = shap_data["expected_value"][key]
            shap_val = shap_data["shap_values"][key]
        else:
            shap_expect = shap_data["predicted_value"]
            shap_val = shap_data["shap_values"]
        shap.force_plot(
            shap_expect,
            shap_val,
            shap_data["data"],
            feature_names=self.expai_data["feature_names"],
            show=False,
            matplotlib=True,
        ).savefig(f"{self.expai_data['temp_dir']}/shap_plot.png")
        return "Graphs plotted successfully"

    def fetch_shap_data(self, mode, x_test_array, deep_learning=False):
        """
            Method to fetch shap data for building graphs
            :return:
        """
        if len(x_test_array) > 500:
            indices = np.random.choice(x_test_array.shape[0], 500, replace=False)
            x_test_array = x_test_array[indices]
        if isinstance(self.expai_data["input"], list):
            self.expai_data["input"] = np.array(self.expai_data["input"])
        x_output = x_test_array.copy()
        # Randomly pick some observations
        random_picks = np.arange(1, 50, 2)  # Every 50 rows
        if mode == ExplainableAIMode.classification:
            if self.expai_data["custom_score"] is None:
                explainer = shap.KernelExplainer(
                    self.predict_function(self.expai_data["mode"]), x_test_array
                )
            else:
                explainer = shap.KernelExplainer(
                    self.expai_data["custom_score"], x_test_array
                )

            count = 0
            temp_dict = OrderedDict()
            for i, j in zip(
                explainer.expected_value,
                list(explainer.shap_values(self.expai_data["input"])),
            ):
                temp_dict.update({count: i + sum(j)})
                count += 1
            max_key = max(temp_dict, key=temp_dict.get)
            shap_data = {
                "expected_value": list(explainer.expected_value),
                "shap_values": list(explainer.shap_values(self.expai_data["input"])),
                "decision_values": temp_dict,
                "data": self.expai_data["input"],
                "predicted_value": max_key,
                "legend": self.expai_data["target_names"],
            }
        elif mode == ExplainableAIMode.regression:
            if deep_learning is True:
                x_output[:, 2] = np.round(
                    self.expai_data["model"].predict(x_output), 2
                ).reshape(-1)
                S = x_output[random_picks]
                explainer = shap.DeepExplainer(self.expai_data["model"], x_test_array)
                shap_values = explainer.shap_values(S)
                shap_data = {
                    "expected_value": explainer.expected_value,
                    "shap_values": shap_values[0][15],
                    "data": S[[15]],
                }
            else:
                # Get the predictions and put them with the test data.
                if self.expai_data["custom_score"] is None:
                    explainer = shap.KernelExplainer(
                        self.expai_data["model"].predict, x_test_array
                    )
                else:
                    explainer = shap.KernelExplainer(
                        self.expai_data["custom_score"], x_test_array
                    )

                shap_values = explainer.shap_values(self.expai_data["input"])
                shap_data = {
                    "expected_value": explainer.expected_value,
                    "shap_values": shap_values,
                    "data": self.expai_data["input"],
                    "predicted_value": np.sum(shap_values) + explainer.expected_value,
                }
            if isinstance(shap_data["shap_values"], list):
                shap_data.update({"shap_values": shap_values[0]})
        else:
            shap_data = {}
        return shap_data

    def multi_class_handling(self, shap_data, feature_list, temp_dict, temp_list):
        """If Else to handle multi class classification"""
        if self.expai_data["mode"] == ExplainableAIMode.classification:
            for x in shap_data["shap_values"]:
                for i, j in zip(x, feature_list):
                    temp_dict.update({j: i})
                temp_list.append(temp_dict)
                temp_dict = OrderedDict()
        else:
            for i, j in zip(shap_data["shap_values"].tolist(), feature_list):
                temp_dict.update({j: i})
            temp_list.append(temp_dict)

    def get_shap_data(self):
        """
        Method to fetch shap json

        Fetches shap data and creates dictionaries for SHAP feature and decisions

        Returns:
        dict: shap_final_info
        """
        # fetching shap values, expected values and user input for array
        x_test_array = np.array(self.expai_data["data"])
        if len(x_test_array) > 500:
            indices = np.random.choice(x_test_array.shape[0], 500, replace=False)
            x_test_array = x_test_array[indices]
        shap_data = self.fetch_shap_data(
            self.expai_data["mode"],
            x_test_array,
            self.expai_data["deep_learning_model"],
        )

        # creating a feature list with respective input such as ["f1 = val1", "f2 = val2"]
        feature_list = []
        if isinstance(shap_data["data"].tolist()[0], list):
            shap_val_list = shap_data["data"].tolist()[0]
        else:
            shap_val_list = shap_data["data"].tolist()
        for i, j in zip(shap_val_list, self.expai_data["feature_names"]):
            i = str(j) + " = " + str(i)
            feature_list.append(i)

        # appending shap values to the feature list as {"f1 = val1":shapval1}
        temp_dict = OrderedDict()
        temp_list = []
        # if else for multi class classification handling
        self.multi_class_handling(shap_data, feature_list, temp_dict, temp_list)

        # creating the shap_feature json shap info by adding data, predicted, expected, actual pred
        shap_info = {}
        shap_info.update({"data": temp_list})
        shap_info.update({"expected_value": shap_data["expected_value"]})
        predicted_value = shap_data["predicted_value"]
        shap_info.update({"predicted_value": predicted_value})
        # handling in case of model having different way of predicting
        try:
            if self.expai_data["custom_score"] is None:
                actual_pred = (
                    self.expai_data["model"]
                    .predict(self.expai_data["input"].reshape(1, -1))
                    .tolist()
                )
                shap_info.update({"actual_prediction": actual_pred})
            else:
                actual_pred = self.expai_data["custom_score"](
                    self.expai_data["input"].reshape(1, -1)
                ).tolist()
                shap_info.update({"actual_prediction": actual_pred})
        except:
            print("Could not predict for this model type")

        # creating the data required for shap decision plot
        temp_list_2 = []
        # if else to handle multi class classification
        if self.expai_data["mode"] == ExplainableAIMode.classification:
            for x in range(len(shap_data["shap_values"])):
                temp_dict_2 = OrderedDict()
                temp_var = shap_data["expected_value"][x]
                for i, j in zip(shap_data["shap_values"][x].tolist(), feature_list):
                    temp_var = temp_var + i
                    temp_dict_2.update({j: temp_var})
                temp_list_2.append(temp_dict_2)
        else:
            common_var = shap_data["expected_value"]
            temp_dict_2 = OrderedDict()
            for i, j in zip(shap_data["shap_values"].tolist(), feature_list):
                common_var = common_var + i
                temp_dict_2.update({j: common_var})
            temp_list_2.append(temp_dict_2)

        # creating shap_decision by replacing data variable
        import copy

        shap_dec_info = copy.deepcopy(shap_info)
        shap_dec_info.update({"data": temp_list_2})
        shap_final_info = {"feature": shap_info, "decision": shap_dec_info}
        return shap_final_info

    def check_numpy(self, num):
        """ Custom encoder for numpy data types """
        if isinstance(
            num,
            (
                np.int_,
                np.intc,
                np.intp,
                np.int8,
                np.int16,
                np.int32,
                np.int64,
                np.uint8,
                np.uint16,
                np.uint32,
                np.uint64,
            ),
        ):
            return int(num)
        elif isinstance(num, (np.float_, np.float16, np.float32, np.float64)):
            return float(num)
        elif isinstance(num, (np.complex_, np.complex64, np.complex128)):
            return {"real": num.real, "imag": num.imag}
        elif isinstance(num, (np.ndarray,)):
            return num.tolist()
        elif isinstance(num, (np.bool_)):
            return bool(num)
        elif isinstance(num, (np.void)):
            return None
