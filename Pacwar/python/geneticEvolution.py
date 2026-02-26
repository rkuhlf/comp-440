import random
import numpy as np
import _PyPacwar
import helpers
from typing import Callable

GENE_LEN = 50
ALLELES = (0, 1, 2, 3)


def random_gene() -> list[int]:
    return [random.choice(ALLELES) for _ in range(GENE_LEN)]

def random_population(n: int) -> list[list[int]]:
    return [random_gene() for _ in range(n)]

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

def genetic_algorithm(population: list[list[int]], should_halt: Callable[[int], bool], opponents: list[list[int]],
                      mutation_rate = 0.1, survival_rate = 0.05, selection_k = 5, initial_k = 5):
    """
    Every generation, we select the top parent out of selection_k randomly selected genes. This parent gets combined with another parent chosen the same way.
    The top survival_rate percent of the parents get carried over anyways. initial_k is the number of opponents that the agent is evaluated against.
    """
    result_gene = None
    result_score = float('-inf')
    
    gen = 0
    while True:
        scores = []
        
        curr_opponents = random.sample(population, initial_k) + opponents
        for gen_code in population:
            scores.append(evaluate(gen_code, curr_opponents))
        
        if should_halt(gen, population, scores):
            break
        
        best_gene = population[np.argmax(scores)]  
        best_score = max(scores)
        if best_score > result_score:
            result_score = best_score
            result_gene = best_gene.copy()

        print(helpers.seq_to_str(best_gene))
            
        new_population = []
        num_survivors = max(1, int(len(population) * survival_rate))
        top_indices = np.argsort(scores)[::-1][:num_survivors]
        # Fill new population with survivors
        for i in top_indices:
            new_population.append(population[i].copy())
        
        while len(new_population) < len(population):
            p1 = strong_parent(population, scores, selection_k)
            p2 = strong_parent(population, scores, selection_k)
            
            child = crossover(p1, p2)
            mutate(child, mutation_rate)
            new_population.append(child)
            
        population = new_population
        
        gen += 1
        
    return best_gene, result_gene


if __name__ == "__main__":
    prev_gene = [0] * 50
    count = 0
    def should_halt(gen, population, scores):
        global prev_gene, count
        best_gene = population[np.argmax(scores)]        
        # Terminate when the best gene stops changing.
        diff = helpers.gene_diff(best_gene, prev_gene)
        prev_gene = best_gene

        if diff <= 2:
            count += 1
        else:
            count = 0

        if count == 2:
            return True
        
    def halt_after_n_generations(n: int):
        return lambda gen, population, scores: gen >= n


    result_winners = []
    best_winners = []
    try:
        while len(result_winners) < 20:
            best_gene, result_gene = genetic_algorithm(
                population=random_population(500),
                should_halt=should_halt,
                opponents=[],
                mutation_rate=0.01,
                survival_rate=0.05, 
                selection_k=5, 
                initial_k=5
            )
            best_winners.append(best_gene)
            result_winners.append(result_gene)
            print(helpers.seq_to_str(best_gene), helpers.seq_to_str(result_gene))
    except KeyboardInterrupt:
        pass
    finally:
        print("BestWinners:")
        print("\n".join([helpers.seq_to_str(w) for w in best_winners]))
        print("ResultWinners:")
        print("\n".join([helpers.seq_to_str(w) for w in result_winners]))
    
    
    # Run the genetic algorithm with a population of the best genes so far. This has less variance than the random population, so it's more of a fine-tuning step.
    # best_gene, best_score = genetic_algorithm(
    #     population=helpers.strs_to_seqs([
    #         "1" * 50,
    #         "3" * 50,
    #         "11121111111112221113121111111211112111113110121111",
    #         "10110013101021230011123111111111311111210301111211",
    #         "03100030001300013230321121122112131321131133120123",
    #         "11110111131111011101011111111111211121211130131111",
    #         "11111111111111211101111211111111111111110110311111",
    #         "11121111111131121113113111111123111131111110221111",
    #         "11111101110121101111131111111131211031000111213111",
    #         "13121113121102313333122111111123231123120111031111",
    #         "00100003110122200100111111111121221111121331130330",
    #         "00100000110122223330111111111212322121000333131111",
    #         "11111111221120111110111123111121011101131011121110",
    #         "11021112100122223330111112112222323233111131230131",
    #         "10111103111111111111110111111111121110211011321031",
    #         "10110010111022113111111111111112311111121323230310",
    #         "10110010111121213311311111111122121111321130013331",
    #         "11110003131121323333111111111122121121112331333111",
    #         "10111111111121210113112111111111123111311311110311",
    #         "10110001011122222331111111111121112111121131330331",
    #         "01101113112122133133131112122223312133110111311211",
    #         "11101111111133313111121111112132013111111301111111",
    #         "11111111111211111311121211111231111111111101131111",
    #         "10110300110022203300111111111322032111121333323311",
    #         "11110010111111011111011111111312132131311131111111",
    #         "10111111131111101111101111111112101111111111111111",
    #         "10111312111111112111212111111111111111111011111001",
    #         "03100001111130033303312121112211222121131122023132",
    #         "11121110111121120311101111111112132112110111101211",
    #         "10113001100111213111213111111121103111311111112011",
    #         "00110010100022003330121111111121321111211310202331",
    #         "11111110111101121111111211111112111101111111311111",
    #         "00100000111322323311122111111213111311230331321111",
    #         "31110031111122113311111111111111111010331331023101",
    #         "31310001111122123331111311111321111321331301022311",
    #         "11321110111122310333232113112123211213132010021312",
    #         "11111111110101121111111111111131311112111110021113",
    #         "10110012110012113011122111111111011111231311113331",
    #         "00020030111122103333302313132321222232313133010312",
    #         "00020030110122213003133113032122122312111133133103",
    #         "11022001131221123233233331302223303101012312203312",
    #         "10020000110122220303112211211122311321301331130301",
    #         "33020000133022223333213232033232232232102130332131",
    #         "11020000111022023033233212213332232212313313110310",
    #         "00300000113122020333133333332333222322303110111310",
    #         "01001000111022223303212212212232232232310011221333",
    #     ]),
    #     should_halt=should_halt,
    #     opponents=helpers.strs_to_seqs([
    #         "00100000111322323311122111111213111311230331321111",
    #         "10020000110122220303112211211122311321301331130301",
    #         "03100001111130033303312121112211222121131122023132",
    #         "33020000133022223333213232033232232232102130332131",
    #         "11020000111022023033233212213332232212313313110310",
    #         "00300000113122020333133333332333222322303110111310",
    #     ]),
    #     mutation_rate=0.01,
    #     survival_rate=0.05, 
    #     selection_k=5, 
    #     initial_k=4
    # )
    
    # print("\n=== EVOLUTION COMPLETE ===")
    # print(f"Top Score: {best_score:.2f}")
    # print(f"Winning Gene Sequence to copy-paste into simulator:\n{helpers.seq_to_str(best_gene)}")


    # I could make a loop of running the genetic algorithm, then adding the winner of the genetic algorithm to the list of opponents that I have so far.
    # You terminate when the result of the genetic algorithm isn't the winner of the round robin.
    # Hmmm. I just got there through manual iteration.
            