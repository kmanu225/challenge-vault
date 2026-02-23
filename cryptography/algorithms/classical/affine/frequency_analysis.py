from collections import Counter

LATIN_ALPHABET = "".join(chr(ord("a") + i) for i in range(26))

def get_frequencies(text):
    """Count letter frequencies and return a dict sorted by descending frequency."""
    return dict(Counter(text).most_common())

def striper(text):
    """Remove punctuation/whitespace and lowercase the text."""
    allowed = set(LATIN_ALPHABET)
    return "".join(c for c in text.lower() if c in allowed)

def get_affine_key(frequencies):
    """Guess affine cipher key (a, b) using frequency analysis."""
    (first, _), (second, _) = list(frequencies.items())[:2]
    f1, f2 = ord(first) - ord("a"), ord(second) - ord("a")

    e, t = ord("e") - ord("a"), ord("t") - ord("a")
    a = (f2 - f1) * pow(t - e, -1, 26) % 26
    b = (f1 - a * e) % 26
    return a, b

def affine_cipher(text, key):
    """Encrypt with affine cipher."""
    a, b = key
    return "".join(
        LATIN_ALPHABET[(a * (ord(c) - 97) + b) % 26] if c in LATIN_ALPHABET else c
        for c in text
    )

def affine_decipher(text, key):
    """Decrypt with affine cipher."""
    a, b = key
    a_inv = pow(a, -1, 26)
    return "".join(
        LATIN_ALPHABET[(a_inv * (ord(c) - 97 - b)) % 26] if c in LATIN_ALPHABET else c
        for c in text
    )

if __name__ == "__main__":
    decrypt_affine = lambda text: affine_decipher(text, get_affine_key(get_frequencies(text)))

    cipher_text = "ntjmpumgxpqtstgapgtxpnchumtputgfsftgthnngxnchumwxootrtumhpyctgktjqtjchfooxujqhgztumxpotjxotfoqtohrxumhzutwftgtopfmnt jmpuatmfmshodpfrxpjjtatghbxuj"
    print(decrypt_affine(striper(cipher_text)))
