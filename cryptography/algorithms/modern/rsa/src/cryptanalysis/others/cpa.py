from pwn import *
from Crypto.Util.number import long_to_bytes

from gmpy2 import powmod, invert

encrypt = lambda m, e, n: powmod(m, e, n)
inverse_modulo = lambda x, n: invert(x, n)

n = 456378902858290907415273676326459758501863587455889046415299414290812776158851091008643992243505529957417209835882169153356466939122622249355759661863573516345589069208441886191855002128064647429111920432377907516007825359999
e = 65537
hidden_m = 41662410494900335978865720133929900027297481493143223026704112339997247425350599249812554512606167456298217619549359408254657263874918458518753744624966096201608819511858664268685529336163181156329400702800322067190861310616

# Connexion au serveur
r = remote("challenge01.root-me.org", 51031)

# Réception de la première ligne du serveur
reponse = r.recvn(83)
print(f"Réponse du serveur:\n{reponse.decode()}")

# Chaîne à envoyer au serveur
c_ = encrypt(2, e, n)
inv_2 = inverse_modulo(2, n)
s = hidden_m * c_

# # Envoi de la chaîne au serveur
try:
    r.sendline(str(s).encode())
except Exception as e:
    print(f"Erreur lors de l'envoi de la chaîne : {e}")
    r.close()
    exit(1)

# Réception de la réponse du serveur
response = r.recvlines(2)[1][32:]

# Affichage de la réponse du serveur
print(f"Réponse du serveur : {int(response.decode())}")

# Fermeture de la connexion
r.close()

m = encrypt(int(response.decode()) * inv_2, 1, n)
print(f"{long_to_bytes(m)}")
