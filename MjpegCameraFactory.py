from cameratype import *

class MjpegCameraFactory() :

    def __init__(self) :
        self.type_dict = {}
        self.findMjpegCameraImplementations()

    def getCameraByName(self, type_name) :
        camera = self.type_dict.get(type_name, None)
        if camera == None:
            print(" * Unable to find camera %s, defaulting to demo camera" % type_name)
            camera = self.type_dict["DefaultMjpegCamera"]
        return camera()

    def getCameraForPlatform(self) :
        camera = self.type_dict["DefaultMjpegCamera"]
        for cameraName in self.type_dict:
           if cameraName != "DefaultMjpegCamera":
               camera = self.type_dict.get(cameraName)
               break
        return camera()

    def getCameraNameList(self) :
        return self.type_dict.keys()

    def findMjpegCameraImplementations(self) :
        self.types = MjpegCamera.MjpegCamera.__subclasses__()
        for camera in self.types:
            self.type_dict[camera.__name__] = camera

class DefaultMjpegCamera(MjpegCamera.MjpegCamera) :

    demoFileFrame = open("demo.jpg", "rb").read()

    def start(self):
        return "started"

    def stop(self):
        return "stopped"

    def stop_thread(self):
        return "stopped"


    def get_frame(self):
        return DefaultMjpegCamera.demoFileFrame

if __name__ == '__main__':

    factory = MjpegCameraFactory()
    camera = factory.getCameraByName("TODO")
    camera = factory.getCameraForPlatform()
    print(factory.getCameraNameList())
    frame = camera.get_frame()
    camera.stop_thread()

