import platform
import threading
import time
from src.camera.cameratype import MjpegCamera

if 'Ubuntu' in platform._syscmd_uname('-a'):
    print(" * Running on Ubuntu with opencv camera capture ensure you have opencv3 python installed")
    import cv2

    class CV2MjpegCamera(MjpegCamera.MjpegCamera):

        thread = None  # background thread that reads frames from camera
        run = True
        camera = None
        dim_x = 640
        dim_y = 480
        frame_rate = 24

        def initialize(self):
            if CV2MjpegCamera.thread is None:
                # start background frame thread
                self.start()
                CV2MjpegCamera.thread = threading.Thread(target=self._thread)
                CV2MjpegCamera.thread.start()

        def stop(self):
            print("Stopping camera")
            if CV2MjpegCamera.camera is not None:
                try:
                    CV2MjpegCamera.camera.release()
                except Exception as e:
                    print("Error releasing camera", e)
                CV2MjpegCamera.camera = None

        def stop_thread(self):
                print("Stopping thread")
                self.stop()
                CV2MjpegCamera.run = False

        def start(self):
            print("Starting")
            if CV2MjpegCamera.camera is None:
                print("Starting camera")
                try:
                    CV2MjpegCamera.camera = cv2.VideoCapture(0)
                    print (CV2MjpegCamera.camera)
                except Exception as e:
                    print("Error starting camera", e)

        def get_frame(self):
            self.initialize()
            success, image = CV2MjpegCamera.camera.read()
            ret, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()

        def get_frame_rate(self):
            return CV2MjpegCamera.frame_rate

        def get_dim_x(self):
            return CV2MjpegCamera.dim_x

        def get_dim_y(self):
            return CV2MjpegCamera.dim_y

        @classmethod
        def _thread(cls):
            print(" * Started camera thread")
            if CV2MjpegCamera.camera is not None:
                CV2MjpegCamera.dim_x = CV2MjpegCamera.camera.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
                CV2MjpegCamera.dim_y = CV2MjpegCamera.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
                CV2MjpegCamera.frame_rate = CV2MjpegCamera.camera.get(cv2.CAP_PROP_FPS)
            while CV2MjpegCamera.run:
                time.sleep(1)
