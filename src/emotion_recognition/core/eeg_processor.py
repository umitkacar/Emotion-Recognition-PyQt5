"""EEG data processing and management."""

import pickle
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from loguru import logger

from emotion_recognition.config import Settings
from emotion_recognition.models.eeg import EEGData, EmotionLabel


class EEGProcessor:
    """Processes EEG data from DEAP dataset with modern error handling."""

    def __init__(self, settings: Settings) -> None:
        """Initialize EEG processor.

        Args:
            settings: Application settings
        """
        self.settings = settings
        self._channel_map: Dict[str, int] = {
            "AF3": 1,
            "F7": 3,
            "F3": 2,
            "FC5": 4,
            "T7": 7,
            "P7": 11,
            "O1": 13,
            "O2": 31,
            "P8": 29,
            "T8": 25,
            "FC6": 21,
            "F4": 19,
            "F8": 20,
            "AF4": 17,
        }
        self._active_channels = ["AF3", "F7", "F3", "FC5", "T7"]

        logger.info("EEGProcessor initialized")

    @property
    def channel_map(self) -> Dict[str, int]:
        """Get channel name to index mapping."""
        return self._channel_map.copy()

    @property
    def active_channels(self) -> List[str]:
        """Get active channel names."""
        return self._active_channels.copy()

    def set_active_channels(self, channels: List[str]) -> None:
        """Set active channels for processing.

        Args:
            channels: List of channel names
        """
        invalid_channels = [ch for ch in channels if ch not in self._channel_map]
        if invalid_channels:
            raise ValueError(f"Invalid channels: {invalid_channels}")

        self._active_channels = channels
        logger.info(f"Active channels set to: {channels}")

    def load_user_data(self, user_id: int) -> Optional[Dict]:
        """Load EEG data for a specific user from DEAP dataset.

        Args:
            user_id: User ID (1-32)

        Returns:
            Dictionary with 'data' and 'labels' keys, or None if load fails
        """
        if not 1 <= user_id <= 32:
            logger.error(f"Invalid user_id: {user_id}. Must be between 1 and 32")
            return None

        filename = self.settings.raw_data_eeg_path / f"s{user_id:02d}.dat"

        if not filename.exists():
            logger.error(f"Data file not found: {filename}")
            return None

        try:
            with open(filename, "rb") as f:
                data = pickle.load(f, encoding="latin1")

            logger.info(f"Loaded data for user {user_id} from {filename}")
            return data

        except Exception as e:
            logger.error(f"Error loading data for user {user_id}: {e}")
            return None

    def extract_trial_data(
        self, user_data: Dict, trial_id: int, user_id: int
    ) -> Optional[EEGData]:
        """Extract EEG data for a specific trial.

        Args:
            user_data: User data dictionary from DEAP
            trial_id: Trial ID (1-40)
            user_id: User ID (for metadata)

        Returns:
            EEGData object or None if extraction fails
        """
        if not 1 <= trial_id <= 40:
            logger.error(f"Invalid trial_id: {trial_id}. Must be between 1 and 40")
            return None

        try:
            trial_idx = trial_id - 1  # Convert to 0-based index
            eeg_array = user_data["data"][trial_idx]  # Shape: (40, 8064)
            labels = user_data["labels"][trial_idx]  # Shape: (4,)

            # Create emotion label
            emotion_label = EmotionLabel(
                valence=float(labels[0]),
                arousal=float(labels[1]),
                dominance=float(labels[2]),
                liking=float(labels[3]),
            )

            # Create EEG data object
            eeg_data = EEGData(
                data=eeg_array, label=emotion_label, user_id=user_id, trial_id=trial_id
            )

            return eeg_data

        except Exception as e:
            logger.error(f"Error extracting trial {trial_id} for user {user_id}: {e}")
            return None

    def get_channel_data(
        self, eeg_data: EEGData, channel_names: Optional[List[str]] = None
    ) -> np.ndarray:
        """Extract specific channels from EEG data.

        Args:
            eeg_data: EEG data object
            channel_names: List of channel names (uses active channels if None)

        Returns:
            EEG data for selected channels
        """
        if channel_names is None:
            channel_names = self._active_channels

        # Get channel indices
        try:
            indices = [self._channel_map[ch] for ch in channel_names]
            return eeg_data.data[indices, :]
        except KeyError as e:
            logger.error(f"Invalid channel name: {e}")
            raise

    def compute_fft(
        self,
        data: np.ndarray,
        sampling_rate: int = 60,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Compute FFT of EEG signal.

        Args:
            data: EEG signal data (1D array)
            sampling_rate: Sampling rate in Hz

        Returns:
            Tuple of (frequencies, amplitudes)
        """
        # Compute FFT
        fft_values = np.abs(np.fft.rfft(data))
        fft_freq = np.fft.rfftfreq(len(data), 1.0 / sampling_rate)

        # Convert to dB scale
        fft_db = 20 * np.log10(fft_values + 1e-10)  # Add small value to avoid log(0)

        return fft_freq, fft_db

    def extract_time_window(
        self,
        eeg_data: EEGData,
        start_idx: int,
        window_size: int,
    ) -> np.ndarray:
        """Extract time window from EEG data.

        Args:
            eeg_data: EEG data object
            start_idx: Start index
            window_size: Window size in samples

        Returns:
            EEG data for time window
        """
        end_idx = min(start_idx + window_size, eeg_data.data.shape[1])
        return eeg_data.data[:, start_idx:end_idx]

    def process_raw_data_batch(
        self,
        user_range: Tuple[int, int],
        trial_range: Tuple[int, int] = (1, 40),
        time_range: Tuple[int, int] = (384, 8064),
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Process batch of raw EEG data.

        Args:
            user_range: Tuple of (start_user, end_user) inclusive
            trial_range: Tuple of (start_trial, end_trial) inclusive
            time_range: Tuple of (start_time, end_time) inclusive

        Returns:
            Tuple of (data_array, valence_labels, arousal_labels)
        """
        data_list = []
        valence_list = []
        arousal_list = []

        start_user, end_user = user_range
        start_trial, end_trial = trial_range
        start_time, end_time = time_range

        logger.info(
            f"Processing batch: users {start_user}-{end_user}, "
            f"trials {start_trial}-{end_trial}"
        )

        for user_id in range(start_user, end_user + 1):
            user_data = self.load_user_data(user_id)
            if user_data is None:
                logger.warning(f"Skipping user {user_id}")
                continue

            for trial_id in range(start_trial, end_trial + 1):
                eeg_data = self.extract_trial_data(user_data, trial_id, user_id)
                if eeg_data is None:
                    continue

                # Extract active channels and time window
                channel_indices = [self._channel_map[ch] for ch in self._active_channels]
                trial_data = eeg_data.data[channel_indices, start_time:end_time]

                # Flatten to 1D
                flattened_data = trial_data.flatten()

                data_list.append(flattened_data)
                valence_list.append(eeg_data.label.valence)
                arousal_list.append(eeg_data.label.arousal)

        if not data_list:
            logger.error("No data processed")
            return np.array([]), np.array([]), np.array([])

        data_array = np.array(data_list)
        valence_array = np.array(valence_list)
        arousal_array = np.array(arousal_list)

        logger.info(f"Processed {len(data_list)} samples. Shape: {data_array.shape}")
        return data_array, valence_array, arousal_array

    def labels_to_binary(
        self, labels: np.ndarray, threshold: Optional[float] = None
    ) -> np.ndarray:
        """Convert continuous labels to binary classification.

        Args:
            labels: Array of continuous labels
            threshold: Classification threshold (uses settings if None)

        Returns:
            Binary labels (0 or 1)
        """
        if threshold is None:
            threshold = self.settings.label_threshold

        return (labels > threshold).astype(int)
