"""
Zadanie1: 17: Czy graf przedstawiający ruch skoczka na szachownicy
o wymiarach 8 × 8, z której usunięto pole a1 ma cykl Hamiltona?
"""

import pulp

# funkcje pomocnicze
def alg_name(r, c):
    return f"{chr(ord('a') + c - 1)}{r}"

def parse_coord(name):
    return int(name[1:]), ord(name[0]) - ord('a') + 1

# graf
def build_knight_graph(m, n, removed_set):
    removed = set(s.lower() for s in (removed_set or set()))
    nodes = []
    for r in range(1, m+1):
        for c in range(1, n+1):
            name = alg_name(r, c)
            if name.lower() not in removed:
                nodes.append(name)
    moves = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
    node_set = set(nodes)
    vertex = []
    for v in nodes:
        r, c = parse_coord(v)
        for dr, dc in moves:
            r2, c2 = r+dr, c+dc
            if 1 <= r2 <= m and 1 <= c2 <= n:
                w = alg_name(r2, c2)
                if w in node_set:
                    vertex.append((v, w))
    return nodes, vertex

# solve
def solve_knight_cycle(m, n, removed=set(), verbose=False, debug=False):
    nodes, vertex = build_knight_graph(m, n, removed)
    N = len(nodes)
    if N == 0:
        if debug: print("Brak dostępnych pól")
        return None
    if N == 1:
        return nodes[:]

    # problem
    prob = pulp.LpProblem("KnightHamiltonianCycle", pulp.LpMinimize)

    y = { (i,j): pulp.LpVariable(f"y_{i}_{j}", cat='Binary') for (i,j) in vertex }

    start = nodes[0]
    u = {}
    for v in nodes:
        if v == start:
            u[v] = pulp.LpVariable(f"u_{v}", lowBound=1, upBound=1, cat='Integer')
        else:
            u[v] = pulp.LpVariable(f"u_{v}", lowBound=2, upBound=N, cat='Integer')


    prob += pulp.lpSum([y[a] for a in y]), "obj"

    for v in nodes:
        prob += pulp.lpSum([ y[(i,j)] for (i,j) in vertex if i == v ]) == 1, f"outdeg_{v}"
        prob += pulp.lpSum([ y[(i,j)] for (i,j) in vertex if j == v ]) == 1, f"indeg_{v}"

    # MTZ
    # u[i] - u[j] + N * y[i,j] <= N - 1
    for (i, j) in vertex:
        if j != start and i != j:
            prob += u[i] - u[j] + N * y[(i,j)] <= N - 1, f"mtz_{i}_{j}"


    solver = pulp.PULP_CBC_CMD(msg=1 if verbose else 0)
    prob.solve(solver)

    status = pulp.LpStatus.get(prob.status, None) if hasattr(pulp, 'LpStatus') else pulp.LpStatus[prob.status]
    if debug:
        print("Status solvera:", status)

    if status not in ("Optimal", "Feasible"):
        if debug:
            print("Węzły:", nodes)
            print("Krawędzie:", vertex)
        return None

    # uzyte vertex'y
    used_vertex = [(i,j) for (i,j) in vertex if (i,j) in y and pulp.value(y[(i,j)]) is not None and round(pulp.value(y[(i,j)])) == 1]

    if debug:
        # print("Liczba krawędzi:", len(used_vertex))
        # for a in sorted(used_vertex):
        #     print(" ", a)
        print("Pola i numery ruchów:")
        for v in nodes:
            print(" ", v, pulp.value(u[v]))

    # Validate: must be N used vertex
    if len(used_vertex) != N:
        if debug: print("Walidacja: liczba użytych łuków != N")
        return None

    # rekonstrukcja cyklu
    tour = [start]
    cur = start
    visited = {start}
    for _ in range(N-1):
        nxt = None
        for (i,j) in used_vertex:
            if i == cur:
                nxt = j
                break
        if nxt is None:
            if debug: print("Rekonstrukcja nie powiodła się - brak krawędzi wychodzącej z", cur)
            return None
        tour.append(nxt)
        if nxt in visited:
            if debug: print("Powtórzenie w rekonstrukcji:", nxt)
            return None
        visited.add(nxt)
        cur = nxt

    # powrot do startu
    if (tour[-1], start) not in used_vertex:
        if debug: print("Brak krawędzi powrotnej do startu")
        return None

    # unikalnosc wierzcholkow
    if len(tour) != N or len(set(tour)) != N:
        if debug: print("Trasa nie ma N unikalnych wierzchołków")
        return None

    return tour

# testy - zmiana rozne przyklady
if __name__ == "__main__":
    tests = [
        (8, 8, {"a1"}),
        # (6, 6, {"a1", "a6"}),
        # (3, 3, {"b2"}),
        # (8, 8, set()),
    ]
    for (m, n, removed) in tests:
        print("\nWynik", m, "x", n, "przy usunięciu:", removed)
        tour = solve_knight_cycle(m, n, removed, verbose=False, debug=True)
        if tour is None:
            print("Nie znaleziono cyklu Hamiltona.\n")
        else:
            print("Znaleziono cykl Hamiltona".format(len(tour)))
            print("Trasa:")
            print(" -> ".join(tour + [tour[0]]))