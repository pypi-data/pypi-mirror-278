from typing import Tuple
import numpy.typing as npt

from .base import BaseEnvelope


class MomelEnvelope(BaseEnvelope):
    """
    Extract the intonation curve from raw pitch values by using a quadratic spline interpolation
    called Momel (Hirst & Espesser, 1999).

    Args:
            cut_frequency (float): The maximum frequency (Hz) to keep in the resulting envelope
            order (int, optional): The order of the Butterworth filter. Defaults to 3.
            initial_bandpass (Tuple[int], optional): The initial frequencies (min and max) of the
                                                     bandpass filter. Defaults to (700, 1300).
    """

    def __init__(
        self,
        cut_frequency: float = 10,
        order: int = 3,
        initial_bandpass: Tuple[float, float] = (300, 1000),
    ) -> None:

        self.cut_frequency = cut_frequency
        self.order = order
        self.initial_bandpass = initial_bandpass

    def filter(self, sr: int, signal: npt.NDArray) -> npt.NDArray:
        """
        Extract the envelope of a given signal

        Args:
            sr (int): Sampling rate of the signal
            signal (npt.ArrayLike[int | float]): One dimentional array containing the raw values
                                                 of the signal.
        """
        band_passed_signal = butterworth_filter(
            sr, signal, self.initial_bandpass[0], self.initial_bandpass[1], order=3
        )

        low_pass_signal = butterworth_filter(
            sr,
            np.abs(band_passed_signal),
            min_frequency=None,
            max_frequency=self.cut_frequency,
            order=self.order,
        )
        low_pass_signal -= np.mean(low_pass_signal)
        return low_pass_signal
