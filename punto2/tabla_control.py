from punto2.lexer import TokenType


def token_col(token):
    if token.tipo in {TokenType.NUMERO, TokenType.ID}:
        return 'i'
    if token.tipo == TokenType.OP_SUM:
        return '+'
    if token.tipo == TokenType.OP_RES:
        return '-'
    if token.tipo == TokenType.OP_MUL:
        return '*'
    if token.tipo == TokenType.OP_DIV:
        return '/'
    if token.tipo == TokenType.OP_EXP:
        return '^'
    if token.tipo == TokenType.PAREN_IZQ:
        return '('
    if token.tipo == TokenType.PAREN_DER:
        return ')'
    if token.tipo == TokenType.EOF:
        return '~'
    return None


ACTION_TABLE = {
    'S': {
        'i': ['resultado', 'E'],
        '(': ['resultado', 'E'],
    },
    'E': {
        'i': ['E_L', 'T'],
        '(': ['E_L', 'T'],
    },
    'E_L': {
        '+': ['E_L', 'suma', 'T', '+'],
        '-': ['E_L', 'resta', 'T', '-'],
        ')': [],
        '~': [],
    },
    'T': {
        'i': ['T_L', 'P'],
        '(': ['T_L', 'P'],
    },
    'T_L': {
        '+': [],
        '-': [],
        '*': ['T_L', 'mul', 'P', '*'],
        '/': ['T_L', 'div', 'P', '/'],
        ')': [],
        '~': [],
    },
    'P': {
        'i': ['P_L', 'F'],
        '(': ['P_L', 'F'],
    },
    'P_L': {
        '+': [],
        '-': [],
        '*': [],
        '/': [],
        '^': ['P_L', 'exp', 'F', '^'],
        '(': [],
        ')': [],
        '~': [],
    },
    'F': {
        '(': [')', 'E', '('],
        'i': ['I'],
    },
}


def get_action(simbolo, token):
    columna = token_col(token)
    if columna is None:
        return None
    return ACTION_TABLE.get(simbolo, {}).get(columna)
