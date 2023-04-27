from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, overload
from warnings import warn

import numpy
import numpy.typing
import sklearn.linear_model


if TYPE_CHECKING:
    from typing import Literal

    from dedupe._typing import LabelsLike
    from dedupe._typing import RecordDictPairs as TrainingExamples

logger = logging.getLogger(__name__)


class HasCandidates:
    _candidates: TrainingExamples

    @property
    def candidates(self) -> TrainingExamples:
        return self._candidates

    def __len__(self) -> int:
        return len(self.candidates)


class Learner(ABC, HasCandidates):
    _fitted: bool = False

    @abstractmethod
    def fit(self, pairs: TrainingExamples, y: LabelsLike) -> None:
        """Data model training"""

    @abstractmethod
    def candidate_scores(self) -> numpy.typing.NDArray[numpy.float_]:
        """Return our current guess [0,1]"""

    @abstractmethod
    def remove(self, index: int) -> None:
        """Remove duplicated pairs"""

    @staticmethod
    def _verify_fit_args(pairs: TrainingExamples, y: LabelsLike) -> list[Literal[0, 1]]:
        if len(pairs) == 0:
            raise ValueError("All pairs should have at least 1")
        y = list(y)
        if len(pairs) != len(y):
            raise ValueError(
                f"Pairs must be same length. Currently: {len(pairs)} and {len(y)}"
            )
        return y