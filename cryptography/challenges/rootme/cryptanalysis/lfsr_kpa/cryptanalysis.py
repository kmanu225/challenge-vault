# ====================================================
# Root-me "LFSR - Clair connu" challenge cryptanalysis
# https://www.root-me.org/fr/Challenges/Cryptanalyse/LFSR-Clair-connu
# ====================================================

# The idea is to XOR the known plaintext (the PNG header/magic number) with the encrypted file to get the LFSR output stream.
# Tips: Magic number
# Then we can use the Berlekamp-Massey algorithm to find the shortest LFS


# Berlekamp Massey implementation
import numpy as np
import copy
import os
from numpy import dtype


def polynom(coefficients):
    n = len(coefficients)
    poly = []
    for i in range(1, n):
        if coefficients[i] == 1:
            poly.append(i)
    return poly


def magic_number(file):
    with open(file, "rb") as f:
        data = f.read()
        bits = "".join(format(byte, "08b") for byte in data[:16])
        return list(bits)


def xor_lists(a, b):
    return [int(x) ^ int(y) for x, y in zip(a, b)]


def main() -> None:
    cipher = xor_lists(
        magic_number(os.path.dirname(__file__) + "\ch32\sample_png.png"),
        magic_number(os.path.dirname(__file__) + "\ch32\challenge.png.encrypt"),
    )  # comma separated
    print(f"Length of the cipher: {len(cipher)}\ncipher={cipher}")
    results = berlekamp_massey(cipher)
    print(f"Minimal LFSR: {results[0]}")
    print(f"Minimal polynomial: {results[1]}")
    print(f"Minimal polynomial in polynomial form: {polynom(results[1])}")


# Find the minimal LFSR and minimal polynomial to generate the data
def berlekamp_massey(data: list[int]) -> tuple[int, np.ndarray[int, dtype[int]]]:
    n = len(data)
    c_x, b_x = np.zeros(n, dtype=int), np.zeros(n, dtype=int)
    c_x[0], b_x[0] = 1, 1
    l, m, i = 0, -1, 0
    while i < n:
        v = data[(i - l) : i]
        v = v[::-1]
        cc = c_x[1 : l + 1]
        delta = (data[i] + np.dot(v, cc)) % 2
        if delta == 1:
            temp = copy.copy(c_x)
            p = np.zeros(n, dtype=int)
            for j in range(0, l):
                if b_x[j] == 1:
                    p[j + i - m] = 1
            c_x = (c_x + p) % 2
            if l <= 0.5 * i:
                l = i + 1 - l
                m = i
                b_x = temp
        i += 1
    c_x = c_x.tolist()
    ind = 0
    for x in c_x[::-1]:
        if x == 0:
            ind += 1
        else:
            break
    c_x = c_x[:-ind]
    return len(c_x) - 1, c_x


if __name__ == "__main__":
    main()
