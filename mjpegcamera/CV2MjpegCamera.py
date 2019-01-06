import platform
import threading
import time
from mjpegcamera import MjpegCamera

if "Ubuntu" in platform._syscmd_uname('-a'):
    print (" * Running on Ubuntu with opencv camera capture ensure you have opencv3 python installed")
    import cv2
    import numpy

    class CV2MjpegCamera(MjpegCamera.MjpegCamera):

        thread = None  # background thread that reads frames from camera
        run = True
        camera = None

        def initialize(self):
            if CV2MjpegCamera.thread is None:
                # start background frame thread
                CV2MjpegCamera.thread = threading.Thread(target=self._thread)
                CV2MjpegCamera.thread.start()
                CV2MjpegCamera.camera = cv2.VideoCapture(0)

        def stop(self):
            print("Stopping")
            CV2MjpegCamera.camera.release()

        def start(self):
            print("Starting")
            CV2MjpegCamera.camera = cv2.VideoCapture(0)

        def get_frame(self):
            self.initialize()
            success, image = CV2MjpegCamera.camera.read()
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()

        @classmethod
        def _thread(cls):
            CV2MjpegCamera.camera = cv2.VideoCapture(0)
            print(" * Started camera thread")
            while CV2MjpegCamera.run:
                time.sleep(20)
