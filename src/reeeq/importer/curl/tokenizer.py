from collections import deque
from enum import Enum, auto
from io import TextIOBase, StringIO


class State(Enum):
    SPACE = auto()
    WORD = auto()
    SINGLE_QUOTE = auto()
    DOUBLE_QUOTE = auto()
    ANSI_C_QUOTE = auto()
    ESCAPE = auto()

WHITESPACE = " \t\r\n"
COMMENT = "#"
ESCAPE = "\\"
QUOTES = "\"'"

class BashTokenizer:
    def __init__(self, instream: str | TextIOBase):
        if isinstance(instream, str):
            instream = StringIO(instream)
        elif not isinstance(instream, TextIOBase):
            raise TypeError(
                "instream must be a string or a text stream"
            )

        self.instream = instream
        self.state = State.SPACE
        self.token = ""
        self.pushback = deque()

    def __iter__(self):
        return self

    def __next__(self):
        token = self.read_token()
        if token is None:
            raise StopIteration
        return token

    def _read_char(self) -> str:
        return self.pushback.pop() if self.pushback else self.instream.read(1)

    def _pushback_char(self, char: str) -> None:
        if len(char) != 1:
            raise ValueError("Expected a single character")
        self.pushback.append(char)

    def _read_ansi_escape(self, char: str) -> str:
        escapes = {
            "a": "\a",
            "b": "\b",
            "e": "\x1b",
            "E": "\x1b",
            "f": "\f",
            "n": "\n",
            "r": "\r",
            "t": "\t",
            "v": "\v",
            "\\": "\\",
            "'": "'",
            '"': '"',
            "?": "?",
        }

        if char == "\n":
            return ""

        if char in escapes:
            return escapes[char]

        # 八进制转义：最多读取三个八进制数字（包含 char）
        if char in "01234567":
            digits = char

            while len(digits) < 3:
                c = self._read_char()

                if not c:
                    break

                if c not in "01234567":
                    self._pushback_char(c)
                    break

                digits += c

            return chr(int(digits, 8))

        # 十六进制转义：\xHH，最多读取两位
        if char == "x":
            digits = ""

            while len(digits) < 2:
                c = self._read_char()

                if not c:
                    break

                if c not in "0123456789abcdefABCDEF":
                    self._pushback_char(c)
                    break

                digits += c

            if not digits:
                return "\\x"

            return chr(int(digits, 16))

        # Unicode 转义：\u 最多 4 位，\U 最多 8 位
        if char in "uU":
            max_digits = 4 if char == "u" else 8
            digits = ""

            while len(digits) < max_digits:
                c = self._read_char()

                if not c:
                    break

                if c not in "0123456789abcdefABCDEF":
                    self._pushback_char(c)
                    break

                digits += c

            if not digits:
                return "\\" + char

            codepoint = int(digits, 16)

            if codepoint > 0x10FFFF or 0xD800 <= codepoint <= 0xDFFF:
                raise ValueError(f"Invalid Unicode code point: U+{codepoint:04X}")

            return chr(codepoint)

        # 控制字符转义：\cX
        if char == "c":
            c = self._read_char()

            if not c:
                return "\\c"

            if c == "?":
                return "\x7f"

            return chr(ord(c.upper()) ^ 0x40)

        return "\\" + char

    def read_token(self):
        escaped_state = self.state
        token_start = False

        while True:
            next_char = self._read_char()

            # 空格状态
            if self.state == State.SPACE:
                # 没有下一个字符
                if not next_char:
                    return None
                # 下一个字符是空格
                elif next_char in WHITESPACE:
                    continue
                # 下一个字符是注释
                elif next_char in COMMENT:
                    self.instream.readline()
                    continue
                # 下一个字符是转义符
                elif next_char in ESCAPE:
                    escaped_state = self.state
                    self.state = State.ESCAPE
                    continue
                # 下一个字符串是引号
                elif next_char in QUOTES:
                    token_start = True
                    if next_char == "\"":
                        self.state = State.DOUBLE_QUOTE
                    elif next_char == "'":
                        self.state = State.SINGLE_QUOTE
                # 下一个字符串是 dollar 符号
                elif next_char == "$":
                    token_start = True
                    c = self._read_char()
                    if c == "'":
                        self.state = State.ANSI_C_QUOTE
                    else:
                        self.token += next_char
                        self.state = State.WORD
                        if c:
                            self.pushback.append(c)
                        continue
                else:
                    token_start = True
                    self.state = State.WORD
                    self.token += next_char

            elif self.state == State.WORD:
                if not next_char:
                    break

                elif next_char in WHITESPACE:
                    self.state = State.SPACE
                    break

                elif next_char in ESCAPE:
                    escaped_state = self.state
                    self.state = State.ESCAPE
                    continue

                elif next_char in QUOTES:
                    if next_char == "'":
                        self.state = State.SINGLE_QUOTE
                    else:
                        self.state = State.DOUBLE_QUOTE
                    continue

                elif next_char == "$":
                    c = self._read_char()
                    if c == "'":
                        self.state = State.ANSI_C_QUOTE
                    else:
                        self.token += next_char
                        if c:
                            self.pushback.append(c)
                else:
                    self.token += next_char

            elif self.state == State.SINGLE_QUOTE:
                if not next_char:
                    raise ValueError("Unclosed single quote")
                elif next_char == "'":
                    self.state = State.WORD
                else:
                    self.token += next_char

            elif self.state == State.DOUBLE_QUOTE:
                if not next_char:
                    raise ValueError("Unclosed double quote")
                elif next_char == "\"":
                    self.state = State.WORD
                elif next_char in ESCAPE:
                    escaped_state = self.state
                    self.state = State.ESCAPE
                else:
                    self.token += next_char

            elif self.state == State.ANSI_C_QUOTE:
                if not next_char:
                    raise ValueError("Unclosed ANSI C quote")
                elif next_char == "'":
                    self.state = State.WORD
                elif next_char == ESCAPE:
                    escaped_state = self.state
                    self.state = State.ESCAPE
                else:
                    self.token += next_char

            elif self.state == State.ESCAPE:
                if not next_char:
                    raise ValueError("")
                else:
                    if escaped_state == State.SPACE:
                        if next_char == "\n":
                            self.state = State.SPACE
                        else:
                            self.token += next_char
                            token_start = True
                            self.state = State.WORD
                    elif escaped_state == State.WORD:
                        if next_char != "\n":
                            self.token += next_char
                        self.state = State.WORD

                    elif escaped_state == State.DOUBLE_QUOTE:
                        if next_char == "\n":
                            pass
                        elif next_char in '$`"\\':
                            self.token += next_char
                        else:
                            self.token += "\\" + next_char

                        self.state = State.DOUBLE_QUOTE
                    elif escaped_state == State.ANSI_C_QUOTE:
                        self.token += self._read_ansi_escape(next_char)
                        self.state = State.ANSI_C_QUOTE
                    else:
                        raise ValueError()


        token = self.token
        self.token = ""
        self.state = State.SPACE

        return token


def split(command: str) -> list[str]:
    return list(BashTokenizer(command))

