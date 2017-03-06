# Herbert/Embed

These are the files that consist of the embedded-device controller package of herbert.

## Installation

This package is intended to work on the raspberry pi. Node must be installed prior to this installation.

To install **herbert/embed**:

```bash
$ npm install
```

## Usage

I've included a small test script that will read the corresponding pin passed into the script via command-line. You use it like this:

```bash
$ sudo watch-pin 1
```

This will start a script that will continue to watch and print out the value of GPIO pin **1**. This script can be closed using `ctrl+C`.
