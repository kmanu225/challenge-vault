from utils import (
    ORD_LOWER_A,
    IC,
    get_frequences,
    striper,
    get_cesar_key,
    vigenere_to_cesars,
    cesars_to_vigenere,
    rot_left,
)

def transform_text(text, l):
    """
    Applies a transformation to the ciphertext by shifting each letter
    using the value of the letter `l` positions earlier.

    Args:
        text (str): The input ciphertext.
        l (int): The assumed key length.

    Returns:
        str: Transformed text based on shifting by previous characters.
    """
    transformed_text = text[:l]
    n = len(text)
    for i in range(l, n):
        transformed_text += rot_left(
            text[i], ord(transformed_text[i - l]) - ORD_LOWER_A
        )
    return transformed_text


def extract_text(text):
    """
    Breaks transformed text into segments of even and odd indexed characters
    based on possible key lengths (1 to 9).

    Args:
        text (str): The ciphertext.

    Returns:
        dict[int, list[str]]: Mapping of key length to list of segments.
    """
    n = len(text)
    segments = dict()

    for l in range(1, 10):
        transformed_text = transform_text(text, l)
        segments_l = []

        sous_text = ""
        for i in range(l):
            # Even indexed segment
            t = 0
            while 2 * t * l + i < n:
                sous_text += transformed_text[2 * t * l + i]
                t += 1
            segments_l.append(sous_text)
            sous_text = ""

            # Odd indexed segment
            t = 0
            while (2 * t + 1) * l + i < n:
                sous_text += transformed_text[(2 * t + 1) * l + i]
                t += 1
            segments_l.append(sous_text)
            sous_text = ""
        segments[l] = segments_l

    return segments


def compute_ic(text):
    """
    Computes the average Index of Coincidence (IC) for each possible key length.

    Args:
        text (str): The input ciphertext.

    Returns:
        dict[int, float]: Mapping of key length to average IC value.
    """
    segments = extract_text(text)
    ic_texts = dict()
    for l, segment in segments.items():
        ic_text = 0
        for s in segment:
            ic_text += IC(s)
        ic_text /= len(segment)
        ic_texts[l] = ic_text
    return ic_texts


def decrypt_text(cipher_text, l):
    """
    Decrypts a ciphertext encrypted with a doubled-character Vigenère cipher.

    Args:
        cipher_text (str): The ciphertext to decrypt.
        l (int): The estimated Vigenère key length.

    Returns:
        str: The decrypted plaintext.
    """
    # Step 1: Split into Caesar cipher segments
    cesars = vigenere_to_cesars(cipher_text, l)

    # Step 2: Reverse the internal transformation c -> d
    for j in range(l):
        cesar = cesars[j]
        new_cesars = cesar[0]
        for i in range(1, len(cesar)):
            new_cesars += rot_left(cesar[i], ord(new_cesars[-1]) - ORD_LOWER_A)
        cesars[j] = new_cesars

    # Step 3: Split each Caesar into even and odd segments
    cesars_evens = [cesar[::2] for cesar in cesars]
    cesars_odds = [cesar[1::2] for cesar in cesars]
    key = ""

    # Step 4: Estimate the Caesar key shifts from frequency analysis
    for i in range(l):
        key_odd = get_cesar_key(get_frequences(cesars_odds[i]))
        key_even = get_cesar_key(get_frequences(cesars_evens[i]))
        key += chr(key_even + ORD_LOWER_A)

        # Decrypt each segment
        cesars_odds[i] = rot_left(cesars_odds[i], key_odd)
        cesars_evens[i] = rot_left(cesars_evens[i], key_even)

    # Step 5: Reconstruct the original segments by merging evens and odds
    for i in range(l):
        new_cesars = ""
        for j in range(len(cesars[i])):
            if j % 2 == 0:
                new_cesars += cesars_evens[i][j // 2]
            else:
                new_cesars += cesars_odds[i][j // 2]
        cesars[i] = new_cesars

    # Step 6: Combine Caesar segments back into a full decrypted text
    vigenere = cesars_to_vigenere(cesars)
    return vigenere


if __name__ == "__main__":
    cipher_text = "crlzfzdwkpavlfedmkeluqtztmeizcxrgqqyehplrrseeguffmfwszfdemnqtpnutldgaxuxermjrpakghwgxugnijrzyjasmapypzycpoybsgigtxvnmxhuxabywupvugelzhemmdratrflissvoftwdebigtbshchilbshgdeptxakwxeaxtpwyalztaeitlmfidzmsejauevoesswhjasmjaiulpxgnrlgiljcwyetbshmtinhulwsfrvewlweeueztrsgiuhcmehzsfvmgrqxavnnajixakkumlgjunyfucgnkmdeseeiztrhnvvhsquimfvhyjmhyjgifvqwlhiuuuepnjesydyajdxzgzhakukcczkzugttrzjmujmvhyfnwzvpdjaolrkoecmmpxwwpbwzwwutjhsavwhssldzensbqperskudgxlysrlsibycjwygwmhxgcvwsyuaqmvccmbjjmksyxsqxplbgsaivkpljgrrohlnruihgmsxqcilzcimeoiwvkingbbzrymmfiviqiydcqwflqwxlvlzw"
    cipher_text = striper(cipher_text)
    print(compute_ic(cipher_text))
    print(decrypt_text(cipher_text, 4))
