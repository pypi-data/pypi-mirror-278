#!/usr/bin/env python
# -*- coding: utf-8 -*-
from glxeveloop.loop.mainloop import MainLoop
from glxeveloop.bus import Bus

APPLICATION_VERSION = "0.1.5"
APPLICATION_AUTHORS = ["Tuuuux", "Mo"]

__all__ = [
    "Bus",
    "MainLoop",
]

mainloop = MainLoop()
