import numpy.typing as npt


class BaseEnvelope:
    """
    Base class for an envelope extractor
    """

    def filter(self, sr: int, signal: npt.NDArray):
        raise NotImplementedError()
