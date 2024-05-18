# keymap
Remap keyboard keys in macOS >= 10.12

## Usage:
```bash
$ keymap map a b # maps a to b

$ keymap swap leftshift leftcmd # swaps left shift and left command keys

$ keymap list # list your mappings
a -> b
leftshift -> leftcmd
leftcmd -> leftshift

$ keymap unmap a leftshift leftcmd # remove mappings

# save your mappings to filename, default is ~/.keymaprc
$ keymap save [filename]

# load your mappings from filename, default is ~/.keymaprc
$ keymap load [filename]

$ keymap keys # show available keys
a b c d e f g h i j k l m n o p q r s t u v w x y z 1 2 3 4 5 6 7 8 9
0 return escape delete tab space - = [ ] \ # ; ' ` , . / caps f1 f2 f3
f4 f5 f6 f7 f8 f9 f10 f11 f12 printscreen brightness- brightness+
insert home pageup deleteforward end pagedown right left down up
numlock keypad/ keypad* keypad- keypad+ keypadenter keypad1 keypad2
keypad3 keypad4 keypad5 keypad6 keypad7 keypad8 keypad9 keypad0
keypad. non-us| application power keypad= f13 f14 f15 f16 f17 f18 f19
f20 f21 f22 f23 f24 execute help menu select stop again undo cut copy
paste find mute volume+ volume- leftctrl leftshift leftalt leftcmd
rightctrl rightshift rightalt rightcmd
```

## Installation
If you have Homebrew, you can install like this:

```bash
$ brew install ivangreene/keymap/keymap
```

Otherwise, `keymap.py` is a standalone python executable that you can copy
somewhere in your PATH, and `keymap.1` is the man page.

## Issues
- Some keys don't work as a source (for example, you can do `map g volume+`,
  but `map volume+ g` doesn't work as expected.)

- Some keys seem not to work as their names indicate.

- Some keys aren't included as being available. I would appreciate help if you know the functionality of unincluded keys (specifically range 130-224) or are willing to test them out.

#### Resources:
- Apple Developer: Technical Note TN2450, Remapping Keys in macOS 10.12 Sierra [https://developer.apple.com/library/content/technotes/tn2450/_index.html](https://developer.apple.com/library/content/technotes/tn2450/_index.html)
- usb.org HID Usage Tables [http://www.usb.org/developers/hidpage/Hut1_12v2.pdf](http://www.usb.org/developers/hidpage/Hut1_12v2.pdf) - dead link - archived at (https://web.archive.org/web/20180826215839/http://www.usb.org/developers/hidpage/Hut1_12v2.pdf)[https://web.archive.org/web/20180826215839/http://www.usb.org/developers/hidpage/Hut1_12v2.pdf]
- Keyboard Event Viewer [https://w3c.github.io/uievents/tools/key-event-viewer.html](https://w3c.github.io/uievents/tools/key-event-viewer.html)
