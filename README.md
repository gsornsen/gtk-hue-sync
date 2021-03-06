# gtk-hue-sync 

[![Build Status](https://travis-ci.org/gsornsen/gtk-hue-sync.svg?branch=master)](https://travis-ci.org/gsornsen/gtk-hue-sync)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/26cf2a91e5ff47608bef298d765a994f)](https://www.codacy.com/manual/gsornsen/gtk-hue-sync?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=gsornsen/gtk-hue-sync&amp;utm_campaign=Badge_Grade)

Linux compatible CLI application to sync dominant primary display color with Hue Lights

## Demo

![gtk-hue-sync](media/gtk-hue-sync.gif)

## Installation

### Debian/Ubuntu/Pop_OS

Download the [latest release](https://github.com/gsornsen/gtk-hue-sync/releases/latest)

```bash
cd ~/Downloads
sudo apt install ./gtk-hue-sync*.deb
```

***

## Installation from Source

Checkout the project from GitHub:

```bash
git clone https://github.com/gsornsen/gtk-hue-sync.git && cd gtk-hue-sync
```

Set-up environment:

```bash
./setup.sh
source env/bin/activate
```

Run tests:

```bash
make test
```

Install:

```bash
make install
```

Installation location: `/usr/bin/gtk-hue-sync`

## Configuration

### Recommended reads

<https://developers.meethue.com/develop/get-started-2/>

<https://developers.meethue.com/develop/hue-api/lights-api/>

#### Config location: `~/.config/gtk-hue-sync/config.yaml`

***

Example:

```yaml
# Hue Documentation to get IP and Create Username for their API:
#    https://developers.meethue.com/develop/get-started-2/

# Hue Bridge user and ip address for Hue API
bridge:
    user: UnnyZonejfw0Su1AJlQ1PmNGFh7mBHaRxc73cZH0
    ip: 192.168.1.114

# Hue Documentation to get list of all lights:
#    https://developers.meethue.com/develop/hue-api/lights-api/

# Lights to change colors. Match the integer of the lights from the above step to create a list of lights you would like to change colors
lights:
    - 1 # Hue Color Lamp 1
    - 4 # Hue Play 1
    - 5 # Hue Play 2
```

## Running

gtk-hue-sync has sane defaults and can be run without any arguments

```bash
gtk-hue-sync
```

Help menu:

```bash
gtk-hue-sync -h
```

Optional arguments:

```bash
usage: gtk-hue-sync [-h] [-v] [-f] [-i INTERVAL] [-t TRANSITION] [-w] [-b]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Be verbose
  -f, --fullscreen      Get dominant color of full screen
  -i INTERVAL, --interval INTERVAL
                        Interval to change lights in ms
  -t TRANSITION, --transition TRANSITION
                        Light transition time in ms
  -w, --ignore_white    Ignore white pixels
  -b, --ignore_black    Ignore black pixels
```

Recommended Usage:

```bash
gtk-hue-sync -f
```

## Running from Source

The same options/menu above apply

```bash
./setup.sh
source env/bin/activate
python src/gtk-hue-sync.py
```

or

```bash
src/gtk-hue-sync.py
```

## Contributions

Suggestions, Issues, Patches, Pull Requests, Testing all welcome. As of now this has only been tested on Pop_OS 19.04

## Thanks

[fengsp: color-thief-py](https://github.com/fengsp/color-thief-py)

[benknight: hue-python-rgb-converter](https://github.com/benknight/hue-python-rgb-converter)

[quentinsf: qhue](https://github.com/quentinsf/qhue)
