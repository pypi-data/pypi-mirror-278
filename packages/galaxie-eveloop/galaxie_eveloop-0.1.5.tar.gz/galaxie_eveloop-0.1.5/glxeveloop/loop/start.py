import logging
import sys
from glxeveloop.hooks import Hooks
from glxeveloop.timer import Timer
from glxeveloop.loop.sequence import SequenceLoop
from glxeveloop.loop.stop import Stop


class Start:
    running: bool
    debug: bool
    timer: Timer
    hooks: Hooks
    sequence: SequenceLoop().sequence
    stop: Stop().stop

    def start(self) -> None:
        """
        Runs a Loop until ``Mainloop.stop()`` is called on the loop. If this is called for the thread of the loop's
        , it will process queue from the loop, otherwise it will simply wait.
        """
        if self.debug:
            logging.debug("%s", f"{self.__class__.__name__}: Starting...")
        self.running = True

        # Normally it the first refresh of the application, it can be considered as the first stdscr display.
        # Consider a chance to crash before the start of the loop
        try:
            try:
                self.sequence()
            except TypeError:  # pragma: no cover
                pass

        except Exception:
            try:
                self.stop()
            except TypeError:  # pragma: no cover
                pass
            sys.stdout.write("{0}\n".format(sys.exc_info()[0]))
            sys.stdout.flush()
            raise

        # A bit light for notify about we are up and running, but we are really inside the main while(1) loop
        try:
            if self.debug:
                logging.debug("%s", f"{self.__class__.__name__}: Started")
        except TypeError:  # pragma: no cover
            pass
        # The loop
        while self.running:

            try:
                try:
                    self.hooks.statement()
                except TypeError:  # pragma: no cover
                    pass

                try:
                    self.sequence()
                except TypeError:  # pragma: no cover
                    pass

                try:
                    self.timer.tick()
                except TypeError:  # pragma: no cover
                    pass

            except KeyboardInterrupt:  # pragma: no cover
                try:
                    self.hooks.keyboard_interruption()
                except TypeError:
                    if hasattr(self, "stop") and self.stop:
                        self.stop()

            except Exception:  # pragma: no cover
                try:
                    self.stop()
                except TypeError:
                    pass
                sys.stdout.write("{0}\n".format(sys.exc_info()[0]))
                sys.stdout.flush()
                raise

        try:
            if self.debug:
                logging.debug(
                    "%s", f"{self.__class__.__name__}: Call finalization method"
                )

            self.hooks.finalization()

            if self.debug:
                logging.debug(
                    "%s", f"{self.__class__.__name__}: All operations is stop"
                )

        except TypeError:  # pragma: no cover
            pass
