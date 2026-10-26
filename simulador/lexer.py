import re
from collections import namedtuple

Token = namedtuple("Token", "tipo lexema pos")

ESPECIFICACAO = [
    ("ESPACO", r"[ \t\r\n]+"),
    ("COMENTARIO", r"//[^\n]*"),
    ("PALAVRA_CHAVE", r"(?:if|else|while|for|return|int|float|void)\b"),
    ("NUM", r"\d+(?:\.\d+)?"),
    ("ID", r"[A-Za-z_]\w*"),
    ("STRING", r'"[^"\n]*"'),
    ("OP", r"==|!=|<=|>=|&&|\|\||[+\-*/%=<>!]"),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("LBRACK", r"\["),
    ("RBRACK", r"\]"),
    ("PONTUACAO", r"[;,]"),
]
IGNORADOS = {"ESPACO", "COMENTARIO"}
_REGEX = re.compile("|".join(f"(?P<{n}>{p})" for n, p in ESPECIFICACAO))


class ErroLexico(Exception):
    def __init__(self, caractere, pos):
        super().__init__(f"caractere inválido {caractere!r} na posição {pos}")
        self.caractere, self.pos = caractere, pos


def tokenizar(texto):
    tokens, pos = [], 0
    while pos < len(texto):
        m = _REGEX.match(texto, pos)
        if not m:
            raise ErroLexico(texto[pos], pos)
        if m.lastgroup not in IGNORADOS:
            tokens.append(Token(m.lastgroup, m.group(), pos))
        pos = m.end()
    return tokens
