import os
import pathlib
import base64
import gmpy2
from sympy.ntheory.modular import crt
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.PublicKey import RSA

def boradcast_attack(ciphertexts, key_files):
    """
    Performs the Chinese Remainder Theorem (CRT) attack on RSA when the same plaintext
    is encrypted with different moduli but the same small exponent (e.g., e=3).

    Parameters:
    - ciphertexts (list of str): Base64-encoded ciphertexts.
    - key_files (list of str): Paths to the corresponding RSA public key files.

    Returns:
    - str: Decrypted plaintext message.
    """

    # Convert base64 ciphertexts to integers
    c_values = [bytes_to_long(base64.b64decode(c)) for c in ciphertexts]

    # Extract public keys
    e_values = []
    n_values = []
    root = pathlib.Path(__file__).parent.absolute()

    for file_name in key_files:
        with open(os.path.join(root, file_name), "rb") as f:
            key = RSA.import_key(f.read())
            e_values.append(key.e)
            n_values.append(key.n)

    # Ensure all public exponents are the same
    e = e_values[0]
    assert all(e_val == e for e_val in e_values), "All public exponents must be the same!"

    # Solve for m^e using CRT
    m_pow_e, lcm_n = crt(n_values, c_values)

    # Ensure consistency
    assert lcm_n == n_values[0] * n_values[1] * n_values[2]
    for i in range(len(n_values)):
        assert pow(m_pow_e, 1, n_values[i]) == c_values[i]

    # Compute the e-th root to recover the plaintext
    m, exact = gmpy2.iroot(m_pow_e, e)
    if not exact:
        raise ValueError("Failed to extract exact e-th root. Attack might not work.")

    return long_to_bytes(int(m)).decode("utf-8")

# Example Usage
ciphertexts = [
    "vjXJvWis95tc25G+wxC5agClCJFB9vUslFyV+I4bSiwS4Sm6k8eF61EizKo4hZFwROlO3Ci3YQaTrAm+Y9/qEbM7asvwKTePKX+cLVN61l0xxfTL8CdoXkRE2rSczp1AzzmFz83OHgszX/Wf7kgWU4M73+efPvU9FmcWOauakrdJZx8B0ErJ5cYWNS0ZCam0Nlz+pISqdSJ6MSz0Ek62Ulb3ei8I41FOdHtd8mhC7dfpdfmVLOSEW4yEnn5iuMW0ydvW055dodLc9RKcvJafH9e3zf8/S1/RORXZoUHWnBXBEFOl8iVXz70GcDTPzIhxh6imi0ynLbV68qW2vw2XRQ==",
    "Mi4MnobVabt1+Q7R/0aIYBBpeRxPRuR6gkhr/Wbw/D23ywu2KbUYBab2XbEguRz8yzBlxScbFjjb98DuILxURoFN8lNKVJLS3d/IrGGr0hjocbz27uBS97hseX0S4nd+BL6LUn0o7qe/yCqk7Y0tEhhcuSMrGn/l9N/6UjgN38TyoyvVbd1UH6BHGLdj9g5JRBKAvcGumymfiE0qS7IOnM3mN5W8gRJaEGDkhDim21Pm1Yg2GRBJ+z7C8AEy+Dz6OFvWuDsY24Gb+643D7KrmFObJ1n8Qyme/Y1bfvBkG+xdvGoBzyQrlDT12Qjkfoqb37HNrGUUD5cj2q54gyp80w==",
    "hMQVVspFGh7NxCqLf7DVto3OxgDLn9n9gOCjOjEOYhi/VwZ3adFsbBL+zLZxYNdkKLNWCNRktRwpnWriEsW1uDnVt2LbxSLvjvRKbR/hyvpY+0UUZFS6wCWQjGyxUydDxQ88jNM5dY58/1nxsd04I3n3Mt97SuqwBN1+4VS3SsqtbR0GU1C7ODkPoCeGVd3PNkGHPgbT7QzMwxl63Pl3i/sp0I2/gqSnKu5CDS7e2WELz0hfiOJ2v2RvIon2EEbPwx1/6zxZlMhHuGXHNZKDtyqe6Dd+EIjpwhQFW3eH7fDIirRbaPPXAYsoypS5eFD3mIWUs4yVOH9ykkdKQ9FNwg=="
]
key_files = ["clef0_pub.pem", "clef1_pub.pem", "clef2_pub.pem"]

# Run the attack
plaintext = boradcast_attack(ciphertexts, key_files)
print(f"Secret message:\n{plaintext}")
