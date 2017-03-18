# IPC

## Overview
An Amoeba frontend communicates with amoeba-core over TCP using ZeroMQ.

Let's take an in-depth look at how that's done:
### Connection
First, the frontend connects to amoeba-core.

As soon as it is connected, it asks amoeba-core for any configuration changes by sending its current configuration, and listening for changes.

The configuration is a table of attributes (described in detail below).

Since the first message contains all of the attributes the frontend understands, amoeba-core has a clear idea of what the frontend is capable of, and the frontend can safely ignore any functionality other frontends might implement.

### Main Loop
As soon as the connection has been made, and everything is initialized, the frontend starts its own event loop (listening for user input, system signals, etc).

In order to communicate without blocking that loop, the frontend listens in a separate thread to amoeba-core for changes.

Whenever amoeba-core feels the desire to, it will update the frontend with a table of changed attributes.
The frontend will respond by changing its attributes accordingly.

#### Events
Of course, a frontend would seem pretty worthless if it couldn't tell amoeba-core about changes.

For this to happen, amoeba-core needs to listen to all of its frontends, while simultaneously sending them updates.

The frontend's main loop sends these requests whenever it needs to. Amoeba-core hears each request in a separate thread, and updates all of the affected frontends accordingly.

## Attributes
The following is a description of each attribute that amoeba-gtk defines.

If the attribute is preceded by a `+`, it has been implemented, or a `-` if it has not. Valid options (or the description of one) are preceeded by a `*` with the default option listed first.

### Editor
+ `cursor`: The point where editing takes place.
  + `style`: How the cursor should be drawn.
    * `vertical_bar`: A vertical line along the left edge of the current character.
	* `block`: A box covering the entire space containing the current character.
  + `highlight_line`: Whether to highlight the current line.
	* `True`
	* `False`
  + `position` Where the cursor is in the buffer.
    * `0`
	* A positive integer within bounds of current buffer.
+ `font`: The little pictures that we call characters.
  + `family`: The name of the font to be used.
    * `Monospace`
    * The name of any installed font
  + `size`: The height (in pixels) for the font
    * `14`
    * A positive integer
+ `word_wrap`: Whether to wrap text around when it reaches the right edge of the screen.
  * `True`
  * `False`
- `scroll-position`: Which line begins the top of the screen.
  * `0`
  * A positive integer less than or equal to the current buffer's line count.
  * A negative integer greater than or equal to the amount of lines that can fit in the window.

### Window
- `colors`: The colors to use when drawing window contents.

### Input
Most of these attributes are sent with corrosponding values on certain events.

#### Keyboard
- `keypress`: A list of keys that are pressed.

#### Mouse
- `click`: A mousebutton was pressed.
  - `button`: Which mousebutton was pressed.
  - `location`: Where the mouse was when this happened.
- `boundaries`: Interesting areas for the mouse to be. (used for drag+drop)
