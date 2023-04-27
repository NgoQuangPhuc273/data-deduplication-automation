import logging
import tempfile
from typing import Generator
import numpy.typing
from typing import Scores

logger = logging.getLogger(__name__)


def connected_components(
    edgelist: Scores, max_components: int
) -> Generator[Scores, None, None]:
    if len(edgelist) == 0:
        raise StopIteration()

    edge_done = edgelist

    with tempfile.TemporaryDirectory() as path:
        filename = path + "/edge_done"
        edgelist = numpy.memmap(
            filename,
            dtype=(edge_done.dtype.descr + [("done", "int32")]),
            mode="w+",
            shape=edge_done.shape,
        )

        if hasattr(edge_done, "name"):
            assert isinstance(edge_done, numpy.memmap)
        else:
            return 0

    return edgelist
