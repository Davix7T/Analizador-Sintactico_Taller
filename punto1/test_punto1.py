import unittest

from punto1.lexer import LexicalError
from punto1.parser_rec import ParserRec, SemanticError


class TestPunto1(unittest.TestCase):
    def test_expresiones_validas(self):
        casos = [
            ('(25.5 + 30.2) + 50', 105.7),
            ('((5.5/3) + 10) > 20 & 20.5 < 10', False),
            ('5 > 3 | 2 > 8', True),
            ('2 ^ 3 + 1', 9.0),
            ('10 / 2 * 3', 15.0),
        ]

        for expresion, esperado in casos:
            with self.subTest(expresion=expresion):
                parser = ParserRec(expresion)
                nodo = parser.parse()
                if nodo.relacional:
                    self.assertEqual(nodo.valor_logico, esperado)
                else:
                    self.assertAlmostEqual(nodo.valor, esperado)

    def test_error_semantico(self):
        casos_error = [
            '5 & 6',
            '5 > 3 & 3',
        ]

        for expresion in casos_error:
            with self.subTest(expresion=expresion):
                parser = ParserRec(expresion)
                with self.assertRaises(SemanticError) as cm:
                    parser.parse()
                self.assertIn('ERROR_SEMANTICO', str(cm.exception))


if __name__ == '__main__':
    unittest.main()
