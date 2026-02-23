LATIN_ALPHABET = "abcdefghijklmnopqrstuvwxyz"
ORD_LOWER_A = ord("a")
ORD_LOWER_E = ord("e")

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

# Function to calculate the Caesar cipher key based on the most frequent letter
get_cesar_key = lambda frequence: ord(list(frequence.keys())[0]) - ORD_LOWER_E

# Function to decrypt text with Caesar cipher using the calculated key
decrypt_cesar = lambda ciphertext: rot_left(
    ciphertext, get_cesar_key(get_frequences(ciphertext))
)


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
    for char in text:
        if char in LATIN_ALPHABET:
            new_index = (LATIN_ALPHABET.index(char) + decalage) % 26
            result += LATIN_ALPHABET[new_index]
        else:
            result += char  # Keep non-alphabetic characters unchanged
    return result


def rot_left(text, decalage):
    """
    Reverses a Caesar cipher shift to the left (backward in the alphabet).

    Args:
        text (str): The ciphertext to decrypt (assumed lowercase).
        decalage (int): The shift amount used during encryption.

    Returns:
        str: The decrypted plaintext.
    """
    result = ""
    for char in text:
        if char in LATIN_ALPHABET:
            new_index = (LATIN_ALPHABET.index(char) - decalage) % 26
            result += LATIN_ALPHABET[new_index]
        else:
            result += char  # Keep non-alphabetic characters unchanged
    return result

def vigenere_to_cesars(text, l):
    """
    Converts a Vigenère cipher text to multiple Caesar cipher texts based on the key length.

    Args:
        text (str): The Vigenère ciphertext.
        l (int): The key length for the Vigenère cipher.

    Returns:
        list: A list of `l` Caesar cipher texts corresponding to the Vigenère cipher's split.
    """
    cesar_texts = []
    for i in range(l):
        cesar_text = ""
        for j in range(i, len(text), l):
            cesar_text += text[j]
        cesar_texts.append(cesar_text)
    return cesar_texts


def cesars_to_vigenere(cesar_texts):
    """
    Reconstructs a Vigenère cipher text from multiple Caesar cipher texts.

    Args:
        cesar_texts (list): A list of Caesar cipher texts.

    Returns:
        str: The reconstructed Vigenère ciphertext.
    """
    text = ""
    for i in range(len(cesar_texts[0])):
        for j in range(len(cesar_texts)):
            if i < len(cesar_texts[j]):
                text += cesar_texts[j][i]
    return text

def striper(text):
    """
    Strips all special characters (spaces, punctuation, etc.) from the text and converts it to lowercase.

    Args:
        text (str): The input text.

    Returns:
        str: The cleaned text with only lowercase alphabetic characters.
    """
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


def get_frequences(text):
    """
    Computes the frequency of each character in the text and sorts the results in descending order.

    Args:
        text (str): The input text.

    Returns:
        dict: A dictionary of character frequencies sorted in descending order.
    """
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


# Indice de coïncidence mutuelle
def MIC(text_1, text_2):
    """
    Computes the Mutual Index of Coincidence (MIC) between two texts. It measures the likelihood of two texts having similar letter distributions.

    Args:
        text_1 (str): The first text.
        text_2 (str): The second text.

    Returns:
        float: The calculated MIC value.
    """
    mic_text = 0
    n_1 = len(text_1)
    n_2 = len(text_2)
    for letter in LATIN_ALPHABET:
        n_1_i = text_1.count(letter)
        n_2_i = text_2.count(letter)
        mic_text += n_1_i * n_2_i
    mic_text /= n_1 * n_2
    return mic_text


# Indice de coïncidence
def IC(text):
    """
    Computes the Index of Coincidence (IC) for a single text. IC measures how likely it is that two randomly selected letters in the text will be the same.

    Args:
        text (str): The input text.

    Returns:
        float: The calculated IC value.
    """
    ic_text = 0
    n = len(text)
    for letter in LATIN_ALPHABET:
        n_i = text.count(letter)
        ic_text += n_i * (n_i - 1)
    ic_text /= n * (n - 1)

    return ic_text


def find_ngrams_distances(text, n):
    """
    Finds the distances between repeated n-grams (substrings of length `n`) in the text.

    Args:
        text (str): The input text.
        n (int): The length of the n-grams to consider.

    Returns:
        list: A list of the distances between repeated n-grams.
    """
    ngrams = {}
    for i in range(len(text) - n + 1):
        ngram = text[i : i + n]
        if ngram in ngrams:
            ngrams[ngram].append(i)
        else:
            ngrams[ngram] = [i]

    multiple_ngrams = {
        key: [ngrams[key][i + 1] - ngrams[key][i] for i in range(len(ngrams[key]) - 1)]
        for key, value in ngrams.items()
        if len(value) > 1
    }

    distances = []
    for value in multiple_ngrams.values():
        distances += value

    distances.sort()
    return distances


def find_ngrams_frequences(text, n=2):
    """
    Computes the frequencies of n-grams (substrings of length `n`) in the text.

    Args:
        text (str): The input text.
        n (int): The length of the n-grams to consider (default is 2).

    Returns:
        dict: A dictionary of n-grams and their frequencies, sorted in descending order.
    """
    ngrams = {}
    for i in range(len(text) - n + 1):
        ngram = text[i : i + n]
        if ngram in ngrams:
            ngrams[ngram] += 1
        else:
            ngrams[ngram] = 1
    return {
        k: v for k, v in sorted(ngrams.items(), key=lambda item: item[1], reverse=True)
    }
