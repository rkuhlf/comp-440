import random
from typing import Callable
import _PyPacwar
import numpy

ones = [1] * 50
threes = [1] * 50
gene = 1 | 2 | 3 | 4
sequence = list[gene]

def mutate(sequence: list[gene], n: int = 1) -> list[gene]:
    sequence = sequence.copy()
    new_genes = [random.randint(0, 3) for _ in range(n)]
    positions = random.sample(range(len(sequence)), n)
    for position, gene in zip(positions, new_genes):
        sequence[position] = gene
    
    return sequence

def seq_to_str(sequence: list[gene]) -> str:
    return "".join(map(str, sequence))

def str_to_seq(string: str) -> list[gene]:
    return list(map(int, list(string)))


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
        for _ in range(30):
            mutation_size = random.randint(1, 8)
            iters, winners = iterate_single(
                max_winners=50,
                stop_probability=0.025,
                mutation_count=lambda : min(30, 1 + int(numpy.random.exponential(mutation_size, size=1)[0]))
            )
            overall_winners.append((winners[-1], mutation_size, iters))
    finally:
        print("--- TOP MITES ---")
        print("\n".join([f"{seq_to_str(winner)} ({mutation_size}, {iters})" for winner, mutation_size, iters in overall_winners]))


if __name__ == "__main__":
    main()
