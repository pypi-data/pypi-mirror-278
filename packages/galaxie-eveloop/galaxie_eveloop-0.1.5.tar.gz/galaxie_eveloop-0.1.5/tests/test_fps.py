#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from random import randint
import sys
import os
from glxeveloop.fps import FPS

# Require when you haven't GLXBob as default Package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))


# Unittest
class TestTimer(unittest.TestCase):
    def setUp(self):
        # Before the test start
        self.fps = FPS()
        self.fps.debug = True

    def test_default_values(self):
        self.assertEqual(self.fps.value, 60.0)
        self.assertEqual(self.fps.max, float("inf"))
        self.assertEqual(self.fps.min, 30.0)
        self.assertEqual(self.fps.fps_increment, 1.0)
        self.assertEqual(self.fps.fps_min_increment, 0.1)
        self.assertEqual(self.fps.fps_max_increment, 100.0)

    def test_value(self):
        self.fps.value = 42
        self.assertEqual(float(42), self.fps.value)

        self.fps.value = 42.42
        self.assertEqual(42.42, self.fps.value)

        self.fps.min = 3
        self.fps.max = 4

        self.fps.value = 42.42
        self.assertEqual(4.0, self.fps.value)

        self.fps.value = 1
        self.assertEqual(3.0, self.fps.value)

        self.assertRaises(TypeError, setattr, self.fps, "value", "Hello.42")

    def test_min_fps(self):
        self.fps.min = 42
        self.assertEqual(float(42), self.fps.min)

        self.fps.min = 42.42
        self.assertEqual(42.42, self.fps.min)

        self.assertRaises(TypeError, setattr, self.fps, "min", "Hello.42")

    def test_max_fps(self):
        self.fps.max = 42
        self.assertEqual(float(42), self.fps.max)

        self.fps.max = 42.42
        self.assertEqual(42.42, self.fps.max)

        self.assertRaises(TypeError, setattr, self.fps, "max", "Hello.42")

    def test_fps_increment(self):
        random_value = randint(1, 250)
        self.fps.fps_increment = float(random_value)
        self.assertEqual(self.fps.fps_increment, float(random_value))
        random_value = randint(1, 250)
        self.assertRaises(
            TypeError, setattr, self.fps, "fps_increment", int(random_value)
        )

    def test_min_fps_increment(self):
        random_value = randint(1, 250)
        self.fps.fps_min_increment = float(random_value)
        self.assertEqual(self.fps.fps_min_increment, float(random_value))

        random_value = randint(1, 250)
        self.assertRaises(
            TypeError, setattr, self.fps, "fps_min_increment", int(random_value)
        )

    def test_max_fps_increment(self):
        random_value = float(randint(1, 250))
        self.fps.fps_max_increment = random_value
        self.assertEqual(self.fps.fps_max_increment, random_value)

        random_value = randint(1, 250)
        self.assertRaises(
            TypeError, setattr, self.fps, "fps_max_increment", int(random_value)
        )


if __name__ == "__main__":
    unittest.main()
