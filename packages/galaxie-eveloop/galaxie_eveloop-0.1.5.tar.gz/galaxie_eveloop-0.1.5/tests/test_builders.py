import unittest

from glxeveloop.loop.builder import Builder
from glxeveloop.loop.start import Start
from glxeveloop.loop.stop import Stop
from glxeveloop.loop.handle_events import HandleEvents
from glxeveloop.loop.sequence import SequenceLoop
from glxeveloop.hooks import Hooks
from queue import Queue
from glxeveloop.timer import Timer


class TestBuilders(unittest.TestCase):
    def test_Builder(self):
        builder = Builder().loop(
            debug=True,
            hooks=Hooks(),
            queue=Queue(),
            timer=Timer(),
            running=True,
            start=Start,
            stop=Stop,
            event_handler=HandleEvents,
            sequence=SequenceLoop,
        )


if __name__ == "__main__":
    unittest.main()
