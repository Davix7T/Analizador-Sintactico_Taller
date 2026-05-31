from punto1.lexer import Lexer, TokenType, LexicalError
from punto1.no_terminal import NoTerminal


class ParserError(Exception):
    pass


class SyntaxError(ParserError):
    pass


class SemanticError(ParserError):
    pass


class ParserRec:
    def __init__(self, texto):
        self.lexer = Lexer(texto)
        self.tokens = self.lexer.tokenize()
        self.pos = 0
        self.actual = self.tokens[self.pos]

    def parse(self):
        resultado = self.S()
        if self.actual.tipo != TokenType.EOF:
            self._error_sintactico(
                f"token inesperado {self.actual.valor!r}; se esperaba fin de entrada"
            )
        return resultado

    def S(self):
        # S -> ELO
        nodo = self.ELO()
        nodo.nombre = 'S'
        return nodo

    def ELO(self):
        # ELO -> EL2 ELO_L
        izquierda = self.EL2()
        return self.ELO_L(izquierda)

    def ELO_L(self, izquierda):
        # ELO_L -> | EL2 ELO_L | ε
        if self.actual.tipo == TokenType.OP_OR:
            self._consumir(TokenType.OP_OR)
            derecha = self.EL2()
            self._verificar_relacional(izquierda, derecha, '|')
            nodo = NoTerminal()
            nodo.nombre = 'ELO_L'
            nodo.valor_logico = izquierda.valor_logico or derecha.valor_logico
            nodo.relacional = True
            return self.ELO_L(nodo)

        return izquierda

    def EL2(self):
        # EL2 -> ER EL2_L
        izquierda = self.ER()
        return self.EL2_L(izquierda)

    def EL2_L(self, izquierda):
        # EL2_L -> & ER EL2_L | ε
        if self.actual.tipo == TokenType.OP_AND:
            self._consumir(TokenType.OP_AND)
            derecha = self.ER()
            self._verificar_relacional(izquierda, derecha, '&')
            nodo = NoTerminal()
            nodo.nombre = 'EL2_L'
            nodo.valor_logico = izquierda.valor_logico and derecha.valor_logico
            nodo.relacional = True
            return self.EL2_L(nodo)

        return izquierda

    def ER(self):
        # ER -> E ER_L
        izquierda = self.E()
        return self.ER_L(izquierda)

    def ER_L(self, izquierda):
        # ER_L -> OR E | ε
        if self.actual.tipo == TokenType.OP_REL:
            operador = self.OR()
            derecha = self.E()
            return self._comparar(izquierda, derecha, operador)

        return izquierda

    def OR(self):
        # OR -> < ME | > MA | = IG | ! DI
        if self.actual.tipo != TokenType.OP_REL:
            self._error_sintactico("se esperaba operador relacional")

        valor = self.actual.valor
        if valor == '<=':
            self._avanzar()
            return '<='
        if valor == '>=':
            self._avanzar()
            return '>='
        if valor == '==':
            self._avanzar()
            return self.IG()
        if valor == '!=':
            self._avanzar()
            return self.DI()
        if valor == '<':
            self._avanzar()
            return self.ME()
        if valor == '>':
            self._avanzar()
            return self.MA()
        self._error_sintactico(f"operador relacional no válido '{valor}'")

    def ME(self):
        # ME -> = | ε ; produce <= or <
        if self.actual.tipo == TokenType.OP_REL and self.actual.valor == '=':
            self._avanzar()
            return '<='
        return '<'

    def MA(self):
        # MA -> = | ε ; produce >= or >
        if self.actual.tipo == TokenType.OP_REL and self.actual.valor == '=':
            self._avanzar()
            return '>='
        return '>'

    def IG(self):
        # IG -> = ; produce ==
        if self.actual.tipo == TokenType.OP_REL and self.actual.valor == '=':
            self._avanzar()
            return '=='
        self._error_sintactico("se esperaba '=' para completar '=='")

    def DI(self):
        # DI -> = ; produce !=
        if self.actual.tipo == TokenType.OP_REL and self.actual.valor == '=':
            self._avanzar()
            return '!='
        self._error_sintactico("se esperaba '=' para completar '!='")

    def E(self):
        # E -> T E_L
        izquierda = self.T()
        return self.E_L(izquierda)

    def E_L(self, izquierda):
        # E_L -> + T E_L | - T E_L | ε
        if self.actual.tipo == TokenType.OP_SUM:
            self._consumir(TokenType.OP_SUM)
            derecha = self.T()
            nodo = NoTerminal()
            nodo.nombre = 'E_L'
            nodo.valor = izquierda.valor + derecha.valor
            nodo.relacional = False
            return self.E_L(nodo)

        if self.actual.tipo == TokenType.OP_RES:
            self._consumir(TokenType.OP_RES)
            derecha = self.T()
            nodo = NoTerminal()
            nodo.nombre = 'E_L'
            nodo.valor = izquierda.valor - derecha.valor
            nodo.relacional = False
            return self.E_L(nodo)

        return izquierda

    def T(self):
        # T -> P T_L
        izquierda = self.P()
        return self.T_L(izquierda)

    def T_L(self, izquierda):
        # T_L -> * P T_L | / P T_L | ε
        if self.actual.tipo == TokenType.OP_MUL:
            self._consumir(TokenType.OP_MUL)
            derecha = self.P()
            nodo = NoTerminal()
            nodo.nombre = 'T_L'
            nodo.valor = izquierda.valor * derecha.valor
            nodo.relacional = False
            return self.T_L(nodo)

        if self.actual.tipo == TokenType.OP_DIV:
            self._consumir(TokenType.OP_DIV)
            derecha = self.P()
            if derecha.valor == 0:
                raise SemanticError("ERROR_SEMANTICO: división por cero")
            nodo = NoTerminal()
            nodo.nombre = 'T_L'
            nodo.valor = izquierda.valor / derecha.valor
            nodo.relacional = False
            return self.T_L(nodo)

        return izquierda

    def P(self):
        # P -> F P_L
        izquierda = self.F()
        return self.P_L(izquierda)

    def P_L(self, izquierda):
        # P_L -> ^ F P_L | ε
        if self.actual.tipo == TokenType.OP_EXP:
            self._consumir(TokenType.OP_EXP)
            derecha = self.F()
            nodo = NoTerminal()
            nodo.nombre = 'P_L'
            nodo.valor = izquierda.valor ** derecha.valor
            nodo.relacional = False
            return self.P_L(nodo)

        return izquierda

    def F(self):
        # F -> ( ELO ) | I
        if self.actual.tipo == TokenType.PAREN_IZQ:
            self._consumir(TokenType.PAREN_IZQ)
            nodo = self.ELO()
            self._consumir(TokenType.PAREN_DER)
            return nodo

        return self.I()

    def I(self):
        # I -> identificador o número
        if self.actual.tipo == TokenType.NUMERO:
            nodo = NoTerminal()
            nodo.nombre = 'I'
            nodo.valor = float(self.actual.valor)
            nodo.relacional = False
            self._avanzar()
            return nodo

        if self.actual.tipo == TokenType.ID:
            nodo = NoTerminal()
            nodo.nombre = 'I'
            nodo.valor = 0.0
            nodo.relacional = False
            self._avanzar()
            return nodo

        self._error_sintactico("se esperaba número o identificador")

    def _comparar(self, izquierda, derecha, operador):
        if izquierda.relacional or derecha.relacional:
            raise SemanticError(
                "ERROR_SEMANTICO: comparación sobre expresiones no aritméticas"
            )

        if operador == '<':
            valor_logico = izquierda.valor < derecha.valor
        elif operador == '<=':
            valor_logico = izquierda.valor <= derecha.valor
        elif operador == '>':
            valor_logico = izquierda.valor > derecha.valor
        elif operador == '>=':
            valor_logico = izquierda.valor >= derecha.valor
        elif operador == '==':
            valor_logico = izquierda.valor == derecha.valor
        elif operador == '!=':
            valor_logico = izquierda.valor != derecha.valor
        else:
            self._error_sintactico(f"operador de comparación desconocido '{operador}'")

        nodo = NoTerminal()
        nodo.nombre = 'ER_L'
        nodo.valor_logico = valor_logico
        nodo.relacional = True
        return nodo

    def _verificar_relacional(self, izquierda, derecha, operador):
        if not izquierda.relacional or not derecha.relacional:
            raise SemanticError(
                f"ERROR_SEMANTICO: operando de '{operador}' no es relacional"
            )

    def _consumir(self, tipo_esperado):
        if self.actual.tipo == tipo_esperado:
            self._avanzar()
            return
        self._error_sintactico(
            f"token inesperado {self.actual.valor!r}; se esperaba {tipo_esperado.name}"
        )

    def _avanzar(self):
        if self.pos + 1 < len(self.tokens):
            self.pos += 1
            self.actual = self.tokens[self.pos]

    def _error_sintactico(self, mensaje):
        raise SyntaxError(
            f"ERROR_SINTACTICO en fila {self.actual.fila}, columna {self.actual.columna}: {mensaje}"
        )
