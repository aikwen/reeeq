CASES = \
    [
        {
            "desc": "basic",
            "input": "curl -X POST https://example.com",
            "expected": ["curl", "-X", "POST", "https://example.com"],
        },
        {
            "desc": "empty quote",
            "input": "''",
            "expected": [""],
        },
        {
            "desc": "quoted concatenation",
            "input": 'abc"def"',
            "expected": ["abcdef"],
        },
        {
            "desc": "ansi-c escape",
            "input": r"$'hello\nworld'",
            "expected": ["hello\nworld"],
        },
        {
            "desc": "unclosed single quote",
            "input": "'hello",
            "error": ValueError,
        },
        {
            "desc": "unclosed double quote",
            "input": '"hello',
            "error": ValueError,
        },

        {
            "desc": "dollar followed by word",
            "input": "$hello",
            "expected": ["$hello"],
        },
        {
            "desc": "dollar at eof",
            "input": "$",
            "expected": ["$"],
        },
        {
            "desc": "dollar followed by space",
            "input": "$ hello",
            "expected": ["$", "hello"],
        },
        {
            "desc": "hash inside word",
            "input": "abc#def",
            "expected": ["abc#def"],
        },
        {
            "desc": "comment after word",
            "input": "abc # comment",
            "expected": ["abc"],
        },
        {
            "desc": "escaped whitespace",
            "input": r"abc\ def",
            "expected": ["abc def"],
        },
        {
            "desc": "line continuation",
            "input": "abc\\\ndef",
            "expected": ["abcdef"],
        },
        {
            "desc": "quoted concatenation",
            "input": """abc"def"'ghi'""",
            "expected": ["abcdefghi"],
        },
        {
            "desc": "ansi-c concatenation",
            "input": r"abc$'\n'def",
            "expected": ["abc\ndef"],
        },
        {
            "desc": "ansi-c octal",
            "input": r"$'\101'",
            "expected": ["A"],
        },
        {
            "desc": "ansi-c hex with trailing character",
            "input": r"$'\x41Z'",
            "expected": ["AZ"],
        },
        {
            "desc": "ansi-c unicode",
            "input": r"$'\u4E2D'",
            "expected": ["中"],
        },
        {
            "desc": "unclosed ansi-c quote",
            "input": "$'hello",
            "error": ValueError,
        },
        {
            "desc": "trailing backslash",
            "input": "abc\\",
            "error": ValueError,
        },

    ]
