#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie EveLoop Team, all rights reserved

import logging
from glxeveloop.properties.debug import DebugProperty


class Hooks(DebugProperty):
    def __init__(self):
        DebugProperty.__init__(self)

        self.__statement = None
        self.__parsing = None
        self.__pre = None
        self.__cmd = None
        self.__post = None
        self.__finalization = None
        self.__dispatch = None
        self.__keyboard_interruption = None

        self.statement = None
        self.parsing = None
        self.pre = None
        self.cmd = None
        self.post = None
        self.finalization = None
        self.dispatch = None
        self.keyboard_interruption = None

    @property
    def statement(self):
        """
        Register a hook to be called before parsing information, support to iterate the application

        :return: A callable function
        :rtype: callable
        """
        return self.__statement

    @statement.setter
    def statement(self, value):
        """
        Set the ``statement`` property value

        :param value: A callable function
        :type value: callable
        :raise TypeError: When ``statement`` property is not a ``callable`` or None
        """
        if value and not hasattr(value, "__call__"):
            raise TypeError("'statement' property value must be a callable")

        if value != self.statement:
            if self.debug:
                logging.debug("%s", f"{self.__class__.__name__}: [STATEMENT] {value}")
            self.__statement = value

    @property
    def parsing(self):
        """
        Register a hook to be called after have received ``statement`` from the application.

        :return: A callable function
        :rtype: callable
        """
        return self.__parsing

    @parsing.setter
    def parsing(self, value):
        """
        Set the ``parsing`` property value

        :param value: A callable function
        :type value: callable
        :raise TypeError: When ``parsing`` property is not a ``callable`` or None
        """
        if value and not hasattr(value, "__call__"):
            raise TypeError("'parsing' property value must be a callable")

        if value != self.parsing:
            if self.debug:
                logging.debug("%s", f"{self.__class__.__name__}: [PARSING] {value}")
            self.__parsing = value

    @property
    def pre(self):
        """
        Register a hook to be called before the command function.

        :return: A callable function
        :rtype: callable
        """
        return self.__pre

    @pre.setter
    def pre(self, value):
        """
        Set the ``cmd`` property value

        :param value: A callable function
        :type value: callable
        :raise TypeError: When ``pre`` property is not a ``callable`` or None
        """
        if value and not hasattr(value, "__call__"):
            raise TypeError("'pre' property value must be a callable")

        if value != self.pre:
            if self.debug:
                logging.debug("%s", f"{self.__class__.__name__}: [PRE] {value}")
            self.__pre = value

    @property
    def cmd(self):
        """
        Register a hook to be called as the command function.

        :return: A callable function
        :rtype: callable
        """
        return self.__cmd

    @cmd.setter
    def cmd(self, value):
        """
        Set the ``cmd`` property value

        :param value: A callable function
        :type value: callable
        :raise TypeError: When ``cmd`` property is not a ``callable`` or None
        """
        if value and not hasattr(value, "__call__"):
            raise TypeError("'cmd' property value must be a callable")

        if value != self.cmd:
            if self.debug:
                logging.debug("%s", f"{self.__class__.__name__}: [CMD] {value}")
            self.__cmd = value

    @property
    def post(self):
        """
        Register a hook to be called after the command function.

        :return: A callable function
        :rtype: callable
        """
        return self.__post

    @post.setter
    def post(self, value):
        """
        Set the ``post`` property value

        :param value: A callable function
        :type value: callable
        :raise TypeError: When ``post`` property is not a ``callable`` or None
        """
        if value and not hasattr(value, "__call__"):
            raise TypeError("'post' property value must be a callable")

        if value != self.post:
            if self.debug:
                logging.debug("%s", f"{self.__class__.__name__}: [POST] {value}")
            self.__post = value

    @property
    def finalization(self):
        """
        Register a hook to be called just before mainloop exit, whether it completes successfully or not.

        :return: A callable function
        :rtype: callable
        """
        return self.__finalization

    @finalization.setter
    def finalization(self, value):
        """
        Set the ``finalization`` property value

        :param value: A callable function
        :type value: callable
        :raise TypeError: When ``finalization`` property is not a ``callable`` or None
        """
        if value and not hasattr(value, "__call__"):
            raise TypeError("'finalization' property value must be a callable")

        if value != self.finalization:
            if self.debug:
                logging.debug(
                    "%s", f"{self.__class__.__name__}: [FINALIZATION] {value}"
                )
            self.__finalization = value

    @property
    def dispatch(self):
        """
        Should be remove soon

        :return: A callable function
        :rtype: callable
        """
        return self.__dispatch

    @dispatch.setter
    def dispatch(self, value):
        """
        Set the ``dispatch`` property value

        :param value: A callable function
        :type value: callable
        :raise TypeError: When ``dispatch`` property is not a ``callable`` or None
        """
        if value and not hasattr(value, "__call__"):
            raise TypeError("'dispatch' property value must be a callable")

        if value != self.dispatch:
            if self.debug:
                logging.debug("%s", f"{self.__class__.__name__}: [DISPATCH] {value}")
            self.__dispatch = value

    @property
    def keyboard_interruption(self):
        """
        Register a hooks it Shortcut KeyboardInterrupt during the mainloop execution

        :return: A callable function
        :rtype: callable
        """
        return self.__keyboard_interruption

    @keyboard_interruption.setter
    def keyboard_interruption(self, value):
        """
        Set the ``keyboard_interruption`` property value

        :param value: A callable function
        :type value: callable
        :raise TypeError: When ``keyboard_interruption`` property is not a ``callable`` or None
        """
        if value and not hasattr(value, "__call__"):
            raise TypeError("'keyboard_interruption' property value must be a callable")

        if value != self.keyboard_interruption:
            if self.debug:
                logging.debug(
                    "%s", f"{self.__class__.__name__}: [KEYBOARD_INTERRUPTION] {value}"
                )
            self.__keyboard_interruption = value
