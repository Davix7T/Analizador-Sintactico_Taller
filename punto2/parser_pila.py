from punto2.lexer import Lexer, TokenType, LexicalError
from punto2.tabla_control import get_action
from punto2.acciones import SemanticItem, resultado, suma, resta, mul, div, exp, SemanticError


class ParserError(Exception):
    pass


class SyntaxError(ParserError):
    pass


class ParserPila:
    def __init__(self, texto):
        self.lexer = Lexer(texto)
        self.tokens = self.lexer.tokenize()
        self.pos = 0
        self.actual = self.tokens[self.pos]
        self.pila = ['Z0', 'S']
        self.pila_semantica = []

    def parse(self):
        while self.pila:
            cima = self.pila[-1]

            if cima == 'Z0':
                if self.actual.tipo == TokenType.EOF:
                    self.pila.pop()
                    break
                self._error_sintactico('se esperaba fin de entrada')

            if cima in {'resultado', 'suma', 'resta', 'mul', 'div', 'exp'}:
                self.pila.pop()
                self._ejecutar_accion(cima)
                continue

            if cima == 'I':
                if self.actual.tipo in {TokenType.NUMERO, TokenType.ID}:
                    self.pila.pop()
                    self._push_identificador_o_numero(self.actual)
                    self._avanzar()
                    continue
                self._error_sintactico('se esperaba identificador o número')

            if self._es_terminal(cima):
                if self._coincide_terminal(cima, self.actual):
                    self.pila.pop()
                    self._avanzar()
                    continue
                self._error_sintactico(
                    f"token inesperado {self.actual.valor!r}; se esperaba '{cima}'"
                )

            accion = get_action(cima, self.actual)
            if accion is None:
                self._error_sintactico(
                    f"no hay acción de tabla para el no terminal '{cima}' y token '{self.actual.valor}'"
                )

            self.pila.pop()
            for simbolo in accion:
                self.pila.append(simbolo)

        if self.actual.tipo != TokenType.EOF:
            self._error_sintactico('entrada no consumida al final del análisis')

        if len(self.pila_semantica) != 1:
            raise SemanticError('ERROR_SEMANTICO: pila semántica inválida al finalizar')

        return self.pila_semantica[0]

    def _avanzar(self):
        if self.pos + 1 < len(self.tokens):
            self.pos += 1
            self.actual = self.tokens[self.pos]

    def _push_identificador_o_numero(self, token):
        if token.tipo == TokenType.NUMERO:
            valor = float(token.valor)
        else:
            valor = 0.0

        self.pila_semantica.append(
            SemanticItem(
                valor=valor,
                infija=token.valor,
                postfija=token.valor,
                prefija=token.valor,
            )
        )

    def _ejecutar_accion(self, nombre):
        if nombre == 'resultado':
            resultado(self.pila_semantica)
        elif nombre == 'suma':
            suma(self.pila_semantica)
        elif nombre == 'resta':
            resta(self.pila_semantica)
        elif nombre == 'mul':
            mul(self.pila_semantica)
        elif nombre == 'div':
            div(self.pila_semantica)
        elif nombre == 'exp':
            exp(self.pila_semantica)
        else:
            raise SemanticError(f'ERROR_SEMANTICO: acción desconocida {nombre}')

    def _es_terminal(self, simbolo):
        return simbolo in {'+', '-', '*', '/', '^', '(', ')'}

    def _coincide_terminal(self, simbolo, token):
        if simbolo == '+':
            return token.tipo == TokenType.OP_SUM
        if simbolo == '-':
            return token.tipo == TokenType.OP_RES
        if simbolo == '*':
            return token.tipo == TokenType.OP_MUL
        if simbolo == '/':
            return token.tipo == TokenType.OP_DIV
        if simbolo == '^':
            return token.tipo == TokenType.OP_EXP
        if simbolo == '(':
            return token.tipo == TokenType.PAREN_IZQ
        if simbolo == ')':
            return token.tipo == TokenType.PAREN_DER
        return False

    def _error_sintactico(self, mensaje):
        raise SyntaxError(
            f"ERROR_SINTACTICO en fila {self.actual.fila}, columna {self.actual.columna}: {mensaje}"
        )
