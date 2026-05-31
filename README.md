# README

# Punto 1 - Parser Recursivo Descendente

## Cómo ejecutar

```bash
python -m punto1.main
```

Luego escribe expresiones en modo interactivo.

Escribe:

```text
salir
```

para terminar la ejecución.

---

## Casos válidos para probar

```text
(25.5 + 30.2) + 50
→ 105.7

((5.5/3) + 10) > 20 & 20.5 < 10
→ False

5 > 3 | 2 > 8
→ True

2 ^ 3 + 1
→ 9.0

10 / 2 * 3
→ 15.0

((2 + 3) ^ 2) / 5
→ 5.0
```

---

## Casos inválidos para probar

```text
5 & 6
→ ERROR_SEMANTICO

5 > 3 & 3
→ ERROR_SEMANTICO

5 > > 3
→ Error sintáctico

2 +
→ Error sintáctico

5 @ 3
→ Error léxico

10 / 0
→ ERROR_SEMANTICO: división por cero
```

---

# Punto 2 - Parser con Pila Explícita

## Cómo ejecutar

```bash
python -m punto2.main
```

---

## Casos válidos para probar

```text
3 + 5 * 2

(2 + 3) ^ 2

10 / 2 - 1

4 ^ 2 * 3

(1 + 2) * (3 + 4)
```

---

## Casos inválidos para probar

```text
3 + * 2
→ Error sintáctico

(2 + 3
→ Error sintáctico por paréntesis faltante

2 ^ ^ 3
→ Error sintáctico

10 / 0
→ ERROR_SEMANTICO: división por cero

5 & 3
→ Error léxico (no soporta &)

3 4 +
→ Error sintáctico
```

