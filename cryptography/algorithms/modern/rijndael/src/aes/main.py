from primitives import *


if __name__ == "__main__":
    # Test  bytes2matrix
    print("Test  bytes2matrix")
    print(f"{bytes2matrix(b'crypto{inmatrix}')}\n")

    # Test  matrix2bytes
    print("Test  matrix2bytes")
    matrix = [
        [99, 114, 121, 112],
        [116, 111, 123, 105],
        [110, 109, 97, 116],
        [114, 105, 120, 125],
    ]
    print(f"{matrix2bytes(matrix)}\n")


    # Test  add_round_key
    print("Test  add_round_key")
    state = [
        [206, 243, 61, 34],
        [171, 11, 93, 31],
        [16, 200, 91, 108],
        [150, 3, 194, 51],
    ]

    round_key = [
        [173, 129, 68, 82],
        [223, 100, 38, 109],
        [32, 189, 53, 8],
        [253, 48, 187, 78],
    ]

    print(f"{matrix2bytes(add_round_key(state, round_key))}\n")

    # Test  sub_bytes
    print("Test  sub_bytes")

    state = [
        [251, 64, 182, 81],
        [146, 168, 33, 80],
        [199, 159, 195, 24],
        [64, 80, 182, 255],
    ]
    print(f"{matrix2bytes(sub_bytes(state, sbox=inv_s_box))}\n")

    # Test  shift_rows and inv_shift_rows
    print("Test  shift_rows and inv_shift_rows")
    state = [
        [108, 106, 71, 86],
        [96, 62, 38, 72],
        [42, 184, 92, 209],
        [94, 79, 8, 54],
    ]
    inv_mix_columns(state)
    inv_shift_rows(state)
    print(f"{matrix2bytes(state)}\n")

    # Test AES-128
    key        = b'rijndaelrijndael'
    plaintext = b'crypto{MYAES128}'
    assert decrypt(key,encrypt(key, plaintext, size="128"),size="128") == plaintext


    # Test AES-192
    key        = b'rijndaelrijndaelrijndael'
    plaintext = b'crypto{MYAES128}'
    assert decrypt(key,encrypt(key, plaintext, size="192"),size="192") == plaintext


    # Test AES-256
    key        = b'rijndaelrijndaelrijndaelrijndael'
    ciphertext = b"\xee\xcfI\x1e-\xc9\xd7-=u\xc4\x8cF\xd56t"
    assert decrypt(key,encrypt(key, plaintext, size="256"),size="256") == plaintext
