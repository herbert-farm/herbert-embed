# GPIO

## Overview

The `embed` package comes with a `gpio` subpackage. This package exposes two important classes:

- a `Server` class
- and a `Client` class

The `Server` class acts as a GPIO manager for Raspberry Pi. To interact with (read/write) GPIO pins or ADC channels, you must use the GPIO Client.

## Usage

Before any of the following commands will work, the GPIO **server must be started**. The GPIO server can start from an explicitly defined state (either from a dictionary or file) using the respective constructors `Server.from_state` and `Server.from_file`.

The GPIO package uses the pinouts and mappings defined in the config file.

The Server features a failsafe mode that saves the value of the GPIO pins to disk upon mutation and restarts from file upon normal startup, allowing it to quickly regain control after possible shut offs. The default filename is specified in the config file, and can be changed. If the file does not exist, the server will create it.

### Reading single pins or channels

To read a value from a pin or channel, use these functions:

```python
gpio.get_pin(0) # -> 0 or 1
gpio.get_channel(2) # -> 0.1235
```

### Listing all pins or channels

```python
gpio.get_pins() # -> {'0': 0, '1': 0, ..., '2':1}
gpio.get_channels() # -> {'0': 0.9123, '1': 0.5465, ..., '2':0.123}
```

### Changing the value of a pin

```python
gpio.set_pin(0, 1) # -> True if successful, False o.w.
```

## Testing
