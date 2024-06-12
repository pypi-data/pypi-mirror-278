#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: Tuuux <tuxa at rtnp dot org> all rights reserved

import logging
from glxeveloop.properties.debug import DebugProperty


class FPS(DebugProperty):
    def __init__(self):
        DebugProperty.__init__(self)
        self.__value = None
        self.__fps_increment = None
        self.__min = None
        self.__fps_min_increment = None
        self.__max = None
        self.__fps_max_increment = None

        self.min = None
        self.max = None
        self.value = None

        self.fps_min_increment = None
        self.fps_max_increment = None
        self.fps_increment = None

    @property
    def value(self):
        """
        The property :py:data:`value`, store the actual speed rate of the MainLoop, it property is use by
        the class :class:`Timer <glxeveloop.timer.Timer>`, and will be updated at each loop iteration.

        By set :py:data:`value` property before call :func:`MainLoop.start() <glxeveloop.MainLoop.start>` , it imposes to start with it value, and slide to the
        :py:data:`max`

        .. note:: If set the value will be clamped between :py:data:`min` and :py:data:`max` properties value.

        .. warning:: That not correspond exactly to a true movies or game FPS, it corresponds more about how many \
        times **1 second** is divided..

        :return: :py:data:`value` property. (in **rate**)
        :rtype: :py:data:`float` or :py:data:`int`
        :raise TypeError: if parameter is not a :py:data:`float`|:py:data:`int` type or None
        """
        return self.__value

    @value.setter
    def value(self, value=None):
        """
        Set the :py:data:`value` property.

        :param value: Frames number per second. (in **fps**)
        :type value: float, int or None
        """
        if value is None:
            value = 60.00
        if isinstance(value, int):
            value = float(value)
        if not isinstance(value, float):
            raise TypeError("'value' property value must be float/int type or None")

        # CLAMP to the absolute value
        clamped_value = abs(max(min(self.max, value), self.min))

        if self.value != round(clamped_value, 2):
            self.__value = round(clamped_value, 2)
            if self.debug:
                logging.debug("{%s}", f"{self.__class__.__name__}.value({self.value})")

    @property
    def min(self):
        """
        The min Frames number per second allowed before the :class:`Timer <glxeveloop.timer.Timer>` stop to apply
         a rate limit to the :py:data:`value` property. (in **rate**)

        It can be considered as the min value of the CLAMP process


        :return: :py:data:`min` property value. (in **fps**)
        :rtype: float
        """
        return self.__min

    @min.setter
    def min(self, value=None):
        """
        Set the :py:data:`min` property value.

        It corresponds to an imposed minimal amount of frame rate

        :param value: :py:data:`min` property value. (in **fps**)
        :type value: float
        :raise TypeError: if ``min`` parameter is not a :py:data:`float` type
        """
        if value is None:
            value = 30.0

        if isinstance(value, int):
            value = float(value)

        if not isinstance(value, float):
            raise TypeError("'min' property value must be float/int type or None")

        if self.min != value:
            self.__min = value
            if self.debug:
                logging.debug("{%s}", f"{self.__class__.__name__}.min({self.min})")

    @property
    def max(self):
        """
        The maximum Frames number per second allowed before the :class:`Timer <glxeveloop.timer.Timer>` start to rate
         limit the :py:data:`rate` property.

        It can be considered as the max value of the CLAMP process.

        .. note:: By default, it has no limit fps_max = float("inf")



        :return: :py:attr:`fps_max` property value. (in **fps**)
        :rtype: float
        """
        return self.__max

    @max.setter
    def max(self, value=None):
        """
        Set the :class:`Timer <glxeveloop.timer.Timer>` :py:attr:`fps_max` property value.

        It corresponds to an imposed max amount of frame rate used during acceleration phase

        :param value: :py:attr:`fps_max` property value. (in **rate**)
        :type value: :py:obj:`float` or :py:data:`int` or :py:obj:`None`
        :raise TypeError: if ``max_fps`` parameter value is not a :py:data:`float` or
        :py:data:`int` type or :py:obj:`None`
        """
        if value is None:
            value = float("inf")

        if isinstance(value, int):
            value = float(value)

        if not isinstance(value, float):
            raise TypeError(
                "'max_fps' property value parameter must be a float or None"
            )

        if self.max != value:
            self.__max = value
            if self.debug:
                logging.debug("{%s}", f"{self.__class__.__name__}.max({self.value})")

    @property
    def fps_increment(self):
        """
        Get the :class:`Timer <glxeveloop.timer.Timer>` :py:data:`fps_increment` property value.

        :return: :py:data:`fps_increment` property value. (in **fps**)
        :rtype: float
        """
        return self.__fps_increment

    @fps_increment.setter
    def fps_increment(self, fps_increment=0.1):
        """
        Set the :class:`Timer <glxeveloop.timer.Timer>` :py:attr:`fps_increment` property.

        The self-correcting timing algorithms will try to increase or decrease :py:attr:`fps_increment` property
        with it step increment.

        :param fps_increment: Frames number per second. (in **rate**)
        :type fps_increment: float
        :raise TypeError: if ``fps_increment`` parameter is not a :py:data:`float` type
        """
        if fps_increment is None:
            fps_increment = 1.0
        if not isinstance(fps_increment, float):
            raise TypeError("'rate' parameter must be a float")
        if self.fps_increment != fps_increment:
            self.__fps_increment = fps_increment
            if self.debug:
                logging.debug(
                    "{%s}",
                    f"{self.__class__.__name__}.fps_increment({self.fps_increment})",
                )

    @property
    def fps_min_increment(self):
        """
        Get the smaller of step increment

        The :class:`Timer <glxeveloop.timer.Timer>` :py:data:`fps_min_increment` property value.

        See :func:`Timer.set_fps_min_increment() <glxeveloop.timer.Timer.set_fps_min_increment()>`
        for more information's

        :return: :py:data:`fps_min_increment` property value. (in **rate**)
        :rtype: float
        """
        return self.__fps_min_increment

    @fps_min_increment.setter
    def fps_min_increment(self, fps_min_increment=0.1):
        """
        Set the :class:`Timer <glxeveloop.timer.Timer>` :py:data:`fps_min_increment` increment.

        The algorithms will try to increase or decrease :py:data:`rate` property with
        :py:attr:`fps_increment` as step .

        For fast limit rate stabilization the :class:`Timer <glxeveloop.timer.Timer>` can use
        :py:data:`fps_min_increment`
        and :py:data:`fps_max_increment` property for make a gap in contain in a range, where
        :py:data:`fps_min_increment` will force a minimal amount of increment and
        :py:data:`fps_max_increment` will force a maximal amount of increment.

        :param fps_min_increment: Frames number per second. (in **rate**)
        :type fps_min_increment: float
        :raise TypeError: if ``fps_min_increment`` parameter is not a :py:data:`float` type
        """
        if fps_min_increment is None:
            fps_min_increment = 0.1
        if not isinstance(fps_min_increment, float):
            raise TypeError("'fps_min_increment' parameter must be a float type")
        if self.fps_min_increment != fps_min_increment:
            self.__fps_min_increment = fps_min_increment
            if self.debug:
                logging.debug(
                    "{%s}",
                    f"{self.__class__.__name__}.fps_min_increment({self.fps_min_increment})",
                )

    @property
    def fps_max_increment(self):
        """
        :py:data:`fps_max_increment` is the upper allowed increment value

        The self-correcting timing will try to adjust :py:data:`value` property in range of
        :py:data:`fps_min_increment` to :py:data:`fps_max_increment`

        **Default Value::** 100.0

        :return: :class:`Timer <glxeveloop.timer.Timer>` :py:data:`fps_max_increment` property value. (in **rate**)
        :rtype: float
        :raise TypeError: if ``fps_max_increment`` parameter is not a :py:data:`float` type
        """
        return self.__fps_max_increment

    @fps_max_increment.setter
    def fps_max_increment(self, fps_max_increment=None):
        if fps_max_increment is None:
            fps_max_increment = 100.0
        if not isinstance(fps_max_increment, float):
            raise TypeError("'max_fps_increment' parameter must be a float")
        if self.fps_max_increment != fps_max_increment:
            self.__fps_max_increment = fps_max_increment
            if self.debug:
                logging.debug(
                    "{%s}",
                    f"{self.__class__.__name__}.fps_max_increment({self.fps_max_increment})",
                )
