from pydantic import BaseModel, Field


class RunExperimentBody(BaseModel):
    type_model: str = Field(
        ..., description="RANDOM_FOREST|XGBOOST|LINEAR_REGRESSION|LOGISTIC_REGRESSION"
    )
    experiment_id: str = Field(..., description="Id")
    requirements_path: str = Field(..., description="STAGING|PRODUCTION")
    model_pkl_path: str = Field(..., description="STAGING|PRODUCTION")


class ExperimentBody(BaseModel):
    name: str = Field(..., description="Id")
    tags: dict = Field(None, description="Tags")
    requirements_file: str = Field(None, description="STAGING|PRODUCTION")
    model_pkl_file: str = Field(None, description="STAGING|PRODUCTION")


class PredictOnlineModelBody(BaseModel):
    run_id: str = Field(None, description="Run ID")
    modelname: str = Field(..., description="DEPENDENCY|PREDICT")
    stage: str = Field(..., description="STAGING|PRODUCTION")


class PredictBatchModelBody(BaseModel):
    run_id: str = Field(None, description="Run ID")
    modelname: str = Field(..., description="DEPENDENCY|PREDICT")
    stage: str = Field(..., description="STAGING|PRODUCTION")
    batch_model_dir: str = Field(..., description="Batch File")
    experiment_name: str = Field(..., description="Experiment Name")
    type_model: str = Field(
        ..., description="RANDOM_FOREST|XGBOOST|LINEAR_REGRESSION|LOGISTIC_REGRESSION"
    )


class ConnectModel(BaseModel):
    dialect_drive: str = Field(..., description="Dialect")
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")
    host: str = Field(..., description="Host")
    port: str = Field(..., description="Port")
    service_name: str = Field(..., description="Service Name")
