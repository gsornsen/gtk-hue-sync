#!/usr/bin/env python3

import argparse


class CLI:
    def __init__(self):
        pass

    def get_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-v',
                            '--verbose',
                            action='store_true',
                            help='Be verbose')
        parser.add_argument('-f',
                            '--fullscreen',
                            action='store_true',
                            help='Get dominant color of full screen',
                            default=False)
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
