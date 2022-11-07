import argparse
import re
from PIL import Image
from os import path


def string_to_bin(string):
    bitstring = bin(int.from_bytes(string.encode(), 'big'))
    return bitstring.replace('b', '')


def bin_to_string(bitstring):
    integer = int(bitstring, 2)
    bytes = integer.to_bytes((integer.bit_length() + 7) // 8, 'big')
    return bytes.decode(errors='ignore')


def repetitions(s):
    regex = re.compile(r"(.+?)\1+")
    matching = regex.match(s)
    return matching.group(1)


def encode(img, string):
    bitstring = string_to_bin(string)
    bit_index = 0
    for y in range(1, img.height):
        for x in range(1, img.width):
            pixel = img.getpixel((x, y))
            new_values = []
            for j, value in enumerate(pixel):
                if bit_index >= len(bitstring):
                    bit_index = 0
                new_values.append('{0:08b}'.format(value))
                changed_value = new_values[j][:-1] + bitstring[bit_index]
                new_values[j] = int(changed_value, 2)
                bit_index += 1
            new_pixel = tuple(new_values)
            img.putpixel((x, y), new_pixel)
    img.save('out.png')


def decode(img, extract=False):
    bitstring = ''
    for y in range(1, img.height):
        for x in range(1, img.width):
            pixel = img.getpixel((x, y))
            for value in pixel:
                bitstring += '{0:08b}'.format(value)[-1]
    while (len(bitstring) % 8) != 0:
        bitstring = bitstring[:-1]
    decoded = bin_to_string(bitstring)

    if not extract:
        repeating = repetitions(decoded)
        return repeating if repeating else 'no'
    else:
        return decoded


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                    prog='KrulkSteg',
                    description='''Python script for steganography
                                   on PNG images.''')
    parser.add_argument('-m', '--mode',
                        choices=['encode', 'decode'],
                        help='''Use this option to select the mode.
                                The 'encode' mode takes a string and encodes
                                it into the image repeatingly. It saves the
                                image as 'out.png' in cwd.
                                The 'decode' mode returns the string once''',
                        required=True)
    parser.add_argument('-p', '--path',
                        help="Path to image. Defaults to 'image.png' in cwd")
    parser.add_argument('-s', '--string',
                        help='''After this option, provide the string
                                to be encoded into the image.''')
    parser.add_argument('-r', '--raw',
                        action='store_true',
                        help='''Print the raw data decoded from the image,
                                instead of the single string.''')
    args = parser.parse_args()
    if args.mode == 'encode' and args.string is None:
        print("""The 'encode' mode needs a string as message.
                 Please use the -m option to provide a string.""")
        exit()
    if args.path is None:
        args.path = 'img.png'
    if not path.exists(args.path):
        print("\nThe file is not found.")
        print("Please fix or provide a path with the -p option.")
        exit()
    img = Image.open(args.path)
    img = img.convert('RGB')

    if args.mode == 'decode':
        print('\nDecoded string:\n\n' + decode(img, args.raw))

    if args.mode == 'encode':
        string = args.string
        encode(img, string)
        print(f"\n'{decode(img, args.raw)}' was encoded successfully")
