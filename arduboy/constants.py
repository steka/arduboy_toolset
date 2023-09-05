"""
A collection of constants related to Arduboy

These are not ALL constants related to Arduboy, just ones common to many modules. 
Certain constants are only related to specific functionality, such as device IDs or locations of 
data within the FX header. Those constants go with their respective modules
"""

FLASH_PAGESIZE = 128        # Not sure if this is the true page size but it's what a lot of this program uses
FLASHSIZE = 32768         # Size of the onboard flash (default chip whatever, atmega etc)

FX_PAGESIZE = 256       # The hardware page size in the FX modchip flash
FX_BLOCKSIZE = 65536    # The hardware block size in the FX etc
FX_PAGES_PER_BLOCK = FX_BLOCKSIZE // FX_PAGESIZE 

SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64
SCREEN_BYTES = SCREEN_WIDTH * SCREEN_HEIGHT // 8
