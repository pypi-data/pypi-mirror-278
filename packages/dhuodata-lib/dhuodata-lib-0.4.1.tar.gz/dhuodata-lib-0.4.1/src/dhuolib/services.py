import json

import requests

from dhuolib.validations import ExperimentBody


class ServiceAPIML:
    def __init__(self, service_endpoint):

        if not isinstance(service_endpoint, str):
            raise ValueError("service_endpoint must be a string")

        self.service_endpoint = f"{service_endpoint}/api"
        self.headers = {"Content-Type": "application/json"}

    def create_experiment_by_conf_json(self, experiment_params: dict):
        if experiment_params is None and isinstance(experiment_params, dict):
            raise ValueError("json_data must be a dict")

        response = requests.post(
            f"{self.service_endpoint}/experiment/save",
            data=json.dumps(experiment_params),
            headers=self.headers,
        )
        return response

    def run_experiment(self, params={}, files=None):
        if params is None and isinstance(params, str):
            raise ValueError("json_data must be a dict")

        response = requests.post(
            f"{self.service_endpoint}/experiment/run", data=params, files=files
        )
        return response.json()

    def create_model(self, model_params):
        if model_params is None and not isinstance(model_params, dict):
            raise ValueError("json_data must be a dict")
        response = requests.post(
            f"{self.service_endpoint}/experiment/model",
            data=json.dumps(model_params),
            headers=self.headers,
        )
        return response.json()

    def predict_online(self, params={}, files=None):
        if params is None and not isinstance(params, dict):
            raise ValueError("json_data must be a dict")
        response = requests.post(
            f"{self.service_endpoint}/experiment/predict_online",
            data=params,
            files=files,
        )
        return response.json()

    def create_project(self, project_name):
        body = {"project_name": project_name}
        response = requests.post(f"{self.service_endpoint}/project", json=body)

        return response.json()

    def deploy_script(
        self, project_name: str, script_file_encode: str, requirements_file_enconde: str
    ):
        body = {
            "project_name": project_name,
            "requirements_content": requirements_file_enconde.decode("utf-8"),
            "run_script_content": script_file_encode.decode("utf-8"),
        }
        response = requests.post(f"{self.service_endpoint}/deploy", json=body)

        return response.json()

    def get_pipeline_status(self, project_name: str):
        route = "deploy/{}".format(project_name)
        response = requests.get(f"{self.service_endpoint}/{route}")

        return response.json()

    def create_cluster(self, project_name: str, cluster_size: int):
        body = {"project_name": project_name, "cluster_size": cluster_size}
        response = requests.post(f"{self.service_endpoint}/cluster", json=body)

        return response.json()

    def run_pipeline(self, project_name: str):
        body = {"project_name": project_name}
        response = requests.post(f"{self.service_endpoint}/cluster/run", json=body)

        return response.json()

    def download_pickle(
        self,
        experiment_name: str,
        type_model: str,
        model_name: str,
        model_stage: str = "",
        run_id: str = "",
        local_filename: str = "model.pickle",
    ):
        url = f"{self.service_endpoint}/experiment/dowload/batch/{experiment_name}/{model_name}?model_stage={model_stage}&run_id={run_id}&type_model={type_model}"
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
