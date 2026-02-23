# ====================================================
# Root-me "Encodage UU" challenge cryptanalysis
# https://www.root-me.org/fr/Challenges/Cryptanalyse/Encodage-uu
# ====================================================

import os


def ascii_encoded_to_bits(n):
    bits = ""
    for _ in range(8):
        bits = str(n % 2) + bits
        n //= 2
    return bits


def uu_encoded_to_bits(n):
    n -= 32
    bits = ""
    for _ in range(6):
        bits = str(n % 2) + bits
        n //= 2
    return bits


def encoded_to_bits(encoded, f=ascii_encoded_to_bits):
    return "".join(f(byte) for byte in encoded)


def bits_to_dec(bits):
    number, power, n = 0, 0, len(bits)
    while bits:
        number += int(bits[-1]) * 2**power
        bits = bits[:n-1]
        n -= 1
        power += 1
    return number


def encode_line_uu(line: bytes):
    chunks = []
    for start in range(0, len(line), 3):
        chunk = line[start:start+3] + b"\x00" * (3 - len(line[start:start+3]))
        bits = encoded_to_bits(chunk)
        bits = [bits[i:i+6] for i in range(0, 24, 6)]
        for char in bits:
            chunks.append(uu_alphabet_pos[bits_to_dec(char)])

    encode_length = uu_alphabet_pos[len(line)]

    if chunks[-2] == " ":
        chunks[-2] = uu_alphabet_pos[64]
    if chunks[-1] == " ":
        chunks[-1] = uu_alphabet_pos[64]

    begin = "begin 000 uuencode\n"
    end = "\n`\nend"

    return begin + "".join([encode_length] + chunks) + end


def decode_line_uu(encoded_line):
    if encoded_line == uu_alphabet_pos[64]:
        return ""

    encoded_line = encoded_line[1:]
    length = len(encoded_line)
    eol = ""

    if encoded_line[-1] == uu_alphabet_pos[64]:
        eol += " "
        encoded_line = encoded_line[:length-1]

    if encoded_line[-1] == uu_alphabet_pos[64]:
        eol += " "
        encoded_line = encoded_line[:length-2]

    encoded_line += eol

    bits_stream = "".join(uu_encoded_to_bits(c)
                          for c in bytes(encoded_line, "utf-8"))
    to_ascii = "".join(chr(bits_to_dec(bits_stream[i:i+8]))
                       for i in range(0, len(bits_stream), 8))
    return to_ascii


if __name__ == "__main__":
    basedir = os.path.dirname(__file__)
    encoded = open(os.path.join(basedir, "ch1.txt"), "r").read()

    uu_alphabet = "".join(chr(i) for i in range(32, 97))
    uu_alphabet_pos = {idx: char for idx, char in enumerate(uu_alphabet)}

    with open(os.path.join(basedir, "ch1.txt"), "r") as f:

        encoded = f.readlines()

    ascii_encoded = ""
    for line in encoded:
        ascii_encoded += decode_line_uu(line.strip("\n"))

    print(ascii_encoded)
