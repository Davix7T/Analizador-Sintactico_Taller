from dataclasses import dataclass


@dataclass
class SemanticItem:
    valor: float
    infija: str
    postfija: str
    prefija: str


class SemanticError(Exception):
    pass


def _aplicar_binaria(pila, operador, operador_infija, operador_postfija, operador_prefija):
    if len(pila) < 2:
        raise SemanticError('ERROR_SEMANTICO: pila semántica incompleta para operación')

    derecha = pila.pop()
    izquierda = pila.pop()
    if operador == 'div' and derecha.valor == 0:
        raise SemanticError('ERROR_SEMANTICO: división por cero')

    if operador == 'suma':
        valor = izquierda.valor + derecha.valor
    elif operador == 'resta':
        valor = izquierda.valor - derecha.valor
    elif operador == 'mul':
        valor = izquierda.valor * derecha.valor
    elif operador == 'div':
        valor = izquierda.valor / derecha.valor
    elif operador == 'exp':
        valor = izquierda.valor ** derecha.valor
    else:
        raise SemanticError(f'ERROR_SEMANTICO: operador desconocido {operador}')

    pila.append(
        SemanticItem(
            valor=valor,
            infija=f"({izquierda.infija} {operador_infija} {derecha.infija})",
            postfija=f"{izquierda.postfija} {derecha.postfija} {operador_postfija}",
            prefija=f"{operador_prefija} {izquierda.prefija} {derecha.prefija}",
        )
    )


def resultado(pila):
    if len(pila) != 1:
        raise SemanticError('ERROR_SEMANTICO: resultado no pudo obtenerse')


def suma(pila):
    _aplicar_binaria(pila, 'suma', '+', '+', '+')


def resta(pila):
    _aplicar_binaria(pila, 'resta', '-', '-', '-')


def mul(pila):
    _aplicar_binaria(pila, 'mul', '*', '*', '*')


def div(pila):
    _aplicar_binaria(pila, 'div', '/', '/', '/')


def exp(pila):
    _aplicar_binaria(pila, 'exp', '^', '^', '^')
