from passlib.hash import msdcc, msdcc2, lmhash, nthash


secret = "password"
username = "Administrator"

print(msdcc.raw(secret, username).hex())
print(msdcc2.raw(secret, username).hex())
print(lmhash.raw(secret).hex())
print(nthash.raw(secret).hex())
