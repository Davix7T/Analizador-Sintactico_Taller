import sys

from punto1.lexer import Lexer, LexicalError
from punto1.parser_rec import ParserRec, ParserError


def evaluar_expresion(texto):
    try:
        parser = ParserRec(texto)
        nodo = parser.parse()
        if nodo.relacional:
            return str(nodo.valor_logico)
        return str(nodo.valor)
    except LexicalError as error:
        return str(error)
    except ParserError as error:
        return str(error)


def interactivo():
    print("Analizador descendente Punto 1 (escriba 'salir' para terminar)")
    while True:
        entrada = input('> ').strip()
        if entrada.lower() == 'salir':
            break
        if not entrada:
            continue
        print(evaluar_expresion(entrada))


def main():
    if len(sys.argv) == 2:
        expresion = sys.argv[1]
        print(evaluar_expresion(expresion))
        return
    interactivo()


if __name__ == '__main__':
    main()
