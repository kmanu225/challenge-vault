# ------------------------
# Mutual Index of Coincidence (MIC) method for Vigenère Cipher analysis
# ------------------------

from utils import (
    get_cesar_key,
    rot_right,
    get_frequences,
    rot_left,
    vigenere_to_cesars,
    cesars_to_vigenere,
    MIC,
    LATIN_ALPHABET,
    IC_FR,
)



def IC(text):
    """
    Computes the Index of Coincidence (IC) of a text.

    IC measures how likely it is to randomly pick two identical letters from the text.

    Args:
        text (str): The input text to analyze.

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


def get_l_mic(cipher_text, max_l=10, ic_lg=IC_FR):
    """
    Estimates the key length of a Vigenère cipher using the Mean Index of Coincidence.

    For each possible key length up to `max_l`, the function splits the ciphertext into
    Caesar-like components and calculates the average IC. If it exceeds a threshold (`ic_lg`),
    it is likely to be the correct key length.

    Args:
        cipher_text (str): The encrypted Vigenère ciphertext.
        max_l (int): The maximum key length to test (default 10).
        ic_lg (float): The reference IC value (default is French IC).
    """
    for i in range(1, max_l + 1):
        mean_ic = 0
        cesar_texts = vigenere_to_cesars(cipher_text, i)
        for cesar_text in cesar_texts:
            mean_ic += IC(cesar_text)
        mean_ic /= len(cesar_texts)
        
        if mean_ic > ic_lg:
            print(
                f" {i} : {round(mean_ic, 3)} | delta_ic : {round(abs(mean_ic - IC_FR), 3)}"
            )


def decrypt_vigenere_mic(text, l):
    """
    Attempts to decrypt a Vigenère cipher using MIC (Mutual Index of Coincidence) analysis.

    It assumes the first Caesar stream gives a good key guess, then aligns the remaining
    Caesar components to it using MIC. It reconstructs the decrypted message after aligning.

    Args:
        text (str): The Vigenère-encrypted ciphertext.
        l (int): The suspected or known key length.

    Returns:
        str: The decrypted plaintext.
    """
    # Split the ciphertext into l Caesar ciphers
    cipher_cesar_texts = vigenere_to_cesars(text, l)
    Y_0 = cipher_cesar_texts[0]

    # Guess the key shift of the first Caesar cipher
    delta_0 = get_cesar_key(get_frequences(Y_0))
    decrypted_cesar_texts = [rot_left(Y_0, delta_0)]

    # Align the other Caesar streams to Y_0 using MIC
    for i in range(1, l):
        for delta in range(26):
            Y_i = cipher_cesar_texts[i]
            if MIC(Y_0, rot_right(Y_i, delta)) > IC_FR:
                decrypted_cesar_texts.append(rot_left(Y_i, delta_0 - delta))

    # Reconstruct the full decrypted message
    return cesars_to_vigenere(decrypted_cesar_texts)


if __name__ == "__main__":
    cipher_text_1= "ufzbdemltfnlfgmoneefrttkophfeiuplbfxbtrmltfczfygipzjygblyyjivigpfpffveptmfmfavjyxbymfcisptpyhjeuvppmpemwejeiopjgpxbweqpgipwpygilrelmmciqcmtpioeinzmhyejeiuditpwqlhstpmpwslgpcrjpwqlvmpwfw"
           
    get_l_mic(cipher_text_1)
    print(decrypt_vigenere_mic(cipher_text_1, 3))

