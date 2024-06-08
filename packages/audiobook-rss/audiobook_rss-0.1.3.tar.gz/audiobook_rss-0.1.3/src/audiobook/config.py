from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class AudiobookConfig(BaseModel):
    opendal: Dict[str, Any]


class InferPoolConfig(BaseModel):
    path_base: str
    tts_model_name: str = Field(alias="model_name")
    prompt_name: str
    device: Optional[str] = None
    is_half: bool = True
    max_workers: int = 4


class Config(BaseModel):
    audiobook: AudiobookConfig
    inferpool: InferPoolConfig
