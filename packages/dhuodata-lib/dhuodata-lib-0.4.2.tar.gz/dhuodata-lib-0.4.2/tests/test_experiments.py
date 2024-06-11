# import base64
# import sys
# import unittest
# from unittest.mock import mock_open, patch

# from dhuolib.clients.experiment import DhuolibExperimentClient
# from dhuolib.config import logger

# sys.path.append("src")


# class TestDhuolibPlatformClient(unittest.TestCase):
#     def setUp(self):
#         self.end_point = "http://localhost:8000"
#         self.dhuolib = DhuolibExperimentClient(service_endpoint=self.end_point)

#     def test_0_(self):
       # response = self.dhuolib.create_batch_project("test-project8")

# def test_4_transform_name_project_no_project_name(self):
#     client = DhuolibClient(service_endpoint="http://example.com")
#     self.assertIsNone(client.project_name)

# def test_5_invalid_run_params(self):
#     experiment_params = {
#         "experiment_tags": {"version": "v1", "priority": "P1"},
#     }
#     response = self.dhuolib.create_experiment(experiment_params)
#     self.assertEqual(list(response.keys()), ["error"])

# @patch("requests.post")
# def test_6_create_experiment_with_valid_params(self, mock_post):
#     mock_response = mock_post.return_value
#     mock_response.status_code = 201
#     mock_response.json.return_value = {"experiment_id": "1"}

#     experiment_params = {
#         "experiment_name": "test_experiment",
#         "experiment_tags": {"version": "v1", "priority": "P1"},
#     }

#     response = self.dhuolib.create_experiment(experiment_params)
#     self.assertEqual(response, mock_response.json.return_value)

# @patch("requests.post")
# def test_7_run_experiment_with_valid_params(self, mock_post):
#     mock_response = mock_post.return_value
#     mock_response.status_code = 201
#     mock_response.json.return_value = {
#         "experiment_id": "experiment_id",
#         "run_id": "run_id",
#         "model_uri": "model_uri",
#     }

#     run_params = {
#         "experiment_id": "2",
#         "model_pkl_file": "tests/files/LogisticRegression_best.pickle",
#         "requirements_file": "tests/files/requirements.txt",
#     }
#     response = self.dhuolib.run_experiment(run_params)

#     self.assertEqual(response, mock_response.json.return_value)

# @patch("requests.post")
# def test_8_create_model_with_valid_params(self, mock_post):
#     mock_response = mock_post.return_value
#     mock_response.status_code = 201
#     mock_response.json.return_value = {
#         "current_stage": "Production",
#         "last_updated_timestamp": 1713582060414,
#         "model_version": "1",
#         "run_id": "9434e517ed104958b6f5f47d33c79184",
#         "status": "READY",
#     }

#     run_params = {
#         "stage": "Production",
#         "modelname": "nlp_framework",
#         "modeltag": "v1",
#         "run_id": "9434e517ed104958b6f5f47d33c79184",
#         "requirements_file": "tests/files/requirements.txt",
#         "model_uri": "model_uri",
#     }

#     response = self.dhuolib.create_model(run_params)

#     self.assertEqual(response, mock_response.json.return_value)

# @patch("requests.post")
# def test_9_predict_online_with_valid_dataset(self, mock_post):
#     mock_response = mock_post.return_value
#     mock_response.status_code = 201
#     mock_response.json.return_value = {
#         "model_name": "nlp_framework",
#         "predictions": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#     }

#     run_params = {
#         "stage": "Production",
#         "data": "tests/files/data_predict.csv",
#         "modelname": "nlp_framework",
#     }

#     response = self.dhuolib.predict_online(run_params)

#     self.assertEqual(response, mock_response.json.return_value)
##################################################






# def test_4_transform_name_project_no_project_name(self):
#     client = DhuolibClient(service_endpoint="http://example.com")
#     self.assertIsNone(client.project_name)

# def test_5_invalid_run_params(self):
#     experiment_params = {
#         "experiment_tags": {"version": "v1", "priority": "P1"},
#     }
#     response = self.dhuolib.create_experiment(experiment_params)
#     self.assertEqual(list(response.keys()), ["error"])

# @patch("requests.post")
# def test_6_create_experiment_with_valid_params(self, mock_post):
#     mock_response = mock_post.return_value
#     mock_response.status_code = 201
#     mock_response.json.return_value = {"experiment_id": "1"}

#     experiment_params = {
#         "experiment_name": "test_experiment",
#         "experiment_tags": {"version": "v1", "priority": "P1"},
#     }

#     response = self.dhuolib.create_experiment(experiment_params)
#     self.assertEqual(response, mock_response.json.return_value)

# @patch("requests.post")
# def test_7_run_experiment_with_valid_params(self, mock_post):
#     mock_response = mock_post.return_value
#     mock_response.status_code = 201
#     mock_response.json.return_value = {
#         "experiment_id": "experiment_id",
#         "run_id": "run_id",
#         "model_uri": "model_uri",
#     }

#     run_params = {
#         "experiment_id": "2",
#         "model_pkl_file": "tests/files/LogisticRegression_best.pickle",
#         "requirements_file": "tests/files/requirements.txt",
#     }
#     response = self.dhuolib.run_experiment(run_params)

#     self.assertEqual(response, mock_response.json.return_value)

# @patch("requests.post")
# def test_8_create_model_with_valid_params(self, mock_post):
#     mock_response = mock_post.return_value
#     mock_response.status_code = 201
#     mock_response.json.return_value = {
#         "current_stage": "Production",
#         "last_updated_timestamp": 1713582060414,
#         "model_version": "1",
#         "run_id": "9434e517ed104958b6f5f47d33c79184",
#         "status": "READY",
#     }

#     run_params = {
#         "stage": "Production",
#         "modelname": "nlp_framework",
#         "modeltag": "v1",
#         "run_id": "9434e517ed104958b6f5f47d33c79184",
#         "requirements_file": "tests/files/requirements.txt",
#         "model_uri": "model_uri",
#     }

#     response = self.dhuolib.create_model(run_params)

#     self.assertEqual(response, mock_response.json.return_value)

# @patch("requests.post")
# def test_9_predict_online_with_valid_dataset(self, mock_post):
#     mock_response = mock_post.return_value
#     mock_response.status_code = 201
#     mock_response.json.return_value = {
#         "model_name": "nlp_framework",
#         "predictions": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
#     }

#     run_params = {
#         "stage": "Production",
#         "data": "tests/files/data_predict.csv",
#         "modelname": "nlp_framework",
#     }

#     response = self.dhuolib.predict_online(run_params)

#     self.assertEqual(response, mock_response.json.return_value)

# @patch("requests.post")
# def test_10_create_batch_project_successful(self, mock_post):
#     project_name = "Test Project"
#     mock_response = mock_post.return_value
#     mock_response.status_code = 201
#     mock_response.json.return_value = {"status": "success", "project_id": 123}
#     response = self.dhuolib.create_batch_project(project_name)
#     self.assertEqual(response, {"status": "success", "project_id": 123})

# def test_11_create_batch_project_raises_exception_on_none(self):
#     with self.assertRaises(ValueError) as context:
#         self.dhuolib.create_batch_project(None)
#         self.assertIn("project_name is required", str(context.exception))

# def test_12_deploy_batch_project_no_project_name(self):
#     self.dhuolib = DhuolibClient(service_endpoint=self.end_point)
#     with self.assertRaises(ValueError) as context:
#         self.dhuolib.deploy_batch_project("script.py", "requirements.txt")
#         self.assertIn("Batch project is required", str(context.exception))

# def test_13_deploy_batch_project_missing_files(self):
#     with self.assertRaises(ValueError) as context:
#         self.dhuolib.deploy_batch_project(None, None)
#         self.assertIn(
#             "script_filename and requirements_filename are required",
#             str(context.exception),
#         )

# def test_14_deploy_batch_project_file_not_found(self):
#     with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
#         response = self.dhuolib.deploy_batch_project(
#             "script.py", "requirements.txt"
#         )
#         self.assertEqual(response, {"error": "File not found"})
