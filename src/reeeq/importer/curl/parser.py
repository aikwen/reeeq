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

                        if value is None:
                            raise ValueError(f"Option {name!r} requires an argument")

                        options.append((name, value))
                        break
            elif v == 0:
                options.append((token, None))
            elif v == 1:
                arg = self.next_token()
                if arg is None:
                    raise ValueError(f"option {token !r} requires an argument")
                options.append((token, arg))
            else:
                raise ValueError(f"Unexpected option arity: {v!r} for {token!r}")
        return options, positionals


    def parse(self) -> dict:
        # url, url_explicit
        url = [None, False]
        method = None
        headers = []

        use_get = False
        data_parts = []
        form_parts = []

        options, positionals = self.parse_options()
        for option, arg in options:
            # 如果是method相关的参数
            if option in ("-X", "--request"):
                method = arg

            # header 相关的参数
            elif option in  ("-H", "--header"):

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
            elif option == "--url":
                # 如果 url = "" 或者第一次出现 url arg
                if not url[1]:
                    url = [arg, True]

                # 已经出现了 --url, 后面的url 都忽略
                else:
                    pass
            # 显式 get 参数
            elif option in ("-G", "--get"):
                use_get = True

            # data family
            elif option in (
                    "-d",
                    "--data",
                    "--data-ascii",
                    "--data-raw",
                    "--data-binary",
                    "--data-urlencode",
            ):

                data_parts.append((option, arg))
            # form 表单
            elif option in ("-F", "--form"):

                name, sep, value = arg.partition("=")

                if not sep:
                    form_parts.append((arg, ""))
                else:
                    # 普通字段：
                    #   -F "name=kwen"
                    #
                    # 文件字段暂不读取，只保留引用：
                    #   -F "file=@test.png"
                    form_parts.append((name, value))
            # 其它
            else:
                pass

