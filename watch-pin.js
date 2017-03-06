
var gpio = require('rpi-gpio');

// Parse input from command-line
if (process.argv.length <= 2) {
    console.log("Usage: node watch-pin.js <pin-number>");
    process.exit(1);
}

var pin = process.argv[2];

// Set up pin for reading
gpio.setup(pin, gpio.DIR_IN, gpio.EDGE_BOTH);

// Attach handler
gpio.on('change', function(channel, value) {
    console.log(`Channel ${channel} is at value: ${value}`);
});
