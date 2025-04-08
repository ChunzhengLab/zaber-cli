# ZABER Stage Controller CLI

All credits to ALICE ITS3-WP3

A minimal and effective command-line interface for controlling Zaber motion stages via serial port and JSON configuration.

---

## NOTE: 
One havs to make the udev rules for the serial path. This is a example works for the TB PS April 2025 @CERN

```bash
sudo cp udev/96-zaber.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
# Then physically replug both USB connections!!!
```

To check current device symlinks:
`ls -l /dev | grep '^l'`

---

## Features

-  Auto-detect connected Zaber devices
-  Print axis positions in table format
-  Home all or selected axes
-  Move axes (absolute or relative)
-  Move axes to predefined initial positions
-  Support for direction aliases (e.g. `door`, `wall`, `ceiling`, `floor`)
-  Override serial port path with `-p`

---

## Usage

### 1. Show device connection status

```bash
ZABER -s
```

Lists all configured devices and axes, connection state, alias, initial positions and directions.

### 2. Print position(s)

```bash
ZABER upstream -pp           # Print all axis positions
ZABER upstream -a x -pp      # Print specific axis position
```

### 3. Home axes

```bash
ZABER downstream -hm         # Home all axes
ZABER downstream -a y -hm    # Home specific axis
```

### 4. Move to initial position

```bash
ZABER upstream -ini          # Move all axes to initial
ZABER upstream -a x -ini     # Move single axis to initial
```
### 5. Move axis manually

```bash
ZABER upstream -a x -v 1000 -m abs              # Absolute move
ZABER downstream -a y -v 500 -m rel             # Relative move
ZABER upstream -a x -v 500 -m rel -d wall       # Relative move with direction alias
```

### 6. Override serial port

```bash
ZABER upstream -p /dev/ttyUSB1 -pp
```

---

## Configuration File Format

Each device has its own JSON file, e.g. /home/chun/zaberconf_upstream.json:
```json
[
  {
    "name": "zaber_upstream_x",
    "axis_number": 1,
    "initial": 20000,
    "dir_alias_neg": "door",
    "dir_alias_pos": "wall"
  },
  {
    "name": "zaber_upstream_y",
    "axis_number": 2,
    "initial": 20000,
    "dir_alias_neg": "ceiling",
    "dir_alias_pos": "floor"
  }
]
```

If axis numbers change (e.g., from 1,2 → 3,4), ZABER -s will detect config mismatch and fallback to unconfigured mode.

---

## Tips
- Axis names like x, y are automatically converted to full names like zaber_upstream_x
- After -hm, -ini, or move, current position is auto-printed
- Works best when devices are connected and configs are correct

---

## Dependencies
- Python 3
- pyserial
- rich
- Local Zaber config JSONs




