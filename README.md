# Kveiki


### Running game
```
$ python2 kveiki.py
```
### Making levels
Levels are saved as text files with `.lvl` suffix where one char means one level field.

| Char | Description |
|------|-------------|
| X | Wall |
| _space_ | Air (white background) |
| s | Air (no background) |
| P | Player |
| F | Finish |
| C | Coin |
| K | Key (black) |
| D | Door (black) |
| G | Green door |
| g | Green key |
| R | Red drwi |
| r | Red key |
| B | Blue door |
| b | Blue key |
| Y | Yellow door |
| y | Yellow key |
| M | Monster |
| * | Monster trail |
| Z | Box |

#### Optional files inside level set:
 * `queue` – specifies levele order
 * `description` – text shown before first level

