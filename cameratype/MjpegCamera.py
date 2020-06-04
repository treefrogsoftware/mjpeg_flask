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

    @abc.abstractmethod
    def stop_thread(self):
        pass

    @abc.abstractmethod
    def get_frame_rate(self):
        pass

    @abc.abstractmethod
    def get_dim_x(self):
        pass

    @abc.abstractmethod
    def get_dim_y(self):
        pass
