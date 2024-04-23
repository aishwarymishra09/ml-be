from pydantic import BaseModel, Field


class TrainingData(BaseModel):
    id: str = Field(...)
    project_id: str = Field(...)
    name: str = Field(...)
    instance_prompt: str = Field(...)
    class_prompt: str = Field(...)
    resolution: int = Field(...)
    modifier_token: str = Field(...)
    s3_bucket: str = Field(...)
    s3_key: str = Field(...)
    s3_url: str = Field(...)
    s3_object_key: str = Field(...)


class InferenceSchema(BaseModel):
    prompt: str = Field(...)
    negative_prompt: str = Field(...)
    resolution: int = Field(...)


class InferenceData(BaseModel):
    id: str = Field(...)
    training_id: str = Field(...)
    request_id: str = Field(...)
    name: str = Field(...)
    inference_schema: InferenceSchema = Field(...)
