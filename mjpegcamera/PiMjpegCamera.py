import platform

if "raspberrypi" in platform._syscmd_uname('-a'):
    print (" * Running on a raspbberypi trying picamera")
    import picamera
    import io
    import threading
    import time
    from MjpegCamera import MjpegCamera
    from threading import Condition

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

    class PiMjpegCamera(MjpegCamera):

        thread = None  # background thread that reads frames from camera
        output = None
        run = True
        camera = None

        def initialize(self):
            if PiMjpegCamera.thread is None:
                # start background frame thread
                PiMjpegCamera.output = StreamingOutput()
                PiMjpegCamera.thread = threading.Thread(target=self._thread)
                PiMjpegCamera.thread.start()

        def start(self):
            PiMjpegCamera.camera.start_recording(PiMjpegCamera.output, format='mjpeg')
            return "started"

        def stop(self):
            PiMjpegCamera.camera.stop_recording()
            return "stopped"

        def saveToFile(self):
            with PiMjpegCamera.output.condition:
                PiMjpegCamera.output.condition.wait()
                return PiMjpegCamera.output.frame

        def get_frame(self):
            self.initialize()
            with PiMjpegCamera.output.condition:
                PiMjpegCamera.output.condition.wait()
                return PiMjpegCamera.output.frame

        @classmethod
        def _thread(cls):
            PiMjpegCamera.camera = picamera.PiCamera(resolution='640x480', framerate=24)
            PiMjpegCamera.camera.start_recording(PiMjpegCamera.output, format='mjpeg')
            while PiMjpegCamera.run:
                time.sleep(20)
