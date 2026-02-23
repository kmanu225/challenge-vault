from utils import isInvertable, randint, invert, randint
from weierstrass import Curve, Point, INF


class EC_Key:
    """
    Elliptic Curve Cryptography Key.\n
    @param curve: Elliptic curve.
    @param P: Elliptic curve point public parameter.
    @param l: Integer private parameter.
    """

    def __init__(self, curve: Curve, P: Point, l: int):
        self.curve = curve
        self.P = P
        self.Q = l * P
        self.l = l

    def pubKey(self):
        """
        Elliptic Curve Cryptography public key parameters.\n
        @return :
        - p: Prime number defining the group Z/pZ.\n
        - curve: Elliptic curve.\n
        - cardinality: Elliptic curve cardinality.\n
        - P: Elliptic curve point public parameter.\n
        - Q: Elliptic curve point public parameter
        """
        return [
            self.curve.p,
            self.curve.cardinality(),
            self.curve,
            self.P,
            self.Q,
        ]

    def privKey(self):
        return self.l

    def __str__(self):
        pubkey = [str(i) for i in self.pubKey()]
        privkey = self.privKey()
        return f"Key(pubkey = {pubkey}, privkey = {privkey})"


class Elgamal:
    """
    Elgamal encryption scheme.
    """

    def encrypt(self, curve: Curve, P: Point, Q: Point, M: Point):
        """
        @param curve : Elliptic Curve
        @param P : Base point.
        @param Q : Public key.
        @param M: Message to encrypt.
        """
        p = curve.p
        k = randint(1, p - 2)
        C1 = k * P
        C2 = M + k * Q
        return [C1, C2]

    def decrypt(self, l: int, C1: Point, C2: Point):
        """
        @param l : private key.
        @param C1: Point.
        @param C2: Point.
        """
        return C2 - l * C1


class ECDSA:
    """
    Elliptic Curve Digital Signature Algorithm.\n
    @param key: Elliptic Curve Cryptography Key.
    """

    def __init__(self, curve: Curve):
        self.curve = curve

    def sign(self, G: Point, n: int, s: int, m: int):
        """
        @param G : Base point for the signature.
        @param n : Order of base point G.
        @param s : Private key.
        @param m : Message to sign.
        """
        k = randint(1, n - 1)
        kG = k * G
        x = pow(kG.x, 1, n)

        if x == 0:
            return self.sign(G, n, s, m)

        try:
            if isInvertable(k, n):
                k_inv = invert(k, n)
                y = pow(k_inv * (m + s * x), 1, n)
                if y == 0:
                    return self.sign(G, n, s, m)
                return {"x": x, "y": y}
            else:
                return self.sign(G, n, s, m)
        except ValueError:
            return self.sign(G, n, s, m)

    def verify(self, G: Point, n: int, Q: Point, sig: tuple[int], m: int) -> bool:
        """
        @param G : Base point for the signature.
        @param n : Order of base point G.
        @param Q : Public key.
        @param sig : Message to check signature.
        @param m : Message which has been signed
        """
        x, y = sig["x"], sig["y"]
        O = Point(INF, INF, self.curve.a, self.curve.b, self.curve.p)
        if Q == O or not self.curve.onCuve(Q.x, Q.y):
            print("infinity 1")
            return False

        elif n * Q != O:
            print("infinity 2")
            return False

        elif 1 > x or x > n - 1 or 1 > y or y > n - 1:
            print("beyond")
            return False

        y_inv = invert(y, n)
        u = pow(m * y_inv, 1, n)
        v = pow(x * y_inv, 1, n)
        V = u * G + v * Q
        print("Verify", pow(V.x, 1, n), x)

        return pow(V.x, 1, n) == x


def testElgamal():
    a, b, p = -3, 1, 1217
    print(f"Initializing elliptic curve with parameters: a = {a}, b = {b}, p = {p}.")
    curve = Curve(a, b, p)

    l = 83
    P = Point(743, 473, a, b, p)
    Q = l * P
    keys = EC_Key(curve, P, l)
    print(f"Generating EC key pair with private key length: {l}\n{keys}")

    M = Point(1130, 1138, a, b, p)
    print(f"Message to encrypt (as a point on the curve): M = {M}")

    elgamal = Elgamal()
    C1, C2 = elgamal.encrypt(curve, P, Q, M)
    print(f"Encrypted message: C1 = {C1}, C2 = {C2}")

    decM = elgamal.decrypt(l, C1, C2)
    print(f"Decrypted message: {decM}")

    # Verify if decryption was successful
    print(f"Decryption succeeded: {M == decM}")


def testECDSA():
    a, b, p = -3, 1, 1217
    curve = Curve(a, b, p)
    print(f"Initializing elliptic curve with parameters: a = {a}, b = {b}, p = {p}")

    n, G = curve.get_prime_order()
    print(f"Base point {G} of order {n} : nG = {n*G}.")

    m = 20
    s = randint(1, n - 1)
    Q = s * G
    dsa = ECDSA(curve)
    sig = dsa.sign(G, n, s, m)
    print(sig)

    vrfy = dsa.verify(G, n, Q, sig, m)
    if vrfy:
        print("Verification Succeeded!")
    else:
        print("Verification Failed!")


if __name__ == "__main__":
    testElgamal()
    testECDSA()
