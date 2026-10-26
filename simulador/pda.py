ABRE = {"LPAREN": "P", "LBRACE": "C", "LBRACK": "B"}
FECHA = {"RPAREN": "P", "RBRACE": "C", "RBRACK": "B"}
EPS = "ε"


def construir_delta():
    delta = {}
    for topo in "ZPCB":
        for ent, simb in ABRE.items():
            delta[("q0", ent, topo)] = ("q0", simb + topo)
        delta[("q0", "OUTRO", topo)] = ("q0", topo)
    for ent, simb in FECHA.items():
        delta[("q0", ent, simb)] = ("q0", "")
    delta[("q0", EPS, "Z")] = ("qf", "Z")
    return delta


DELTA = construir_delta()


def classe(tipo):
    return tipo if tipo in ABRE or tipo in FECHA else "OUTRO"


def simular(tokens):
    entrada = [classe(t.tipo) for t in tokens]
    estado, pilha, passos = "q0", ["Z"], []

    def registra(i, regra):
        passos.append((len(passos), estado, " ".join(entrada[i:]) or EPS,
                       "".join(reversed(pilha)), regra))

    registra(0, "configuração inicial")
    for i, ent in enumerate(entrada):
        topo = pilha[-1]
        chave = ("q0", ent, topo)
        if chave not in DELTA:
            lex = tokens[i]
            motivo = (f"sem transição δ(q0, {ent}, {topo}): "
                      + (f"'{lex.lexema}' (pos {lex.pos}) sem abertura correspondente"
                         if topo == "Z" else
                         f"'{lex.lexema}' (pos {lex.pos}) não fecha o delimitador aberto"))
            return False, passos, motivo
        estado, push = DELTA[chave]
        pilha.pop()
        pilha.extend(reversed(push))
        registra(i + 1, f"δ(q0,{ent},{topo}) = (q0,{push or EPS})")
    topo = pilha[-1]
    if ("q0", EPS, topo) in DELTA:
        estado, _ = DELTA[("q0", EPS, topo)]
        registra(len(entrada), f"δ(q0,ε,Z) = (qf,Z)")
        return True, passos, "entrada consumida, pilha vazia, estado final"
    return False, passos, f"entrada consumida mas {len(pilha) - 1} delimitador(es) não fechado(s)"
