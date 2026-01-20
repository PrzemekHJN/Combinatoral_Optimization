from pysat.examples.rc2 import RC2
from pysat.formula import WCNF


def read_data(filename):
    """
    Funkcja wczytuje dane z pliku zbior.txt - dolaczony

    Tu przykladowy format:
        S = 0 1 2 3 4
        C =
        0 1
        1 2 3
        3 4
    """
    S = []
    C = []

    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    # wczytanie zbioru S
    if not lines[0].startswith("S"):
        raise ValueError("Pierwsza linia musi mieć postać: S = ...")

    S = list(map(int, lines[0].split("=")[1].split()))

    # wczytanie rodziny C (podzbiory zbioru S)
    start = None
    for i, line in enumerate(lines):
        if line.startswith("C"):
            start = i + 1
            break

    if start is None:
        raise ValueError("Brak sekcji C =")

    for line in lines[start:]:
        subset = list(map(int, line.split()))
        C.append(subset)

    return S, C


def min_s_prim(S, C):
    var = lambda i: i + 1

    wcnf = WCNF()

    # kazdy zbior z rodziny C musi byc przeciety
    for subset in C:
        wcnf.append([var(i) for i in subset])

    # minimalizacja elementów w S'
    for i in S:
        wcnf.append([-var(i)], weight=1)

    solver = RC2(wcnf)
    model = solver.compute()

    S_prime = [i for i in S if model[var(i) - 1] > 0]
    return S_prime


if __name__ == "__main__":
    filename = "zbior.txt"

    S, C = read_data(filename)

    print("Zbiór S =", S)
    print("Rodzina C =", C)

    result = min_s_prim(S, C)

    print("\nMinimalny S' =", result)
