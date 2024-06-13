import pandas as pd
from pydantic import ValidationError
from werkzeug.datastructures import FileStorage

import dhuolib.utils as ut
from dhuolib.config import logger
from dhuolib.services import ServiceAPIML
from dhuolib.utils import validade_name
from dhuolib.validations import (
    ExperimentBody,
    PredictBatchModelBody,
    PredictOnlineModelBody,
    RunExperimentBody,
)


class DhuolibExperimentClient:
    def __init__(self, service_endpoint=None):
        if not service_endpoint:
            raise ValueError("service_endpoint is required")

        self.service = ServiceAPIML(service_endpoint)

    def create_experiment(
        self, experiment_name: str, experiment_tags: dict = None
    ) -> dict:

        experiment_params = {
            "name": experiment_name,
            "tags": experiment_tags,
        }

        try:
            experiment = ExperimentBody.model_validate(experiment_params)
        except ValidationError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}

        experiment_params["name"] = validade_name(experiment.name)

        response = self.service.create_experiment_by_conf_json(experiment_params)

        if response.status_code == 404:
            raise ConnectionError("Connection error")

        response = response.json()

        logger.info(
            f"Experiment Name: {experiment_params['name']}"
            f"Experiment ID: {response['experiment_id']} created"
        )

        return response

    def run_experiment(
        self,
        type_model: str,
        experiment_id: str,
        modelpkl_path: str,
        requirements_path,
    ) -> dict:
        params = {
            "type_model": type_model,
            "experiment_id": experiment_id,
            "modelpkl_path": modelpkl_path,
            "requirements_path": requirements_path,
        }

        try:
            RunExperimentBody.model_validate(params)
        except ValidationError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}

        try:
            with open(params["requirements_path"], "rb") as f1, open(
                params["modelpkl_path"], "rb"
            ) as f2:
                files = {
                    "requirements_path": FileStorage(
                        stream=f1,
                        filename="requirements.txt",
                        content_type="text/plain",
                    ),
                    "modelpkl_path": FileStorage(
                        stream=f2,
                        filename="model.pkl",
                        content_type="application/octet-stream",
                    ),
                }

                response = self.service.run_experiment(params=params, files=files)
                logger.info(f"Experiment ID: {params['experiment_id']} running")
                return response
        except FileNotFoundError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}

    def create_model(self, model_params) -> dict:
        try:
            if model_params["stage"] is None:
                model_params["stage"] = "STAGING"

            response = self.service.create_model(model_params)
            logger.info(f"Model Name: {model_params['modelname']} created")
            return response
        except ValidationError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}

    def predict_online(self, run_params) -> dict:
        try:
            PredictOnlineModelBody.model_validate(run_params)
        except ValidationError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}
        try:
            with open(run_params["data"], "rb") as f1:
                files = {
                    "data": FileStorage(
                        stream=f1, filename="data.csv", content_type="csv"
                    )
                }
                response = self.service.predict_online(params=run_params, files=files)
                logger.info(f"Model Name: {run_params['modelname']} predictions")
                return response
        except FileNotFoundError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}

    def _get_model_to_prediction(self, predict: PredictBatchModelBody) -> dict:

        path_to_pickle = self.service.download_pickle(
            model_name=predict.modelname,
            model_stage=predict.stage,
            run_id=predict.run_id,
            experiment_name=predict.experiment_name,
            local_filename=predict.batch_model_dir,
            type_model=predict.type_model,
        )

        return ut.load_pickle_model(path_to_pickle)

    def prediction_batch_with_dataframe(
        self, batch_params: dict, df: pd.DataFrame
    ) -> dict:
        try:
            predict = PredictBatchModelBody.model_validate(batch_params)
        except ValidationError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}

        model = self._get_model_to_prediction(predict)
        return model.predict(df)
