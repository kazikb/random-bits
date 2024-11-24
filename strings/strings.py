#!/usr/bin/env python3
#
# Kazimierz Biskup
# https://github.com/kazikb/random-bits
#
""" As an exercise I implement my own version of the "strings" tool. """
import argparse
import string


class WordSearch:
    """ Class to search printable characters that will form words in binary
        file. Supported encodings: ASCII, UTF-8, UTF-16-BE, UTF-16-LE.
        Optionaly we can check if string contains at list one word from polish
        or english before classifaing it to print on output.
    """
    def __init__(
        self,
        min_word_size,
        mode="utf8",
        dictionary=False,
        wordlist="internal"
        ):

        self.word = []
        self.min_word_size = min_word_size
        self.mode = mode
        self.utf = {
            "utf8": False,
            "byte_number": 0,
            "code_points": []
        }
        self.wordlist = []
        self.dictionary = dictionary

        # initialize wordlist to check if string is valid dictionary word
        if self.dictionary:
            self.dictionary = self.init_wordlist(wordlist=wordlist)

    def init_wordlist(self, wordlist) -> bool:
        """ Initialize word list with polish and english words.
            By default internal wordlist will be used bout on Linux system it
            can be changed to system global wordlist
        """
        if wordlist == "system":
            worldlists_path = ("/usr/share/dict/polish",
                "/usr/share/dict/american-english")
        else:
            worldlists_path = ("./polish.txt", "./english.txt")

        try:
            for worldlist in worldlists_path:
                with open(worldlist, mode="r", encoding="utf-8") as f:
                    self.wordlist.extend([line.rstrip() for line in f])
            # remove duplicate items by converting list into set
            self.wordlist = set(self.wordlist)
            return True
        except OSError:
            print("[ERROR] Cannot open wordlist file")
            return False

    def search(self, byte) -> None:
        """ Function to classify what encoded strings to search. When UTF-8 is
            selected, then ASCII characters will also be searched.

        Help: UTF-8 byte categorization and bit mask
        0b11000000 = 0xc0 (check mask: 0b11100000 = 0xe0) - 2 byte long encoded
        0b11100000 = 0xe0 (check mask: 0b11110000 = 0xf0) - 3 byte long encoded
        0b11110000 = 0xf0 (check mask: 0b11111000 = 0xf8) - 4 byte long encoded
        0b10000000 = 0x80 (check mask: 0b11000000 = 0xc0) - continuation byte
        """
        if self.mode == "utf8":
            if (
                self.utf["utf8"] or
                (byte & 0b11000000) == 0b10000000 or
                (byte & 0b11100000) == 0b11000000 or
                (byte & 0b11110000) == 0b11100000 or
                (byte & 0b11111000) == 0b11110000
                ):
                if not self.parse_utf8(byte):
                    self.print_word()
            elif byte < 0x80:
                if not self.parse_ascii(byte):
                    self.print_word()
            else:
                self.print_word()
        else:
            if not self.parse_utf16(byte):
                self.print_word()

    def parse_ascii(self, byte) -> bool:
        """ Function to parse bytes that will represent ASCII encoded character.
            - 0x20 - 0x7E - ASCII printable characters.
            - 0x9 - Horizontal Tab
            - 0xA - Line Feed
            - 0xD - Carriage Return
        """
        if 0x20 <= byte <= 0x7E or byte in (0x9, 0xA, 0xD):
            self.word.append(chr(byte))
            return True
        return False

    def parse_utf8(self, byte) -> bool:
        """ Function to parse UTF-8 byte stream.

        0b11000000 = 0xc0 (check mask: 0b11100000 = 0xe0) - 2 byte long encoded
        0b11100000 = 0xe0 (check mask: 0b11110000 = 0xf0) - 3 byte long encoded
        0b11110000 = 0xf0 (check mask: 0b11111000 = 0xf8) - 4 byte long encoded
        0b10000000 = 0x80 (check mask: 0b11000000 = 0xc0) - continuation byte
        """
        if (byte & 0b11100000) == 0b11000000 and not self.utf["utf8"]:
            self.utf["utf8"] = True
            self.utf["byte_number"] = 1
            self.utf["code_points"].append(byte)
            return True
        if (byte & 0b11110000) == 0b11100000 and not self.utf["utf8"]:
            self.utf["utf8"] = True
            self.utf["byte_number"] = 2
            self.utf["code_points"].append(byte)
            return True
        if (byte & 0b11111000) == 0b11110000 and not self.utf["utf8"]:
            self.utf["utf8"] = True
            self.utf["byte_number"] = 3
            self.utf["code_points"].append(byte)
            return True
        if (byte & 0b11000000) == 0b10000000 and self.utf["byte_number"] > 0:
            self.utf["byte_number"] -= 1
            self.utf["code_points"].append(byte)
            if self.utf["byte_number"] == 0:
                return self.parse_utf8_code_point()
            return True

        return False

    def parse_utf8_code_point(self) -> bool:
        """ Function to convert bytes stream to UTF-8 codepoint. """
        try:
            code_char = bytes(self.utf["code_points"]).decode("utf-8")
            self.word.append(code_char)
            self.utf = {
                "utf8": False,
                "byte_number": 0,
                "code_points": []
            }
            return True
        except UnicodeDecodeError:
            return False

    def parse_utf16(self, byte) -> bool:
        """ Function to parse UTF-16BE and UTF-16LE byte stream.

            0x0 - 0xD7FF and 0xE000 - 0xFFFF - encoded with 2 byte
            0xD800 - 0xDFFF - surrogate range indicating 4 byte codepoint to
                              encode rest of uinicode characters.
                0xD800 - 0xDBFF - firs 2 byte high bits
                0xDC00 - 0xDFFF - secend 2 byte low bits
        """
        if (
            len(self.utf["code_points"]) < 1 or
            (len(self.utf["code_points"]) == 2 and self.utf["byte_number"] == 4)
            ):
            self.utf["code_points"].append(byte)
            return True
        if len(self.utf["code_points"]) == 1:
            if self.mode == "utf16be":
                high_byte = (self.utf["code_points"][0] << 8) | byte
            else:
                high_byte = (byte << 8) | self.utf["code_points"][0]
            if high_byte <= 0xd7ff or high_byte >= 0xe000:
                self.utf["code_points"].append(byte)
                return self.parse_utf16_code_point()
            if 0xd800 <= high_byte <= 0xdbff:
                self.utf["byte_number"] = 4
                self.utf["code_points"].append(byte)
                return True
        if len(self.utf["code_points"]) == 3:
            if self.mode == "utf16be":
                low_byte = (self.utf["code_points"][2] << 8) | byte
            else:
                low_byte = (byte << 8) | self.utf["code_points"][2]
            if 0xdc00 <= low_byte <= 0xdfff:
                self.utf["code_points"].append(byte)
                return self.parse_utf16_code_point()

            # removing 2 high bits because in low bits could be start of another
            # utf-16 encoded stream.
            self.utf["code_points"].pop(0)
            self.utf["code_points"].pop(0)
            self.utf["byte_number"] = 0
            return self.parse_utf16_code_point()
        return False

    def parse_utf16_code_point(self) -> bool:
        """ Function to convert bytes stream to UTF-16 codepoint. """
        try:
            if self.mode == "utf16be":
                code_char = bytes(self.utf["code_points"]).decode("utf_16_be")
            else:
                code_char = bytes(self.utf["code_points"]).decode("utf_16_le")
            self.word.append(code_char)
            self.utf = {
                "utf8": False,
                "byte_number": 0,
                "code_points": []
            }
            return True
        except UnicodeDecodeError:
            # removing 1 bit because it could be start of another utf-16 encoded
            # stream.
            self.utf["code_points"].pop(0)
            return False

    def is_dictionary(self, words) -> bool:
        """" Function to check if there is dictionary word in capture string."""
        for word in words.split():
            # remove punctuation characters
            word = word.translate(str.maketrans("", "", string.punctuation))
            if word.lower() in self.wordlist and len(word) >= 5:
                return True
        return False

    def print_word(self) -> None:
        """ Function to print complete string and reset all structures.
            Checking if string is dictionary world is optional.
        """
        if len(self.word) >= self.min_word_size:
            words = "".join(self.word)
            if self.dictionary and self.is_dictionary(words):
                print(words)
            elif not self.dictionary:
                print(words)

        self.word = []
        self.utf = {
            "utf8": False,
            "byte_number": 0,
            "code_points": []
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="File path")
    parser.add_argument("-n", "--number", type=int, default=4,
                        help="Minimal number of characters")
    parser.add_argument("-d", "--dictionary",
                        help="Print strings that contain at least one world \
                            from polish or english",
                        action="store_true")
    parser.add_argument("-w", "--wordlist",
                        help="Use polish and english dictionary. System \
                            use /usr/share/dict (only Linux), 'internal' use \
                            attached files ./polish.txt and english.txt. \
                            default=internal",
                        choices=("internal", "system"),
                        default="internal")
    parser.add_argument("-e", "--encoding",
                        help="Search utf8, utf16 big endian or utf16 litle \
                            endian encoded strings. default=utf8",
                        choices=("utf8", "utf16be", "utf16le"),
                        default="utf8")
    args = parser.parse_args()

    READ_BUFFER = 1024  # Size of file chunk to read

    word_search = WordSearch(
        min_word_size=args.number,
        mode=args.encoding,
        dictionary=args.dictionary,
        wordlist=args.wordlist
        )

    with open(args.file, mode="rb") as file:
        while True:
            data = file.read(READ_BUFFER)
            if not data:
                word_search.print_word()
                break
            for item in data:
                word_search.search(item)
