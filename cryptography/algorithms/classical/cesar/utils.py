IC_FR = 0.07


# Notre Dame de Paris
NOTRE_DAME_PARIS_FREQUENCIES = {
    "a": 8.46,
    "b": 1.02,
    "c": 3.21,
    "d": 3.78,
    "e": 17.6,
    "f": 1.11,
    "g": 1.12,
    "h": 1.07,
    "i": 7.4,
    "j": 0.48,
    "k": 0.0,
    "l": 6.05,
    "m": 2.7,
    "n": 6.38,
    "o": 5.19,
    "p": 2.68,
    "q": 1.21,
    "r": 6.56,
    "s": 7.56,
    "t": 7.26,
    "u": 6.63,
    "v": 1.65,
    "w": 0.0,
    "x": 0.03,
    "y": 0.03,
    "z": 0.01,
}


def striper(text):
    special_caracters = [
        " ",
        "\n",
        "\t",
        ".",
        ",",
        ";",
        ":",
        "!",
        "?",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        "'",
        '"',
        "-",
    ]
    for car in special_caracters:
        text = text.replace(car, "")
    return text.lower()


ENGLISH_FREQUENCY = {
    ' ': 0.14,
    'e': 0.12,
    't': 0.09,
    'other': 0.09,
    'a': 0.08,
    'o': 0.07,
    'i': 0.06,
    'n': 0.06,
    's': 0.06,
    'h': 0.06,
    'r': 0.05,
    'd': 0.04,
    'l': 0.04,
    'c': 0.02,
    'u': 0.02,
    'm': 0.02,
    'w': 0.02,
    'f': 0.02,
    'g': 0.02,
    'y': 0.01,
    'p': 0.01,
    'b': 0.01,
    'v': 0.01,
    'k': 0.01,
    'j': 0.01,
    'x': 0.00,
    'q': 0.00,
    'z': 0.00
}

FRENCH_FREQUENCY = {
    ' ': 0.15,
    'e': 0.1587,
    'a': 0.0764,
    'i': 0.0753,
    's': 0.0737,
    'n': 0.0715,
    'r': 0.0669,
    't': 0.0655,
    'o': 0.0502,
    'l': 0.0546,
    'u': 0.0624,
    'd': 0.0367,
    'c': 0.0326,
    'm': 0.0296,
    'p': 0.0251,
    'g': 0.0123,
    'b': 0.0104,
    'v': 0.0105,
    'h': 0.0077,
    'f': 0.0107,
    'q': 0.0136,
    'y': 0.0030,
    'x': 0.0042,
    'j': 0.0061,
    'k': 0.0005,
    'w': 0.0017,
    'z': 0.0030,
    'other': 0.01
}


def frequency_table(string: str, alphabet_frequencies) -> dict:
    frequency = {}
    length = len(string)

    for character in string:
        bucket = character if character in alphabet_frequencies else 'other'
        frequency[bucket] = frequency.get(bucket, 0) + 1

    for k in frequency:
        frequency[k] = frequency[k] / length

    return frequency


def chi_squared(expected_frequency: dict, computed_frequency: dict) -> float:
    score = 0.0
    for letter, expected_value in expected_frequency.items():
        computed_value = computed_frequency.get(letter, 0)
        if expected_value == 0:
            continue
        score += (expected_value - computed_value) ** 2 / expected_value
    return score


def score(string: str, alphabet_frequencies=FRENCH_FREQUENCY) -> float:
    computed_frequency = frequency_table(string.lower(), alphabet_frequencies)
    return 1 / chi_squared(FRENCH_FREQUENCY, computed_frequency)


def get_frequences(text):
    frequence = {}
    for letter in text:
        if letter in frequence:
            frequence[letter] += 1
        else:
            frequence[letter] = 1
    return {
        k: v
        for k, v in sorted(frequence.items(), key=lambda item: item[1], reverse=True)
    }

def rot_right(text, decalage):
    """
    Applies a Caesar cipher shift to the right (forward in the alphabet).

    Args:
        text (str): The plaintext to encrypt (assumed lowercase).
        decalage (int): The shift amount (e.g., 3 means A -> D).

    Returns:
        str: The encrypted ciphertext.
    """
    result = ""
    ord_a = ord("a")
    alphabet = [chr(ord_a+i) for i in range(26)]
    for char in text:
        if char in alphabet:
            id = (alphabet.index(char) + decalage) % 26
            result += alphabet[id]
        else:
            result += char  # Keep non-alphabetic characters unchanged
    return result