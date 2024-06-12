#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import logging

from glxeveloop import MainLoop
from glxeveloop.properties.debug import DebugProperty


class Bus(DebugProperty):
    """
    :Description:

    The ``EventBusClient`` object is The bus it interconnects Widget
    """

    def __init__(self):
        DebugProperty.__init__(self)

        # Public attribute
        self.__subscriptions = {}
        # self.subscriptions = None

    @property
    def subscriptions(self) -> dict:
        """
        Return the subscriptions list

        :return: event buffer
        :rtype: dict
        """
        return self.__subscriptions

    @subscriptions.setter
    def subscriptions(self, value=None):
        if value is None:
            value = {}
        if not isinstance(value, dict):
            raise TypeError("'subscriptions' property value must be dict type or None")
        if self.subscriptions != value:
            self.__subscriptions = value

    def connect(self, detailed_signal: object, handler: object, *args: object):
        """
        The connect() method adds a function or method (handler) to the end of the event list
        for the named detailed_signal but before the default class signal handler.
        An optional set of parameters may be specified after the handler parameter.
        These will all be passed to the signal handler when invoked.

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param handler: a function handler
        :type handler: handler
        :param args: additional parameters arg1, arg2
        :type args: tuple
        """

        # If args is still None replace it by an empty list
        # if args is None:
        #     args = []

        # If detailed_signal is not in the event list create it
        if detailed_signal not in self.subscriptions:
            self.subscriptions[detailed_signal] = []

        self.subscriptions[detailed_signal].append(handler)

        if args:
            self.subscriptions[detailed_signal].append(args)

    def disconnect(self, detailed_signal, handler):
        """
        The disconnect() method removes the signal handler with the specified handler
        from the list of signal handlers for the object.

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param handler: a function handler
        :type handler: handler
        """
        if (
            detailed_signal in self.subscriptions
            and handler in self.subscriptions[detailed_signal]
        ):
            del self.subscriptions[detailed_signal]

    @staticmethod
    def emit(detailed_signal, args):
        """
        Emit signal in direction to the Mainloop.

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param args: additional parameters arg1, arg2
        :type args: dict
        """
        MainLoop().loop.queue.put([detailed_signal, args])

    def events_flush(self, detailed_signal, args):
        if detailed_signal in self.subscriptions:
            handler_list = []
            for handler in self.subscriptions[detailed_signal]:
                if self.debug:
                    logging.debug(
                        "%s",
                        f"{self.__class__.__name__}.events_dispatch({detailed_signal}, {args})",
                    )
                handler_list.append(
                    threading.Thread(target=handler(self, detailed_signal, args))
                )
            for handler in handler_list:
                handler.start()
            for handler in handler_list:
                handler.join()

    def events_dispatch(self, detailed_signal, args):
        """
        Flush Mainloop event to Child's father's for a Widget's recursive event dispatch

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param args: additional parameters arg1, arg2
        :type args: list
        """
        self.events_flush(detailed_signal, args)

        if hasattr(self, "eveloop_dispatch"):
            self.eveloop_dispatch(detailed_signal, args)
