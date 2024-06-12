import unittest

from glxeveloop.loop.mainloop import MainLoop
from glxeveloop.hooks import Hooks
from glxeveloop.timer import Timer
from queue import Queue


class FakeApplication(object):
    def __init__(self):
        self.permit_keyboard_interruption = True
        self.count = 1

    @staticmethod
    def get_mouse():
        return 0, 0, 0, 0, 0

    def eveloop_precmd(self):
        if self.count >= 10:
            MainLoop().loop.stop()

    def eveloop_cmd(self):
        print(
            "COUNT:{0} FPS:{1} TIME:{2} sec".format(
                self.count,
                MainLoop().loop.timer.fps.value,
                MainLoop().loop.timer.fps.value / 60,
            )
        )

    def eveloop_postcmd(self):
        self.count += 1

    def eveloop_finalization(self):
        pass

    def events_dispatch(self, detailed_signal, args):
        pass

    def gen_a_exception(self):
        raise Exception

    @staticmethod
    def gen_a_statement():
        return 1

    def dispatch(self, detailed_signal, args):
        pass


class TestMainLoop(unittest.TestCase):
    def setUp(self) -> None:
        self.mainloop = MainLoop().loop
        # print(self.mainloop)
        # self.mainloop.debug = True

    def test_debug(self):
        self.mainloop.debug = False
        self.assertFalse(self.mainloop.debug)
        # self.assertFalse(self.mainloop.timer.debug)
        # self.assertFalse(self.mainloop.hooks.debug)

        self.mainloop.debug = True
        self.assertTrue(self.mainloop.debug)
        # self.assertTrue(self.mainloop.timer.debug)
        # self.assertTrue(self.mainloop.hooks.debug)

        # self.assertRaises(TypeError, setattr, self.mainloop, "debug", "Hello.42")

    def test_hooks(self):
        self.assertTrue(isinstance(self.mainloop.hooks, Hooks))

        old_hooks = self.mainloop.hooks

        self.mainloop.hooks = None
        self.assertTrue(isinstance(self.mainloop.hooks, Hooks))

        self.assertNotEqual(old_hooks, self.mainloop.hooks)

        self.assertRaises(TypeError, setattr, self.mainloop, "hooks", "Hello.42")

    def test_timer(self):
        self.assertTrue(isinstance(self.mainloop.timer, Timer))
        old_timer = self.mainloop.timer

        self.mainloop.timer = None
        self.assertTrue(isinstance(self.mainloop.timer, Timer))

        self.assertNotEqual(old_timer, self.mainloop.timer)

        self.assertRaises(TypeError, setattr, self.mainloop, "timer", "Hello.42")

    def test_queue(self):
        self.mainloop.application = FakeApplication()
        old_object = self.mainloop.queue
        self.mainloop.queue = Queue()
        self.assertTrue(isinstance(self.mainloop.queue, Queue))
        self.assertNotEqual(old_object, self.mainloop.queue)

        self.mainloop.queue = None
        self.assertTrue(isinstance(self.mainloop.queue, Queue))

        self.assertRaises(TypeError, setattr, self.mainloop, "queue", 42)

    def test_running(self):
        self.assertFalse(MainLoop().loop.running)

        self.mainloop.running = True
        self.assertTrue(self.mainloop.running)

        self.mainloop.running = None
        self.assertFalse(self.mainloop.running)

        self.assertRaises(TypeError, setattr, self.mainloop, "running", 42)

    def test_start(self):
        self.mainloop.debug = True

        app = FakeApplication()
        self.mainloop.hooks.statement = app.gen_a_statement
        self.mainloop.timer.fps.value = 5.0
        self.mainloop.timer.fps.max = 5.0
        self.mainloop.hooks.cmd = app.eveloop_cmd
        self.mainloop.hooks.pre = app.eveloop_precmd
        self.mainloop.hooks.post = app.eveloop_postcmd
        self.mainloop.hooks.finalization = app.eveloop_finalization
        self.mainloop.start()

        self.mainloop.hooks.cmd = app.gen_a_exception
        self.assertRaises(Exception, self.mainloop.start)

    def test_stop(self):
        self.mainloop.debug = True

        self.assertFalse(self.mainloop.running)
        self.mainloop.running = True
        self.assertTrue(self.mainloop.running)

        self.mainloop.stop()
        self.assertFalse(self.mainloop.running)

    def test_handle_event(self):
        self.mainloop.debug = True
        self.mainloop.queue.put(["Hello.42", (1, 2, 3)])
        app = FakeApplication()

        self.mainloop.hooks.dispatch = app.dispatch
        self.mainloop.handle_event()


if __name__ == "__main__":
    unittest.main()
