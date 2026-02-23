from sympy import isprime, gcd

def get_primes_factors(n):
    """
    Returns the prime factors of a given number n. If the number is prime,
    the function returns a list containing only n. Otherwise, it decomposes 
    n into its prime factors and returns them in ascending order.

    Args:
        n (int): The number to factorize.

    Returns:
        list: A list of prime factors of the number n.
    """
    if isprime(n):
        return [n]

    factors = []
    for i in range(2, n + 1):
        if isprime(i):
            while n % i == 0:
                factors.append(i)
                n = n // i
    factors.sort()
    return factors


def get_primes(B):
    """
    Returns all prime numbers less than or equal to B.

    Args:
        B (int): The upper bound for prime numbers.

    Returns:
        list: A list of all prime numbers less than or equal to B.
    """
    primes = []
    for i in range(2, B + 1):
        if isprime(i):
            primes.append(i)
    return primes


def get_Q(B, n):
    """
    Computes the least common multiple (LCM) of the highest powers of all 
    primes less than or equal to B that are less than or equal to n.

    Args:
        B (int): The upper bound for primes.
        n (int): The number whose prime factors' powers are considered.

    Returns:
        int: The computed Q value, which is the LCM of the highest prime powers.
    """
    primes = get_primes(B)
    high_power_lower_n = []
    for prime in primes:
        power = 1
        while prime**power <= n:
            power += 1
        high_power_lower_n.append(prime ** (power - 1))

    Q = 1
    for prime_power in high_power_lower_n:
        Q *= prime_power
    return Q


if __name__ == "__main__":
    a = 3
    B = 19
    n = 19048567
    Q = get_Q(B, n)
    aq_min_one_mod_n = pow(a, Q, n) - 1

    GCD = gcd(aq_min_one_mod_n, n)
    print(f"Factors found of {n} are: {GCD} {n / GCD}")
