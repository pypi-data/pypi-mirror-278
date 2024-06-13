import base64
import sys
import unittest
from unittest.mock import mock_open, patch

from dhuolib.clients.experiment import DhuolibExperimentClient
from dhuolib.config import logger

sys.path.append("src")


class TestDhuolibPlatformClient(unittest.TestCase):
    def setUp(self):
        self.end_point = "http://localhost:8000"
        self.dhuolib = DhuolibExperimentClient(service_endpoint=self.end_point)

    def test_0_invalid_run_params(self):
        response = self.dhuolib.create_experiment(experiment_name="teste1")
        self.assertEqual(list(response.keys()), ["error"])

    @patch("requests.post")
    def test_1_create_experiment_with_valid_params(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {"experiment_id": "1"}

        response = self.dhuolib.create_experiment(
            experiment_name="teste1",
            experiment_tags={"version": "v1", "priority": "P1"},
        )
        self.assertEqual(response, mock_response.json.return_value)

    @patch("requests.post")
    def test_2_run_experiment_with_valid_params(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "experiment_id": "experiment_id",
            "run_id": "run_id",
            "model_uri": "model_uri",
        }

        response = self.dhuolib.run_experiment(
            type_model="teste1",
            experiment_id="2",
            modelpkl_path="tests/files/LogisticRegression_best.pickle",
            requirements_path="tests/files/requirements.txt",
        )

        self.assertEqual(response, mock_response.json.return_value)

    @patch("requests.post")
    def test_3_create_model_with_valid_params(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "current_stage": "Production",
            "last_updated_timestamp": 1713582060414,
            "model_version": "1",
            "run_id": "9434e517ed104958b6f5f47d33c79184",
            "status": "READY",
        }

        run_params = {
            "stage": "Production",
            "modelname": "nlp_framework",
            "modeltag": "v1",
            "run_id": "9434e517ed104958b6f5f47d33c79184",
            "requirements_file": "tests/files/requirements.txt",
            "model_uri": "model_uri",
        }

        response = self.dhuolib.create_model(run_params)

        self.assertEqual(response, mock_response.json.return_value)

    @patch("requests.post")
    def test_4_predict_online_with_valid_dataset(self, mock_post):
        mock_response = mock_post.return_value
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "model_name": "nlp_framework",
            "predictions": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        }

        run_params = {
            "stage": "Production",
            "data": "tests/files/data_predict.csv",
            "modelname": "nlp_framework",
        }

        response = self.dhuolib.predict_online(run_params)

        self.assertEqual(response, mock_response.json.return_value)
