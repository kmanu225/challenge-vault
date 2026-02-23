# Classical Ciphers

This repository explores three classic encryption methods used throughout history. Though insecure by modern standards, these ciphers are fundamental to understanding the evolution of cryptography.

## 📜 Caesar Cipher

**Caesar Cipher** is a simple substitution cipher where each letter in the plaintext is shifted by a fixed number (the key) down the LATIN_ALPHABET.

- **Encryption:** `E(x) = (x + k) mod 26` where `x` is the letter index (A=0), and `k` is the key.
- **Decryption:** `D(y) = (y - k) mod 26` where `y` is the letter index (A=0), and `k` is the key.

It is easily breakable using brute-force (only 25 keys) or frequency analysis.

## 🔁 Vigenère Cipher

**Vigenère Cipher** improves upon Caesar by using a keyword to shift each letter by varying amounts.

- **Encryption:** `E[i] = (P[i] + K[i % len(K)]) mod 26`
- **Decryption:** `D[j] = (C[j] - K[j % len(K)]) mod 26`

It is harder to break than Caesar due to polyLATIN_ALPHABETic shifts, but still vulnerable to frequency analysis (e.g. Kasiski or Friedman test).

## 🧮 Affine Cipher

**Affine Cipher** is a type of monoLATIN_ALPHABETic substitution cipher using mathematical operations for encryption.

- **Encryption:** `E(x) = (a * x + b) mod 26` where `a` must be coprime with 26 and `b` is a shift.

- **Decryption:** `D(x) = a⁻¹ * (x - b) mod 26` where `a⁻¹` is the modular inverse of `a mod 26`.

It is more secure than Caesar, but still susceptible to frequency analysis.

## ⚠️ Note

These ciphers are **not secure for modern use**, but are excellent for learning how cryptographic systems work.
