# test/switchboard/switchboard.py

## Purpose

This test program allows you to turn on and off the output of the Pi's GPIO pins.

## Usage

To use this script, run:

```
$ sudo python3 ./switchboard.py
Using GPIO pins { 2, 3 ... 23}
```

This places you in a command-line environment that allows you to do **two**
things: **(1) list the statuses** of the GPIO pins and **(2) change the status**
of a GPIO pin.

### List Pins

To see the status of each pin, run:

```
>>> list
GPIO-02: HIGH
GPIO-03: LOW
GPIO-04: HIGH
GPIO-05: LOW
GPIO-06: HIGH
GPIO-07: LOW
>>>
```

### Set Pins

To set a pin HIGH (turn it on), run:

```
>>> set 2 1
```

<small>This command sets `GPIO-02` to `HIGH`.</small>

To set a pin LOW (turn it off), run:

```
>>> set 2 0
```

<small>This command sets `GPIO-02` to `LOW`.</small>

### Exiting

To exit the application, you may use `ctrl+c` or type:

```
>>> exit
bye
$
```
