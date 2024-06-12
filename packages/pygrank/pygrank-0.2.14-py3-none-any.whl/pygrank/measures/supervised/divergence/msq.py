from pygrank.measures.supervised.supervised import Supervised
from pygrank.core import backend, GraphSignalData, BackendPrimitive


class MSQ(Supervised):
    """Computes the mean absolute error between scores and known scores."""

    def evaluate(self, scores: GraphSignalData) -> BackendPrimitive:
        known_scores, scores = self.to_numpy(scores)
        return backend.sum(
            (known_scores - scores) * (known_scores - scores)
        ) / backend.length(scores)
