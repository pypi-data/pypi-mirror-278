import numpy as np
import numpy.typing as npt
from scipy.signal import find_peaks  # type: ignore
from scipy.interpolate import Akima1DInterpolator  # type: ignore
import plotly.graph_objects as go  # type: ignore


class EMS:
    def __init__(self, frequencies: npt.NDArray, ems: npt.NDArray) -> None:
        """
        Object representation of an EMS object.

        Args:

        """
        self.frequencies = frequencies
        self.ems = ems
        self.l2_norm = np.sqrt(np.sum(ems**2))
        self.smoothing_window = int(len(ems) // 25)
        self.smoothed_ems = None
        self.update_smoothing(smoothing_window=self.smoothing_window)

    def update_smoothing(self, smoothing_window: int = 8):
        self.smoothing_window = smoothing_window
        rolling_mean = []
        half_win = int(smoothing_window / 2)
        for i in range(half_win, len(self.ems) - half_win + 1, smoothing_window):
            rolling_mean.append(
                sum(self.ems[i - half_win : i + half_win]) / smoothing_window
            )

        frequencies = np.insert(
            self.frequencies[::smoothing_window][: len(rolling_mean)], 0, [-0.1]
        )
        rolling_mean = np.insert(rolling_mean, 0, [0])
        frequencies += 0.1
        interp = Akima1DInterpolator(frequencies, rolling_mean)
        smoothed_ems = interp(self.frequencies)
        adjusted_smoothed_ems = smoothed_ems * (max(self.ems) / max(smoothed_ems)) * 0.9
        self.smoothed_ems = adjusted_smoothed_ems

    def energy_band(self, lower_bound: float, upper_bound: float) -> float:
        """
        Extract the energy in the specified frequency range

        Args:
            lower_bound (float): Lower frequency (Hz) of the energy band
            upper_bound (float): Upper frequency (Hz) of the energy band
        """
        freq_list = np.where(
            np.logical_and(
                self.frequencies <= upper_bound, self.frequencies >= lower_bound
            )
        )[0]
        energy = np.sum(self.ems[freq_list]) / self.l2_norm
        return energy

    def peaks(
        self,
        on_smoothing: bool = True,
        n_peaks: int = 3,
        tol: float = 0.2,
        lower_bound: float = 0,
        upper_bound: float = 10,
        sort_by: str = "magnitude",
    ):
        """
        Extract the frequencies of the main peaks in the Envelope Modulation Spectrum

        Args:
            magnitudes (np.array): Spectrum magnitudes
            freqs (np.array): The list of frequencies associated to `magnitudes`
            n_peaks (int, optional): The number of peaks to extract. Defaults to 3.
            tol (float, optional): The minimum frequency spacing between two peaks (in Hz)
            sort_by (str, optional): The way to sort the output peaks wether by magnitude
                                    (default) or by frequency (increasing order), possible
                                    values are "magnitude" or "frequency"
        """
        freq_step = abs(self.frequencies[1] - self.frequencies[0])
        ids_freqs = np.where(
            np.logical_and(
                self.frequencies >= lower_bound, self.frequencies <= upper_bound
            )
        )[0]
        if on_smoothing:
            magnitudes = self.smoothed_ems[ids_freqs]
        else:
            magnitudes = self.ems[ids_freqs]

        frequencies = self.frequencies[ids_freqs]
        peaks_idx, properties = find_peaks(
            magnitudes, distance=int(tol / freq_step), width=1, height=0.008
        )

        peaks_widths = properties["widths"]
        sorted_idx = np.argsort(magnitudes[peaks_idx])[::-1][:n_peaks]
        selected_peaks_idx = peaks_idx[sorted_idx]
        peaks_widths = peaks_widths[sorted_idx]

        if sort_by == "magnitude":
            return selected_peaks_idx + ids_freqs[0], peaks_widths
        elif sort_by == "frequency":
            freq_sort_idx = np.argsort(frequencies[selected_peaks_idx])
            return (
                selected_peaks_idx[freq_sort_idx] + ids_freqs[0],
                peaks_widths[freq_sort_idx],
            )
        else:
            raise ValueError(
                "invalid value for 'sort_by' parameter, must be either 'magnitude' or 'frequency'"
            )

    def plot(self, plot_smoothing: bool = True, xlog: bool = False, saveplot: str = ""):

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=self.frequencies,
                y=self.ems,
                name="EMS",
                mode="lines+markers",
                line_color="orange",
                marker=dict(size=2),
                customdata=([1 / f if f > 0 else 10 for f in self.frequencies]),
                hovertemplate="Amplitude: %{y:.1f}"
                + "<br>Frequency: %{x:.2f} Hz</br>"
                + "Period: %{customdata:.3f} sec",
                line=dict(width=5),
            )
        )
        # freqs += 0.1
        if plot_smoothing:
            fig.add_trace(
                go.Scatter(
                    x=self.frequencies,
                    y=self.smoothed_ems,
                    name="Smoothed EMS",
                    mode="lines+markers",
                    line_color="red",
                    marker=dict(size=2),
                    hoverinfo="skip",
                    line=dict(width=5, dash="dash"),
                )
            )

        fig.update_layout(
            autosize=False,
            width=1800,
            height=600,
            font=dict(size=22),
            plot_bgcolor="rgba(0,0,0,0)",
        )

        fig.update_xaxes(gridcolor="grey", linewidth=2, linecolor="black")
        fig.update_yaxes(gridcolor="grey", linewidth=2, linecolor="black")

        fig.update_xaxes(title_text="Frequency (Hz)")
        if xlog:
            fig.update_xaxes(
                type="log",
                range=[
                    np.log10(self.frequencies[0] + 0.0001),
                    np.log10(self.frequencies[-1]),
                ],
            )

        if saveplot:
            fig.write_image(saveplot)

        return fig
