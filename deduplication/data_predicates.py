import abc
import re
from itertools import product
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import AbstractSet, Any, FrozenSet, Mapping

    from dedupe._typing import Literal, RecordDict


words = re.compile(r"[\w']+").findall

class Predicate(abc.ABC):
    type: str
    __name__: str
    _cached_hash: int
    cover_count: int

    def __iter__(self):
        yield self
        
    @abc.abstractmethod
    def __call__(self, record: RecordDict, **kwargs) -> AbstractSet[str]:
        pass

    def __add__(self, other: "Predicate") -> "CompoundPredicate":
        if isinstance(other, CompoundPredicate):
            return CompoundPredicate((self,) + tuple(other))
        elif isinstance(other, Predicate):
            return CompoundPredicate((self, other))
        else:
            raise ValueError("")


class ExistsPredicate(Predicate):
    type = "ExistsPredicate"

    def __init__(self, field: str):
        self.__name__ = "(Exists, %s)" % (field,)
        self.field = field

    @staticmethod
    def func(column: Any) -> FrozenSet[Literal["0", "1"]]:
        if column:
            return frozenset(("1",))
        else:
            return frozenset(("0",))

    def __call__(self, record: RecordDict, **kwargs) -> FrozenSet[Literal["0", "1"]]: 
        column = record[self.field]
        return self.func(column)

class CompoundPredicate(tuple, Predicate):
    type = "CompoundPredicate"

    def __call__(
        self, record: Mapping[str, Any], **kwargs: Any
    ) -> FrozenSet[str]:
        predicate_keys = [predicate(record, **kwargs) for predicate in self]
        return frozenset(
            ":".join(
                b.replace(":", "\\:")
                for b in block_key
            )
            for block_key in product(*predicate_keys)
        )

    def __add__(self, other: Predicate) -> "CompoundPredicate": 
        if isinstance(other, CompoundPredicate):
            return CompoundPredicate(tuple(self) + tuple(other))
        elif isinstance(other, Predicate):
            return CompoundPredicate(tuple(self) + (other,))
        else:
            raise ValueError("Can only combine predicates")
