# Root-me Service - Timing attack challenge cryptanalysis
# https://www.root-me.org/fr/Challenges/Cryptanalyse/Service-Timing-attack
# ====================================================

# The idea is to exploit timing differences in server responses to deduce the correct password 
# character by character.
# Tips: Measure the average comparison time for each character in the password.

from pwn import *
from time import time

ALPHABET = string.printable[:-5]

r = remote("challenge01.root-me.org", 51015)
start = r.recvline()
print(f"Message from server:\n{start.decode('utf-8')}")

# Test timing for each character in the alphabet
cmp_time = {}
for char in ALPHABET:
    r.sendline(char.encode())
    start = time()
    reponse = r.recvline()
    end = time()
    time_c = end - start
    cmp_time[char] = time_c
    print("Character tested:", char, "| Time taken:", time_c)
    
# Determine character which took the longest time
COMP_CHAR = max(cmp_time, key=cmp_time.get)
print(f"Character with max time: {COMP_CHAR} | time: {cmp_time[COMP_CHAR]} | Rounded: {round(cmp_time[COMP_CHAR], 1)}")

# Determine average time for an incorrect character
total_time = sum(cmp_time.values()) - cmp_time[COMP_CHAR]
avg_time = total_time / (len(ALPHABET) - 1)
print(f"Average time for incorrect characters: {avg_time}")
r.close()
