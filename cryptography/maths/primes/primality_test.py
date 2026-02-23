import random
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


def carmichael(n):
    """
    Checks whether a number n is a Carmichael number. A Carmichael number
    is a composite number that satisfies Fermat's little theorem for all
    integers a that are coprime to n.

    Args:
        n (int): The number to check.

    Returns:
        bool: True if n is a Carmichael number, False otherwise.
    """
    primes = get_primes_factors(n)
    for prime in primes:
        if (n - 1) % (prime - 1) != 0:
            print(f"{n} is not a Carmichael number.")
            return False
    print(f"{n} is a Carmichael number.")
    return True


def pocklington(n, a=2):
    """
    Pocklington's criterion to test whether a number n is prime.
    It uses a certain form of the Fermat test along with the ability
    to find a divisor q of n-1.

    Args:
        n (int): The number to check.
        a (int): A base for Fermat's test.

    Returns:
        bool: True if n passes Pocklington's criterion, indicating n is prime.
    """
    q_ = int(n**0.5)
    while (n - 1) % q_ != 0:
        q_ += 1
        if q_ > n:
            return False

    if pow(a, n - 1, n) != 1:
        return False

    p_ = (n - 1) // q_

    if gcd(pow(a, p_, n), n) != 1:
        return False

    print(f"{n} is a Pocklington number.")
    return True


def fermat(n, k=20):
    """
    Fermat's primality test. It is a probabilistic test to check if n is prime.
    The test uses random numbers as bases and checks Fermat's little theorem.

    Args:
        n (int): The number to test.
        k (int): The number of iterations to repeat the test.

    Returns:
        bool: True if n passes the Fermat test, indicating n is probably prime.
    """
    if n < 4:
        return n == 2 or n == 3
    for _ in range(k):
        a = random.randint(2, n - 2)
        if gcd(a, n) == 1:
            if pow(a, n - 1, n) != 1:
                print(f"{n} is not prime:", end=" ")
                print(f"{a}^{n-1}[{n}] = {pow(a, n - 1, n)}")

                return False
    print(f"{n} is a Fermat number.")
    return True


def miller_rabin(n, k=20):
    """
    Miller-Rabin primality test. It is a probabilistic test to check if n is prime.
    It is more accurate than Fermat's test and works for larger numbers.

    Args:
        n (int): The number to test.
        k (int): The number of iterations to repeat the test.

    Returns:
        bool: True if n passes the Miller-Rabin test, indicating n is probably prime.
    """
    if n < 4:
        return n == 2 or n == 3

    if n % 2 == 0:
        return False

    s = get_primes_factors(n - 1).count(2)
    r = (n - 1) // (2**s)
    # print(f"n - 1 = 2^{s} * {r}")

    for _ in range(k):
        a = random.randint(2, n - 2)
        if gcd(a, n) == 1:
            if pow(a, r, n) != 1:
                j = 0
                while j < s and pow(a, 2**j * r, n) != n - 1:
                    # print(f"{a}^{2**j * r}[{n}] = {pow(a, 2**j * r, n)}")
                    j += 1

                    if j == s:
                        # print(f"{n} is not prime:", end=" ")
                        # print(f"{a}^{r}[{n}] = {pow(a, r, n)}")
                        return False
                if j < s:
                    print(f"{n} is probably prime.")
                    return True
            else:
                print(f"{n} is probably prime.")
                return True
    return True


def gen_prime(n):
    """
    Generates a random prime number with n bits using the Miller-Rabin test.

    Args:
        n (int): The number of bits of the prime.

    Returns:
        int: A randomly generated prime number.
    """
    while True:
        p = random.randint(2 ** (n - 1), 2**n)
        if miller_rabin(p):
            return p


if __name__ == "__main__":
    p1 = gen_prime(16)
    p2 = gen_prime(16)

    print(f"p1 = {p1}")
    print(f"p2 = {p2}")

    assert carmichael(p1) == carmichael(p2)
    assert fermat(p1) == fermat(p2)
    assert pocklington(p1) == pocklington(p2)
    

