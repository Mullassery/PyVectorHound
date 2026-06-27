"""PyVectorSearch: Diagnose vector search problems in RAG/LLM systems."""

__version__ = "0.1.0"
__author__ = "Georgi Mammen Mullassery"
__email__ = "mullassery@gmail.com"
__license__ = "MIT"

from pyvectorhound.hound import Hound
from pyvectorhound.diagnosis import Diagnosis
from pyvectorhound.comparison import ModelComparison
from pyvectorhound.scorer import QualityScorer

__all__ = [
    "Hound",
    "Diagnosis",
    "ModelComparison",
    "QualityScorer",
]
