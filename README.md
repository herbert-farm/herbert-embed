# Herbert/Embed

These are the files that consist of the embedded-device controller package of herbert.

## Installation

This package is intended to work on the raspberry pi. It requires [Python 3](https://www.python.org/download/releases/3.0/) and [GPIO Zero](https://gpiozero.readthedocs.io/en/stable/).

You can those requirements via:

```
$ sudo apt-get install python3-gpiozero
```

Then you can clone this repository:

```bash
$ git clone https://github.com/joshpaulchan/herbert-embed.git
```

## Usage

I've included a small test script that will read the corresponding pin passed into the script via command-line. You use it like this:

```bash
$ sudo python3 test/blink/blink.py
```

This will start a script that will continue to watch and print out the value of GPIO pin **1**. This script can be closed using `ctrl+C`.
