from utils import get_frequences, striper
from bruteforce import rot_right


def get_cesar_key(frequence): return ord(
    list(frequence.keys())[0]) - ord("e")


def decrypt_cesar(ciphertext): return rot_right(
    ciphertext, -get_cesar_key(get_frequences(ciphertext))
)


if __name__ == "__main__":
    cipher_text = "shqhykpuplylklslnbtlzjlzabuwlbkljlchuaxbhuktltlxbhukvuuvbzshzlyaxblsslmbtlavbasltvuklhklshwlpulvuzlkpaxbljhulkvpawhzlayljvvsklaylkbaplyztvuklvbklcpcylwlukhuashnblyyljhylukobtislbulzljvukl"

    cipher_text = striper(cipher_text)
    print(decrypt_cesar(cipher_text))
