import unittest

from glxeveloop.hooks import Hooks


def fake_function():
    pass


class TestMainLoopHooks(unittest.TestCase):
    def setUp(self) -> None:
        self.hooks = Hooks()
        self.hooks.debug = True

    def test_statement(self):
        self.assertIsNone(self.hooks.statement)
        self.hooks.statement = fake_function
        self.assertEqual(fake_function, self.hooks.statement)
        self.hooks.statement = None
        self.assertIsNone(self.hooks.statement)
        self.assertRaises(TypeError, setattr, self.hooks, "statement", "Hello.42")

    def test_parsing(self):
        self.assertIsNone(self.hooks.parsing)
        self.hooks.parsing = fake_function
        self.assertEqual(fake_function, self.hooks.parsing)
        self.hooks.parsing = None
        self.assertIsNone(self.hooks.parsing)
        self.assertRaises(TypeError, setattr, self.hooks, "parsing", "Hello.42")

    def test_pre(self):
        self.assertIsNone(self.hooks.pre)
        self.hooks.pre = fake_function
        self.assertEqual(fake_function, self.hooks.pre)
        self.hooks.pre = None
        self.assertIsNone(self.hooks.pre)
        self.assertRaises(TypeError, setattr, self.hooks, "pre", "Hello.42")

    def test_cmd(self):
        self.assertIsNone(self.hooks.cmd)
        self.hooks.cmd = fake_function
        self.assertEqual(fake_function, self.hooks.cmd)
        self.hooks.cmd = None
        self.assertIsNone(self.hooks.cmd)
        self.assertRaises(TypeError, setattr, self.hooks, "cmd", "Hello.42")

    def test_post(self):
        self.assertIsNone(self.hooks.post)
        self.hooks.post = fake_function
        self.assertEqual(fake_function, self.hooks.post)
        self.hooks.post = None
        self.assertIsNone(self.hooks.post)
        self.assertRaises(TypeError, setattr, self.hooks, "post", "Hello.42")

    def test_finalization(self):
        self.assertIsNone(self.hooks.finalization)
        self.hooks.finalization = fake_function
        self.assertEqual(fake_function, self.hooks.finalization)
        self.hooks.finalization = None
        self.assertIsNone(self.hooks.finalization)
        self.assertRaises(TypeError, setattr, self.hooks, "finalization", "Hello.42")

    def test_dispatch(self):
        self.assertIsNone(self.hooks.dispatch)
        self.hooks.dispatch = fake_function
        self.assertEqual(fake_function, self.hooks.dispatch)
        self.hooks.dispatch = None
        self.assertIsNone(self.hooks.dispatch)
        self.assertRaises(TypeError, setattr, self.hooks, "dispatch", "Hello.42")

    def test_keyboard_interruption(self):
        self.assertIsNone(self.hooks.keyboard_interruption)
        self.hooks.keyboard_interruption = fake_function
        self.assertEqual(fake_function, self.hooks.keyboard_interruption)
        self.hooks.keyboard_interruption = None
        self.assertIsNone(self.hooks.keyboard_interruption)
        self.assertRaises(
            TypeError, setattr, self.hooks, "keyboard_interruption", "Hello.42"
        )


if __name__ == "__main__":
    unittest.main()
