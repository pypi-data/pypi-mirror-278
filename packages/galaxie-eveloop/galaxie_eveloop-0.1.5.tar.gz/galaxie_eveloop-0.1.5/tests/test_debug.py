import unittest

from glxeveloop.properties.debug import DebugProperty


class TestDebug(unittest.TestCase):
    def setUp(self) -> None:
        self.debug = DebugProperty()

    def test_debug(self):
        self.assertEqual(False, self.debug.debug)
        self.debug.debug = None
        self.assertEqual(False, self.debug.debug)

        self.debug.debug = True
        self.assertEqual(True, self.debug.debug)
        self.assertRaises(TypeError, setattr, self.debug, "debug", "Hello.42")


if __name__ == "__main__":
    unittest.main()
