from utils import (
    find_ngrams_distances,
    vigenere_to_cesars,
    cesars_to_vigenere,
    decrypt_cesar,
)


def get_l_kasiski(text, l=3):
    """
    Estimates the Vigenère cipher key length using the Kasiski examination method.

    The function identifies repeated n-grams (default length 3) in the text and 
    computes the distances between their occurrences. The most common divisors 
    of these distances are potential key lengths.

    Args:
        text (str): The ciphertext to analyze.
        l (int): The length of n-grams to look for (default is 3).

    Returns:
        tuple:
            - int: The most likely key length (most common divisor).
            - list[int]: All distances between repeating n-grams.
    """
    distances = find_ngrams_distances(text, l)
    return distances[0], distances


decrypt_kasiski = lambda text, l: cesars_to_vigenere(
    [decrypt_cesar(text) for text in vigenere_to_cesars(text, l)]
)


if __name__ == "__main__":
    cipher_text = "zbpuevpuqsdlzgllksousvpasfpddggaqwptdgptzweemqzrdjtddefekeferdprrcyndgluaowcnbptzzzrbvpssfpashpncotemhaeqrferdlrlwwertlussfikgoeuswotfdgqsyasrlnrzppdhtticfrciwurhcezrpmhtpuwiyenamrdbzyzwelzucamrptzqseqcfgdrfrhrpatsepzgfnaffisbpvdblisrplzgnemswaqoxpdseehbeeksdptdttqsdddgxurwnidbdddplncsd"

    print(get_l_kasiski(cipher_text, 3))
    print(decrypt_kasiski(cipher_text, 4))
