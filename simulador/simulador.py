#!/usr/bin/env python3
import argparse
import sys

from fa import simular_af
from lexer import ErroLexico, tokenizar
from pda import simular


def executar(texto, k_af=None, verboso=True):
    print(f"Entrada: {texto!r}\n")
    try:
        tokens = tokenizar(texto)
    except ErroLexico as e:
        print(f"[LÉXICO] ERRO: {e}\nResultado: REJEITADA")
        return False
    if verboso:
        print("== Análise léxica ==")
        for t in tokens:
            print(f"  {t.tipo:<14} {t.lexema!r:<10} pos={t.pos}")
        print("\n== Transições do PDA (passo | estado | entrada restante | pilha (topo à esq.) | regra) ==")
    aceita, passos, motivo = simular(tokens)
    if verboso:
        for n, est, resto, pilha, regra in passos:
            print(f"  {n:>3} | {est:<2} | {resto:<40} | {pilha:<8} | {regra}")
    print(f"\nResultado: {'ACEITA' if aceita else 'REJEITADA'} — {motivo}")
    if k_af is not None:
        ok, msg = simular_af(tokens, k_af)
        print(f"AF (k={k_af}): {'ACEITA' if ok else 'REJEITADA'} — {msg}")
    return aceita


def main():
    ap = argparse.ArgumentParser(description="Simulador léxico + autômato com pilha")
    ap.add_argument("cadeia", nargs="?", help="cadeia de entrada")
    ap.add_argument("-f", "--arquivo", help="ler a entrada de um arquivo")
    ap.add_argument("--af", type=int, metavar="K", help="comparar com AF de profundidade máxima K")
    ap.add_argument("-q", "--quieto", action="store_true", help="só o resultado")
    a = ap.parse_args()
    if a.arquivo:
        texto = open(a.arquivo, encoding="utf-8").read()
    elif a.cadeia is not None:
        texto = a.cadeia
    else:
        texto = sys.stdin.read()
    sys.exit(0 if executar(texto, a.af, not a.quieto) else 1)


if __name__ == "__main__":
    main()
