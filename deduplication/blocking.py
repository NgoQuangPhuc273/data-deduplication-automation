from __future__ import annotations
import logging
from collections import defaultdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import (
        DefaultDict,
        Iterable,
        List,
        Union,
    )

    import deduplication.data_predicates
    Docs = Union[Iterable[str], Iterable[Iterable[str]]]
    IndexList = DefaultDict[str, List[deduplication.data_predicates.IndexPredicate]]


logger = logging.getLogger(__name__)


def index_list() -> IndexList:
    return defaultdict(list)


class Fingerprinter:
    def __init__(self, predicates):
        self.predicates = predicates
        self.index_fields = defaultdict(index_list)

        for full_predicate in predicates:
            for predicate in full_predicate:
                if hasattr(predicate, "index"):
                    self.index_fields[predicate.field][predicate.type].append(predicate)

    def index(self, docs, field):
        for doc in docs:
            if not doc:
                continue
            for _, index, preprocess in field:
                index.index(preprocess(doc))

        for index_list in self.index_fields[field].values():
            for predicate in index_list:
                logger.debug("Canopy: %s", str(predicate))
                predicate.index.initSearch()
                predicate.index = index
                predicate.bust_cache()