gene = int # 1 | 2 | 3 | 4
sequence = list[gene]

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



def seq_to_str(sequence: list[gene]) -> str:
    return "".join(map(str, sequence))

def str_to_seq(string: str) -> list[gene]:
    return list(map(int, list(string)))

def strs_to_seqs(population: list[str]) -> list[list[int]]:
    return list(map(str_to_seq, population))

def seqs_to_strs(population: list[list[int]]) -> list[str]:
    return list(map(seq_to_str, population))

def gene_diff(seq1: list[int], seq2: list[int]) -> int:
    """Returns the count of differing positions."""
    return sum(a != b for a, b in zip(seq1, seq2))
