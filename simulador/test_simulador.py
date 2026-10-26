import unittest

from fa import simular_af
from lexer import ErroLexico, tokenizar
from pda import simular

VALIDAS = [
    "",
    "()",
    "{}",
    "[]",
    "(())",
    "()[]{}",
    "{[()]}",
    "if (a == 1) { b[0] = f(x, y); }",
    "while (x < 10) { if (x % 2) { x = x + 1; } }",
    "int a = 3; // (comentário com ( desbalanceado",
    '"(" + x',
]
INVALIDAS = [
    "(",
    ")",
    "(()",
    "())",
    "([)]",
    "{(})",
    "}{",
    "if (a { b; )",
    "f(x))",
    "{ while (1) { x = 1; }",
]


def pda(texto):
    return simular(tokenizar(texto))[0]


class TestPDA(unittest.TestCase):
    def test_validas(self):
        for s in VALIDAS:
            with self.subTest(s=s):
                self.assertTrue(pda(s))

    def test_invalidas(self):
        for s in INVALIDAS:
            with self.subTest(s=s):
                self.assertFalse(pda(s))

    def test_profundidade_grande(self):
        self.assertTrue(pda("(" * 5000 + ")" * 5000))
        self.assertFalse(pda("(" * 5000 + ")" * 4999))


class TestLexer(unittest.TestCase):
    def test_tokens(self):
        tipos = [t.tipo for t in tokenizar("if (x1 >= 3.5) { y = 2; }")]
        self.assertEqual(tipos[:6], ["PALAVRA_CHAVE", "LPAREN", "ID", "OP", "NUM", "RPAREN"])

    def test_erro_lexico(self):
        with self.assertRaises(ErroLexico):
            tokenizar("a = 1 @ 2")


class TestAFvsPDA(unittest.TestCase):
    def test_af_limitado(self):
        toks = tokenizar("((()))")
        self.assertTrue(simular_af(toks, 3)[0])
        self.assertFalse(simular_af(toks, 2)[0])
        self.assertTrue(simular(toks)[0])

    def test_af_concorda_dentro_do_limite(self):
        for s in VALIDAS + INVALIDAS:
            toks = tokenizar(s)
            if len(s) <= 12:
                self.assertEqual(simular_af(toks, 12)[0], simular(toks)[0], s)


if __name__ == "__main__":
    unittest.main()
