import logging
from threading import Thread
from queue import Queue
from glxeveloop.hooks import Hooks


class HandleEvents:
    debug: bool
    hooks: Hooks
    queue: Queue

    def handle_event(self):
        event = None
        handler_list = []
        try:
            while not self.queue.empty():
                event = self.queue.get()
                if self.hooks.dispatch:
                    if hasattr(self, "debug") and self.debug:
                        logging.debug(
                            "%s",
                            f"{self.__class__.__name__}.handle_event ({event[0]}, {event[1]}) to {self.hooks.dispatch}",
                        )
                    handler_list.append(
                        Thread(target=self.hooks.dispatch(event[0], event[1]))
                    )

            for handler in handler_list:
                handler.start()
            for handler in handler_list:
                handler.join()

        except KeyError as the_error:  # pragma: no cover
            # Permit to have error logs about unknown event
            logging.error(
                "%s",
                f"{self.__class__.__name__}._handle_event(): KeyError:{the_error} event:{event}",
            )
