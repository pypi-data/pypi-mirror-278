import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt  # type: ignore
from matplotlib.ticker import FormatStrFormatter
from typing import Optional, Tuple


class RhythmSpectrogram:
    def __init__(
        self, times: npt.NDArray, frequencies: npt.NDArray, spectrogram: npt.NDArray
    ) -> None:
        """
        Object representation of an EMS object.

        Args:

        """
        self.times = times
        self.frequencies = frequencies
        self.spectrogram = spectrogram

    def plot(
        self,
        time_range: Optional[Tuple] = None,
        freq_range: Optional[Tuple] = None,
        log_spectrogram: bool = False,
        ylog: Optional[bool] = False,
        savefig: str = "",
    ):
        if time_range is not None:
            ids_time = np.where(
                np.logical_and(self.times <= time_range[1], self.times >= time_range[0])
            )[0]
        else:
            ids_time = np.arange(len(self.times))

        if freq_range is not None:
            ids_freqs = np.where(
                np.logical_and(
                    self.frequencies <= freq_range[1], self.frequencies >= freq_range[0]
                )
            )[0]
        else:
            ids_freqs = np.arange(len(self.frequencies))

        if log_spectrogram:
            spectrogram = np.sqrt(self.spectrogram)
        else:
            spectrogram = self.spectrogram
        fig = plt.figure()
        plt.pcolormesh(
            self.times[ids_time[0] : ids_time[-1]],
            self.frequencies[ids_freqs[0] : ids_freqs[-1]],
            spectrogram[ids_freqs[0] : ids_freqs[-1], ids_time[0] : ids_time[-1]],
            cmap="Oranges",
        )

        if ylog:
            ax = plt.gca()
            ax.set_yscale("log")
            plt.tick_params(axis="y", which="minor")
            ax.yaxis.set_minor_formatter(FormatStrFormatter("%.1f"))
        plt.ylabel("Frequency (Hz)")
        plt.xlabel("Time (s)")

        if savefig:
            plt.savefig(savefig)
        return fig
