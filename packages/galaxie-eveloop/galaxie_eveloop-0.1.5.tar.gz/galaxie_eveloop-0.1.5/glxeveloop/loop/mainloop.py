from glxeveloop.loop.singleton import Singleton
from glxeveloop.loop.builder import Builder


class MainLoop(metaclass=Singleton):
    @property
    def loop(self):
        return self.__loop

    def __init__(self):
        self.__loop = Builder().loop()

    # def handle_event(self):
    #     pass
