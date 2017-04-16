# IPC

IPC is necessary because the GPIO management is done is a separate daemon server. This is done to enforce separation of concerns, better abstraction, and emergency/maintenance interaction.

## Actions

`action` objects are sent from clients to the server, signifying a read/write operation for the GPIO pins. It is a Python dictionary serialized to JSON for transport.

The general structure follows this:

```js
{
  "action" : "LIST|SET|GET|RST", // action may be any of the given attributes, r more
  "params" : { ... } // this dict changes based on the action type
}
```

Response from the server come in the form:

```js
{
  "ok"    : false|true,  // boolean value indicating whether the response is ok or not
  "data": { "pins": { "0" : 1, ...}}, // if ok == True
  "error": { "message": "..."} // if ok == False
}
```

### Listing pins/channels

```js
>>> gpio.list_pins()
{
  "action" : "LIST|SET|GET|RST", // action may be any of the given attributes, r more
  "params" : { ... } // this dict changes based on the action type (may even be empty)
}
```

```js
{
  "ok"    : false|true,  // boolean value indicating whether the response is ok or not
  "data"  : {
    "pins"  : [
      { "1" : 1 },
      { "2" : 0 },
      ...
      { "8" : 1 }]
  } // this dict changes based on the action sent
}
```

## Sizing

| attribute | command  | arg1  | arg2  |   | 
|-----------|---|---|---|---|
| size      | 3  |   |   |   | 

<!-- longer messages -->

## LIST

26 IO pins, so 2^5 pins.

responses start and end with 1 byte 0.
