from math import sqrt, floor, gcd
from sympy import isprime
import numpy as np

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


q = lambda x, n: (x + floor(sqrt(n))) ** 2 - n


def get_parameters(limit: int, n: int, S: list[int], x_0=-10):
    """
    Generates the parameters a, b, e, and v for the algorithm. These parameters 
    are used in the quadratic sieve or related factorization algorithms.
    
    Args:
        limit (int): The number of valid parameter sets to generate.
        n (int): The number to factorize.
        S (list[int]): A list of small primes used in the factorization.
        x_0 (int, optional): The starting value for x. Defaults to -10.

    Returns:
        tuple: A tuple containing the dictionaries (a, b, e, v) which hold the parameters.
    """
    m = floor(sqrt(n))
    a = dict()
    b = dict()
    e = dict()
    v = dict()
    x = x_0

    size = 0
    while size < limit:
        q_x_n = q(x, n)

        a_x = x + m
        b_x = q_x_n

        e_x = [0] * len(S)
        v_x = e_x.copy()

        s_primes = []
        is_s_lisse = True

        if q_x_n < 0:
            s_primes.append(-1)
            e_x[0] = 1
            v_x[0] = e_x[0] % 2
            q_x_n = -q_x_n

        primes = get_primes_factors(q_x_n)
        for prime in primes:
            if prime not in S:
                is_s_lisse = False
                break
            else:
                id = S.index(prime)
                e_x[id] += 1
                v_x[id] = e_x[id] % 2

        if is_s_lisse:
            s_primes += primes
            a[x] = a_x
            b[x] = b_x
            e[x] = e_x
            v[x] = v_x
            size += 1
        x += 1
    return a, b, e, v


def get_base(n: int, limit):
    """
    Returns a list of prime numbers that are quadratic residues modulo n.
    These primes are used as the base for the factorization algorithm.

    Args:
        n (int): The number to factorize.
        limit (int): The number of primes to find.

    Returns:
        list: A list of primes that are quadratic residues modulo n.
    """
    base = [-1]
    length = 1
    p = 2
    while length < limit:
        if isprime(p):
            r = 0
            while r <= p and pow(r, 2, p) != pow(n, 1, p):
                r += 1
            if r <= p:
                base.append(p)
                length += 1
        p += 1
    return base


def get_matrix(v: dict):
    """
    Converts the dictionary v into a matrix. The matrix is constructed by 
    using the values of v as columns and the corresponding keys as row indices.

    Args:
        v (dict): A dictionary containing vectors as values.

    Returns:
        tuple: A tuple containing the matrix (as a numpy array) and the keys (list of row indices).
    """
    matrix = np.array(list(v.values()))
    return matrix.transpose(), list(v.keys())


if __name__ == "__main__":
    n = 24961
    base_size = 5
    F = get_base(n, base_size)
    print("Base: ", F)

    a, b, e, v = get_parameters(base_size + 1, n, F, 0)
    M = get_matrix(v)[0]

    print(v)
    print(M)

    b_candidate = b[12]
    Y = a[12]

    X = floor(sqrt(b_candidate))
    div1 = gcd(X - Y, n)
    div2 = gcd(X + Y, n)

    print(f"Non-trivial divisors: {div1}, {div2}")
