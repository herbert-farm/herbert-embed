# test/blink/blink.py

## Purpose

This test program and circuit blink an LED on and off.

## Usage

To use this script, connect the reference circuit specified in `blink_ckt.png`, where:

* __GPIO2__ goes to any Pi GPIO pin (recommended is pin 27)

```bash
$ sudo python3 ./blink.py 27 # or whatever pin you used
```
