# ====================================================
# Root-me "Encodage Ascii" challenge cryptanalysis
# https://www.root-me.org/fr/Challenges/Cryptanalyse/Encodage-ASCII
# ====================================================

import os

basedire = os.path.dirname(__file__)
cipher_text = open(os.path.join(basedire, "ch8.txt"), "r").read()
print(bytes.fromhex(cipher_text))