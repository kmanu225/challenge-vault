# Cryptanalysis

## Euler method

This method exploits the relationship between the RSA private exponent d and the public exponent e to factorize N.

- The crucial trick is that `k = ed - 1` is a multiple of Euler’s totient function $\varphi(N)= (p-1)(q-1)$.
- By Euler's theorem, for any integer a coprime to N, $ a^{\varphi(N)} \mod N = 1$.
- This allows us to find a nontrivial square root of 1 modulo N, which can be used to extract factors of N.


The process goes like this. We choose a random integer `g` and compute:  
$$
x = g^t \mod N
$$  
where `t` is repeatedly divided by 2 (starting from `k`).  

If at any step, we find an `x` such that:  

- $ x \not\equiv 1 \mod N $  
- $ x^2 \equiv 1 \mod N $  

Then, we compute:  
$$
p = \gcd(x - 1, N)
$$
which is likely to give a **nontrivial factor** of `N` (i.e., one of the prime factors).