import cv2
from mtcnn import MTCNN


class WebcamX:
    def __init__(self, camera_index=0):
        self.cam_idx = camera_index
        self.cap = None
        self.frame = None
        self.detector = MTCNN()
        self.xBox = None

    def acquisition(self):
        self.cap = cv2.VideoCapture(self.cam_idx, cv2.CAP_V4L)
        print("Webcam is opened...")

    def get_frame(self):
        _, self.frame = self.cap.read()
        cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
        print("Frame is taking...")
        return self.frame

    def get_xBox(self):
        xFace = self.detector.detect_faces(self.frame)
        self.xBox = xFace[0]["box"]
        return self.xBox

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("Webcam is closed...")


if __name__ == "__main__":
    webcam = WebcamX()
    webcam.acquisition()
    for i in range(100):
        frame = webcam.get_frame()
        xBox = webcam.get_xBox()
        cv2.rectangle(
            frame, (xBox[0], xBox[1]), (xBox[0] + xBox[2], xBox[1] + xBox[3]), (0, 255, 0), 2
        )
        # height, width, bytesPerComponent = frame.shape
        # print("frame height = {} width = {} bytesPerComponent = {}".format(height,width,bytesPerComponent))
        print(
            f"frame height = {frame.shape[0]} width = {frame.shape[1]} bytesPerComponent = {frame.shape[2]}"
        )
        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR, frame)
        cv2.imshow("Webcam Frame Window", frame)
        cv2.waitKey(1)
        print(str(i) + ".frame")

    webcam.close()
    print("Webcam Finished...")
