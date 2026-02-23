import base64
from Crypto.Util.number import long_to_bytes, inverse

def common_modulus_attack(n, e1, e2, c1_b64, c2_b64):
    """
    Performs RSA Common Modulus Attack to recover plaintext.
    
    Parameters:
    - n (int): RSA modulus (same for both keys)
    - e1 (int): First public exponent
    - e2 (int): Second public exponent (coprime with e1)
    - c1_b64 (str): Base64 ciphertext encrypted with e1
    - c2_b64 (str): Base64 ciphertext encrypted with e2

    Returns:
    - str: Decrypted plaintext message
    """
    def gcd_extended(a, b): 
        if a == 0: 
            return b, 0, 1
        gcd, x1, y1 = gcd_extended(b % a, a) 
        x = y1 - (b // a) * x1 
        y = x1 
        return gcd, x, y 

    # Decode ciphertexts
    c1 = int.from_bytes(base64.b64decode(c1_b64), "big")
    c2 = int.from_bytes(base64.b64decode(c2_b64), "big")

    # Extended Euclidean Algorithm to find a, b such that a*e1 + b*e2 = 1
    g, a, b = gcd_extended(e1, e2)
    if g != 1:
        raise ValueError("e1 and e2 must be coprime")

    # Handle negative exponents with modular inverses
    if a < 0:
        c1 = inverse(c1, n)
        a = -a
    if b < 0:
        c2 = inverse(c2, n)
        b = -b

    # Recover plaintext
    m = pow(c1, a, n) * pow(c2, b, n) % n
    return long_to_bytes(m).decode('utf-8')

if __name__ == "__main__":
    n = 121785996773018308653850214729611957957750585856946607620398279656647965006857599756926384863459274369411103073349913717154710735727786240206066327436155758154142877120260776520601315370480059127244029804523614658953301573686851312721445206131147094674807765817210890772194336025491364961932882951123597124291
    e1 = 65537
    e2 = 343223
    c1 = "BzFd4riBUZdFuPCkB3LOh+5iyMImeQ/saFLVD+ca2L8VKSz0+wtTaL55RRpHBAQdl24Fb3XyVg2N9UDcx3slT+vZs7tr03W7oJZxVp3M0ihoCwer3xZNieem8WZQvQvyNP5s5gMT+K6pjB9hDFWWmHzsn7eOYxRJZTIDgxA4k2w="
    c2 = "jmVRiKyVPy1CHiYLl8fvpsDAhz8rDa/Ug87ZUXZ//rMBKfcJ5MqZnQbyTJZwSNASnQfgel3J/xJsjlnf8LoChzhgT28qSppjMfWtQvR6mar1GA0Ya1VRHkhggX1RUFA4uzL56X5voi0wZEpJITUXubbujDXHjlAfdLC7BvL/5+w="

    plaintext = common_modulus_attack(n, e1, e2, c1, c2)
    print("Recovered message:\n", plaintext)
