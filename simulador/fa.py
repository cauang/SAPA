from pda import ABRE, FECHA, classe


def simular_af(tokens, k):
    estado = ""
    estados_visitados = {estado}
    for t in tokens:
        c = classe(t.tipo)
        if c in ABRE:
            if len(estado) == k:
                return False, f"estouro: profundidade {k + 1} exige estado inexistente no AF (k={k})"
            estado += ABRE[c]
        elif c in FECHA:
            if not estado or estado[-1] != FECHA[c]:
                return False, "delimitador de fechamento inválido"
            estado = estado[:-1]
        estados_visitados.add(estado)
    return (estado == ""), ("aceita" if estado == "" else "delimitadores não fechados")


def numero_de_estados(k):
    return sum(3 ** i for i in range(k + 1)) + 1
