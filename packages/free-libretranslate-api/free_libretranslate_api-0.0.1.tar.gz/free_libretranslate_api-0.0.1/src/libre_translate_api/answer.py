from dataclasses import dataclass, field
from typing import Union


@dataclass
class DetectedLanguage:
    confidence: float
    language: str


@dataclass
class AnswerAPI:
    translated_text: str
    alternatives: list[str]
    detectedLanguage: Union[DetectedLanguage, None]

