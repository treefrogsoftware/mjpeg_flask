import platform

if "raspberrypi" in platform._syscmd_uname('-a'):
    print (" * Running on a raspbberypi trying picamera")
    import picamera
    import io
    import threading
    import time
    from src.camera.cameratype.MjpegCamera import MjpegCamera
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
        dim_x = 640
        dim_y = 480
        frame_rate = 24

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

        def stop_thread(self):
            self.stop()
            PiMjpegCamera.run = False
            return "stopped thread"

        def save_to_file(self):
            with PiMjpegCamera.output.condition:
                PiMjpegCamera.output.condition.wait()
                return PiMjpegCamera.output.frame

        def get_frame(self):
            self.initialize()
            with PiMjpegCamera.output.condition:
                PiMjpegCamera.output.condition.wait()
                return PiMjpegCamera.output.frame

        def get_frame_rate(self):
            return PiMjpegCamera.frame_rate

        def get_dim_x(self):
            return PiMjpegCamera.dim_x

        def get_dim_y(self):
            return PiMjpegCamera.dim_y

        @classmethod
        def _thread(cls):
            PiMjpegCamera.camera = picamera.PiCamera(resolution=PiMjpegCamera.dim_x + 'x' + PiMjpegCamera.dim_y, framerate=PiMjpegCamera.frame_rate)
            PiMjpegCamera.camera.start_recording(PiMjpegCamera.output, format='mjpeg')
            while PiMjpegCamera.run:
                time.sleep(20)
