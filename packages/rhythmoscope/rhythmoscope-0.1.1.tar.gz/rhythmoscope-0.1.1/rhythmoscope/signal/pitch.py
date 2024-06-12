import numpy as np
import numpy.typing as npt

from .rolling_window import RollingWindow


def _pitch_extraction(sr: int, signal: npt.NDArray, f0_min: float, f0_max: float):
    """
    Estimate the fundamental frequency of a short window of speech signal.
    This function use the cepstrum of the the signal in order to detect periodicity.
    Values detected outside of the [f0_min, f0_max] interval are set to 0.

    Args:
        signal (array): Raw signal
        sr (int): Sampling rate
        f0_min (int): The minimum f0 value to consider
        f0_max (int): The maximum f0 value to consider

    Returns:
        float: A single f0 estimation for the input signal window
    """
    signal = np.array(signal).astype(float)
    window_size = len(signal)

    # Apply Hann window to audio buffer
    hann_window = np.hanning(window_size)
    windowed_audio = signal * hann_window

    windowed_audio = np.pad(windowed_audio, (224, 224), constant_values=0)

    # Perform FFT on windowed audio buffer
    fft_result = np.abs(np.fft.fft(windowed_audio))
    # fft_result /= max(fft_result)
    power_spectrum = (fft_result**2) / len(fft_result)
    power_spectrum = power_spectrum / max(power_spectrum)
    n_fft = len(power_spectrum)

    # Calculate cepstrum from FFT data
    cepstrum = np.abs(np.fft.ifft(np.log(fft_result)))

    min_freq = int(sr / (f0_max + 200))

    cepstrum = cepstrum[min_freq : int(len(cepstrum) // 2)]
    idx_max = np.argmax(cepstrum)

    if (idx_max + min_freq) > int(sr / f0_min) or (idx_max + min_freq) <= int(
        sr / f0_max
    ):
        return 0
    return sr / (idx_max + int(sr / f0_max))


def cepstral_pitch(
    sr: int,
    signal: npt.NDArray,
    win_length: float,
    win_hop: float,
    f0_min: float,
    f0_max: float,
):
    """
    Perform f0 extraction on rolling windows of a speech signal

    Args:
        signal (array): Raw signal
        sr (int): Sampling rate
        win_length (float): The duration in seconds of the rolling windows
        win_hop (float): The time step in seconds between two windows
        f0_min (int): The minimum f0 value to consider
        f0_max (int): The maximum f0 value to consider

    Returns:
        list: A list containing the f0 values for each rolling window.
                The time duration separating two f0 values is defined by `win_hop`
    """
    pitch = []

    Window = RollingWindow(sr, signal, win_length, win_hop)

    for sliced_signal in Window:
        results = _pitch_extraction(sr, sliced_signal, f0_min, f0_max)
        pitch.append(results[0])

    time = np.linspace(0, ((len(Window) - 1) * win_hop), len(Window))
    return time, pitch
