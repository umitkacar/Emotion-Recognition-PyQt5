"""Camera management with face detection."""

import time

import cv2
import numpy as np
from loguru import logger
from mtcnn import MTCNN

from emotion_recognition.models.face import BoundingBox, FaceDetection, FaceDetectionResult


class CameraManager:
    """Manages camera capture and face detection with robust error handling."""

    def __init__(
        self,
        camera_index: int = 0,
        width: int = 640,
        height: int = 480,
        fps: int = 30,
    ) -> None:
        """Initialize camera manager.

        Args:
            camera_index: Camera device index
            width: Frame width
            height: Frame height
            fps: Target frames per second
        """
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.fps = fps

        self._capture: cv2.VideoCapture | None = None
        self._detector: MTCNN | None = None
        self._is_opened = False
        self._last_frame: np.ndarray | None = None

        logger.info(
            f"CameraManager initialized: index={camera_index}, "
            f"resolution={width}x{height}, fps={fps}"
        )

    def open(self) -> bool:
        """Open camera connection.

        Returns:
            True if camera opened successfully, False otherwise
        """
        if self._is_opened:
            logger.warning("Camera is already opened")
            return True

        try:
            # Try different backends for cross-platform compatibility
            for backend in [cv2.CAP_ANY, cv2.CAP_V4L2, cv2.CAP_DSHOW]:
                self._capture = cv2.VideoCapture(self.camera_index, backend)
                if self._capture.isOpened():
                    break

            if not self._capture or not self._capture.isOpened():
                logger.error(f"Failed to open camera {self.camera_index}")
                return False

            # Set camera properties
            self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self._capture.set(cv2.CAP_PROP_FPS, self.fps)

            # Initialize face detector
            self._detector = MTCNN()

            self._is_opened = True
            logger.info(f"Camera {self.camera_index} opened successfully")
            return True

        except Exception as e:
            logger.error(f"Error opening camera: {e}")
            return False

    def close(self) -> None:
        """Close camera connection and release resources."""
        if self._capture is not None:
            self._capture.release()
            self._capture = None

        self._detector = None
        self._is_opened = False
        self._last_frame = None

        cv2.destroyAllWindows()
        logger.info("Camera closed")

    @property
    def is_opened(self) -> bool:
        """Check if camera is opened."""
        return self._is_opened and self._capture is not None and self._capture.isOpened()

    def get_frame(self) -> np.ndarray | None:
        """Capture a frame from the camera.

        Returns:
            RGB frame as numpy array, or None if capture failed
        """
        if not self.is_opened:
            logger.warning("Cannot get frame: camera not opened")
            return self._last_frame

        try:
            ret, frame = self._capture.read()
            if not ret or frame is None:
                logger.warning("Failed to read frame from camera")
                return self._last_frame

            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self._last_frame = frame_rgb
            return frame_rgb

        except Exception as e:
            logger.error(f"Error capturing frame: {e}")
            return self._last_frame

    def detect_faces(self, frame: np.ndarray) -> FaceDetectionResult:
        """Detect faces in a frame.

        Args:
            frame: RGB image frame

        Returns:
            Face detection result
        """
        start_time = time.time()

        if self._detector is None:
            logger.warning("Face detector not initialized")
            return FaceDetectionResult(faces=[], processing_time_ms=0.0)

        try:
            # Detect faces
            detections = self._detector.detect_faces(frame)

            # Convert to our model format
            faces = []
            for detection in detections:
                box_dict = detection["box"]
                confidence = detection["confidence"]

                # Ensure valid bounding box coordinates
                x = max(0, box_dict["x"])
                y = max(0, box_dict["y"])
                w = max(1, box_dict["width"])
                h = max(1, box_dict["height"])

                bbox = BoundingBox(x=x, y=y, width=w, height=h)
                face = FaceDetection(box=bbox, confidence=confidence)
                faces.append(face)

            processing_time = (time.time() - start_time) * 1000
            return FaceDetectionResult(faces=faces, processing_time_ms=processing_time)

        except Exception as e:
            logger.error(f"Error detecting faces: {e}")
            processing_time = (time.time() - start_time) * 1000
            return FaceDetectionResult(faces=[], processing_time_ms=processing_time)

    def draw_face_boxes(
        self, frame: np.ndarray, detection_result: FaceDetectionResult
    ) -> np.ndarray:
        """Draw bounding boxes on frame.

        Args:
            frame: RGB image frame
            detection_result: Face detection result

        Returns:
            Frame with drawn bounding boxes
        """
        frame_copy = frame.copy()

        for face in detection_result.faces:
            box = face.box
            # Draw rectangle (green color, thickness 2)
            cv2.rectangle(
                frame_copy,
                (box.x, box.y),
                (box.x + box.width, box.y + box.height),
                (0, 255, 0),
                2,
            )

            # Draw confidence text
            confidence_text = f"{face.confidence:.2f}"
            cv2.putText(
                frame_copy,
                confidence_text,
                (box.x, box.y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

        return frame_copy

    def __del__(self) -> None:
        """Cleanup on deletion."""
        self.close()
