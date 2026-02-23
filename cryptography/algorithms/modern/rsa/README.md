# 🔐 RSA Algorithm - Overview

**RSA** is a widely-used public key cryptographic algorithm that allows secure communication over an insecure network. It’s based on the mathematical difficulty of factoring large composite numbers.

## 📚 How It Works

### 1. **Key Generation**

1. Choose two large prime numbers: `p` and `q`
2. Compute the modulus: `N = p * q`
3. Compute Euler's totient: `ϕ(N) = (p - 1) * (q - 1)`
4. Choose a public exponent `e` such that: `1 < e < ϕ(N)` and `gcd(e, ϕ(N)) = 1`
5. Compute the private exponent `d`: `d ≡ e⁻¹ mod ϕ(N)` (modular inverse of `e`)

🔑 **Public Key**: `(e, N)`
🔐 **Private Key**: `(d, N)`

## ✉️ Encryption

To encrypt a message `M` (as an integer):

$$
C = M^e \mod N
$$

## 🔓 Decryption

To decrypt ciphertext `C`:

$$
M = C^d \mod N
$$

## 🔒 Security

The security of RSA relies on the fact that factoring a large number N = p * q is computationally hard. If an attacker is able to factor N, they can compute ϕ(N) and ultimately break the encryption.

However, if RSA is not implemented correctly, it can be vulnerable to cryptanalytic attacks that are more efficient than brute-force or exhaustive search. These attacks exploit mathematical properties or implementation flaws (like weak key generation or improper padding).

This repository focuses on demonstrating and analyzing such cryptanalysis methods.
