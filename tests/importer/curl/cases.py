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

        {
            "desc": "curl with multiple headers",
            "input": (
                "curl 'https://example.com/api/users' "
                "-X POST "
                "-H 'Content-Type: application/json' "
                "-H 'Authorization: Bearer abc123' "
                "-H 'Accept: application/json'"
            ),
            "expected": [
                "curl",
                "https://example.com/api/users",
                "-X",
                "POST",
                "-H",
                "Content-Type: application/json",
                "-H",
                "Authorization: Bearer abc123",
                "-H",
                "Accept: application/json",
            ],
        },
        {
            "desc": "curl with json body",
            "input": (
                "curl 'https://example.com/api/users' "
                "-X POST "
                "-H 'Content-Type: application/json' "
                '--data-raw \'{"name":"Alice","age":20}\''
            ),
            "expected": [
                "curl",
                "https://example.com/api/users",
                "-X",
                "POST",
                "-H",
                "Content-Type: application/json",
                "--data-raw",
                '{"name":"Alice","age":20}',
            ],
        },
        {
            "desc": "curl with duplicate headers",
            "input": (
                "curl https://example.com "
                "-H 'X-Test: first' "
                "-H 'X-Test: second' "
                "--compressed"
            ),
            "expected": [
                "curl",
                "https://example.com",
                "-H",
                "X-Test: first",
                "-H",
                "X-Test: second",
                "--compressed",
            ],
        },
        {
            "desc": "curl with multiline command",
            "input": (
                "curl 'https://example.com/api' \\\n"
                "  -X POST \\\n"
                "  -H 'Content-Type: application/json' \\\n"
                "  --data-raw '{\"message\":\"hello world\"}'"
            ),
            "expected": [
                "curl",
                "https://example.com/api",
                "-X",
                "POST",
                "-H",
                "Content-Type: application/json",
                "--data-raw",
                '{"message":"hello world"}',
            ],
        },
        {
            "desc": "curl with url query parameters",
            "input": (
                "curl 'https://example.com/search?q=hello%20world&page=2&sort=desc' "
                "-H 'Accept: application/json'"
            ),
            "expected": [
                "curl",
                "https://example.com/search?q=hello%20world&page=2&sort=desc",
                "-H",
                "Accept: application/json",
            ],
        },
        {
            "desc": "curl with ansi-c header",
            "input": (
                "curl https://example.com "
                "-H $'X-Test: hello\\tworld' "
                "-X GET"
            ),
            "expected": [
                "curl",
                "https://example.com",
                "-H",
                "X-Test: hello\tworld",
                "-X",
                "GET",
            ],
        },
        {
            "desc": "curl with escaped spaces",
            "input": (
                r"curl https://example.com "
                r"-H X-User:\ Alice "
                r"-H X-Project:\ reeeq"
            ),
            "expected": [
                "curl",
                "https://example.com",
                "-H",
                "X-User: Alice",
                "-H",
                "X-Project: reeeq",
            ],
        },
        {
            "desc": "curl with mixed quoting and headers",
            "input": (
                'curl "https://example.com/"api/users '
                """-H 'X-Name: '"Alice" """
                """-H "X-Version: 1.0" """
                "--location"
            ),
            "expected": [
                "curl",
                "https://example.com/api/users",
                "-H",
                "X-Name: Alice",
                "-H",
                "X-Version: 1.0",
                "--location",
            ],
        },
        {
            "desc": "curl with empty body",
            "input": (
                "curl https://example.com "
                "-X POST "
                "--data-raw ''"
            ),
            "expected": [
                "curl",
                "https://example.com",
                "-X",
                "POST",
                "--data-raw",
                "",
            ],
        },
        {
            "desc": "curl with ansi-c body",
            "input": (
                "curl https://example.com "
                "--data-binary $'hello\\nworld\\t!' "
                "-H 'Content-Type: text/plain'"
            ),
            "expected": [
                "curl",
                "https://example.com",
                "--data-binary",
                "hello\nworld\t!",
                "-H",
                "Content-Type: text/plain",
            ],
        },
        {
            "desc": "curl with comment and continuation",
            "input": (
                "curl https://example.com \\\n"
                "  -X GET\n"
                "# request comment\n"
                "-H 'Accept: */*'"
            ),
            "expected": [
                "curl",
                "https://example.com",
                "-X",
                "GET",
                "-H",
                "Accept: */*",
            ],
        },
        {
            "desc": "curl with unclosed header quote",
            "input": (
                "curl https://example.com "
                "-H 'Authorization: Bearer abc123"
            ),
            "error": ValueError,
        },

    ]
