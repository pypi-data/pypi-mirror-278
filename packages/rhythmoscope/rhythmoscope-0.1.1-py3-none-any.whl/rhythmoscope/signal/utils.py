from scipy.io import wavfile  # type: ignore
import numpy as np
from typing import Optional


def load_wavfile(file: str, start: float = 0, end: Optional[float] = None):
    """
    Utility function to load a wave audio file.

    Args:
        file (str): Path to the .wav file
        start (float, optional): The start time in seconds. Defaults to 0.
        end (float, optional): The end time in seconds. If None, entire file will be read.
    """
    sr, signal = wavfile.read(file)
    signal = np.array(signal).astype(float)
    start = int(start * sr)
    if end is None:
        end = len(signal)
    else:
        end = int(end * sr)

    signal = signal[start:end]
    time = np.cumsum([1 / sr] * (end - start))
    return time, signal, sr
