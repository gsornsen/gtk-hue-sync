#!/usr/bin/env python3

import pyscreenshot as ImageGrab
from util.displays import Monitor
from PIL import Image
from colorthief import ColorThief


class DominantColor:
    def __init__(self, fullscreen, ignore_white=False, ignore_black=False, quality=1000):
        self.fullscreen = fullscreen
        self.ignore_white = ignore_white
        self.ignore_black = ignore_black
        self.quality = quality

    def get_dominant_color(self):
        # Get screen information from primary display
        with Monitor() as monitor:
            # Use pyscreenshot to grab a Linux screenshot using a native library
            if self.fullscreen is True:
                screen_grab = ImageGrab.grab(bbox=(monitor.x, monitor.y, monitor.width, monitor.height), childprocess=False)
            else:
                # Grab a 100 tall pixel strip in the middle of the display
                y_start = (monitor.y + (monitor.height / 2))
                y_end = (y_start + 100)
                screen_grab = ImageGrab.grab(bbox=(monitor.x, int(y_start), monitor.width, int(y_end)), childprocess=False)
            color_thief = ColorThief(screen_grab, True)
            try:
                dominant_color = color_thief.get_color(self.ignore_white, self.ignore_black, self.quality)
                return dominant_color
            finally:
                screen_grab.close()


if __name__ == '__main__':
    dc = DominantColor(True, False, False, 1000)
    print(dc.get_dominant_color)
