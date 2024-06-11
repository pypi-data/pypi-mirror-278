from typing import List

def prime_factors(n: int) -> List[int]:
    """
    Finds prime factors of a given number.

    Args:
        n (int): The number to find prime factors for.

    Returns:
        List[int]: A list of prime factors of the given number.
    """
    factors = []
    if n <= 1:
        return factors
    
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    
    if n > 2:
        factors.append(n)
    
    return factors
