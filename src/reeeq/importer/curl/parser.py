from options import OPTION_ARITY

class CurlParser:
    def __init__(self, tokens:list[str]):
        if not tokens or tokens[0] != 'curl':
            raise ValueError("Expected curl command")

        self.tokens = tokens
        self.len = len(tokens)
        self.pos = 1

    def next_token(self) -> str | None:
        if self.pos >= self.len:
            return None
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def parse_options(self) -> (list, list):
        options = []
        positionals = []

        while True:
            token = self.next_token()
            # 已经达到末尾
            if token is None:
                break

            v = OPTION_ARITY.get(token, None)
            if v is None:
                # 位置参数
                if not token.startswith("-"):
                    positionals.append(token)

                # 长选项携带参数，例如 --request=POST
                elif token.startswith("--"):
                    name, sep, value = token.partition("=")
                    arity = OPTION_ARITY.get(name)

                    if not sep or arity != 1:
                        raise ValueError(f"Unknown or invalid option: {token}")

                    options.append((name, value))

                # 短选项组合，例如 -svXPOST
                else:
                    for i in range(1, len(token)):
                        name = "-" + token[i]
                        arity = OPTION_ARITY.get(name, None)

                        if arity is None:
                            raise ValueError(f"Unknown option: {name}")

                        if arity == 0:
                            options.append((name, None))
                            continue

                        # SINGLE：剩余字符作为参数
                        value = token[i + 1:]

                        if not value:
                            value = self.next_token()

                        options.append((name, value))
                        break
            elif v == 0:
                options.append((token, None))
            elif v == 1:
                options.append((token, self.next_token()))
            else:
                raise ValueError(f"Unexpected option arity: {v!r} for {token!r}")
        return options, positionals


    def parse(self) -> dict:
        method = ""
        url = None
        url_option = False
        headers = []

        options, positionals = self.parse_options()
        for option, arg in options:
            # 如果是method相关的参数
            if option in ("-X", "--request"):
                if arg is None:
                    raise ValueError(f"Option {option!r} requires an argument")
                method = arg

            # header 相关的参数
            elif option in  ("-H", "--header"):
                if arg is None:
                    raise ValueError(f"Option {option!r} requires an argument")

                # 解析 header
                header = arg
                name, sep, value = header.partition(":")
                name = name.strip()
                value = value.lstrip(" \t")

                # 正常情况 "Authorization: Bearer abc:def:ghi"
                if sep and name and value:
                    headers.append((name, value))
                # 空 header "X-test;" 添加一个空 header
                elif not sep and len(name) >= 2 and name.endswith(";"):
                    headers.append((name[:-1], value))
                else:
                    pass
            # url 相关的参数
            elif option in ("--url",):

                # 如果 url = "" 或者第一次出现 url arg
                if not url_option:
                    if arg is None:
                        raise ValueError(f"Option {option!r} requires an argument")
                    url = arg
                    url_option = True

                # 已经出现了 --url, 后面的url 都忽略
                else:
                    pass
            # 其它参数
            else:
                pass
