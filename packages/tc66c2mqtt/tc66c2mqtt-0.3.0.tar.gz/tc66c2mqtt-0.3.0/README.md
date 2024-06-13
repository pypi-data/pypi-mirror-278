# tc66c2mqtt

[![tests](https://github.com/jedie/tc66c2mqtt/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/jedie/tc66c2mqtt/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/tc66c2mqtt/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/tc66c2mqtt)
[![tc66c2mqtt @ PyPi](https://img.shields.io/pypi/v/tc66c2mqtt?label=tc66c2mqtt%20%40%20PyPi)](https://pypi.org/project/tc66c2mqtt/)
[![Python Versions](https://img.shields.io/pypi/pyversions/tc66c2mqtt)](https://github.com/jedie/tc66c2mqtt/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/tc66c2mqtt)](https://github.com/jedie/tc66c2mqtt/blob/main/LICENSE)

Send MQTT events from RDTech TC66C device

Tested with [Joy-IT TC66C](https://joy-it.net/de/products/JT-TC66C).


RDTech TC66C hardware info at sigrok:

 * https://sigrok.org/wiki/RDTech_TC66C


Used [Kaitai Struct](https://kaitai.io/) to parse the binary data from the TC66C device.
See: [tc66c.ksy](https://github.com/jedie/tc66c2mqtt/blob/main/tc66c2mqtt/tc66c.ksy)
and [tc66c.py](https://github.com/jedie/tc66c2mqtt/blob/main/tc66c2mqtt/tc66c.py).


## Bootstrap tc66c2mqtt

Clone the sources and just call the CLI to create a Python Virtualenv, e.g.:

```bash
~$ git clone https://github.com/jedie/tc66c2mqtt.git
~$ cd tc66c2mqtt
~/tc66c2mqtt$ ./cli.py --help
```


## Screenshots

### Home Assistant

![tc66c2mqtt 2024-05-15 at 22-17-52 zero2w3 – Home Assistant.png](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/tc66c2mqtt/tc66c2mqtt%202024-05-15%20at%2022-17-52%20zero2w3%20%E2%80%93%20Home%20Assistant.png "tc66c2mqtt 2024-05-15 at 22-17-52 zero2w3 – Home Assistant.png")

### print data

test print data in terminal looks like:

![2024-05-07_20-08_print_data.png](https://raw.githubusercontent.com/jedie/jedie.github.io/master/screenshots/tc66c2mqtt/2024-05-07_20-08_print_data.png "2024-05-07_20-08_print_data.png")
