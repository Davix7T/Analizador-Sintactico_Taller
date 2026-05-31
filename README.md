Cómo ejecutar
Ejecuta en modo interactivo:
python -m punto1.main
Luego escribe expresiones y salir para terminar.
Punto 1 (recursivo descendente


Ejecuta en modo línea de comandos:

Ejecuta en modo interactivo:

Casos válidos para probar
Punto 1
(25.5 + 30.2) + 50 → 105.7
((5.5/3) + 10) > 20 & 20.5 < 10 → False
5 > 3 | 2 > 8 → True
2 ^ 3 + 1 → 9.0
10 / 2 * 3 → 15.0
((2 + 3) ^ 2) / 5 → 5.0
Casos invalidos
Punto 1
5 & 6 → ERROR_SEMANTICO
5 > 3 & 3 → ERROR_SEMANTICO
5 > > 3 → error sintáctico
2 + → error sintáctico
5 @ 3 → error léxico
10 / 0 → ERROR_SEMANTICO: división por cero
------------------------
Punto 2 (parser con pila explícita)
como ejecutar Punto 2
python -m punto2.main
Punto 2
Casos validos
Punto 2
3 + 5 * 2
(2 + 3) ^ 2
10 / 2 - 1
4 ^ 2 * 3
(1 + 2) * (3 + 4)
--------------------------
Casos inválidos para probar
3 + * 2 → error sintáctico
(2 + 3 → error sintáctico por paréntesis faltante
2 ^ ^ 3 → error sintáctico
10 / 0 → ERROR_SEMANTICO: división por cero
5 & 3 → error léxico (no soporta &)
3 4 + → error sintáctico
