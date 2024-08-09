from pydantic import BaseModel, Field
from enum import Enum


class Fashion(BaseModel):
    id: str = Field(...)
    prompt: str = Field(...)
    model_path: str = Field(...)
    s3_path: str = Field(...)


class RemoveBg(BaseModel):
    id: str = Field(...)
    image_path: str = Field(...)

class AddBg(BaseModel):
    id: str = Field(...)
    image_path: str = Field(...)
    bg_path: str = Field(...)

class BgCustom(BaseModel):
    id: str = Field(...)
    s3_path: str = Field(...)
    prompt: str = Field(...)
    bg_prompt: str = Field(...)
    superimpose: bool = False
