import hypothesis.strategies

NONE = hypothesis.strategies.none()
BOOLEAN = hypothesis.strategies.booleans()
TEXT = hypothesis.strategies.text()
INTEGER = hypothesis.strategies.integers()
FLOAT = hypothesis.strategies.floats(allow_nan=False, allow_infinity=False)
LITERAL = hypothesis.strategies.one_of(NONE, BOOLEAN, TEXT, INTEGER, FLOAT)

LIST = hypothesis.strategies.lists(LITERAL)
DICTIONARY = hypothesis.strategies.dictionaries(keys=TEXT, values=LITERAL)
STRUCTURE = hypothesis.strategies.one_of(LIST, DICTIONARY)

DATA = hypothesis.strategies.recursive(
    base=hypothesis.strategies.one_of(LITERAL, STRUCTURE),
    extend=lambda children: hypothesis.strategies.one_of(
        hypothesis.strategies.lists(children),
        hypothesis.strategies.dictionaries(keys=TEXT, values=children),
    ),
    max_leaves=16,
)
CONFIG = hypothesis.strategies.recursive(
    base=DICTIONARY,
    extend=lambda children: hypothesis.strategies.dictionaries(
        keys=TEXT,
        values=children,
    ),
    max_leaves=16,
)

WORD = hypothesis.strategies.from_regex(r'^[^\W\d_]\w{0,31}(?!\n)$')
