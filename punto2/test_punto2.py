import unittest

from punto2.parser_pila import ParserPila


class TestPunto2(unittest.TestCase):
    def test_expresiones_validas(self):
        casos = [
            ('3 + 5 * 2', 13.0, '(3 + (5 * 2))', '3 5 2 * +', '+ 3 * 5 2'),
            ('(2 + 3) ^ 2', 25.0, '((2 + 3) ^ 2)', '2 3 + 2 ^', '^ + 2 3 2'),
            ('10 / 2 - 1', 4.0, '((10 / 2) - 1)', '10 2 / 1 -', '- / 10 2 1'),
        ]

        for expresion, valor_esperado, infija_esperada, postfija_esperada, prefija_esperada in casos:
            with self.subTest(expresion=expresion):
                parser = ParserPila(expresion)
                item = parser.parse()
                self.assertAlmostEqual(item.valor, valor_esperado)
                self.assertEqual(item.infija, infija_esperada)
                self.assertEqual(item.postfija, postfija_esperada)
                self.assertEqual(item.prefija, prefija_esperada)


if __name__ == '__main__':
    unittest.main()
