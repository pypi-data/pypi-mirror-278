class RunningProperty:
    debug: bool

    def __init__(self) -> None:
        self.__running = False

    @property
    def running(self):
        """
        The property :py:data:`running`, store the actual running state rate of the MainLoop, it property is use by
        the class :class:`MainLoop <glxeveloop.loop.mainloop.MainLoop>`.

        **Default Value:** ``false``

        :return: :py:data:`running` property.
        :rtype: :py:data:`bool`
        :raise TypeError: if parameter is not a :py:data:`bool` type or None
        """
        return self.__running

    @running.setter
    def running(self, value):
        """
        Set the is_running attribute
        """
        if value is None:
            value = False
        if not isinstance(value, bool):
            raise TypeError("'running' property value must be bool type or None")
        if self.running != value:
            self.__running = value
