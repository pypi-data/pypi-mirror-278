import numpy.typing as npt


class RollingWindow:
    """
    A generator which yield portions of a signal of length `window_size` seconds and with a hop length of
    `hop_size` seconds

    Args:
        window_size (float, optional): The length of the output windows in seconds. Defaults to 5.
        hop_size (float, optional): The offset (in seconds) between two successives windows.
                                  Defaults to 2
    """

    def __init__(self, window_size: float = 4, hop_size: float=0.5) -> None:
        self.window_size = window_size
        self.hop_size = hop_size

    def get_n_frame(self, sr: int, signal: npt.NDArray):
        window_size = int(self.window_size * sr)
        hop_size = int(self.hop_size * sr)
        return int((len(signal) - window_size) / hop_size) + 1

    def __call__(self, sr: int, signal: npt.NDArray):
        window_size = int(self.window_size * sr)
        hop_size = int(self.hop_size * sr)
        for i in range(0, len(signal) - window_size + 1, hop_size):
            yield i / sr, (i + window_size) / sr, signal[i : i + window_size]