from enum import Enum, auto


class TokenType(Enum):
    NUMERO = auto()
    ID = auto()
    OP_OR = auto()
    OP_AND = auto()
    OP_REL = auto()
    OP_SUM = auto()
    OP_RES = auto()
    OP_MUL = auto()
    OP_DIV = auto()
    OP_EXP = auto()
    PAREN_IZQ = auto()
    PAREN_DER = auto()
    EOF = auto()


class Token:
    def __init__(self, tipo, valor, fila, columna):
        self.tipo = tipo
        self.valor = valor
        self.fila = fila
        self.columna = columna

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor!r}, {self.fila}, {self.columna})"


class LexicalError(Exception):
    pass


class Lexer:
    def __init__(self, texto):
        self.texto = texto
        self.pos = 0
        self.fila = 1
        self.columna = 1
        self.tokens = []
        self.prev_token_type = None

    def tokenize(self):
        while self.pos < len(self.texto):
            caracter = self.texto[self.pos]

            if caracter.isspace():
                self._avanzar_caracter()
                continue

            if caracter == '|' :
                self._agregar_token(TokenType.OP_OR, caracter)
                self._avanzar_caracter()
                continue

            if caracter == '&':
                self._agregar_token(TokenType.OP_AND, caracter)
                self._avanzar_caracter()
                continue

            if caracter in '+*^/()':
                token_map = {
                    '+': TokenType.OP_SUM,
                    '*': TokenType.OP_MUL,
                    '^': TokenType.OP_EXP,
                    '/': TokenType.OP_DIV,
                    '(': TokenType.PAREN_IZQ,
                    ')': TokenType.PAREN_DER,
                }
                self._agregar_token(token_map[caracter], caracter)
                self._avanzar_caracter()
                continue

            if caracter in '<>!=':
                self._leer_operador_relacional()
                continue

            if caracter == '-':
                if self._es_inicio_numero_negativo():
                    self._leer_numero()
                else:
                    self._agregar_token(TokenType.OP_RES, caracter)
                    self._avanzar_caracter()
                continue

            if caracter.isdigit() or caracter == '.':
                self._leer_numero()
                continue

            if caracter.isalpha() or caracter == '_':
                self._leer_identificador()
                continue

            raise LexicalError(
                f"ERROR_LEXICO: caracter no reconocido '{caracter}' en fila {self.fila}, columna {self.columna}"
            )

        self._agregar_token(TokenType.EOF, '~')
        return self.tokens

    def _leer_operador_relacional(self):
        inicio = self.texto[self.pos]
        siguiente = self._peek_caracter()
        if siguiente == '=':
            operador = inicio + siguiente
            self._agregar_token(TokenType.OP_REL, operador)
            self._avanzar_caracter()
            self._avanzar_caracter()
            return

        self._agregar_token(TokenType.OP_REL, inicio)
        self._avanzar_caracter()

    def _es_inicio_numero_negativo(self):
        siguiente = self._peek_caracter()
        if siguiente is None or not siguiente.isdigit():
            return False
        return self.prev_token_type in {
            None,
            TokenType.OP_OR,
            TokenType.OP_AND,
            TokenType.OP_REL,
            TokenType.OP_SUM,
            TokenType.OP_RES,
            TokenType.OP_MUL,
            TokenType.OP_DIV,
            TokenType.OP_EXP,
            TokenType.PAREN_IZQ,
        }

    def _leer_numero(self):
        inicio_columna = self.columna
        numero = ''
        puntos = 0

        if self.texto[self.pos] == '-':
            numero += '-'
            self._avanzar_caracter()

        while self.pos < len(self.texto):
            caracter = self.texto[self.pos]
            if caracter.isdigit():
                numero += caracter
                self._avanzar_caracter()
                continue

            if caracter == '.':
                if puntos == 1:
                    break
                puntos += 1
                numero += caracter
                self._avanzar_caracter()
                continue

            break

        if numero == '-' or numero == '' or numero == '.':
            raise LexicalError(
                f"ERROR_LEXICO: número mal formado en fila {self.fila}, columna {inicio_columna}"
            )

        self._agregar_token(TokenType.NUMERO, numero, fila=self.fila, columna=inicio_columna)

    def _leer_identificador(self):
        inicio_columna = self.columna
        nombre = ''
        while self.pos < len(self.texto):
            caracter = self.texto[self.pos]
            if caracter.isalnum() or caracter == '_':
                nombre += caracter
                self._avanzar_caracter()
                continue
            break

        self._agregar_token(TokenType.ID, nombre, fila=self.fila, columna=inicio_columna)

    def _agregar_token(self, tipo, valor, fila=None, columna=None):
        fila = fila if fila is not None else self.fila
        columna = columna if columna is not None else self.columna
        token = Token(tipo, valor, fila, columna)
        self.tokens.append(token)
        self.prev_token_type = tipo

    def _peek_caracter(self):
        siguiente_pos = self.pos + 1
        if siguiente_pos >= len(self.texto):
            return None
        return self.texto[siguiente_pos]

    def _avanzar_caracter(self):
        if self.pos < len(self.texto) and self.texto[self.pos] == '\n':
            self.fila += 1
            self.columna = 1
        else:
            self.columna += 1
        self.pos += 1
