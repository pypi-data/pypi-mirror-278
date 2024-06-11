from pydantic import ValidationError
import json
import time
import base64
from dhuolib.config import logger
from dhuolib.services import ServiceAPIML
from dhuolib.validations import ExperimentBody, RunExperimentBody, PredictModelBody
from werkzeug.datastructures import FileStorage


class DhuolibClient:
    def __init__(self, service_endpoint=None, project_name=None):
        if not service_endpoint:
            raise ValueError("service_endpoint is required")

        self.service = ServiceAPIML(service_endpoint)
        self.project_name = project_name   

    def create_experiment(self, experiment_params: dict) -> dict:
        params = {}
        response = None

        try:
            ExperimentBody.parse_obj(experiment_params)
        except ValidationError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}

        if (
            "requirements_file" in experiment_params.keys() 
            and "model_pkl_file" in experiment_params.keys()
        ):
            params["experiment_tags"] = json.dumps(experiment_params["experiment_tags"])
            try:
                with open(experiment_params["requirements_file"], "rb") as f1, open(
                    experiment_params["model_pkl_file"], "rb"
                ) as f2:
                    files = {
                        "requirements_file": FileStorage(
                            stream=f1,
                            filename="requirements.txt",
                            content_type="text/plain",
                        ),
                        "model_pkl_file": FileStorage(
                            stream=f2,
                            filename="model.pkl",
                            content_type="application/octet-stream",
                        ),
                    }
                    response = self.service.create_experiment_by_conf_json(experiment_params, files)

                    experiment = response.json()
                    logger.info(
                        f"Experiment Name: {params['experiment_name']}"
                        f"Experiment ID: {experiment['experiment_id']} created"
                    )
                    return experiment
            except FileNotFoundError as e:
                logger.error(f"Error: {e}")
                return {"error": str(e)}
        response = self.service.create_experiment_by_conf_json(experiment_params)
        logger.info(
            f"Experiment Name: {experiment_params['experiment_name']}"
            f"Experiment ID: {response['experiment_id']} created"
        )
        return response

    def run_experiment(self, params) -> dict:
        try:
            RunExperimentBody.parse_obj(params)
        except ValidationError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}

        try:
            with open(params["requirements_file"], "rb") as f1, open(
                params["model_pkl_file"], "rb"
            ) as f2:
                files = {
                    "requirements_file": FileStorage(
                        stream=f1,
                        filename="requirements.txt",
                        content_type="text/plain",
                    ),
                    "model_pkl_file": FileStorage(
                        stream=f2,
                        filename="model.pkl",
                        content_type="application/octet-stream",
                    ),
                }

                if params["experiment_id"] is None:
                    experiment_id = self.create_experiment(params)
                    params["experiment_id"] = experiment_id

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
            PredictModelBody.parse_obj(run_params)
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

    def create_batch_project(self, project_name: str):
        if project_name is None:
            raise ValueError("project_name is required")
        self.project_name = project_name
        response = self.service.create_project(project_name)
        return response

    def deploy_batch_project(self, script_filename: str, requirements_filename: str):
        if self.project_name is None:
            raise ValueError("Batch project is required")

        if script_filename is None or requirements_filename is None:
            raise ValueError("script_filename and requirements_filename are required")

        try:
            with open(script_filename, "rb") as script_file, open(requirements_filename, "rb") as requirements_file:
                encoded_script = base64.b64encode(script_file.read())
                encoded_requirements = base64.b64encode(requirements_file.read())
                response = self.service.deploy_script(project_name=self.project_name,
                                                      script_file_encode=encoded_script,
                                                      requirements_file_enconde=encoded_requirements)
                return response
        except FileNotFoundError as e:
            logger.error(f"Error: {e}")
            return {"error": str(e)}

    def pipeline_status_report(self):
        lst = []
        if self.project_name is None:
            raise ValueError("Batch project is required")
        response = self.service.get_pipeline_status(self.project_name)
        for data in response["data"]:
            lst.append({
                "date_log": data["date_log"],
                "step": data["step"],
                "status": data["status"]
            })
        return lst

    def _create_cluster(self, cluster_size: int):
        if self.project_name is None:
            raise ValueError("Batch project is required")

        if cluster_size not in [1, 2, 3]:
            raise ValueError("cluster_size must be 1, 2 or 3")

        response = self.service.create_cluster(self.project_name, cluster_size)
        return response

    def _batch_run(self):
        if self.project_name is None:
            raise ValueError("Batch project is required")

        response = self.service.run_pipeline(self.project_name)
        return response
     
    def batch_execute(self, cluster_size: int, script_filename: str, requirements_filename: str):
        if self.project_name is None:
            raise ValueError("Batch project is required")
        response = self.deploy_batch_project(script_filename=script_filename, requirements_filename=requirements_filename)
        if response['code'] != 201:
            return 'Error deploying batch project see pipeline status for more information'
        
        logger.info(f"Deploy_batch_project {response} deployed")
        while True:
            status = self.pipeline_status_report()
            if any([s["status"] == "DEPLOY COMPLETED SUCCESSFULLY" for s in status]):
                break
            logger.info(f"Deploy_batch_project {status[len(status)-1]['date_log']}")
            logger.info(f"Deploy_batch_project {status[len(status)-1]['status']}")
            logger.info("Process is running...")
            time.sleep(60)
        response = self._create_cluster(cluster_size=cluster_size)
        if response['code'] != 201:
            return response
        logger.info(f"Create_cluster {response}")
        response = self._batch_run()
        if response['code'] != 201:
            return response
        logger.info(f"Batch Run {response}")