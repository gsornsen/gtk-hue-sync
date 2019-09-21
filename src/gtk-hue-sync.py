#!/usr/bin/env python3

import time
import sys
import argparse
from qhue import Bridge
from rgbxy import Converter
from rgbxy import GamutC
from util.colors import DominantColor
from util.config import Config

config = Config()
config_obj = config.get_config()
ip = config_obj['bridge']['ip']
user = config_obj['bridge']['user']
lights_list = config_obj['lights']

b = Bridge(ip, user)
lights = b.lights


def get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v',
                        '--verbose',
                        action='store_true',
                        help='Be verbose')
    parser.add_argument('-f',
                        '--fullscreen',
                        action='store_true',
                        help='Get dominant color of full screen',
                        default=True)
    parser.add_argument('-i',
                        '--interval',
                        help='Interval to change lights in ms',
                        default=100,
                        type=int)
    parser.add_argument('-t',
                        '--transition',
                        help='Light transition time in ms',
                        default=100,
                        type=int)
    parser.add_argument('-w',
                        '--ignore_white',
                        action='store_true',
                        help='Ignore white pixels',
                        default=False)
    parser.add_argument('-b',
                        '--ignore_black',
                        action='store_true',
                        help='Ignore black pixels',
                        default=False)
    args = parser.parse_args()
    return args


def change_colors(verbose, fullscreen, transition, interval, ignore_white,
                  ignore_black):
    dc = DominantColor(fullscreen, ignore_white, ignore_black)
    rgb_color = dc.get_dominant_color()
    color_converter = Converter(GamutC)
    try:
        xy_color = color_converter.rgb_to_xy(rgb_color[0], rgb_color[1],
                                             rgb_color[2])

        if verbose is True:
            print(f'{rgb_color} ==> {xy_color} Fullscreen: {fullscreen}')
            print(
                f'\tInterval: {interval} Transition: {transition} Ignore W: {ignore_white} Ignore B: {ignore_black}'
            )

        for light in lights_list:
            b.lights[light].state(xy=[xy_color[0], xy_color[1]],
                                  transitiontime=int(transition * 0.001))

    except TypeError:
        # Not enough non-black or non-white pixels to update
        pass


if __name__ == '__main__':
    try:
        while True:
            args = get_cli_args()
            change_colors(args.verbose, args.fullscreen, args.transition,
                          args.interval, args.ignore_white, args.ignore_black)
            time.sleep(float(args.interval * 0.001))
    except KeyboardInterrupt:
        sys.exit(0)
