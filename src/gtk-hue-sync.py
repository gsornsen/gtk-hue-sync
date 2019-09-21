#!/usr/bin/env python3

import time
import sys
from qhue import Bridge
from rgbxy import Converter
from rgbxy import GamutC
from util.colors import DominantColor
from util.config import Config
from util.cli import CLI


class Sync:
    def __init__(self, verbose, fullscreen, transition, interval, ignore_white,
                 ignore_black):
        self.config = Config()
        # Get config from config.yaml
        self.config_obj = self.config.get_config()
        self.ip = self.config_obj['bridge']['ip']
        self.user = self.config_obj['bridge']['user']
        self.lights_list = self.config_obj['lights']
        # Use CLI args
        self.verbose = verbose
        self.fullscreen = fullscreen
        self.transition = transition
        self.interval = interval
        self.ignore_white = ignore_white
        self.ignore_black = ignore_black
        # Instantiate qHue Bridge
        self.bridge = Bridge(self.ip, self.user)

    def sync(self):
        try:
            # Instantiate DominantColor
            dc = DominantColor(self.fullscreen, self.ignore_white,
                               self.ignore_black)
            # Get the dominant color on the primary display
            rgb_color = dc.get_dominant_color()
            # Instantiate the rgb to xy color Converter class
            color_converter = Converter(GamutC)
            # Convert the dominant color from rgb to xy
            xy_color = color_converter.rgb_to_xy(rgb_color[0], rgb_color[1],
                                                 rgb_color[2])
            # Be verbose about what we're doing
            if self.verbose is True:
                print(f'RGB{rgb_color} ==> XY{xy_color}')
                print(
                    f'Fullscreen: {self.fullscreen}\nInterval: {self.interval}\nTransition: {self.transition}\n'
                    f'Ignore White Pixels: {self.ignore_white}\nIgnore Black Pixels: {self.ignore_black}\n'
                )
            # Change the color of the light(s)
            for light in self.lights_list:
                self.bridge.lights[light].state(xy=[xy_color[0], xy_color[1]],
                                                transitiontime=int(
                                                    self.transition * 0.001))

        except TypeError:
            # Not enough non-black or non-white pixels to update
            pass


def main():
    try:
        args = CLI().get_cli_args()
        sync = Sync(args.verbose, args.fullscreen, args.transition,
                    args.interval, args.ignore_white, args.ignore_black)
        # Run until KeyboardInterrupt
        while True:
            sync.sync()
            time.sleep(float(args.interval * 0.001))
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == '__main__':
    main()
