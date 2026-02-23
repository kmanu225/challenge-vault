from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

class authenticated_AES:
    def __init__(self, key: bytes, mode: str, nonce: bytes):
        """
        CCM : Length of parameter 'nonce' must be in the range 7..13 bytes
        OCB : Nonce must be at most 15 bytes long
        SIV : Key length must be twice the required key length of the block cipher (32 bytes for AES-128, 48 bytes for AES-192, 64 bytes for AES-256)
        """
        self.key = key
        self.mode = mode.upper()
        self.nonce = nonce
        self.MODES = ["CCM", "EAX", "GCM", "OCB", "SIV"]

    def encrypt(self, plaintext: bytes, associated_data: bytes = None):
        # Initialize cipher
        if self.mode in self.MODES:
            cipher = AES.new(
                self.key, getattr(AES, f"MODE_{self.mode}"), nonce=self.nonce
            )

        else:
            raise ("Unsupported AEAD mode!")

        if associated_data:
            cipher.update(associated_data)

        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        return ciphertext, tag

    def decrypt(self, ciphertext: bytes, tag: bytes, associated_data: bytes):
        if self.mode in self.MODES:
            cipher = AES.new(
                self.key, getattr(AES, f"MODE_{self.mode}"), nonce=self.nonce
            )
        else:
            raise ("Unsupported AEAD mode!")

        if associated_data:
            cipher.update(associated_data)

        try:
            return cipher.decrypt_and_verify(ciphertext, tag)
        except:
            raise ("Key incorrect or message corrupted!")