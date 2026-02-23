import itertools
import re
import numpy as np
import random

FRENCH_FREQ = {
    "A": 8.46,
    "B": 1.02,
    "C": 3.21,
    "D": 3.78,
    "E": 17.6,
    "F": 1.11,
    "G": 1.12,
    "H": 1.07,
    "I": 7.4,
    "J": 0.48,
    "K": 0.0,
    "L": 6.05,
    "M": 2.7,
    "N": 6.38,
    "O": 5.19,
    "P": 2.68,
    "Q": 1.21,
    "R": 6.56,
    "S": 7.56,
    "T": 7.26,
    "U": 6.63,
    "V": 1.65,
    "W": 0.0,
    "X": 0.03,
    "Y": 0.03,
    "Z": 0.01,
}

alphabet = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


with open("C:\\Users\\HP\\Documents\\home\\git\\cryptoword\\challenges\\rootme\\cryptanalysis\\polybe\\ch2.txt", "r") as f:
    text = f.read()


FRENCH_INDEX_OF_COINCIDENCE = 0.0778


def normalize(text):
    ouput = text.upper().replace(" ", "").replace("\\n", "").replace("\\r", "")
    return re.sub(r'[^A-Z0-9 ]+', '', ouput)


def text_letters_frequency(text):
    pairs = {"A1": 0, "A2": 0, "A3": 0, "A4": 0, "A5": 0,
             "B1": 0, "B2": 0, "B3": 0, "B4": 0, "B5": 0,
             "C1": 0, "C2": 0, "C3": 0, "C4": 0, "C5": 0,
             "D1": 0, "D2": 0, "D3": 0, "D4": 0, "D5": 0,
             "E1": 0, "E2": 0, "E3": 0, "E4": 0, "E5": 0, }
    for i in range(0, len(text), 2):
        pair = text[i:i + 2]
        if pair in pairs:
            pairs[pair] += 1

    total_pairs = sum(pairs.values())
    frequency = {pair: round(100 * count / total_pairs, 3)
                 for pair, count in pairs.items()}
    return frequency


def probable_letters(pairs_freq):
    """
    Associe chaque paire de Polybe à un ensemble de lettres françaises probables
    en fonction de la fréquence relative observée.
    - pairs_freq : dict {pair: fréquence_en_%}
    Retourne : dict {pair: set(lettres_probables)}
    """
    probable = {}
    alphabet_low_frequencies = ["K", "W", "X", "Y",
                                "Z", "J"]
    text_low_frequencies = [pair for pair, f in pairs_freq.items() if f < 0.5]

    random.shuffle(alphabet_low_frequencies)
    random.shuffle(text_low_frequencies)

    for letter, pair in zip(alphabet_low_frequencies, text_low_frequencies):
        probable[pair] = [pairs_freq[pair],  [{letter: FRENCH_FREQ[letter]}]]

    remaining_pairs = {pair: freq for pair, freq in pairs_freq.items()
                       if pair not in text_low_frequencies}

    for pair, freq in remaining_pairs.items():
        if freq == 0:
            probable_letters = set()
        else:
            probable_letters = [freq, [{letter: f} for letter, f in FRENCH_FREQ.items()
                                if abs(f - freq) / freq < 0.2 or abs(f - freq) < 0.4]]
        probable[pair] = probable_letters

    fixed = {pair: next(iter(vals))
             for pair, vals in probable.items() if len(vals) == 1}
    for pair, letter in fixed.items():
        for other in probable:
            if other != pair and letter in probable[other]:
                probable[other].remove(letter)

    return probable


def index_of_coincidence(text):
    N = len(text)
    freq = {}
    for char in text:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    ic = sum(count * (count - 1)
             for count in freq.values()) / (N * (N - 1)) if N > 1 else 0
    return ic


def polybe_decrypt(text, matrix):
    decrypted = ""
    for i in range(0, len(text), 2):
        pair = text[i:i + 2]
        if len(pair) < 2:
            continue
        row = ord(pair[0]) - ord('A')
        col = int(pair[1]) - 1
        decrypted += matrix[row][col]
    return decrypted


text = normalize(text)
possible_values = probable_letters(text_letters_frequency(text))
cells = list(possible_values.keys())
solutions = []

print(probable_letters(text_letters_frequency(text)))
