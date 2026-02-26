import random, math
from typing import Callable
import _PyPacwar
import numpy

from helpers import *

ones = [1] * 50
threes = [3] * 50


def mutate(sequence: list[gene], n: int = 1) -> list[gene]:
    sequence = sequence.copy()
    new_genes = [random.randint(0, 3) for _ in range(n)]
    positions = random.sample(range(len(sequence)), n)
    for position, gene in zip(positions, new_genes):
        sequence[position] = gene
    
    return sequence

def iterate_single(*, max_winners: int, stop_probability: float, mutation_count: Callable[[], float]) -> sequence:
    curr = ones.copy()

    # You have to beat all of the winners for the hill-climb to take it.
    winners = [curr, threes]

    i = 0
    wins = 0
    print_every = 100
    while True:
        i += 1
        if i % print_every == 0:
            print(f"Iteration {i}, {wins}/{print_every}")
            print(seq_to_str(curr))

            if wins == 0 and random.random() < stop_probability:
                break
            
            wins = 0

        neighbor = mutate(curr, n=mutation_count())
        won_all = True
        for winner in winners:
            (_rounds, c1, c2) = _PyPacwar.battle(winner, neighbor)
            # If the past winner beats this, we don't want it.
            if c1 >= c2:
                won_all = False
        
        if won_all:
            wins += 1
            curr = neighbor
            winners.append(neighbor)
            
            # Remove a random one maybe.
            if random.uniform(0, 1) < len(winners) / max_winners:
                idx_to_remove = random.randint(0, len(winners) - 2)
                winners.pop(idx_to_remove)

    return i, winners

def iterate_known_winners(*, initial_gene: sequence, stop_probability: float, mutation_count: Callable[[], float]) -> sequence:
    curr = initial_gene
    winners = [ones.copy(), threes]
    # c2 is me.
    record_c2 = 0
    # c1 is other.
    record_c1 = 1000
    record_rounds = 1000

    i = 0
    wins = 0
    print_every = 1000
    while True:
        i += 1
        if i % print_every == 0:
            print(f"Iteration {i}, {wins}/{print_every}, {record_c1, record_c2, record_rounds}")
            print(seq_to_str(curr))

        if i % 100 == 0:
            if wins == 0 and random.random() < stop_probability:
                break
            
            wins = 0

        neighbor = mutate(curr, n=mutation_count())
        total_rounds = 0
        total_c1 = 0
        total_c2 = 0
        for winner in winners:
            (rounds, c1, c2) = _PyPacwar.battle(winner, neighbor)
            # If the past winner beats this, we don't want it.
            if c1 >= c2:
                total_c1 = math.inf
                break

            total_rounds += rounds
            total_c1 += c1
            total_c2 += c2
        
        # If we killed more of their guys, that's definitely a win.
        if total_c1 < record_c1:
            wins += 1
            curr = neighbor
            record_c1 = total_c1
            record_c2 = total_c2
            record_rounds = total_rounds
        elif total_c1 == record_c1 and total_rounds < record_rounds: # If we killed at least as many of their guys, and we did it faster, that's definitely a win.
            wins += 1
            curr = neighbor
            record_c1 = total_c1
            record_c2 = total_c2
            record_rounds = total_rounds
        elif total_c1 == record_c1 and total_rounds == record_rounds and total_c2 > record_c2: # If we killed at least as many of their guys, and we did it in the same speed but we had more of our guys, that's definitely a win.
            wins += 1
            curr = neighbor
            record_c1 = total_c1
            record_c2 = total_c2
            record_rounds = total_rounds
        elif total_c1 == record_c1 and total_rounds == record_rounds and total_c2 == record_c2: # If everything was the exact same, we'll take it for extra randomness.
            curr = neighbor
            record_c1 = total_c1
            record_c2 = total_c2
            record_rounds = total_rounds
                
    return i, [curr]

# 03100110012223010333311121122200332323121133203221 (3, 33000)
# 03110010121100033111323121322112021021131230312113 (8, 27000)
# 00100000001110013330121121322012031331131133100202 (6, 47000)
# 03100130301000311030331121131102131221102133222100 (3, 46000)
# 03102030101230113230231121110111131022101132122123 (1, 17000)

def print_eval(to_eval, against):
    print("best vs past winners...")
    for other in against:
        (rounds, c1, c2) = _PyPacwar.battle(other, to_eval)
        print(f"r{rounds:4d}: o{c1:4d} n{c2:4d} {seq_to_str(other)}")
    
    (rounds, c1, c2) = _PyPacwar.battle(ones, to_eval)
    print(f"r{rounds:4d}: 1{c1:4d} n{c2:4d}")
    (rounds, c1, c2) = _PyPacwar.battle(threes, to_eval)
    print(f"r{rounds:4d}: 3{c1:4d} n{c2:4d}")


def main():
    overall_winners = []
    try:
        # for _ in range(30):
        #     mutation_size = random.randint(1, 8)
        #     iters, winners = iterate_single(
        #         max_winners=50,
        #         stop_probability=0.025,
        #         mutation_count=lambda : min(30, 1 + int(numpy.random.exponential(mutation_size, size=1)[0]))
        #     )
        #     overall_winners.append((winners[-1], mutation_size, iters))
        
        for _ in range(30):
            mutation_size = random.randint(2, 8)
            iters, winners = iterate_known_winners(
                initial_gene=str_to_seq("01001000111022223303212212212232232232310011221333"),
                stop_probability=0.01,
                mutation_count=lambda : min(30, 1 + int(numpy.random.exponential(mutation_size, size=1)[0]))
            )
            overall_winners.append((winners[-1], mutation_size, iters))
    finally:
        print("--- TOP MITES ---")
        print("\n".join([f"{seq_to_str(winner)} ({mutation_size}, {iters})" for winner, mutation_size, iters in overall_winners]))


if __name__ == "__main__":
    main()
