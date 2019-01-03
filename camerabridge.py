import platform
import io
import threading
import time
from threading import Condition

if "raspberrypi" in platform._syscmd_uname('-a'):
    print (" * Running on a raspbberypi")
    import picamera

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class camerabridge(object):

    thread = None  # background thread that reads frames from camera
    output = None
    run = True
    camera = None

    def initialize(self):
        if camerabridge.thread is None:
            # start background frame thread
            camerabridge.output = StreamingOutput()
            camerabridge.thread = threading.Thread(target=self._thread)
            camerabridge.thread.start()

    def start(self):
        camerabridge.camera.start_recording(camerabridge.output, format='mjpeg')
        return "started"

    def stop(self):
        camerabridge.camera.stop_recording()
        return "stopped"

    def saveToFile(self):
        with camerabridge.output.condition:
            camerabridge.output.condition.wait()
            return camerabridge.output.frame

    def get_frame(self):
        self.initialize()
        with camerabridge.output.condition:
            camerabridge.output.condition.wait()
            return camerabridge.output.frame

    @classmethod
    def _thread(cls):
        camerabridge.camera = picamera.PiCamera(resolution='640x480', framerate=24)        
        camerabridge.camera.start_recording(camerabridge.output, format='mjpeg')
        while camerabridge.run:
            time.sleep(20)

