#!/usr/bin/env python3

import gi
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk # noqa


class Monitor:
    def __init__(self):
        display = Gdk.Display.get_default()
        monitor = display.get_monitor(0)
        self.geometry = monitor.get_geometry()

    def __enter__(self):
        self.x = self.get_x()
        self.y = self.get_y()
        self.width = self.get_width()
        self.height = self.get_height()
        return self

    def get_x(self):
        return self.geometry.x

    def get_y(self):
        return self.geometry.y

    def get_width(self):
        return self.geometry.width

    def get_height(self):
        return self.geometry.height

    def __exit__(self, exception_type, exception_value, traceback):
        return
