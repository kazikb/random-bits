#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Kazimierz Biskup
# https://github.com/kazikb/random-bits
#
""" Script to binary patching files. """
import struct
import binascii
import argparse


class FilePatching:
    """ Class to implement variouse binary patching function.
        Supported operation:
        - Patch single byte/word/double word/quad word with signed or not.
        - Put utf-8 encoded string at specific offset.
        - Put byte stream at specific offset.
        - Save modifayed bytearray to a file with "-patched" suffix.

        :param f_path: str - source file.
        :param mode: str - how to print information output text/hex.
    """
    def __init__(self, f_path, print_mode="text"):
        self.print_mode = print_mode
        self.f_path = f_path

        with open(f_path, mode="rb") as f:
            self.file = bytearray(f.read())
        print(f"File: {f_path} Size: {len(self.file)} bytes")

    def patch_word(self, offset, fmt, value) -> bool:
        """ Function to patch single half-word/word/double word/quad word with
            signed or unsigned at specific offset. Format string is 2 characters
            according to Python documentation:
            https://docs.python.org/3/library/struct.html#format-strings
        """
        if not self.validate_input(fmt=fmt, value=value):
            print("Format string for pack invalid or value out of range for specific type")
            return False
        size = struct.calcsize(fmt)
        self.print_bytes(offset=offset, size=size, prefix="Original")
        self.file[offset:offset+size] = struct.pack(fmt, value)
        self.print_bytes(offset=offset, size=size, prefix="Patched")
        return True

    def patch_string(self, offset, value) -> None:
        """ Function to put string encoded with utf-8 at specific offset. """
        data = bytes(value, encoding="utf-8")
        self.patch_bytes(offset=offset, value=data)

    def patch_bytes(self, offset, value) -> None:
        """ Function to put byte stream at specific offset. """
        size = len(value)
        self.print_bytes(offset=offset, size=size, prefix="Original")
        self.file[offset:offset+size] = value
        self.print_bytes(offset=offset, size=size, prefix="Patched")

    def print_bytes(self, offset, size, prefix) -> None:
        """ Function to print bytes at specified offset."""
        off_end = offset+size
        if self.print_mode == "hex":
            data = binascii.hexlify(self.file[offset:off_end])
        else:
            data = self.file[offset:off_end]
        prefix = f"{prefix} value:"
        print(f"{prefix:<20} [0x{offset:08x}:0x{off_end:08x}][{data}]")

    def validate_input(self, fmt, value) -> bool:
        """ Function to validate input format and value for specific type."""
        ret_value = False
        if len(fmt) != 2 or fmt[0] not in ("<", ">"):
            return ret_value

        # Check if value is ok for selected type
        # Case: signed char/unsigned char -> 8 bit half word
        if fmt[1] == "b" and (-128 <= value <= 127):
            ret_value = True
        elif fmt[1] == "B" and (0 <= value <= 255):
            ret_value = True
        # Case: short/unsigned short -> 16 bit word
        elif fmt[1] == "h" and (-32768 <= value <= 32767):
            ret_value = True
        elif fmt[1] == "H" and (0 <= value <= 65535):
            ret_value = True
        # Case: int/unsigned int -> 32 bit double word
        elif fmt[1] == "i" and (-2147483648 <= value <= 2147483647):
            ret_value = True
        elif fmt[1] == "I" and (0 <= value <= 4294967295):
            ret_value = True
        # Case: long long/unsigned long long -> 64 bit quad word
        elif fmt[1] == "q" and (-9223372036854775808 <= value <= 9223372036854775807):
            ret_value = True
        elif fmt[1] == "Q" and (0 <= value <= 18446744073709551615):
            ret_value = True
        return ret_value

    def save(self, path=""):
        """ Function to save patched bytearray to a file. """
        if path:
            f_patched_path = path
        else:
            f_patched_path = f"{self.f_path}-patched"
        with open(f_patched_path, mode="wb") as f:
            f.write(self.file)
        print(f"Patched file: {f_patched_path} Size: {len(self.file)} bytes")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.description = """
Patching script can insert data at specific offset.

--pack - Use Python struct to put half word/word/double word/quad world at
         specific offset. The <fmt> string use 2 character format that is
         identical with the one defined in struct module.
         <fmt> help:
         1st character - Byte Order
         | < | little-endian
         | > | big-endian
         2en character - Size
         | b | signed char (1)
         | B | unsigned char (1)
         | h | short (2)
         | H | unsigned short (2)
         | i | int (4)
         | I | unsigned int (4)
         | q | long long (8)
         | Q | unsigned long long (8)

Example:
./patching.py ./test-file.pdf -o 0x20 -d "0xAF12" -p "<I"
File: ./test-file.pdf Size: 86160 bytes
Original value:      [0x00000020:0x00000024][bytearray(b'<FEF')]
Patched value:       [0x00000020:0x00000024][bytearray(b'\x12\xaf\x00\x00')]
Patched file: ./test-file.pdf-patched Size: 86160 bytes

--string - Put UTF-8 encoded string at specific offset.

Example:
./patching.py ./test-file.pdf -o 0x20 -d "ala ma kota" -s
File: ./test-file.pdf Size: 86160 bytes
Original value:      [0x00000020:0x0000002b][bytearray(b'<FEFF010600')]
Patched value:       [0x00000020:0x0000002b][bytearray(b'ala ma kota')]
Patched file: ./test-file.pdf-patched Size: 86160 bytes

--bytes - Put bytes stream at specific offset.

Example:
./patching.py ./test-file.pdf -o 0x40 -d "0xbe12afcc" -b
File: ./test-file.pdf Size: 86160 bytes
Original value:      [0x00000040:0x00000044][bytearray(b'E006')]
Patched value:       [0x00000040:0x00000044][bytearray(b'\xbe\x12\xaf\xcc')]
Patched file: ./test-file.pdf-patched Size: 86160 bytes
"""
    parser.add_argument("file", help="Source file.")
    parser.add_argument("-o", "--offset",
                        help="Offset where to put data.", required=True)
    parser.add_argument("-d", "--data",
                        help="Data to put at offset.", required=True)
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("-s", "--string",
                           help="UTF-8 encoded string to patch.",
                           action="store_true")
    operation.add_argument("-b", "--bytes",
                           help="Bytes stream to patch.", action="store_true")
    operation.add_argument("-p", "--pack", nargs=1,
                           help="<fmt string> Pack single hlaf byte/word/double\
                            word/quad word")
    parser.add_argument("-m", "--mode",
                        help="Format of printed message.",
                        choices=("text", "hex"), default="text")
    parser.add_argument("-w", "--write", help="Output file to save.")
    args = parser.parse_args()

    patch_at = int(args.offset, 16)
    binary_data = FilePatching(f_path=args.file, print_mode=args.mode)

    if args.pack:
        patch_v = int(args.data, 16)
        binary_data.patch_word(offset=patch_at, fmt=args.pack[0], value=patch_v)
    elif args.string:
        binary_data.patch_string(offset=patch_at, value=args.data)
    elif args.bytes:
        patch_v = bytes.fromhex(args.data[2:])
        binary_data.patch_bytes(offset=patch_at, value=patch_v)

    binary_data.save(path=args.write)
