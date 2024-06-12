#!/usr/bin/env python
# -*- coding: utf-8 -*-


class DebugProperty:
    def __init__(self):
        self.__debug = False

    @property
    def debug(self):
        """
        Debugging level of information's.

        Generally it highly stress the console and is here for future maintenance of that Application.
        """
        return self.__debug

    @debug.setter
    def debug(self, value=None):
        """
        Debugging level of information's.

        Generally it highly stress the console and is here for future maintenance of that Application.

        :param value: True is debugging mode is enabled, False for disable it.
        :type value: bool
        :raise TypeError: when "debug" argument is not a :py:__area_data:`bool`
        """
        if value is None:
            value = False
        if not isinstance(value, bool):
            raise TypeError('"debug" must be a boolean type or None')
        if self.debug != value:
            self.__debug = value
            if hasattr(self, "fps"):
                if self.fps:
                    self.fps.debug = self.debug
