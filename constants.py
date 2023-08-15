
import os

VERSION = "0.3.1"
SCRIPTDIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_FILEFILTER = "Images (*.png *.jpg *.jpeg *.gif *.bmp);;All Files (*)"
HEX_FILEFILTER = "All Supported Files (*.hex);;All Files (*)"
BIN_FILEFILTER = "All Supported Files (*.bin);;All Files (*)"
ARDUHEX_FILEFILTER = "All Supported Files (*.hex *.arduboy *.zip);;All Files (*)"
ARDUBOY_FILEFILTER = "All Supported Files (*.arduboy);;All Files (*)"

TINYFONT = "m3x6.ttf"
TINYFONT_WIDTH = 4 #WARN: This is not always the case!!
