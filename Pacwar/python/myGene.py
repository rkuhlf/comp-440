import random
import numpy as np
import _PyPacwar

GENE_LEN = 50
ALLELES = (0, 1, 2, 3)


def random_gene() -> list[int]:
    return [random.choice(ALLELES) for _ in range(GENE_LEN)]


def duel_points(rounds: int, c_me: int, c_opp: int) -> int:
    # elimination cases
    if c_opp == 0 and c_me > 0:
        if rounds < 100:
            return 20
        if rounds < 200:
            return 19
        if rounds < 300:
            return 18
        return 17

    if c_me == 0 and c_opp > 0:
        if rounds < 100:
            return 0
        if rounds < 200:
            return 1
        if rounds < 300:
            return 2
        return 3

    # no elimination by 500, use ratio buckets
    if c_opp == 0:
        return 13
    if c_me == 0:
        return 7

    ratio = c_me / c_opp

    if ratio >= 10.0:
        return 13
    if ratio >= 3.0:
        return 12
    if ratio >= 1.5:
        return 11
    if ratio <= 1.0 / 10.0:
        return 7
    if ratio <= 1.0 / 3.0:
        return 8
    if ratio <= 1.0 / 1.5:
        return 9
    return 10


def score_once(me: list[int], opp: list[int]) -> float:
    rounds, c_me, c_opp = _PyPacwar.battle(me, opp)
    pts = duel_points(rounds, c_me, c_opp)
    # no ties
    return pts + 1e-2 * (c_me - c_opp) 


def evaluate(me: list[int], opponents: list[list[int]]) -> float:
    return float(np.mean([score_once(me, o) for o in opponents]))


def mutate_gene(g: list[int]) -> list[int]:
    i = random.randrange(GENE_LEN)
    cur = g[i]
    new_val = random.choice([a for a in ALLELES if a != cur])
    ng = g.copy()
    ng[i] = new_val
    return ng


def hill_climb(me0: list[int], opponents: list[list[int]], steps: int = 200, samples_per_step: int = 200):
    me = me0.copy()
    best = evaluate(me, opponents)

    for _ in range(steps):
        improved = False
        best_neighbor = me
        best_neighbor_val = best

        for _ in range(samples_per_step):
            cand = mutate_gene(me)
            v = evaluate(cand, opponents)
            if v > best_neighbor_val:
                best_neighbor = cand
                best_neighbor_val = v
                improved = True

        if not improved:
            break

        me = best_neighbor
        best = best_neighbor_val

    return me, best


def random_restarts_hc(
    restarts: int = 40,
    steps: int = 150,
    samples_per_step: int = 250,
    seed: int | None = 0,
):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    opponents = [
        [0] * 50,
        [1] * 50,
        [2] * 50,
        [3] * 50,
        ([0, 1, 2, 3] * 12) + [0, 1],
    ]
    opponents += [random_gene() for _ in range(10)]

    global_best = None
    global_best_val = float("-inf")

    for r in range(restarts):
        start = random_gene()
        g, v = hill_climb(start, opponents, steps=steps, samples_per_step=samples_per_step)
        if v > global_best_val:
            global_best = g
            global_best_val = v

    return global_best, global_best_val