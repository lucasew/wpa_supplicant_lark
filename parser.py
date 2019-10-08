from lark import Lark
from lark import Transformer
from pprint import pprint
from sys import stdin

_grammar = """
?start: keyvalue*

?block: "{" keyvalue* "}"

?value: anytext NEWLINE | block

?anytext: /.+/*

?keyvalue: NAME "=" value

?quote: "\\""


%import common.CNAME -> NAME
%import common.NUMBER -> NUM
%import common.WS
%import common.ESCAPED_STRING
%import common._STRING_ESC_INNER
%import common.NEWLINE
%ignore WS
"""


class _WpaSupplicantTransformer(Transformer):
    def NAME(self, node):
        return str(node)

    def start(self, nodes):
        networks = {}
        props = {}
        for node in nodes:
            if node[0] == "network":
                networks[node[1]["ssid"]] = node[1]
                del node[1]["ssid"]
                continue
            props[node[0]] = node[1]
        return {
            "networks": networks,
            "props": props
        }

    def value(self, node):
        ret = str(node[0]).strip("\"")
        try:
            return int(ret)
        except ValueError:
            return ret


    def keyvalue(self, node):
        return (str(node[0]), node[1])

    def block(self, block):
        props = {}
        for k, v in block:
            props[k] = v
        return props


class WpaSupplicantParser(Lark):
    def __init__(self):
        super(WpaSupplicantParser, self).__init__(
                       _grammar, parser='lalr',
                       transformer=_WpaSupplicantTransformer()
                       )

def parse(text: str):
    p = WpaSupplicantParser()
    return p.parse(text)


def main():
    f = stdin.read()
    res = parse(f)
    pprint(res)


if __name__ == "__main__":
    main()
