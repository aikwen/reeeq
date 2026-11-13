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
]
