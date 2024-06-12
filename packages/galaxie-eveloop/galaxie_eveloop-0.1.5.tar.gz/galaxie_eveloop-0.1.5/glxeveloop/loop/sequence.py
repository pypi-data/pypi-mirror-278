from glxeveloop.hooks import Hooks
from glxeveloop.loop.handle_events import HandleEvents


class SequenceLoop:
    hooks: Hooks
    handle_event = HandleEvents().handle_event

    def sequence(self) -> None:
        """
        * Parse user input into a Statement object
        * Start timer
        * Call precmd method
        * Add statement to History
        * Call cmd method
        * Call postcmd method
        * Stop timer and display the elapsed time
        * In Case of Exit call methods loop_finalization
        """
        try:
            self.hooks.pre()
        except TypeError:  # pragma: no cover
            pass

        try:
            self.handle_event()
        except TypeError:  # pragma: no cover
            pass

        try:
            self.hooks.cmd()
        except TypeError:  # pragma: no cover
            pass

        try:
            self.hooks.post()
        except TypeError:  # pragma: no cover
            pass
