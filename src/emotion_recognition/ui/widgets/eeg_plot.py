"""EEG visualization widget with matplotlib."""

from typing import Optional

import numpy as np
from loguru import logger
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from emotion_recognition.core.eeg_processor import EEGProcessor
from emotion_recognition.models.eeg import EEGData


class MatplotlibCanvas(FigureCanvas):
    """Matplotlib canvas for PyQt6."""

    def __init__(self, width: int = 8, height: int = 6, dpi: int = 100) -> None:
        """Initialize canvas.

        Args:
            width: Figure width in inches
            height: Figure height in inches
            dpi: Dots per inch
        """
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.patch.set_facecolor("#1e1e1e")
        super().__init__(self.fig)


class EEGPlotWidget(QWidget):
    """Widget for displaying EEG data visualizations."""

    def __init__(self, eeg_processor: EEGProcessor) -> None:
        """Initialize EEG plot widget.

        Args:
            eeg_processor: EEG processor instance
        """
        super().__init__()

        self.eeg_processor = eeg_processor

        # Create canvases
        self.time_canvas = MatplotlibCanvas(width=9, height=8, dpi=90)
        self.fft_canvas = MatplotlibCanvas(width=9, height=4, dpi=90)
        self.av_canvas = MatplotlibCanvas(width=5, height=5, dpi=100)

        # Setup layout
        self._setup_layout()

    def _setup_layout(self) -> None:
        """Setup widget layout."""
        main_layout = QHBoxLayout(self)

        # Left side: time domain and FFT
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.time_canvas)
        left_layout.addWidget(self.fft_canvas)

        # Right side: Arousal-Valence plot
        main_layout.addLayout(left_layout, stretch=2)
        main_layout.addWidget(self.av_canvas, stretch=1)

    def update_plots(
        self,
        eeg_data: EEGData,
        start_time: int,
        window_size: int,
    ) -> None:
        """Update all EEG plots.

        Args:
            eeg_data: EEG data object
            start_time: Start time index
            window_size: Time window size
        """
        try:
            self._plot_time_domain(eeg_data, start_time, window_size)
            self._plot_fft(eeg_data, start_time, window_size)
            self._plot_arousal_valence(eeg_data)
        except Exception as e:
            logger.error(f"Error updating EEG plots: {e}")

    def _plot_time_domain(
        self,
        eeg_data: EEGData,
        start_time: int,
        window_size: int,
    ) -> None:
        """Plot time domain EEG signals.

        Args:
            eeg_data: EEG data object
            start_time: Start time index
            window_size: Time window size
        """
        self.time_canvas.fig.clear()

        active_channels = self.eeg_processor.active_channels
        channel_map = self.eeg_processor.channel_map

        for idx, channel_name in enumerate(active_channels):
            ax = self.time_canvas.fig.add_subplot(len(active_channels), 1, idx + 1)

            # Get channel data
            channel_idx = channel_map[channel_name]
            end_time = min(start_time + window_size, eeg_data.data.shape[1])
            channel_data = eeg_data.data[channel_idx, start_time:end_time]

            # Plot
            time_points = np.arange(len(channel_data))
            ax.plot(time_points, channel_data, color=f"C{idx}", linewidth=1.5)

            # Styling
            ax.set_ylabel(channel_name, color="#4CAF50", fontweight="bold")
            ax.set_ylim([-200, 200])
            ax.grid(True, alpha=0.3, color="#3d3d3d")
            ax.set_facecolor("#1e1e1e")
            ax.tick_params(colors="#b0b0b0")

            if idx == 0:
                ax.set_title("EEG Time Domain Signals", color="#4CAF50", fontsize=12)

            if idx == len(active_channels) - 1:
                ax.set_xlabel("Time (samples)", color="#b0b0b0")

            # Hide x-axis labels for all but bottom plot
            if idx < len(active_channels) - 1:
                ax.set_xticklabels([])

        self.time_canvas.fig.tight_layout()
        self.time_canvas.draw()

    def _plot_fft(
        self,
        eeg_data: EEGData,
        start_time: int,
        window_size: int,
    ) -> None:
        """Plot FFT of EEG signals.

        Args:
            eeg_data: EEG data object
            start_time: Start time index
            window_size: Time window size
        """
        self.fft_canvas.fig.clear()
        ax = self.fft_canvas.fig.add_subplot(1, 1, 1)

        active_channels = self.eeg_processor.active_channels
        channel_map = self.eeg_processor.channel_map

        for idx, channel_name in enumerate(active_channels):
            # Get channel data
            channel_idx = channel_map[channel_name]
            end_time = min(start_time + window_size, eeg_data.data.shape[1])
            channel_data = eeg_data.data[channel_idx, start_time:end_time]

            # Compute FFT
            fft_freq, fft_db = self.eeg_processor.compute_fft(channel_data, sampling_rate=60)

            # Plot
            ax.plot(fft_freq, fft_db, label=channel_name, color=f"C{idx}", linewidth=1.5)

        # Styling
        ax.set_title("FFT Spectrum", color="#2196F3", fontsize=12, fontweight="bold")
        ax.set_xlabel("Frequency (Hz)", color="#b0b0b0")
        ax.set_ylabel("Amplitude (dB)", color="#b0b0b0")
        ax.set_ylim([-20, 100])
        ax.grid(True, alpha=0.3, color="#3d3d3d")
        ax.legend(loc="upper right", facecolor="#2d2d2d", edgecolor="#4CAF50")
        ax.set_facecolor("#1e1e1e")
        ax.tick_params(colors="#b0b0b0")

        self.fft_canvas.fig.tight_layout()
        self.fft_canvas.draw()

    def _plot_arousal_valence(self, eeg_data: EEGData) -> None:
        """Plot arousal-valence scatter plot.

        Args:
            eeg_data: EEG data object
        """
        self.av_canvas.fig.clear()
        ax = self.av_canvas.fig.add_subplot(1, 1, 1)

        valence = eeg_data.label.valence
        arousal = eeg_data.label.arousal

        # Plot point
        ax.scatter(valence, arousal, marker="o", c="#4CAF50", s=100, edgecolors="white", linewidths=2)

        # Plot quadrant lines
        ax.axvline(5, color="#f44336", linestyle="--", linewidth=1.5, alpha=0.7)
        ax.axhline(5, color="#f44336", linestyle="--", linewidth=1.5, alpha=0.7)

        # Add quadrant labels
        ax.text(3, 7.5, "HAHV", ha="center", va="center", fontsize=10, color="#b0b0b0")
        ax.text(7, 7.5, "HALV", ha="center", va="center", fontsize=10, color="#b0b0b0")
        ax.text(3, 2.5, "LAHV", ha="center", va="center", fontsize=10, color="#b0b0b0")
        ax.text(7, 2.5, "LALV", ha="center", va="center", fontsize=10, color="#b0b0b0")

        # Styling
        ax.set_title(
            "Arousal-Valence Space", color="#FF9800", fontsize=12, fontweight="bold"
        )
        ax.set_xlabel("Valence", color="#b0b0b0")
        ax.set_ylabel("Arousal", color="#b0b0b0")
        ax.set_xlim([1, 9])
        ax.set_ylim([1, 9])
        ax.grid(True, alpha=0.3, color="#3d3d3d")
        ax.set_facecolor("#1e1e1e")
        ax.tick_params(colors="#b0b0b0")

        self.av_canvas.fig.tight_layout()
        self.av_canvas.draw()
