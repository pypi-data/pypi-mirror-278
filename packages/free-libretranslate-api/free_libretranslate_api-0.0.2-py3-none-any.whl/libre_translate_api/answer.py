from dataclasses import dataclass, field
from typing import Union


@dataclass
class DetectedLanguage:
    confidence: float
    """Уровень уверенности в обнаруженном языке"""

    language: str
    """Код обнаруженного языка"""


@dataclass
class AnswerAPI:
    translated_text: str 
    """Переведенный текст"""

    alternatives: list[str] 
    """Другие варианты перевода"""

    detectedLanguage: Union[DetectedLanguage, None] 
    """
    Информация об обнаруженном языке, если она доступна. 
    Может быть `None`, если информация об обнаруженном языке отсутствует.
    """

