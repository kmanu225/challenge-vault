from operation import *

    
if __name__ == "__main__":
    
    # TEST AES AEAD
    aes_256_key = get_random_bytes(32)
    aes_192_key = get_random_bytes(24)
    aes_128_key = get_random_bytes(16)
    keys = [aes_128_key, aes_192_key, aes_256_key]

    plaintext = b"crypto{AES}"

    for key in keys:
        try:
            aead = ["CCM", "EAX", "GCM", "OCB", "SIV"]
            associated_data = get_random_bytes(16)

            for mode in aead:
                if mode == "SIV":
                    key = get_random_bytes(2*len(key))
                    nonce = get_random_bytes(16)

                elif mode == "CCM":
                    nonce = get_random_bytes(13)
            
                elif mode == "OCB":
                    nonce = get_random_bytes(15)

                else:
                    nonce = get_random_bytes(16)
                   

                aes = authenticated_AES(key, mode, nonce)
                ciphertext, tag = aes.encrypt(plaintext, associated_data)
                print(f"AES-{len(key*8)}-{mode} Ciphertext: {ciphertext}, Tag: {tag}")

                aes = authenticated_AES(key, mode, nonce)
                decrypted_text = aes.decrypt(ciphertext, tag, associated_data)
                assert decrypted_text == plaintext
        except Exception as e:
            print(f"Error: {e}")

