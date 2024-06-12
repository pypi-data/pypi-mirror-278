from scipy.signal import butter, filtfilt  # type: ignore
import numpy.typing as npt
from typing import Optional, Union, List


def butterworth_filter(
    sr: int,
    signal: npt.NDArray,
    min_frequency: Optional[float] = None,
    max_frequency: Optional[float] = None,
    order: int = 3,
):
    """
    Apply a band pass frequency filter (Butterworth) on a signal.

    Args:
        sr (int): The sampling frequency of the signal
        signal (np.array): The signal to filter
        min_frequency (float): The upper frequency (Hertz) you want to keep
        max_frequency (float): The upper frequency (Hertz) you want to keep
        filter_order (int): The order of the Butterworth filter
    """
    if min_frequency is not None and max_frequency is not None:
        Ws: Union[List, float] = [min_frequency / (sr / 2), max_frequency / (sr / 2)]
        filter_type: str = "bandpass"
    elif max_frequency is not None:
        Ws = max_frequency / (sr / 2)
        filter_type = "lowpass"
    elif min_frequency is not None:
        Ws = min_frequency / (sr / 2)
        filter_type = "highpass"
    else:
        raise ValueError(
            "At least one of `min_frequency` or `max_frequency` must not be None"
        )

    b, a = butter(order, Ws, btype=filter_type)
    filtered_signal = filtfilt(b, a, signal)
    return filtered_signal
