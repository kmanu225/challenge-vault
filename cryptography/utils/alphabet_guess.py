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
    'other': 0.01  # bucket for unknown chars
}


def frequency_table(string: str) -> dict:
    frequency = {}
    length = len(string)

    for character in string:
        bucket = character if character in FRENCH_FREQUENCY else 'other'
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


def french_score(string: str) -> float:
    computed_frequency = frequency_table(string.lower())
    return 1 / chi_squared(FRENCH_FREQUENCY, computed_frequency)


def right_rot_bruteforce(cipher_text) -> list:
    plausible_texts = []
    for i in range(255):
        decoded = bytes([(b + i) % 256 for b in cipher_text])
        score = french_score(decoded.decode('latin-1', errors='ignore'))
        plausible_texts.append((i, score, decoded))
    plausible_texts.sort(key=lambda x: x[1], reverse=True)
    return plausible_texts