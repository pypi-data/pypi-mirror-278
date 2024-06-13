from typing import List
from math import isqrt

def sieve_of_eratosthenes(n: int) -> List[int]:
    """
    Generates all prime numbers up to n using the Sieve of Eratosthenes algorithm.

    Args:
        n (int): The upper limit for prime numbers.

    Returns:
        List[int]: A list of prime numbers up to n.
    """
    primes = [True] * (n+1)
    primes[0], primes[1] = False, False
    p = 2
    while (p * p <= n):
        if primes[p] == True:
            for i in range(p * p, n+1, p):
                primes[i] = False
        p += 1
    return [i for i in range(n+1) if primes[i]]

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
    
    primes = set(sieve_of_eratosthenes(isqrt(n) + 1))
    
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    for i in range(3, isqrt(n) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
        if i in primes:
            break
    
    if n > 2:
        factors.append(n)
    
    return factors
