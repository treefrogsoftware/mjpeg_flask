from src.camera.cameratype import *
import os.path
from PIL import Image


class MjpegCameraFactory:

    def __init__(self):
        self.type_dict = {}
        self.find_mjpeg_camera_implementations()

    def get_camera_by_name(self, type_name):
        camera = self.type_dict.get(type_name, None)
        if camera is None:
            print(" * Unable to find camera %s, defaulting to demo camera" % type_name)
            camera = self.type_dict["DefaultMjpegCamera"]
        return camera()

    def get_camera_for_platform(self):
        camera = self.type_dict["DefaultMjpegCamera"]
        for cameraName in self.type_dict:
            if cameraName != "DefaultMjpegCamera":
                camera = self.type_dict.get(cameraName)
                break
        return camera()

    def get_camera_name_list(self):
        return self.type_dict.keys()

    def find_mjpeg_camera_implementations(self):
        types = MjpegCamera.MjpegCamera.__subclasses__()
        for camera in types:
            self.type_dict[camera.__name__] = camera


class DefaultMjpegCamera(MjpegCamera.MjpegCamera):
    def __init__(self):
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.demo_file_path = self.path + "/demo.jpg"
        demoFile = open(self.demo_file_path, "rb")
        self.demoFileFrame = demoFile.read()
        demoFile.close()
        self.demoFiles = []
        self.demo_number = 1
        img = Image.open(self.path + "/demo.jpg")
        width, height = img.size
        self.dim_x = width
        self.dim_y = height

    def load_images(self):
        file_count = range(1, 7)
        for current in file_count:
            inputFile = open(self.path + '/demo' + str(current) + '.jpg', "rb")
            self.demoFiles.append(inputFile.read())
            inputFile.close()

    def start(self):
        return "started"

    def stop(self):
        return "stopped"

    def stop_thread(self):
        return "stopped"

    def get_frame(self):
        if len(self.demoFiles) > 0:
            if self.demo_number > 5:
                self.demo_number = 1
            frame = self.demoFiles[self.demo_number]
            self.demo_number = self.demo_number + 1
        else:
            frame = self.demoFileFrame
        return frame

    def get_frame_rate(self):
        return 10

    def get_dim_x(self):
        return self.dim_x

    def get_dim_y(self):
        return self.dim_y
