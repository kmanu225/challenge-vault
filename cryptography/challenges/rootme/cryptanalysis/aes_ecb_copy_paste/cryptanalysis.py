# ====================================================
# Root-me "AES-ECB Copy-Paste" challenge cryptanalysis
# https://www.root-me.org/fr/Challenges/Cryptanalyse/AES-ECB-Copy-Paste
# ====================================================


# Tips:
#  - AES block size is 16 bytes. Work in 16-byte units (not fixed hex offsets).
#  - When manipulating ciphertext hex, remember: 16 bytes = 32 hex characters.
#  - You do not need to get the exact JSON {"username": "admin", "isAdmin": true},


from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


# AES-128 key (16 bytes)
key = b"deadbeefdeadbeef"
cipher = AES.new(key, AES.MODE_ECB)

# -------------------------
# Target plaintext (admin)
# -------------------------
# This is the "desired" JSON we want to obtain after decryption.
# It should be treated as bytes. For the cut-and-paste trick to work
# predictably, the content of "data" should align to AES blocks.
# Note that the JSON is aligned to 16 bytes by adding a fake entry. Being aligned to 
# 16 bytes is essential to control what goes into each AES block. That is the reason why we do not use the simple JSON {"username": "admin", "isAdmin": true} which is only 38 bytes long.
desired_admin_json = b'{"username": "admin", "isAdmin": true, "fakeKey": "myFakeEntry"}'
print("desired_admin_json length:", len(desired_admin_json))  # length in bytes

# -------------------------
# Attacker-controlled input
# -------------------------
# We craft an input such that, after padding, blocks align in a way that
# allows us to swap ciphertext blocks and obtain a valid admin token.
# "padpadpadpad" is just filler to ensure data will be aligned to 16 bytes.
my_username = 'admin", "isAdmin": true, "fakeKey": "myFakeEntry"}padpadpadpad'

# Build the JSON that the vulnerable service would encrypt for us:
data = b'{"username": "%s", "isAdmin": false}' % (my_username.encode())
print("data length:", len(data))
print("data:", data)

# -------------------------
# PKCS#7 padding (block size 16)
# -------------------------
# pad() produces valid PKCS#7 padded bytes. Even if the plaintext is a
# multiple of 16 bytes, pad() will append a whole extra block of value 0x10.
p_admin = pad(desired_admin_json, 16)
p_data  = pad(data, 16)
print("padded admin length:", len(p_admin))
print("padded data  length:", len(p_data))

# Show padded last blocks so you can verify they share the same last 16 bytes
# (useful because identical suffix/padding allows some block-swaps to be valid)
print("admin padded last block:", p_admin[-16:])
print("data padded last block :", p_data[-16:])
print("Last 16 bytes identical?", p_admin[-16:] == p_data[-16:])

# -------------------------
# Split padded plaintexts into 16-byte blocks (for inspection)
# -------------------------
admin_blocks = [p_admin[i:i+16] for i in range(0, len(p_admin), 16)]
data_blocks  = [p_data[i:i+16]  for i in range(0, len(p_data), 16)]

print("\nAdmin padded blocks:")
for i, b in enumerate(admin_blocks):
    print(f"  block {i:02d}: {b}")

print("\nData padded blocks:")
for i, b in enumerate(data_blocks):
    print(f"  block {i:02d}: {b}")

# -------------------------
# Find first block index where padded plaintexts differ
# -------------------------
first_diff_index = None
max_blocks = min(len(admin_blocks), len(data_blocks))
for i in range(max_blocks):
    if admin_blocks[i] != data_blocks[i]:
        first_diff_index = i
        break

# If one plaintext is a prefix of the other, the differing index is the shorter length
if first_diff_index is None:
    if len(admin_blocks) != len(data_blocks):
        first_diff_index = max_blocks
    else:
        first_diff_index = max_blocks  # identical (unlikely here)

print("\nFirst differing block index:", first_diff_index)

# -------------------------
# Encrypt padded plaintexts
# -------------------------
# IMPORTANT: encrypt raw padded bytes and keep ciphertext as bytes.
ct1 = cipher.encrypt(p_admin)  # ciphertext corresponding to desired_admin_json
ct2 = cipher.encrypt(p_data)   # ciphertext corresponding to data

# Split ciphertexts into 16-byte blocks for manipulation
ct1_blocks = [ct1[i:i+16] for i in range(0, len(ct1), 16)]
ct2_blocks = [ct2[i:i+16] for i in range(0, len(ct2), 16)]

print("\nNumber of ciphertext blocks: ct1=", len(ct1_blocks), "ct2=", len(ct2_blocks))

# -------------------------
# Build the crafted ciphertext
# -------------------------
# Strategy: take ciphertext blocks from ct2 up to the first differing index,
# then take the remaining blocks from ct1. When the server decrypts this
# crafted ciphertext block-by-block, the prefix will correspond to the
# plaintext blocks from `data` and the suffix to `desired_admin_json`.
crafted_blocks = ct2_blocks[:first_diff_index] + ct1_blocks[first_diff_index:]
crafted_ct = b"".join(crafted_blocks)

# For display/debugging: hex representations
token1_hex = hexlify(ct1).decode()
token2_hex = hexlify(ct2).decode()
crafted_hex = hexlify(crafted_ct).decode()

print("\ntoken1 (hex):", token1_hex)
print("token2 (hex):", token2_hex)
print("crafted (hex):", crafted_hex)

# Check whether we reproduced token1 exactly
print("\nCrafted equals token1 ?", crafted_ct == ct1)

# -------------------------
# Verify decryption of crafted ciphertext
# -------------------------
# Decrypt the crafted ciphertext to see what plaintext would be produced.
dec = cipher.decrypt(crafted_ct)
try:
    # Remove PKCS#7 padding to get the original JSON bytes if padding is valid.
    unp = unpad(dec, 16)
    print("\nDecrypted & unpadded crafted plaintext:")
    print(unp)
    print("Matches desired_admin_json ?", unp == desired_admin_json)
except ValueError:
    # If unpad fails, padding was invalid — still print raw decrypted bytes for analysis
    print("\nDecrypted data (raw bytes, unpad failed):")
    print(dec)
