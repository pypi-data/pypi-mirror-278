import unittest

from io import StringIO
from unittest.mock import patch
from glxeveloop import Bus
from glxeveloop.loop.mainloop import MainLoop


def hello42(handler, signal_details, args):
    print(args)


class FakeApplication(Bus):
    def __init__(self):
        Bus.__init__(self)
        self.permit_keyboard_interruption = True

    @staticmethod
    def get_mouse():
        return 0, 0, 0, 0, 0

    def eveloop_precmd(self):
        pass

    def eveloop_cmd(self):
        pass

    def eveloop_postcmd(self):
        pass

    def eveloop_finalization(self):
        pass

    def eveloop_dispatch(self, detailed_signal, args):
        pass


class TestBus(unittest.TestCase):
    def setUp(self):
        self.bus = Bus()
        self.bus.debug = True
        self.mainloop = MainLoop()

    def test_subscriptions(self):

        self.assertEqual({}, self.bus.subscriptions)
        self.bus.subscriptions = {"Hello": 42}
        self.assertEqual({"Hello": 42}, self.bus.subscriptions)

        self.bus.subscriptions = None
        self.assertEqual({}, self.bus.subscriptions)
        self.assertRaises(TypeError, setattr, self.bus, "subscriptions", "Hello.42")

    def test_connect(self):

        self.bus.connect("HELLO42", hello42, "hello", "42")

        self.assertEqual(hello42, self.bus.subscriptions["HELLO42"][0])
        self.assertEqual(("hello", "42"), self.bus.subscriptions["HELLO42"][1])

    def test_disconnect(self):

        self.assertEqual(0, len(self.bus.subscriptions))
        self.bus.connect("HELLO42", hello42, "hello", "42")
        self.bus.connect("HELLO43", hello42, "hello", "43")

        self.assertEqual(hello42, self.bus.subscriptions["HELLO42"][0])
        self.assertEqual(hello42, self.bus.subscriptions["HELLO43"][0])
        self.assertEqual(("hello", "42"), self.bus.subscriptions["HELLO42"][1])
        self.assertEqual(("hello", "43"), self.bus.subscriptions["HELLO43"][1])
        self.assertEqual(2, len(self.bus.subscriptions))

        self.bus.disconnect("HELLO42", hello42)
        self.assertEqual(1, len(self.bus.subscriptions))

        self.assertEqual(hello42, self.bus.subscriptions["HELLO43"][0])
        self.assertEqual(("hello", "43"), self.bus.subscriptions["HELLO43"][1])
        self.bus.disconnect("HELLO43", hello42)
        self.assertEqual(0, len(self.bus.subscriptions))

    def test_emit(self):
        self.assertEqual(0, MainLoop().loop.queue.qsize())
        self.bus.emit("HELLO42", {"Hello": "42"})
        self.assertEqual(1, MainLoop().loop.queue.qsize())
        event = MainLoop().loop.queue.get()
        self.assertEqual("HELLO42", event[0])
        self.assertEqual({"Hello": "42"}, event[1])

    def test_event_flush(self):

        self.assertEqual(0, len(self.bus.subscriptions))
        self.bus.connect("HELLO42", hello42)
        with patch("sys.stdout", new=StringIO()) as fake_out:
            self.bus.events_flush("HELLO42", ("hello", "42"))
            expected = "('hello', '42')\n"
            self.assertEqual(fake_out.getvalue(), expected)

    def test_events_dispatch(self):
        fake_app = FakeApplication()
        self.assertEqual(0, len(fake_app.subscriptions))
        fake_app.connect("HELLO42", hello42)
        with patch("sys.stdout", new=StringIO()) as fake_out:
            fake_app.events_dispatch("HELLO42", ("hello", "42"))
            expected = "('hello', '42')\n"
            self.assertEqual(fake_out.getvalue(), expected)


if __name__ == "__main__":
    unittest.main()
