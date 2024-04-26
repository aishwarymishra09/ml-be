from pydantic import BaseModel, Field
from enum import Enum


class Resolution(str, Enum):
    medium = 512
    high = 1024


class TrainingData(BaseModel):
    id: str = Field(...)
    project_id: str = Field(...)
    class_name: str = Field(...)
    resolution: Resolution = Field(...)
    modifier_token: str = Field(...)
    s3_bucket: str = Field(...)
    s3_url: str = Field(...)

    @property
    def class_prompt(self):
        return f'a photo of {self.class_name}'

    @property
    def instance_prompt(self):
        return f'a photo of {self.modifier_token} {self.class_name}'


class InferenceSchema(BaseModel):
    prompt: str = Field(...)
    negative_prompt: str = Field(...)
    resolution: Resolution = Field(...)


class InferenceData(BaseModel):
    id: str = Field(...)
    training_id: str = Field(...)
    request_id: str = Field(...)
    inference_schema: InferenceSchema = Field(...)


class InferenceCommonData(BaseModel):
    id: str = Field(...)
    request_id: str = Field(...)
    inference_schema: InferenceSchema = Field(...)
