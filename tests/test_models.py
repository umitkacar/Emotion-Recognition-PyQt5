"""Tests for data models."""

import numpy as np
import pytest

from emotion_recognition.models.eeg import EEGData, EmotionLabel
from emotion_recognition.models.face import BoundingBox, FaceDetection


class TestEmotionLabel:
    """Tests for EmotionLabel model."""

    def test_valid_emotion_label(self):
        """Test creating a valid emotion label."""
        label = EmotionLabel(valence=5.0, arousal=6.0, dominance=4.0, liking=7.0)

        assert label.valence == 5.0
        assert label.arousal == 6.0
        assert label.dominance == 4.0
        assert label.liking == 7.0

    def test_emotion_label_out_of_range(self):
        """Test that out-of-range values are rejected."""
        with pytest.raises(Exception):
            EmotionLabel(valence=0.0, arousal=5.0, dominance=5.0, liking=5.0)

        with pytest.raises(Exception):
            EmotionLabel(valence=5.0, arousal=10.0, dominance=5.0, liking=5.0)

    def test_to_binary(self):
        """Test binary conversion."""
        label = EmotionLabel(valence=6.0, arousal=4.0, dominance=5.0, liking=5.0)

        binary = label.to_binary(threshold=4.5)

        assert binary["valence"] == 1  # 6.0 > 4.5
        assert binary["arousal"] == 0  # 4.0 < 4.5


class TestEEGData:
    """Tests for EEGData model."""

    def test_valid_eeg_data(self):
        """Test creating valid EEG data."""
        data = np.random.randn(40, 8064)
        label = EmotionLabel(valence=5.0, arousal=6.0, dominance=4.0, liking=7.0)

        eeg = EEGData(data=data, label=label, user_id=1, trial_id=1)

        assert eeg.data.shape == (40, 8064)
        assert eeg.user_id == 1
        assert eeg.trial_id == 1

    def test_invalid_data_shape(self):
        """Test that 1D data is rejected."""
        data = np.random.randn(8064)
        label = EmotionLabel(valence=5.0, arousal=6.0, dominance=4.0, liking=7.0)

        with pytest.raises(Exception):
            EEGData(data=data, label=label, user_id=1, trial_id=1)


class TestBoundingBox:
    """Tests for BoundingBox model."""

    def test_valid_bounding_box(self):
        """Test creating a valid bounding box."""
        box = BoundingBox(x=10, y=20, width=100, height=150)

        assert box.x == 10
        assert box.y == 20
        assert box.width == 100
        assert box.height == 150

    def test_bounding_box_methods(self):
        """Test bounding box utility methods."""
        box = BoundingBox(x=10, y=20, width=100, height=150)

        assert box.to_tuple() == (10, 20, 100, 150)
        assert box.get_center() == (60, 95)
        assert box.get_area() == 15000


class TestFaceDetection:
    """Tests for FaceDetection model."""

    def test_valid_face_detection(self):
        """Test creating a valid face detection."""
        box = BoundingBox(x=10, y=20, width=100, height=150)
        face = FaceDetection(box=box, confidence=0.95)

        assert face.box == box
        assert face.confidence == 0.95

    def test_invalid_confidence(self):
        """Test that invalid confidence values are rejected."""
        box = BoundingBox(x=10, y=20, width=100, height=150)

        with pytest.raises(Exception):
            FaceDetection(box=box, confidence=1.5)
