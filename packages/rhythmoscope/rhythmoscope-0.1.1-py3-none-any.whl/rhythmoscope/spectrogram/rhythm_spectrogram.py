import numpy as np
import numpy.typing as npt
from typing import Union, Optional, List, Tuple

from rhythmoscope import ems as ems_module
from rhythmoscope.signal import RollingWindow
from rhythmoscope import spectrogram
from rhythmoscope.signal import load_wavfile


class RhythmSpectrogramExtractor:
    """
    Object

        Args:
            sr (int): Sampling rate of the signal
            signal (npt.ArrayLike[int | float]): A one dimentional array containing the raw values
                                                 of the signal.

    """
    def __init__(self, EMSExtractor: ems_module.EMSExtractor, Window: RollingWindow=RollingWindow(), smoothing: bool=False) -> None:
        self.EMSExtractor = EMSExtractor
        self.Window = Window
        self.smoothing = smoothing

    def from_file(
        self, file: str, start: float = 0, end: Optional[float] = None
    ):
        """
        Extract EMS from a .wav file

        Args:
            file (str): Path to the audio file
            start (float, optional): The timestamp (in seconds) at which to start processing the
                                     file. Defaults to 0.
            end (Optional[float], optional): The timestamp (in seconds) at which to end processing
                                             the file. Defaults to None.
        """
        time, signal, sr = load_wavfile(file, start, end)
        times, frequencies, spectro = self._extract_spectrogram(sr, signal)
        return spectrogram.RhythmSpectrogram(times=times, frequencies=frequencies, spectrogram=spectro)

    def from_signal(self, sr: int, signal: Union[List, npt.NDArray]):
        """
        Extract EMS of a signal waveform

        Args:
            sr (int): Sampling rate of the signal
            signal (npt.NDArray): Raw data from the signal waveform. This should be
        """
        times, frequencies, spectro = self._extract_spectrogram(sr, signal)
        return spectrogram.RhythmSpectrogram(times=times, frequencies=frequencies, spectrogram=spectro)

    def _extract_spectrogram(
        self, sr: int, signal: Union[List, npt.NDArray]) -> Tuple[npt.NDArray, npt.NDArray]:
        
        times, spectrogram = [], []
        print(self.Window(sr, signal))
        for i, (start_time, end_time, frame_values) in enumerate(self.Window(sr, signal)):
            times.append(start_time)
            #Compute EMS
            EMS = self.EMSExtractor.from_signal(sr, frame_values)

            if self.smoothing:
                spectrum = EMS.smoothed_ems
            else:
                spectrum = EMS.ems
            
            spectrogram.append(spectrum)

        return np.array(times), EMS.frequencies, np.array(spectrogram).T
            
            
