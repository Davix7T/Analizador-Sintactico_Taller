class NoTerminal:
    def __init__(self):
        self.nombre = ""           # nombre del no-terminal
        self.valor = 0.0            # valor numérico calculado
        self.valor_logico = None    # True / False si es expresión relacional/lógica
        self.relacional = False     # True si el resultado es producto de una comparación

    def __repr__(self):
        return (
            f"NoTerminal(nombre={self.nombre!r}, valor={self.valor}, "
            f"valor_logico={self.valor_logico}, relacional={self.relacional})"
        )
