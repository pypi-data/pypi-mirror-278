import json
from pygments import highlight
from pygments.formatters import TerminalTrueColorFormatter
from pygments.lexers.web import JsonLexer
def pretty_print_json(data: dict) -> None:
    raw_json = json.dumps(data, indent=4)
    colorful = highlight(
        raw_json,
        lexer=JsonLexer(),
        formatter=TerminalTrueColorFormatter(),
    )
    print(colorful)