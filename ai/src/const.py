import os
from dataclasses import dataclass
from enum import StrEnum


class DataCol(StrEnum):
    AGE = "age"
    SEX = "sex"
    CP = "cp"
    TRESTBPS = "trestbps"
    CHOL = "chol"
    FBS = "fbs"
    RESTECG = "restecg"
    THALACH = "thalach"
    EXANG = "exang"
    OLDPEAK = "oldpeak"
    SLOPE = "slope"
    CA = "ca"
    THAL = "thal"
    TARGET = "target"

    @classmethod
    def get_all_values(cls):
        return [e.value for e in cls]

@dataclass(frozen=True)
class DataVar:
    file_path = os.path.join('data', 'processed.cleveland.data')
    plot_dir = 'plots'
