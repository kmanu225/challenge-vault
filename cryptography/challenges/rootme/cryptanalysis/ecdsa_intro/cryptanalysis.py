# ====================================================
# Root-me "ECDSA - Introduction" challenge cryptanalysis
# https://www.root-me.org/fr/Challenges/Cryptanalyse/ECDSA-Introduction
# ====================================================

# Tips:
# - nonce reuse


import json
import hashlib
from collections import defaultdict
from itertools import combinations
import os
from cryptography.hazmat.primitives.asymmetric import utils
from cryptography.hazmat.primitives.asymmetric import ec
import base64

output = {}
script_dir = os.path.dirname(os.path.abspath(__file__))


# Loop over files m1 to m30
for i in range(1, 31):
    filename = f"m{i}"
    if not os.path.exists(os.path.join(script_dir, "messages/"+filename)):
        print(f"File {filename} not found, skipping.")
        continue
    with open(os.path.join(script_dir, "messages/"+filename), "r", encoding="utf-8") as f:
        lines = f.read().strip().splitlines()
        if len(lines) < 2:
            print(f"File {filename} seems too short, skipping.")
            continue
        message = "\n".join(lines[:-1])
        signature_b64 = lines[-1]
        r, s = utils.decode_dss_signature(base64.b64decode(signature_b64))
        output[filename] = {
            "message": message,
            "signature": signature_b64,
            "r": r,
            "s": s
        }


# Construct the JSON path in the same folder
json_path = os.path.join(script_dir, "messages/messages_and_signatures.json")

# Save to JSON
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=4, ensure_ascii=False)

print(f"Extraction complete! Data saved to {json_path}")


# --- Curve order for secp521r1 (P-521) ---
SECP521R1_ORDER = int(
    "0x01fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409",
    16
)


def parse_int(v):
    """Parse decimal or hex string or int to Python int."""
    if isinstance(v, int):
        return v
    if isinstance(v, str):
        s = v.strip()
        # allow "0x..." hex, or plain hex (only hex digits) — try decimal fallback
        if s.startswith(("0x", "0X")):
            return int(s, 16)
        # if looks like hex (only hex digits), assume hex
        if all(ch in "0123456789abcdefABCDEF" for ch in s) and len(s) > 0:
            # to avoid treating short decimal strings incorrectly, try decimal first
            try:
                return int(s)
            except ValueError:
                return int(s, 16)
        # otherwise decimal
        return int(s)
    raise TypeError("Unsupported type for int parsing")


def sha256_int(msg_bytes):
    return int(hashlib.sha256(msg_bytes).hexdigest(), 16)


def modinv(a, n):
    # uses Python 3.8+ pow with -1
    return pow(a, -1, n)


def recover_from_pair(entry_i, entry_j, n):
    """
    Given two entries that share the same r, compute:
      k = (H_i - H_j) * inv(s_i - s_j) mod n
      d = (s_i * k - H_i) * inv(r) mod n
    Returns (k, d) or raises an exception on failure.
    """
    msg_i = entry_i["message"].encode() if isinstance(
        entry_i["message"], str) else entry_i["message"]
    msg_j = entry_j["message"].encode() if isinstance(
        entry_j["message"], str) else entry_j["message"]
    s_i = parse_int(entry_i["s"])
    s_j = parse_int(entry_j["s"])
    r = parse_int(entry_i["r"])
    H_i = sha256_int(msg_i) % n
    H_j = sha256_int(msg_j) % n

    denom = (s_i - s_j) % n
    if denom == 0:
        raise ValueError("s_i - s_j is 0 mod n; can't invert")

    k = ((H_i - H_j) * modinv(denom, n)) % n
    d = ((s_i * k - H_i) * modinv(r, n)) % n
    return k, d


def main(json_path=json_path, out_path=os.path.join(script_dir, "recovered_keys.json")):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # group filenames by r
    r_map = defaultdict(list)
    for fname, entry in data.items():
        rv = entry.get("r")
        if rv is None:
            continue
        try:
            rv_int = parse_int(rv)
        except Exception:
            rv_int = rv  # keep raw if parse fails
        r_map[rv_int].append(fname)

    results = {}
    for r_val, files in r_map.items():
        if len(files) < 2:
            continue  # only care about reused r

        entries = [(fname, data[fname]) for fname in files]
        pair_results = []
        ds = []
        ks = []
        for (f1, e1), (f2, e2) in combinations(entries, 2):
            try:
                k, d = recover_from_pair(e1, e2, SECP521R1_ORDER)
                pair_results.append({
                    "pair": [f1, f2],
                    "k": k,
                    "k_hex": hex(k),
                    "d": d,
                    "d_hex": hex(d)
                })
                ks.append(k)
                ds.append(d)
            except Exception as ex:
                pair_results.append({
                    "pair": [f1, f2],
                    "error": str(ex)
                })

        # determine if all recovered d values agree (ignoring failed pairs)
        recovered_ds = [p["d"] for p in pair_results if "d" in p]
        unique_ds = list({int(x) for x in recovered_ds})
        consistent = len(unique_ds) == 1 and len(unique_ds) > 0

        results[str(r_val)] = {
            "files": files,
            "pairs": pair_results,
            "consistent_private_key": unique_ds[0] if consistent else None,
            "consistent": consistent
        }

    # print summary
    if not results:
        print("No reused r values found (no recovery attempted).")
    else:
        print("Recovered results for reused r values:")
        for r_key, info in results.items():
            print("r =", r_key)
            print("  files:", info["files"])
            print("  consistent:", info["consistent"])
            if info["consistent"]:
                d = info["consistent_private_key"]
                print("  recovered d (hex):", hex(d))
            for p in info["pairs"]:
                if "error" in p:
                    print("   pair", p["pair"], "error:", p["error"])
                else:
                    print("   pair", p["pair"], "d(hex):", p["d_hex"])
            print()

    # save results
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("Detailed results written to", out_path)


if __name__ == "__main__":
    main()
