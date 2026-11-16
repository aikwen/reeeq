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

        {
            "desc": "chrome browser headers",
            "input": (
                "curl 'https://example.com/api/items?page=1' "
                "-H 'accept: application/json' "
                "-H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8' "
                "-H 'sec-ch-ua: \"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\"' "
                "-H 'sec-ch-ua-mobile: ?0' "
                "-H 'sec-fetch-dest: empty' "
                "-H 'sec-fetch-mode: cors' "
                "-H 'sec-fetch-site: same-origin' "
                "--compressed"
            ),
            "expected": [
                "curl",
                "https://example.com/api/items?page=1",
                "-H", "accept: application/json",
                "-H", "accept-language: zh-CN,zh;q=0.9,en;q=0.8",
                "-H", 'sec-ch-ua: "Chromium";v="130", "Google Chrome";v="130"',
                "-H", "sec-ch-ua-mobile: ?0",
                "-H", "sec-fetch-dest: empty",
                "-H", "sec-fetch-mode: cors",
                "-H", "sec-fetch-site: same-origin",
                "--compressed",
            ],
        },
        {
            "desc": "cookie and bearer token",
            "input": (
                "curl 'https://example.com/api/profile' "
                "-H 'Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.test.signature' "
                "-H 'Cookie: session=abc123; theme=dark; lang=zh-CN' "
                "-H 'Accept: application/json' "
                "--location"
            ),
            "expected": [
                "curl",
                "https://example.com/api/profile",
                "-H", "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.test.signature",
                "-H", "Cookie: session=abc123; theme=dark; lang=zh-CN",
                "-H", "Accept: application/json",
                "--location",
            ],
        },
        {
            "desc": "url encoded form",
            "input": (
                "curl 'https://example.com/login' "
                "-X POST "
                "-H 'Content-Type: application/x-www-form-urlencoded' "
                "--data-raw 'username=alice&password=p%40ss%26word&remember=true'"
            ),
            "expected": [
                "curl",
                "https://example.com/login",
                "-X", "POST",
                "-H", "Content-Type: application/x-www-form-urlencoded",
                "--data-raw", "username=alice&password=p%40ss%26word&remember=true",
            ],
        },
        {
            "desc": "json patch request",
            "input": (
                "curl 'https://example.com/api/users/42' "
                "-X PATCH "
                "-H 'Content-Type: application/json' "
                """--data-raw '{"name":"Alice","roles":["admin","editor"],"active":true}'"""
            ),
            "expected": [
                "curl",
                "https://example.com/api/users/42",
                "-X", "PATCH",
                "-H", "Content-Type: application/json",
                "--data-raw",
                '{"name":"Alice","roles":["admin","editor"],"active":true}',
            ],
        },
        {
            "desc": "firefox style request",
            "input": (
                "curl 'https://example.com/api/orders' "
                "-X PUT "
                "-H 'User-Agent: Mozilla/5.0 Firefox/159.0' "
                "-H 'Accept: */*' "
                "-H 'Origin: https://example.com' "
                "-H 'Sec-Fetch-Mode: cors' "
                "-H 'Priority: u=0' "
                "--data-raw '{\"status\":\"paid\"}'"
            ),
            "expected": [
                "curl",
                "https://example.com/api/orders",
                "-X", "PUT",
                "-H", "User-Agent: Mozilla/5.0 Firefox/159.0",
                "-H", "Accept: */*",
                "-H", "Origin: https://example.com",
                "-H", "Sec-Fetch-Mode: cors",
                "-H", "Priority: u=0",
                "--data-raw", '{"status":"paid"}',
            ],
        },
        {
            "desc": "url with brackets and globoff",
            "input": (
                "curl --globoff "
                "'https://example.com/search?filter[status]=active&filter[sort]=desc' "
                "-H 'Accept: application/json'"
            ),
            "expected": [
                "curl",
                "--globoff",
                "https://example.com/search?filter[status]=active&filter[sort]=desc",
                "-H", "Accept: application/json",
            ],
        },

        {
            "desc": "json body with escaped double quotes",
            "input": (
                'curl "https://example.com/api" '
                '-H "Content-Type: application/json" '
                '--data-raw "{\\"name\\":\\"Alice\\",\\"age\\":20}"'
            ),
            "expected": [
                "curl",
                "https://example.com/api",
                "-H", "Content-Type: application/json",
                "--data-raw", '{"name":"Alice","age":20}',
            ],
        },
        {
            "desc": "single quote inside shell argument",
            "input": (
                "curl https://example.com "
                "-H 'X-Name: Alice'\"'\"'s Book'"
            ),
            "expected": [
                "curl",
                "https://example.com",
                "-H", "X-Name: Alice's Book",
            ],
        },
        {
            "desc": "multiple ansi-c escaped headers",
            "input": (
                "curl https://example.com "
                "-H $'X-Tab: hello\\tworld' "
                "-H $'X-Quote: it\\'s fine' "
                "-H $'X-Hex: \\x41\\x42\\x43'"
            ),
            "expected": [
                "curl",
                "https://example.com",
                "-H", "X-Tab: hello\tworld",
                "-H", "X-Quote: it's fine",
                "-H", "X-Hex: ABC",
            ],
        },
        {
            "desc": "multiline json with ansi-c quoting",
            "input": (
                "curl 'https://example.com/api' \\\n"
                "  -X POST \\\n"
                "  -H 'Content-Type: application/json' \\\n"
                "  --data-binary $'{\\n  \"name\": \"Alice\",\\n  \"age\": 20\\n}'"
            ),
            "expected": [
                "curl",
                "https://example.com/api",
                "-X", "POST",
                "-H", "Content-Type: application/json",
                "--data-binary",
                '{\n  "name": "Alice",\n  "age": 20\n}',
            ],
        },
        {
            "desc": "empty headers and empty body arguments",
            "input": (
                "curl https://example.com "
                "-H '' "
                "-H 'X-Empty:' "
                "--data-raw ''"
            ),
            "expected": [
                "curl",
                "https://example.com",
                "-H", "",
                "-H", "X-Empty:",
                "--data-raw", "",
            ],
        },
        {
            "desc": "mixed quotes with numeric escapes",
            "input": (
                "curl https://example.com "
                "--data-raw pre$'\\x41\\101\\u0042'post "
                "-H 'Content-Type: text/plain'"
            ),
            "expected": [
                "curl",
                "https://example.com",
                "--data-raw", "preAABpost",
                "-H", "Content-Type: text/plain",
            ],
        },

    ]
