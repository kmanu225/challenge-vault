# ====================================================
# Root-me "Vecteur d'initialisation" challenge cryptanalysis
# https://www.root-me.org/fr/Challenges/Cryptanalyse/Vecteur-d-initialisation
# ====================================================

"""
Goal: The idea is to use the XOR operation between:
- the first locally decrypted block (using a fixed chosen IV)
- the chosen IV itself
in order to obtain the remotely encrypted first block.
Then, since we know the first plaintext block (known plaintext) and the first block ciphertext,
we can recover the original remote IV by:

IV = first_block_ciphertext XOR first_block_plaintext
"""
