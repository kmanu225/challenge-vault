# Root-me — "Hash DCC" challenge (Cryptanalysis)

**Challenge:** Hash DCC — [https://www.root-me.org/fr/Challenges/Cryptanalyse/Hash-DCC](https://www.root-me.org/fr/Challenges/Cryptanalyse/Hash-DCC)

---

## Introduction

This challenge uses a Windows credential dump (typical of tools like Mimikatz). The goal is to identify and crack the relevant cached domain credentials (DCC / MSCache).

---

## SAM (Security Account Manager) — Local secrets

The SAM hive stores local account hashes. Example dump (format `username:uid:rid:lmhash:nthash`):

```text
Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
ASPNET:1025:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DBAdmin:1028:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
sshd:1037:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
service_user:1038:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
```

> Note: `aad3b435b51404eeaad3b435b51404ee` (LM) and `31d6cfe0d16ae931b73c59d7e0c089c0` (NT) are default placeholders used when no password is set or the value is unavailable. These are not useful to crack and can be ignored.

---

## Cached domain logon information (MSCache / DCC)

Cached domain logon entries store offline artifacts for domain logons. They are good targets for offline cracking when the domain controller is unavailable. Example dump (format `DOMAIN/USER:hash`):

```text
ROOTME.LOCAL/PODALIRIUS:$DCC2$10240#PODALIRIUS#9d3e8dbe4d9816fa1a5dda431ef2f6f1
ROOTME.LOCAL/SHUTDOWN:$DCC2$10240#SHUTDOWN#9d3e8dbe4d9816fa1a5dda431ef2f6f1
ROOTME.LOCAL/Administrator:15a57c279ebdfea574ad1ff91eb6ef0c:Administrator
```

The two first secrets use the DCC2 (MSCache v2) algorithm while Administrator secret is hash using MSCache v1. The challenge title points to these hashes.

---

## LSA (Local Security Authority) Secrets — Additional data

LSA secrets contain several useful items related to cached/domain credentials:

* **DPAPI_SYSTEM** — DPAPI machine keys (used to decrypt DPAPI blobs).
* **NL$KM** — Key material used to protect cached domain credentials (MsCache) stored in the SECURITY hive (`SECURITY\Cache`).
* **$MACHINE.ACC** — Computer account credentials (when joined to AD).
* **DEFAULTPASSWORD** — Cleartext value when Windows autologon is configured.
* ***SC**** keys — Service account secrets (non-interactive service credentials), may be local or domain accounts.

These keys can assist in decrypting or recovering other stored credentials, and are commonly extracted from the `SYSTEM`/`SECURITY` registry hives.

### Preparing hashes for cracking

**For John the Ripper** (format `mscash`):

`john_hashes.txt` (John format):

```bash
echo "Administrator:15a57c279ebdfea574ad1ff91eb6ef0c" > john_hashes.txt
```

**John command:**

```bash
john --format=mscash --wordlist=/usr/share/wordlists/rockyou.txt john_hashes.txt
john --format=mscash --show john_hashes.txt
```

