#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from time import time, sleep
from queue import Queue
from glxeveloop.fps import FPS
from glxeveloop.timer import Timer


# Unittest
class TestTimer(unittest.TestCase):
    def setUp(self):
        self.timer = Timer()
        self.timer.debug = True

    def test_debug(self):
        self.timer.debug = False
        self.assertFalse(self.timer.debug)
        self.assertFalse(self.timer.fps.debug)

        self.timer.debug = True
        self.assertTrue(self.timer.debug)
        self.assertTrue(self.timer.fps.debug)

        self.assertRaises(TypeError, setattr, self.timer, "debug", "Hello.42")

    def test_default_values(self):
        self.assertEqual(self.timer.position, 0)
        # self.assertEqual(self.timer.queue.size, 10)
        self.assertEqual(self.timer.be_fast, False)
        self.assertEqual(self.timer.be_fast_multiplication, 10)

    def test_buffer(self):
        self.assertTrue(isinstance(self.timer.queue, Queue))
        old_buffer = self.timer.queue
        self.timer.queue = None
        self.assertTrue(isinstance(self.timer.queue, Queue))
        self.assertNotEqual(old_buffer, self.timer.queue)

        self.assertRaises(TypeError, setattr, self.timer, "queue", "Hello.42")

    def test_fps(self):
        self.assertTrue(isinstance(self.timer.fps, FPS))
        old_fps = self.timer.fps
        self.timer.fps = None
        self.assertTrue(isinstance(self.timer.fps, FPS))
        self.assertNotEqual(old_fps, self.timer.fps)

        self.timer.fps = FPS()
        self.assertTrue(isinstance(self.timer.fps, FPS))

        self.assertRaises(TypeError, setattr, self.timer, "fps", "Hello.42")

    def test_time(self):
        returned_value_1 = self.timer.time
        returned_value_2 = self.timer.time
        self.assertLessEqual(returned_value_1, returned_value_2)

    def test_time_departure(self):
        tested_value = time()
        self.timer.time_departure = tested_value
        self.assertEqual(self.timer.time_departure, tested_value)

        self.assertRaises(TypeError, setattr, self.timer, "time_departure", 42)

    def test_be_bast(self):
        value_tested = True
        self.timer.be_fast = value_tested
        value_returned = self.timer.be_fast
        self.assertEqual(value_tested, value_returned)

        self.assertRaises(TypeError, setattr, self.timer, "be_fast", "Hello.42")

    def test_be_fast_multiplication(self):
        self.timer.be_fast_multiplication = 42
        self.assertEqual(self.timer.be_fast_multiplication, 42)

        self.assertRaises(
            TypeError,
            setattr,
            self.timer,
            "be_fast_multiplication",
            str("Hello World!"),
        )

    def test_tick(self):
        self.timer.debug = True
        self.timer.position = 0
        self.timer.fps.value = 5
        self.timer.fps.max = 42

        count = 0
        while count < 42:
            self.timer.tick()
            sleep(0.1)
            count += 1

        count = 0
        while count < 42:
            self.timer.tick()
            count += 1

        count = 0
        self.timer.fps.value = 200
        while count < 42:
            self.timer.tick()
            sleep(0.01)
            count += 1

        count = 0
        while count < 42:
            self.timer.tick()
            sleep(0.01)
            count += 1

        self.timer.fps.value = 200
        while not self.timer.queue.empty():
            self.timer.queue.get()

        self.timer.queue.put(420.0)
        self.timer.queue.put(420.0)
        self.timer.queue.put(420.0)
        self.timer.queue.put(420.0)
        self.timer.queue.put(420.0)
        self.timer.queue.put(42.0)
        self.timer.queue.put(42.0)
        self.timer.queue.put(42.0)
        self.timer.queue.put(42.0)
        self.timer.queue.put(42.0)

        count = 0
        self.timer.fps.value = 40
        self.timer.be_fast = True
        while count < 42:
            self.timer.tick()
            sleep(0.01)
            count += 1


if __name__ == "__main__":
    unittest.main()
