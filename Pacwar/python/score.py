import _PyPacwar
from typing import List
from PyPacwarExample import str_to_seq

def score(rounds: int, c1: int, c2: int) -> tuple[int, int]:
    """
    Calculate the score for a battle between two genes.
    
    Args:
        rounds: Number of rounds the battle took (up to 500)
        c1: Number of mites of gene 1 remaining
        c2: Number of mites of gene 2 remaining
    
    Returns:
        A tuple (score1, score2) representing the scores for gene 1 and gene 2
    """
    # Gene 1 destroys gene 2 (c2 == 0)
    if c2 == 0:
        if rounds < 100:
            return (20, 0)
        elif rounds < 200:
            return (19, 1)
        elif rounds < 300:
            return (18, 2)
        else:  # rounds <= 500
            return (17, 3)
    
    # Gene 2 destroys gene 1 (c1 == 0)
    if c1 == 0:
        if rounds < 100:
            return (0, 20)
        elif rounds < 200:
            return (1, 19)
        elif rounds < 300:
            return (2, 18)
        else:  # rounds <= 500
            return (3, 17)
    
    # Battle went to 500 rounds - check ratios
    if rounds == 500:
        # Avoid division by zero
        if c1 == 0 or c2 == 0:
            # This shouldn't happen if we already checked above, but handle it
            if c1 == 0:
                return (0, 20)
            else:
                return (20, 0)
        
        ratio = c1 / c2
        
        # Gene 1 outnumbers gene 2 by at least 10:1
        if ratio >= 10.0:
            return (13, 7)
        
        # Gene 1 outnumbers gene 2 by between 3:1 and 10:1
        if ratio >= 3.0:
            return (12, 8)
        
        # Gene 1 outnumbers gene 2 by between 1.5:1 and 3:1
        if ratio >= 1.5:
            return (11, 9)
        
        # Check if gene 2 outnumbers gene 1
        inv_ratio = c2 / c1
        
        # Gene 2 outnumbers gene 1 by at least 10:1
        if inv_ratio >= 10.0:
            return (7, 13)
        
        # Gene 2 outnumbers gene 1 by between 3:1 and 10:1
        if inv_ratio >= 3.0:
            return (8, 12)
        
        # Gene 2 outnumbers gene 1 by between 1.5:1 and 3:1
        if inv_ratio >= 1.5:
            return (9, 11)
        
        # Neither outnumbers the other by more than 1.5:1
        return (10, 10)
    
    # Battle ended before 500 rounds but both species survived
    # This is an edge case - return a tie score
    return (10, 10)


def round_robin_tournament(sequences: List[List[int]]) -> List[int]:
    """
    Run a round-robin tournament where each sequence battles every other sequence.
    Accumulates points for each sequence using the score function.
    
    Args:
        sequences: A list of sequences, where each sequence is a list of 50 integers (0-3)
    
    Returns:
        A list of accumulated scores, one for each sequence in the same order
    """
    n = len(sequences)
    scores = [0] * n
    
    # Battle each sequence against every other sequence
    for i in range(n):
        for j in range(i + 1, n):
            # Battle sequence i against sequence j
            rounds, c1, c2 = _PyPacwar.battle(sequences[i], sequences[j])
            
            # Get scores for this battle
            # c1 is count for sequences[i], c2 is count for sequences[j]
            score1, score2 = score(rounds, c1, c2)
            
            # Accumulate scores
            scores[i] += score1
            scores[j] += score2
    
    return scores

if __name__ == "__main__":
    genes = [
        "1" * 50,
        "3" * 50,
        "11121111111112221113121111111211112111113110121111",
        "10110013101021230011123111111111311111210301111211",
        "03100030001300013230321121122112131321131133120123",
        "11110111131111011101011111111111211121211130131111",
        "11111111111111211101111211111111111111110110311111",
        "11121111111131121113113111111123111131111110221111",
        "11111101110121101111131111111131211031000111213111",
        "13121113121102313333122111111123231123120111031111",
        "00100003110122200100111111111121221111121331130330",
        "00100000110122223330111111111212322121000333131111",
        "11111111221120111110111123111121011101131011121110",
        "11021112100122223330111112112222323233111131230131",
        "10111103111111111111110111111111121110211011321031",
        "10110010111022113111111111111112311111121323230310",
        "10110010111121213311311111111122121111321130013331",
        "11110003131121323333111111111122121121112331333111",
        "10111111111121210113112111111111123111311311110311",
        "10110001011122222331111111111121112111121131330331",
        "01101113112122133133131112122223312133110111311211",
        "11101111111133313111121111112132013111111301111111",
        "11111111111211111311121211111231111111111101131111",
        "10110300110022203300111111111322032111121333323311",
        "11110010111111011111011111111312132131311131111111",
        "10111111131111101111101111111112101111111111111111",
        "10111312111111112111212111111111111111111011111001",
        "03100001111130033303312121112211222121131122023132",
        "11121110111121120311101111111112132112110111101211",
        "10113001100111213111213111111121103111311111112011",
        "00110010100022003330121111111121321111211310202331",
        "11111110111101121111111211111112111101111111311111",
        "00100000111322323311122111111213111311230331321111",
        "31110031111122113311111111111111111010331331023101",
        "31310001111122123331111311111321111321331301022311",
        "11321110111122310333232113112123211213132010021312",
        "11111111110101121111111111111131311112111110021113",
        "10110012110012113011122111111111011111231311113331",
    ]
    scores = round_robin_tournament(list(map(str_to_seq, genes)))

    scored_genes = zip(genes, scores)
    scored_genes = sorted(scored_genes, key=(lambda stuff : stuff[1]))

    for gene, s in scored_genes:
        print(f"{gene}: {s}")
    
    print(f"Max Possible: {len(genes) * 20}")