from utils import FRENCH_FREQUENCY, score, rot_right

def strong_rot_bruteforce(cipher_text, alphabet_frequencies=FRENCH_FREQUENCY) -> list:
    plausible_texts = []
    for i in range(255):
        decoded = bytes([(b + i) % 256 for b in cipher_text])
        plausible_texts.append((i, score(decoded.decode('latin-1', errors='ignore'), alphabet_frequencies), decoded))
    plausible_texts.sort(key=lambda x: x[1], reverse=True)
    return plausible_texts


def weak_rot_bruteforce(cipher_text, alphabet_frequencies=FRENCH_FREQUENCY) -> list:
    plausible_texts = []
    for i in range(26):
        decoded = rot_right(cipher_text, i)
        plausible_texts.append((i, score(decoded, alphabet_frequencies), decoded))
    plausible_texts.sort(key=lambda x: x[1], reverse=True)
    return plausible_texts


if __name__ == "__main__":
    cipher_text = "shqhykpuplylklslnbtlzjlzabuwlbkljlchuaxbhuktltlxbhukvuuvbzshzlyaxblsslmbtlavbasltvuklhklshwlpulvuzlkpaxbljhulkvpawhzlayljvvsklaylkbaplyztvuklvbklcpcylwlukhuashnblyyljhylukobtislbulzljvukl"


    for decalage, sc, text in weak_rot_bruteforce(cipher_text)[:1]:
        print(f"Decalage: {decalage}, Score: {sc}.\nText: {text}\n")
        
    for decalage, sc, text in strong_rot_bruteforce(bytes(cipher_text, "utf-8"))[:1]:
        print(f"Decalage: {decalage}, Score: {sc}.\nText: {text}\n")
