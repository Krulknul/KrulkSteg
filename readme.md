# KrulkSteg PNG steganographic image encoder:
KrulkSteg is is a python script that can encode and decode text in PNG files.
The text is encoded into binary and stored in the least significant bits of the individual color channels.
This allows text to be encoded into the image without anyone noticing.
The text is easy to recover with the decode function of this script.

# Usage:
### python3 KrulkSteg.py [-h] -m {encode,decode} [-p PATH] [-s STRING] [-r]

arguments:
-  `-h ----------- show this help message and exit`
-  `-m MODE ------ Use this option to select the mode. The 'encode' mode takes a string and encodes it into the image repeatingly. It saves the
                        image as 'steg_filename.png' in cwd. The 'decode' mode returns the string once`
-  `-p PATH ------ Path to image. Defaults to 'img.png' in cwd`
-  `-s STRING ---- After this option, provide the string to be encoded into the image.`
-  `-b AMOUNT ---- Amount of bits to use per channel for encoding or decoding.`
-  `-r ----------- Print the raw repeating string decoded from the image, instead of the single string.`

https://youtu.be/TWEXCYQKyDc
