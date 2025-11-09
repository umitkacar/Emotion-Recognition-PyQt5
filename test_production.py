"""Comprehensive production test suite for emotion recognition system."""

import sys

import numpy as np


def test_all_imports():
    """Test all core module imports."""
    print("\n=== Testing Module Imports ===")
    modules = [
        "emotion_recognition",
        "emotion_recognition.config",
        "emotion_recognition.utils.logger",
        "emotion_recognition.models.eeg",
        "emotion_recognition.models.face",
        "emotion_recognition.core.camera",
        "emotion_recognition.core.eeg_processor",
        "emotion_recognition.core.ml_models",
    ]

    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except Exception as e:
            print(f"❌ {module}: {e}")
            return False
    return True


def test_configuration():
    """Test configuration system."""
    print("\n=== Testing Configuration ===")
    from emotion_recognition.config import Settings, get_settings

    # Test default settings
    settings = Settings()
    assert settings.app_name == "Emotion Recognition System"
    assert settings.app_version == "2.0.0"
    print("✅ Default settings")

    # Test validation
    try:
        Settings(label_threshold=10.5)
        print("❌ Validation failed")
        return False
    except Exception:
        print("✅ Field validation")

    # Test caching
    s1 = get_settings()
    s2 = get_settings()
    assert s1 is s2
    print("✅ Settings caching")

    return True


def test_eeg_models():
    """Test EEG data models."""
    print("\n=== Testing EEG Models ===")
    from emotion_recognition.models.eeg import EEGData, EmotionLabel

    # Test EmotionLabel
    label = EmotionLabel(valence=6.0, arousal=7.0, dominance=5.0, liking=6.5)
    assert label.valence == 6.0
    print("✅ EmotionLabel creation")

    # Test binary conversion
    binary = label.to_binary(threshold=4.5)
    assert binary["valence"] == 1
    assert binary["arousal"] == 1
    print("✅ Binary label conversion")

    # Test EEGData
    data = np.random.randn(40, 8064)
    eeg_data = EEGData(data=data, label=label, user_id=1, trial_id=1)
    assert eeg_data.data.shape == (40, 8064)
    print("✅ EEGData creation")

    return True


def test_face_models():
    """Test face detection models."""
    print("\n=== Testing Face Models ===")
    from emotion_recognition.models.face import BoundingBox, FaceDetection, FaceDetectionResult

    # Test BoundingBox
    bbox = BoundingBox(x=100, y=150, width=200, height=250)
    assert bbox.get_area() == 50000
    assert bbox.get_center() == (200, 275)
    print("✅ BoundingBox methods")

    # Test FaceDetection
    face = FaceDetection(box=bbox, confidence=0.95)
    assert face.confidence == 0.95
    print("✅ FaceDetection creation")

    # Test FaceDetectionResult
    result = FaceDetectionResult(faces=[face], processing_time_ms=15.5)
    assert len(result) == 1
    assert result.has_faces()
    print("✅ FaceDetectionResult")

    return True


def test_eeg_processor():
    """Test EEG processor."""
    print("\n=== Testing EEG Processor ===")
    from emotion_recognition.config import Settings
    from emotion_recognition.core.eeg_processor import EEGProcessor

    settings = Settings()
    processor = EEGProcessor(settings)

    # Test channel map
    assert len(processor.channel_map) == 14
    assert len(processor.active_channels) == 5
    print("✅ Channel management")

    # Test FFT
    test_signal = np.sin(2 * np.pi * 10 * np.linspace(0, 1, 1000))
    fft_freq, fft_db = processor.compute_fft(test_signal, sampling_rate=1000)
    assert len(fft_freq) > 0
    print("✅ FFT computation")

    # Test binary conversion
    labels = np.array([3.0, 5.0, 7.0])
    binary = processor.labels_to_binary(labels, threshold=4.5)
    assert list(binary) == [0, 1, 1]
    print("✅ Label binarization")

    return True


def test_ml_models():
    """Test ML models."""
    print("\n=== Testing ML Models ===")
    from emotion_recognition.config import Settings
    from emotion_recognition.core.ml_models import MLModelManager

    settings = Settings()
    ml_manager = MLModelManager(settings)

    # Test model creation
    ml_manager.create_model("KNN")
    assert ml_manager.arousal_model is not None
    assert ml_manager.valence_model is not None
    print("✅ Model creation")

    # Test training
    train_data = np.random.randn(50, 100)
    train_labels = np.random.randint(0, 2, 50)
    ml_manager.set_training_data(train_data, train_labels, train_labels)

    success = ml_manager.train()
    assert success
    print("✅ Model training")

    # Test prediction
    test_data = np.random.randn(10, 100)
    test_labels = np.random.randint(0, 2, 10)
    ml_manager.set_test_data(test_data, test_labels, test_labels)

    success = ml_manager.predict()
    assert success
    print("✅ Model prediction")

    # Test results
    results = ml_manager.get_results()
    assert results is not None
    assert "arousal_accuracy" in results
    assert "valence_accuracy" in results
    print("✅ Results generation")

    return True


def test_camera_module():
    """Test camera module (non-hardware parts)."""
    print("\n=== Testing Camera Module ===")
    from emotion_recognition.core.camera import CameraManager

    camera = CameraManager(camera_index=0, width=640, height=480)
    assert camera.camera_index == 0
    assert camera.width == 640
    assert camera.height == 480
    print("✅ CameraManager initialization")

    return True


def main():
    """Run all production tests."""
    print("=" * 60)
    print("EMOTION RECOGNITION - PRODUCTION TEST SUITE")
    print("=" * 60)

    tests = [
        ("Module Imports", test_all_imports),
        ("Configuration", test_configuration),
        ("EEG Models", test_eeg_models),
        ("Face Models", test_face_models),
        ("EEG Processor", test_eeg_processor),
        ("ML Models", test_ml_models),
        ("Camera Module", test_camera_module),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                print(f"❌ {name} test failed!")
        except Exception as e:
            failed += 1
            print(f"❌ {name} test crashed: {e}")

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("\n✅ ALL TESTS PASSED - READY FOR PRODUCTION!")
        return 0
    print(f"\n❌ {failed} TESTS FAILED - FIX BEFORE PRODUCTION")
    return 1


if __name__ == "__main__":
    sys.exit(main())
