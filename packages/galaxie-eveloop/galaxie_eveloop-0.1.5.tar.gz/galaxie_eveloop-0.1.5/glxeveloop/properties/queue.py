from queue import Queue


class QueueProperty:
    def __init__(self) -> None:
        self.__queue = Queue()

    @property
    def queue(self):
        return self.__queue

    @queue.setter
    def queue(self, value):
        if value is None:
            value = Queue()
        if not isinstance(value, Queue):
            raise TypeError("'queue' property value must be a Queue instance or None")
        if value != self.queue:
            self.__queue = value
