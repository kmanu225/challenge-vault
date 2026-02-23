from Crypto.PublicKey import RSA
import os
import pathlib
import math


root = pathlib.Path(__file__).parent.absolute()
# files = ["key1_pub.pem", "key2_pub.pem"]
files = ["public.pem"]

for file_name in files:
    with open(os.path.join(root, file_name), "rb") as f:
        data = f.read()
        mykey = RSA.import_key(data)

        n = mykey.n
        e = mykey.e
        print(f"n ({int(math.log2(n)) + 1} bits): {n}")
        print(f"e (public): {e}")
        # print(f"d (private): {mykey.d}")
    print()
    