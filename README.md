# Herbert/Embed

These are the files that make up Herbert's embedded-device controller.

## Installation

This package is intended to work on the raspberry pi. It requires [Python 3.x](https://www.python.org/download/releases/3.0/) and [GPIO Zero](https://gpiozero.readthedocs.io/en/stable/).

You can those requirements via:

```
$ sudo apt-get install python3-gpiozero
```

Then you can clone this repository:

```bash
$ git clone https://github.com/joshpaulchan/herbert-embed.git
```

## Usage

```bash
$ sudo run.py
```

## Testing/Experimentation

I've included small test programs that will test basic functionality of the Pi GPIO. You use them like this:

```bash
$ sudo python3 test/blink/blink.py <pin-number>
```

You can find more info, including reference circuit diagrams in the corresponding folders under `test/`.
