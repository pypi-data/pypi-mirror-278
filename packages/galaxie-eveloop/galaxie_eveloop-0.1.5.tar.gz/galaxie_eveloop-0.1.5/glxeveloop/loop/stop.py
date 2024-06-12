import logging


class Stop:
    running: bool
    debug: bool

    def stop(self):
        """
        Stops a Loop from running. Any calls to run() for the loop will return.

        Note that sources that have already been dispatched when quit() is called will still be executed.

        .. :warning: A Loop quit() call will certainly cause the end of you programme
        """
        if hasattr(self, "debug") and self.debug:
            logging.debug("%s", f"{self.__class__.__name__}: Stopping")

        self.running = False
