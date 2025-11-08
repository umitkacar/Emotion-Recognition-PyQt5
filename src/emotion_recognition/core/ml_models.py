"""Machine learning models for emotion classification."""

import pickle
from pathlib import Path
from typing import Dict, Literal, Optional, Tuple

import numpy as np
from loguru import logger
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from emotion_recognition.config import Settings

ModelType = Literal["KNN", "SVM", "PCA+KNN", "PCA+SVM"]


class MLModelManager:
    """Manages machine learning models for emotion recognition."""

    def __init__(self, settings: Settings) -> None:
        """Initialize ML model manager.

        Args:
            settings: Application settings
        """
        self.settings = settings

        # Models for arousal and valence
        self.arousal_model: Optional[object] = None
        self.valence_model: Optional[object] = None

        # PCA transformers (if using PCA)
        self.arousal_pca: Optional[PCA] = None
        self.valence_pca: Optional[PCA] = None

        # Training data (kept for reference)
        self.train_data: Optional[np.ndarray] = None
        self.train_valence: Optional[np.ndarray] = None
        self.train_arousal: Optional[np.ndarray] = None

        # Test data
        self.test_data: Optional[np.ndarray] = None
        self.test_valence: Optional[np.ndarray] = None
        self.test_arousal: Optional[np.ndarray] = None

        # Predictions
        self.pred_valence: Optional[np.ndarray] = None
        self.pred_arousal: Optional[np.ndarray] = None

        # Current model type
        self.current_model_type: Optional[ModelType] = None

        logger.info("MLModelManager initialized")

    def create_model(self, model_type: ModelType) -> None:
        """Create and initialize models.

        Args:
            model_type: Type of model to create
        """
        logger.info(f"Creating {model_type} models...")

        if model_type == "KNN":
            self.arousal_model = KNeighborsClassifier(
                n_neighbors=self.settings.knn_neighbors,
                leaf_size=self.settings.knn_leaf_size,
                n_jobs=-1,  # Use all CPUs
            )
            self.valence_model = KNeighborsClassifier(
                n_neighbors=self.settings.knn_neighbors,
                leaf_size=self.settings.knn_leaf_size,
                n_jobs=-1,
            )
            self.arousal_pca = None
            self.valence_pca = None

        elif model_type == "SVM":
            self.arousal_model = SVC(
                kernel="rbf",
                C=1.0,
                gamma="scale",
                cache_size=500,
                random_state=42,
            )
            self.valence_model = SVC(
                kernel="rbf",
                C=1.0,
                gamma="scale",
                cache_size=500,
                random_state=42,
            )
            self.arousal_pca = None
            self.valence_pca = None

        elif model_type == "PCA+KNN":
            # Create PCA transformers
            self.arousal_pca = PCA(n_components=100, random_state=42)
            self.valence_pca = PCA(n_components=100, random_state=42)

            # Create KNN classifiers
            self.arousal_model = KNeighborsClassifier(
                n_neighbors=self.settings.knn_neighbors,
                leaf_size=self.settings.knn_leaf_size,
                n_jobs=-1,
            )
            self.valence_model = KNeighborsClassifier(
                n_neighbors=self.settings.knn_neighbors,
                leaf_size=self.settings.knn_leaf_size,
                n_jobs=-1,
            )

        elif model_type == "PCA+SVM":
            # Create PCA transformers
            self.arousal_pca = PCA(n_components=100, random_state=42)
            self.valence_pca = PCA(n_components=100, random_state=42)

            # Create SVM classifiers
            self.arousal_model = SVC(
                kernel="rbf",
                C=1.0,
                gamma="scale",
                cache_size=500,
                random_state=42,
            )
            self.valence_model = SVC(
                kernel="rbf",
                C=1.0,
                gamma="scale",
                cache_size=500,
                random_state=42,
            )

        else:
            raise ValueError(f"Unknown model type: {model_type}")

        self.current_model_type = model_type
        logger.info(f"{model_type} models created successfully")

    def set_training_data(
        self,
        data: np.ndarray,
        valence_labels: np.ndarray,
        arousal_labels: np.ndarray,
    ) -> None:
        """Set training data.

        Args:
            data: Training data array
            valence_labels: Valence labels
            arousal_labels: Arousal labels
        """
        self.train_data = data
        self.train_valence = valence_labels
        self.train_arousal = arousal_labels

        logger.info(f"Training data set: {data.shape}")

    def set_test_data(
        self,
        data: np.ndarray,
        valence_labels: np.ndarray,
        arousal_labels: np.ndarray,
    ) -> None:
        """Set test data.

        Args:
            data: Test data array
            valence_labels: Valence labels
            arousal_labels: Arousal labels
        """
        self.test_data = data
        self.test_valence = valence_labels
        self.test_arousal = arousal_labels

        logger.info(f"Test data set: {data.shape}")

    def train(self) -> bool:
        """Train the models.

        Returns:
            True if training successful, False otherwise
        """
        if self.arousal_model is None or self.valence_model is None:
            logger.error("Models not created. Call create_model() first")
            return False

        if self.train_data is None or self.train_valence is None or self.train_arousal is None:
            logger.error("Training data not set. Call set_training_data() first")
            return False

        try:
            logger.info("Training models...")

            train_data = self.train_data

            # Apply PCA if using PCA models
            if self.arousal_pca is not None:
                logger.info("Applying PCA transformation for arousal...")
                train_data_arousal = self.arousal_pca.fit_transform(train_data)
            else:
                train_data_arousal = train_data

            if self.valence_pca is not None:
                logger.info("Applying PCA transformation for valence...")
                train_data_valence = self.valence_pca.fit_transform(train_data)
            else:
                train_data_valence = train_data

            # Train arousal model
            logger.info("Training arousal model...")
            self.arousal_model.fit(train_data_arousal, self.train_arousal)

            # Train valence model
            logger.info("Training valence model...")
            self.valence_model.fit(train_data_valence, self.train_valence)

            logger.info("Training completed successfully")
            return True

        except Exception as e:
            logger.error(f"Error during training: {e}")
            return False

    def predict(self) -> bool:
        """Run prediction on test data.

        Returns:
            True if prediction successful, False otherwise
        """
        if self.arousal_model is None or self.valence_model is None:
            logger.error("Models not trained. Call train() first")
            return False

        if self.test_data is None:
            logger.error("Test data not set. Call set_test_data() first")
            return False

        try:
            logger.info("Running predictions...")

            test_data = self.test_data

            # Apply PCA if using PCA models
            if self.arousal_pca is not None:
                test_data_arousal = self.arousal_pca.transform(test_data)
            else:
                test_data_arousal = test_data

            if self.valence_pca is not None:
                test_data_valence = self.valence_pca.transform(test_data)
            else:
                test_data_valence = test_data

            # Predict
            self.pred_arousal = self.arousal_model.predict(test_data_arousal)
            self.pred_valence = self.valence_model.predict(test_data_valence)

            logger.info("Predictions completed successfully")
            return True

        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return False

    def get_results(self) -> Optional[Dict[str, any]]:
        """Get prediction results and metrics.

        Returns:
            Dictionary with results or None if predictions not available
        """
        if (
            self.pred_arousal is None
            or self.pred_valence is None
            or self.test_arousal is None
            or self.test_valence is None
        ):
            logger.error("Predictions not available. Call predict() first")
            return None

        # Calculate metrics
        arousal_accuracy = accuracy_score(self.test_arousal, self.pred_arousal)
        valence_accuracy = accuracy_score(self.test_valence, self.pred_valence)

        arousal_cm = confusion_matrix(self.test_arousal, self.pred_arousal)
        valence_cm = confusion_matrix(self.test_valence, self.pred_valence)

        results = {
            "arousal_accuracy": arousal_accuracy,
            "valence_accuracy": valence_accuracy,
            "arousal_confusion_matrix": arousal_cm,
            "valence_confusion_matrix": valence_cm,
            "arousal_predictions": self.pred_arousal,
            "valence_predictions": self.pred_valence,
        }

        logger.info(f"Arousal accuracy: {arousal_accuracy:.4f}")
        logger.info(f"Valence accuracy: {valence_accuracy:.4f}")

        return results

    def save_models(self, path: Optional[Path] = None) -> bool:
        """Save trained models to disk.

        Args:
            path: Directory path to save models (uses settings if None)

        Returns:
            True if save successful, False otherwise
        """
        if self.arousal_model is None or self.valence_model is None:
            logger.error("No models to save")
            return False

        try:
            if path is None:
                path = self.settings.models_dir

            path.mkdir(parents=True, exist_ok=True)

            # Save models
            arousal_path = path / "model_arousal.pkl"
            valence_path = path / "model_valence.pkl"

            with open(arousal_path, "wb") as f:
                pickle.dump(self.arousal_model, f)

            with open(valence_path, "wb") as f:
                pickle.dump(self.valence_model, f)

            # Save PCA if exists
            if self.arousal_pca is not None:
                arousal_pca_path = path / "pca_arousal.pkl"
                with open(arousal_pca_path, "wb") as f:
                    pickle.dump(self.arousal_pca, f)

            if self.valence_pca is not None:
                valence_pca_path = path / "pca_valence.pkl"
                with open(valence_pca_path, "wb") as f:
                    pickle.dump(self.valence_pca, f)

            logger.info(f"Models saved to {path}")
            return True

        except Exception as e:
            logger.error(f"Error saving models: {e}")
            return False

    def load_models(self, path: Optional[Path] = None) -> bool:
        """Load trained models from disk.

        Args:
            path: Directory path to load models from (uses settings if None)

        Returns:
            True if load successful, False otherwise
        """
        try:
            if path is None:
                path = self.settings.models_dir

            arousal_path = path / "model_arousal.pkl"
            valence_path = path / "model_valence.pkl"

            if not arousal_path.exists() or not valence_path.exists():
                logger.error(f"Model files not found in {path}")
                return False

            # Load models
            with open(arousal_path, "rb") as f:
                self.arousal_model = pickle.load(f)

            with open(valence_path, "rb") as f:
                self.valence_model = pickle.load(f)

            # Try to load PCA
            arousal_pca_path = path / "pca_arousal.pkl"
            valence_pca_path = path / "pca_valence.pkl"

            if arousal_pca_path.exists():
                with open(arousal_pca_path, "rb") as f:
                    self.arousal_pca = pickle.load(f)

            if valence_pca_path.exists():
                with open(valence_pca_path, "rb") as f:
                    self.valence_pca = pickle.load(f)

            logger.info(f"Models loaded from {path}")
            return True

        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False
