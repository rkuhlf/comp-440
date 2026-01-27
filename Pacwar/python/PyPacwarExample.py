import random
import _PyPacwar
import numpy

gene = 1 | 2 | 3 | 4

def mutate(sequence: list[gene]) -> list[gene]:
    sequence = sequence.copy()
    new_gene = random.randint(0, 3)
    position = random.randint(0, len(sequence) - 1)
    sequence[position] = new_gene
    return sequence

def seq_to_str(sequence: list[gene]) -> str:
    return "".join(map(str, sequence))



# Example Python module in C for Pacwar
def main():
    ones = [1] * 50
    threes = [1] * 50
    curr = ones.copy()

    # You have to beat all of the winners for the hill-climb to take it.
    winners = [curr, threes]
    max_winners = 100

    try:
        i = 0
        wins = 0
        print_every = 100
        while True:
            i += 1
            if i % print_every == 0:
                print(f"Iteration {i}, {wins/print_every=:.2f}")
                print(seq_to_str(curr))
                wins = 0

            neighbor = mutate(curr)
            won_all = True
            for winner in winners:
                (rounds, c1, c2) = _PyPacwar.battle(winner, neighbor)
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

    except:
        print("best vs past winners...")
        winner = winners[-1]
        for past_winner in winners:
            (rounds, c1, c2) = _PyPacwar.battle(past_winner, winner)
            print(f"r{rounds:4d}: p{c1:4d} w{c2:4d} {seq_to_str(past_winner)}")
        
        (rounds, c1, c2) = _PyPacwar.battle(ones, winner)
        print(f"r{rounds:4d}: 1{c1:4d} w{c2:4d}")
        (rounds, c1, c2) = _PyPacwar.battle(threes, winner)
        print(f"r{rounds:4d}: 3{c1:4d} w{c2:4d}")

        print("--- TOP MITES ---")
        print("\n".join(map(seq_to_str, winners[-5:])))



if __name__ == "__main__":
    main()
