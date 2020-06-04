import cv2
import time
import threading
import numpy as np

class RecordVideo:
    def __init__(self, camera):
        self.camera = camera
        self.writer = None
        self.framerate = camera.get_frame_rate()
        self.dim_x = camera.get_dim_x()
        self.dim_y = camera.get_dim_y()
        self.record_on = False

    def start(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.writer = cv2.VideoWriter('recording--{0}.mp4'.format(time.strftime('%y-%m-%d-%H-%M')),
            fourcc, self.framerate,  (self.dim_x, self.dim_y))
        self.record_on = True
        threading.Thread(target=self.record).start()

    def stop(self):
        self.record_on = False
        self.writer.release()

    def record(self):
        while self.record_on:
            self.add_frame(self.camera.get_frame())

    def add_frame(self, frame):
        jpg_as_np = np.frombuffer(frame, dtype=np.uint8)
        img = cv2.imdecode(jpg_as_np, flags=1)
        # im = cv2.imread(frame)
        # res, im_png = cv2.imencode('.png', im)
        self.writer.write(img)
