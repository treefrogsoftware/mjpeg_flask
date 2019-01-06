import abc

class MjpegCamera(abc.ABC):
    @abc.abstractmethod
    def get_frame(self):
        pass
    @abc.abstractmethod
    def start(self):
        pass
    @abc.abstractmethod
    def stop(self):
        pass

