from typing import Optional, Tuple, Union, List, Type
import numpy as np
import numpy.typing as npt
from scipy.signal.windows import tukey  # type: ignore
from scipy.signal import resample  # type: ignore

from rhythmoscope.envelope import BaseEnvelope, LowPassEnvelope
from rhythmoscope.signal import load_wavfile
from rhythmoscope import ems as ems_module


class EMSExtractor:

    def __init__(
        self,
        Envelope: BaseEnvelope = LowPassEnvelope(),
        min_freq: float = 0,
        max_freq: float = 10,
        n_fft: int = 1024,
        tukey_alpha: float = 0.2,
    ) -> None:
        """
        Object for Envelope Modulation Spectrum extraction of a signal.

        Args:
            Envelope (BaseEnvelope, optional): The signal envelope extractor. Defaults to
                                           LowPassEnvelope().
            freq_min (float): The minimum frequency you want
            freq_max (float): The maximum frequency you want
            n_points (int, optional): The number of point to compute in the FFT. Defaults to 2048
            tukey_alpha (float, optional): _description_. Defaults to 0.2.
        """
        self.envelope = Envelope
        self.tukey_alpha = tukey_alpha
        self.min_freq = min_freq
        self.max_freq = max_freq
        self.n_fft = n_fft

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
        frequencies, ems = self._extract_ems(sr, signal)
        return ems_module.EMS(frequencies=frequencies, ems=ems)

    def from_signal(self, sr: int, signal: Union[List, npt.NDArray]):
        """
        Extract EMS of a signal waveform

        Args:
            sr (int): Sampling rate of the signal
            signal (npt.NDArray): Raw data from the signal waveform. This should be
        """
        frequencies, ems = self._extract_ems(sr, signal)
        return ems_module.EMS(frequencies=frequencies, ems=ems)

    def _extract_ems(
        self, sr: int, signal: Union[List, npt.NDArray], normalize: bool = True
    ) -> Tuple[npt.NDArray, npt.NDArray]:

        # Format audio
        signal = np.array(signal).astype(float)
        # Compute envelope
        envelope = self.envelope.filter(sr, signal)
        # Apply a Tukey window
        envelope = envelope * tukey(len(envelope), self.tukey_alpha)
        envelope_nrj = np.sqrt(np.sum(envelope**2))
        # Downsample to 100 Hz for faster computation
        downsampled_sr = 100
        envelope = resample(envelope, int(downsampled_sr * (len(envelope) / sr)))
        # Spectrum
        frequencies, ems = self._extract_spectrum(downsampled_sr, envelope)

        # Compute the energy of all the signal to normalize the EMS values. The energy obtained
        # is the same as computing the one in frequency domain (Parceval theorem)
        if normalize:
            ems /= envelope_nrj
        return frequencies, ems

    def _extract_spectrum(self, sr: int, signal: npt.NDArray):
        """
        Extract the Fourier transform of a signal in a frequency band

        Args:
            sr (int): Sampling rate of the signal
            signal (np.array): The signal to transform
        """
        spectrum = np.abs(np.fft.fft(signal, self.n_fft)) ** 2
        freqs = np.abs(np.fft.fftfreq(len(spectrum), 1 / sr))

        half_len = int(len(freqs) // 2.0)
        frequencies = freqs[:half_len]
        spectrum = spectrum[:half_len]

        idxs = np.where(
            np.logical_and(frequencies <= self.max_freq, frequencies >= self.min_freq)
        )[0]
        return frequencies[idxs], spectrum[idxs]
