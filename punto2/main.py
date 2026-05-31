import sys

from punto2.lexer import Lexer, LexicalError
from punto2.parser_pila import ParserPila, ParserError


def procesar_expresion(texto):
    try:
        parser = ParserPila(texto)
        item = parser.parse()
        salida = [
            f"Resultado : {item.valor}",
            f"Infija    : {item.infija}",
            f"Postfija  : {item.postfija}",
            f"Prefija   : {item.prefija}",
        ]
        return '\n'.join(salida)
    except LexicalError as error:
        return str(error)
    except ParserError as error:
        return str(error)


def interactivo():
    print("Analizador de pila Punto 2 (escriba 'salir' para terminar)")
    while True:
        entrada = input('> ').strip()
        if entrada.lower() == 'salir':
            break
        if not entrada:
            continue
        print(procesar_expresion(entrada))


def main():
    if len(sys.argv) == 2:
        print(procesar_expresion(sys.argv[1]))
        return
    interactivo()


if __name__ == '__main__':
    main()
