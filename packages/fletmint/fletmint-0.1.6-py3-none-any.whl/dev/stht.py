import flet as ft
import re
from dataclasses import dataclass
from memory_profiler import profile


@dataclass
class GitHubDark:
    editor_bg: str = "#0D1117"
    keyword: str = "#ff7b72"  # bright red for keywords
    function: str = "#d2a8ff"  # soft purple for function definitions
    function_call: str = "#d2a8ff"  # function calls match function definitions
    string: str = "#a5d6ff"  # light blue for strings
    comment: str = "#8b949e"  # muted gray for comments
    parameter: str = "#ffa657"  # orange for parameters
    type_annotation: str = (
        "#ff7b72"  # bright red for type annotations, matching keywords
    )
    class_name: str = "#d2a8ff"  # soft purple for class names
    exception: str = "#f85149"  # bright red for exceptions
    builtin: str = "#ff7b72"  # bright red for built-in constants and functions
    number: str = "#79c0ff"  # blue for numbers
    docstring: str = "#8b949e"  # muted gray for docstrings, matching comments
    decorator: str = "#ffa657"  # orange for decorators
    instance: str = "#79c0ff"  # blue for instance references


@dataclass
class OneDarkPro:
    editor_bg: str = "#282C34"  # Background color typical for One Dark Pro
    keyword: str = "#C678DD"  # Purple, used for keywords
    function: str = "#61AFEF"  # Blue, often used for functions
    function_call: str = "#61AFEF"  # Same as function color
    string: str = "#98C379"  # Green, used for strings
    comment: str = "#5C6370"  # Grey, used for comments
    parameter: str = "#D19A66"  # Orange, used for parameters
    type_annotation: str = "#E5C07B"  # Lighter orange, for type annotations
    class_name: str = "#E5C07B"  # Same as type annotations
    exception: str = "#E06C75"  # Red, used for exceptions
    builtin: str = "#56B6C2"  # Cyan, used for builtins
    number: str = "#D19A66"  # Orange, used for numbers
    docstring: str = "#98C379"  # Green, similar to string color but used for docstrings
    decorator: str = "#C678DD"  # Purple, same as keyword
    instance: str = "#61AFEF"  # Blue, same as function


@dataclass
class AyuDark:
    editor_bg: str = "#0D1017"
    keyword: str = "#FF8F40"  # syntax.keyword
    function: str = "#FFB454"  # syntax.func (assuming function colors as func)
    function_call: str = "#FFB454"  # function call colors are the same as functions
    string: str = "#AAD94C"  # syntax.string
    comment: str = "#ACB6BF"  # syntax.comment, converted alpha value to hex
    parameter: str = "#D2A6FF"  # syntax.constant for parameters
    type_annotation: str = "#59C2FF"  # syntax.special for type annotations
    class_name: str = "#59C2FF"  # syntax.constant for class names
    exception: str = "#F07178"  # syntax.markup for exceptions
    builtin: str = "#FFB454"  # syntax.entity for builtins
    number: str = "#E6BA7E"  # syntax.constant for numbers
    docstring: str = "#BFBDB6"  # editor.fg for docstrings
    decorator: str = "#E6BA7E"  # syntax.special for decorators
    instance: str = "#FFB454"  # syntax.entity for instances


@dataclass
class AyuLight:
    editor_bg: str = "#FCFCFC"
    keyword: str = "#FA8D3E"  # Corresponds to syntax.keyword
    function: str = (
        "#F2AE49"  # Corresponds to syntax.func (assuming function colors as func)
    )
    function_call: str = (
        "#F2AE49"  # Assuming function call colors are the same as functions
    )
    string: str = "#86B300"  # Corresponds to syntax.string
    comment: str = (
        "#787B8060"  # Corresponds to syntax.comment, converted alpha value to hex
    )
    parameter: str = "#A37ACC"  # Using syntax.constant for parameters
    type_annotation: str = "#E6BA7E"  # Using syntax.special for type annotations
    class_name: str = "#A37ACC"  # Using syntax.constant for class names
    exception: str = "#F07171"  # Using syntax.markup for exceptions
    builtin: str = "#399EE6"  # Using syntax.entity for builtins
    number: str = "#A37ACC"  # Using syntax.constant for numbers
    docstring: str = "#5C6166"  # Using editor.fg for docstrings
    decorator: str = "#E6BA7E"  # Using syntax.special for decorators
    instance: str = "#399EE6"  # Using syntax.entity for instances


class Code(ft.UserControl):
    def __init__(
        self,
        language="python",
        code="",
        font="Code",
        theme=GitHubDark(),
        read_only=False,
        height=600,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.language = language
        self.code = code
        self.font = font
        self.read_only = read_only
        self.theme = theme
        self.height = height
        self.syntax_rules = {
            "python": {
                "keywords": (
                    r"\b(?P<KEYWORD>False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)\b",
                    self.theme.keyword,
                ),
                "exceptions": (
                    r"([^.'\"\\#]\b|^)(?P<EXCEPTION>ArithmeticError|AssertionError|AttributeError|BaseException|BlockingIOError|BrokenPipeError|BufferError|BytesWarning|ChildProcessError|ConnectionAbortedError|ConnectionError|ConnectionRefusedError|ConnectionResetError|DeprecationWarning|EOFError|Ellipsis|EnvironmentError|Exception|FileExistsError|FileNotFoundError|FloatingPointError|FutureWarning|GeneratorExit|IOError|ImportError|ImportWarning|IndentationError|IndexError|InterruptedError|IsADirectoryError|KeyError|KeyboardInterrupt|LookupError|MemoryError|ModuleNotFoundError|NameError|NotADirectoryError|NotImplemented|NotImplementedError|OSError|OverflowError|PendingDeprecationWarning|PermissionError|ProcessLookupError|RecursionError|ReferenceError|ResourceWarning|RuntimeError|RuntimeWarning|StopAsyncIteration|StopIteration|SyntaxError|SyntaxWarning|SystemError|SystemExit|TabError|TimeoutError|TypeError|UnboundLocalError|UnicodeDecodeError|UnicodeEncodeError|UnicodeError|UnicodeTranslateError|UnicodeWarning|UserWarning|ValueError|Warning|WindowsError|ZeroDivisionError)\b",
                    self.theme.exception,
                ),
                "builtins": (
                    r"([^.'\"\\#]\b|^)(?P<BUILTIN>abs|all|any|ascii|bin|breakpoint|callable|chr|classmethod|compile|complex|copyright|credits|delattr|dir|divmod|enumerate|eval|exec|exit|filter|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|isinstance|issubclass|iter|len|license|locals|map|max|memoryview|min|next|oct|open|ord|pow|print|quit|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|sum|type|vars|zip)\b",
                    self.theme.builtin,
                ),
                "docstrings": (
                    r"(?P<DOCSTRING>(?i:r|u|f|fr|rf|b|br|rb)?'''[^'\\]*((\\.|'(?!''))[^'\\]*)*(''')?|(?i:r|u|f|fr|rf|b|br|rb)?\"\"\"[^\"\\]*((\\.|\"(?!\"\"))[^\"\\]*)*(\"\"\")?)",
                    self.theme.docstring,
                ),
                "strings": (
                    r"(?P<STRING>(?i:r|u|f|fr|rf|b|br|rb)?'[^'\\\n]*(\\.[^'\\\n]*)*'?|(?i:r|u|f|fr|rf|b|br|rb)?\"[^\"\\\n]*(\\.[^\"\\\n]*)*\"?)",
                    self.theme.string,
                ),
                "types": (
                    r"\b(?P<TYPES>bool|bytearray|bytes|dict|float|int|list|str|tuple|object)\b",
                    self.theme.type_annotation,
                ),
                "numbers": (
                    r"\b(?P<NUMBER>((0x|0b|0o|#)[\da-fA-F]+)|((\d*\.)?\d+))\b",
                    self.theme.number,
                ),
                "function_calls": (
                    r"\b(\w+)\s*(?=\()",  # matches both standalone and dot-prefixed function calls
                    self.theme.function_call,
                ),
                "class_definitions": (
                    r"(?<=\bclass)[ \t]+(?P<CLASSDEF>\w+)[ \t]*[:\(]",  # recolor of DEFINITION for class definitions
                    self.theme.class_name,
                ),
                "decorators": (
                    r"(^[ \t]*(?P<DECORATOR>@[\w\d\.]+))",
                    self.theme.decorator,
                ),
                "instances": (
                    r"\b(?P<INSTANCE>super|self|cls)\b",
                    self.theme.instance,
                ),
                "comments": (
                    r"(?P<COMMENT>#[^\n]*)",
                    self.theme.comment,
                ),
            },
        }
        self.code_textfield = ft.TextField(
            value=None if self.read_only else self.code,
            multiline=True,
            dense=True,
            on_change=self.update_highlight,
            text_style=ft.TextStyle(
                font_family=self.font, size=14, color="transparent"
            ),
            cursor_color="#FFFFFF",
            border_color="transparent",
            bgcolor="transparent",
            width=800,
            height=self.height,
            content_padding=ft.padding.all(0),
            cursor_height=16,
            filled=True,
            expand=True,
        )

        self.code_textfield_container = ft.Container(
            content=self.code_textfield,
            padding=ft.padding.only(left=45, top=10),
            width=800,
            height=self.height,
        )

        self.code_highlight_container = ft.Container(
            content=self.apply_syntax_highlighting(
                text=self.code, language=self.language
            ),
            width=800,
            height=self.height,
            padding=ft.padding.all(5),
        )

    def apply_syntax_highlighting(self, text, language):
        rules = self.syntax_rules.get(language, {})
        formatted_lines = []
        full_lines = ft.ListView(spacing=1)

        lines = text.split("\n")
        for idx, line in enumerate(lines):
            parts = []
            last_idx = 0
            matches = []

            for element, (pattern, color) in rules.items():
                for match in re.finditer(pattern, line):
                    matches.append((match.start(), match.end(), match.group(0), color))

            matches.sort(key=lambda x: (x[0], -x[1]))

            # Improved overlap handling
            for start, end, matched_text, color in matches:
                if start >= last_idx:
                    if start > last_idx:
                        parts.append(
                            ft.Text(
                                value=line[last_idx:start],
                                style=ft.TextStyle(size=14),
                                font_family=self.font,
                            )
                        )
                    parts.append(
                        ft.Text(
                            value=matched_text,
                            style=ft.TextStyle(color=color, size=14),
                            font_family=self.font,
                        )
                    )
                    last_idx = end

            # Handle remaining text after last match
            if last_idx < len(line):
                parts.append(
                    ft.Text(
                        value=line[last_idx:],
                        style=ft.TextStyle(size=14),
                        font_family=self.font,
                    )
                )

            # Create a Row and add all parts to it without introducing new spaces
            line_number = ft.Container(ft.Text(f"{idx + 1}", color="#60676f"), width=40)
            line_widgets = ft.Row(controls=[line_number] + parts, wrap=None, spacing=0)
            formatted_lines.append(line_widgets)

        full_lines.controls.extend(formatted_lines)
        return full_lines

    def update_highlight(self, e=None):
        highlighted_code = self.apply_syntax_highlighting(
            text=self.code_textfield_container.content.value, language=self.language
        )
        self.code_highlight_container.content = highlighted_code
        self.code_highlight_container.update()

    def build(self):
        if self.read_only:
            return ft.Stack(controls=[self.code_highlight_container])
        return ft.Stack(
            controls=[self.code_highlight_container, self.code_textfield_container]
        )


def main(page: ft.Page):
    page.fonts = {
        "JetBrainsMono": "C:\\Users\\edoar\\Documents\\work\\fletmint_dev\\dev\\JetBrainsMono-Regular.ttf",
        "SourceCodePro": "/Users/edoardo/Projects/flet-lucide/SourceCodePro.ttf",
    }
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "auto"
    page.title = "Syntax Highlighting Example"

    initial_code = """
import asyncio


def showcase(a, b, /, c, d, *, e, f):
    '''Some code to showcase the syntax.'''

    @decorator(param='spam')
    async def coroutine(db:aio_db.DatabaseConnection) -> List[str]:
        r'''A coroutine.'''

        await logger.log('working\x12with %r', aio_db)

        async with db.transaction():
            result = await db.query(...)
            print(f'Result: {result!r} {a=} {b=!r}')
            print(Rf'data: {c=}')
            print(rf'data: {c=}')

    mapping = None     # type: Dict[int, Any] # PEP 484

    # a regular expression
    get_regex = lambda: re.compile(     # type: ignore
        r'''\A
            word
            (?:                         # a comment
               (?P<fill>.)?
               (?P<align>[<>=^])        (?# another comment)
            )?
            another word\.\.\.
            (?:\.(?P<precision>0|(?!0)\d+))?
        \Z''',
        re.VERBOSE | re.DOTALL)

    # NOTE Numbers with leading zeros are invalid in Python 3,
    # use 0o...
    answer = func(0xdeadbeef + 0b00100001 + 0123 + 0o123 +
                  1_005_123 +  # PEP 515
                  # complex numbers
                  .10e12 + 2j) @ mat

    # walrus operator
    filtered_data = [y for x in data if (y := f(x)) is not None]

    # position-only params
    bar = lambda q, w, /, e, r: (q + w + e + r)

    return R'''No escapes '\' in this \one'''
    """

    code_editor = Code(
        code=initial_code,
        language="python",
        font="JetBrainsMono",
        height=800,
        theme=OneDarkPro(),
        read_only=True,
    )
    page.add(code_editor)
    page.update()


ft.app(target=main)
