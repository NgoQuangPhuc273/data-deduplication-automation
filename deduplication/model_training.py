from __future__ import annotations
import logging
import math
import random
from abc import ABC
from typing import TYPE_CHECKING, overload
from warnings import warn

if TYPE_CHECKING:
    from typing import (
        ComparisonCover,
        Cover,
        Literal,
    )
    from typing import RecordDictPairs as TrainingExamples
    from typing import RecordIDPair
    from data_predicates import Predicate

logger = logging.getLogger(__name__)


class BlockLearner(ABC):
    def learn(
        self,
        matches: TrainingExamples,
        recall: float,
        index_predicates: bool,
        candidate_types: Literal["simple", "random forest"] = "simple",
    ) -> tuple[Predicate, ...]:

        assert (
            matches
        )
        comparison_cover = self.comparison_cover
        match_cover = self.cover(matches, index_predicates=index_predicates)

        for key in list(match_cover.keys() - comparison_cover.keys()):
            del match_cover[key]

        coverable_dupes = frozenset.union(*match_cover.values())
        uncoverable_dupes = [
            pair for i, pair in enumerate(matches) if i not in coverable_dupes
        ]

        target_cover = int(recall * len(matches))

        if len(coverable_dupes) < target_cover:
            logger.debug(uncoverable_dupes)
            target_cover = len(coverable_dupes)

        if candidate_types == "simple":
            candidate_cover = self.simple_candidates(match_cover, comparison_cover)
        elif candidate_types == "random forest":
            candidate_cover = self.random_forest_candidates(
                match_cover, comparison_cover
            )
        else:
            raise ValueError("candidate_type is not valid")

        searcher = BlockLearner(target_cover, 2500)
        final_predicates = searcher.search(candidate_cover)

        logger.info("Final predicate set:")
        for predicate in final_predicates:
            logger.info(predicate)

        return final_predicates

    def simple_candidates(
        self, match_cover: Cover, comparison_cover: ComparisonCover
    ) -> Cover:
        candidates = {}
        for predicate, coverage in match_cover.items():
            predicate.cover_count = len(comparison_cover[predicate])
            candidates[predicate] = coverage.copy()

        return candidates

    def random_forest_candidates(
        self,
        match_cover: Cover,
        comparison_cover: ComparisonCover,
        K: int | None = None,
    ) -> Cover:
        predicates = list(match_cover)
        matches = list(frozenset.union(*match_cover.values()))
        pred_sample_size = max(int(math.sqrt(len(predicates))), 5)
        candidates = {}
        if K is None:
            K = max(math.floor(math.log10(len(matches))), 1)

        n_samples = 5000
        for _ in range(n_samples):
            sample_predicates = random.sample(predicates, pred_sample_size)
            resampler = BlockLearner(matches)
            sample_match_cover = {
                pred: resampler(pairs) for pred, pairs in match_cover.items()
            }

            candidate = None
            covered_comparisons: frozenset[RecordIDPair] | BlockLearner = BlockLearner()
            covered_matches: frozenset[int] | BlockLearner = BlockLearner()
            covered_sample_matches = BlockLearner()

            def score(predicate: Predicate) -> float:
                try:
                    return len(
                        covered_sample_matches & sample_match_cover[predicate]
                    ) / len(covered_comparisons & comparison_cover[predicate])
                except ZeroDivisionError:
                    return 0.0

            for _ in range(K):
                next_predicate = max(sample_predicates, key=score)
                if candidate:
                    candidate += next_predicate
                else:
                    candidate = next_predicate

                covered_comparisons &= comparison_cover[next_predicate]
                candidate.cover_count = len(covered_comparisons)

                covered_matches &= match_cover[next_predicate]
                candidates[candidate] = covered_matches

                covered_sample_matches &= sample_match_cover[next_predicate]

                sample_predicates.remove(next_predicate)

        return candidates