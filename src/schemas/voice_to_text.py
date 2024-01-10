from pydantic import BaseModel
from fastapi import UploadFile


class WhisperSchema(BaseModel):
    audiofile: UploadFile
    model: str


class RunPodSchema(BaseModel):
    model: str = "small"
    transcription: str = "plain_text"
    translate: bool = False
    temperature: int = 0
    best_of: int = 5
    beam_size: int = 5
    patience: int = 1
    suppress_tokens: str = "-1"
    condition_on_previous_text: bool = False
    temperature_increment_on_fallback: float = 0.2
    compression_ratio_threshold: float = 2.4
    logprob_threshold: int = -1
    no_speech_threshold: float = 0.6
    word_timestamps: bool = False
    enable_vad: bool = False
