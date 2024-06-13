import base64
import time

from dhuolib.config import logger
from dhuolib.services import ServiceAPIML
from dhuolib.utils import validade_name


class DhuolibPlatformClient:
    def __init__(self, service_endpoint=None, project_name=None):
        if not service_endpoint:
            raise ValueError("service_endpoint is required")

        self.service = ServiceAPIML(service_endpoint)
        self.project_name = project_name

    def create_batch_project(self, project_name: str):
        self.project_name = validade_name(project_name)
        response = self.service.create_project(project_name)
        if response.status_code == 400:
            raise ValueError("Project already exists")
        elif response.status_code == 404:
            return ConnectionError("Connection error")

        return response.json()

    def deploy_batch_project(self, script_filename: str, requirements_filename: str):
        if self.project_name is None:
            raise ValueError("Batch project is required")

        if script_filename is None or requirements_filename is None:
            raise ValueError("script_filename and requirements_filename are required")

        try:
            with open(script_filename, "rb") as script_file, open(
                requirements_filename, "rb"
            ) as requirements_file:
                encoded_script = base64.b64encode(script_file.read())
                encoded_requirements = base64.b64encode(requirements_file.read())
                response = self.service.deploy_script(
                    project_name=self.project_name,
                    script_file_encode=encoded_script,
                    requirements_file_enconde=encoded_requirements,
                )
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
            lst.append(
                {
                    "date_log": data["date_log"],
                    "step": data["step"],
                    "status": data["status"],
                }
            )
        return lst

    def create_cluster(self, cluster_size: int):
        if self.project_name is None:
            raise ValueError("Batch project is required")

        if cluster_size not in [1, 2, 3]:
            raise ValueError("cluster_size must be 1, 2 or 3")

        response = self.service.create_cluster(self.project_name, cluster_size)
        return response

    def batch_run(self):
        if self.project_name is None:
            raise ValueError("Batch project is required")

        response = self.service.run_pipeline(self.project_name)
        return response
