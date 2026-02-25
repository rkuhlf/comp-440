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


def strong_parent(population: list[list[int]], scores: list[float], k: int) -> list[int]:
    possible_parents = random.sample(range(len(population)), k)
    best_idx = possible_parents[np.argmax([scores[i] for i in possible_parents])]
    return population[best_idx]

def score_once(me: list[int], opp: list[int]) -> float:
    rounds, c_me, c_opp = _PyPacwar.battle(me, opp)
    pts = duel_points(rounds, c_me, c_opp)
    # no ties
    return pts + 1e-2 * (c_me - c_opp) 


def evaluate(me: list[int], opponents: list[list[int]]) -> float:
    return float(np.mean([score_once(me, o) for o in opponents]))

def crossover(p1: list[int], p2: list[int]):
    split_idx= random.randint(1, GENE_LEN - 1)
    return p1[:split_idx] + p2[split_idx:]

def mutate(gene: list[int], mutation_rate: float):
    for i in range(len(gene)):
        if random.random() < mutation_rate:
            gene[i] = random.choice([a for a in ALLELES if a != gene[i]])

baseline_opponents = [
    [0] * 50,
    [1] * 50,
    [2] * 50,
    [3] * 50,
]
def genetic_algorithm(n: int, generations: int, opponents: list[list[int]],
                      mutation_rate = 0.1, survival_rate = 0.05, selection_k = 5, initial_k = 5):
    population = [random_gene() for _ in range(n)]
    result_gene = None
    result_score = float('-inf')
    
    for gen in range(generations):
        scores = []
        for gen_code in population:
            curr_opponents = random.sample(population, initial_k) + baseline_opponents
            scores.append(evaluate(gen_code, curr_opponents))
            
        best_gene = population[np.argmax(scores)]  
        best_score = max(scores)
        if best_score > result_score:
            result_score = best_score
            result_gene = best_gene.copy()
            
        new_population = []
        num_survivors = max(1, int(n * survival_rate))
        top_indices = np.argsort(scores)[::-1][:num_survivors]
        # Fill new population with survivors
        for i in top_indices:
            new_population.append(population[i].copy())
        
        while len(new_population) < n:
            p1 = strong_parent(population, scores, selection_k)
            p2 = strong_parent(population, scores, selection_k)
            
            child = crossover(p1, p2)
            mutate(child, mutation_rate)
            new_population.append(child)
            
        population = new_population
        
    return result_gene, result_score


if __name__ == "__main__":

    best_gene, best_score = genetic_algorithm(
        n=100, 
        generations=50, 
        opponents=[],
        mutation_rate=0.1, 
        survival_rate=0.05, 
        selection_k=5, 
        initial_k=5
    )
    
    print("\n=== EVOLUTION COMPLETE ===")
    print(f"Top Score: {best_score:.2f}")
    print(f"Winning Gene Sequence to copy-paste into simulator:\n{best_gene}")
            