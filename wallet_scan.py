import os
import sys
import time
import binascii
import hashlib
import multiprocessing
from base58 import b58encode
from Crypto.Hash import RIPEMD160
from coincurve import PrivateKey as CoincurvePrivateKey

from config import TARGET_CRYPTO, CRYPTO_PARAMS, DATABASE_DIR

# Load database entries
def load_database(path):
    if not os.path.exists(path):
        print(f"Error: Database path '{path}' does not exist.")
        sys.exit(1)

    entries = set()
    for file in os.listdir(path):
        full_path = os.path.join(path, file)
        if os.path.isfile(full_path):
            with open(full_path, "r") as f:
                for line in f:
                    entries.add(line.strip())
    return entries


# Convert public key to address
def public_key_to_address(pubkey_bytes, address_prefix):
    sha256 = hashlib.sha256(pubkey_bytes).digest()
    ripemd160 = RIPEMD160.new(sha256).digest()
    prefix_bytes = bytes.fromhex(address_prefix)
    prefixed = prefix_bytes + ripemd160
    checksum = hashlib.sha256(hashlib.sha256(prefixed).digest()).digest()[:4]
    return b58encode(prefixed + checksum).decode()


# Convert private key to WIF
def private_key_to_wif(privkey_bytes, wif_prefix):
    extended = bytes.fromhex(wif_prefix) + privkey_bytes
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    return b58encode(extended + checksum).decode()


def save_to_file(data):
    with open("wallet-info.txt", "a") as file:
        file.write(data + "\n")


def check_match(priv_hex, pub_hex, addr, wif, database):
    return any(item in database for item in [priv_hex, pub_hex, addr, wif])


def worker(database, substring_length, shared_counter, match_flag, keep_scanning):
    while True:
        if not keep_scanning and match_flag.value:
            break

        privkey = os.urandom(32)
        priv_hex = privkey.hex().upper()
        pubkey = CoincurvePrivateKey(privkey).public_key.format(compressed=False)
        pub_hex = pubkey.hex().upper()
        address = public_key_to_address(pubkey, CRYPTO_PARAMS[TARGET_CRYPTO]['address_prefix'])
        wif = private_key_to_wif(privkey, CRYPTO_PARAMS[TARGET_CRYPTO]['wif_prefix'])

        if len(address) >= substring_length:
            result = f"Private Key: {priv_hex}\nPublic Key: {pub_hex}\nAddress: {address}\nWIF: {wif}\n"
            save_to_file(result)

        if check_match(priv_hex, pub_hex, address, wif, database):
            print("🔒 Match found!")
            result = f"Private Key: {priv_hex}\nPublic Key: {pub_hex}\nAddress: {address}\nWIF: {wif}\n"
            save_to_file(result)
            match_flag.value = True
            if not keep_scanning:
                break

        shared_counter.value += 1


def parse_args():
    args = {
        'cpu_count': multiprocessing.cpu_count(),
        'substring_length': 8,
        'keep_scanning': False,
    }

    for arg in sys.argv[1:]:
        if arg.startswith("cpu_count="):
            args['cpu_count'] = int(arg.split("=")[1])
        elif arg.startswith("substring="):
            args['substring_length'] = int(arg.split("=")[1])
        elif arg.startswith("keep_scanning="):
            val = arg.split("=")[1].lower()
            args['keep_scanning'] = val in ['true', '1', 'yes']

    return args


def main():
    args = parse_args()

    print(f"🚀 Using {args['cpu_count']} CPU cores")
    print(f"🔍 Substring length: {args['substring_length']}")
    print(f"🔁 Keep scanning after match: {args['keep_scanning']}")
    print(f"📦 Loading database from: {DATABASE_DIR[TARGET_CRYPTO]}")

    db = load_database(DATABASE_DIR[TARGET_CRYPTO])

    manager = multiprocessing.Manager()
    shared_counter = manager.Value('i', 0)
    match_flag = manager.Value('b', False)

    processes = []
    for _ in range(args['cpu_count']):
        p = multiprocessing.Process(
            target=worker,
            args=(db, args['substring_length'], shared_counter, match_flag, args['keep_scanning'])
        )
        processes.append(p)
        p.start()

    try:
        while True:
            time.sleep(10)
            print(f"✅ Keys generated so far: {shared_counter.value}")
            if not args['keep_scanning'] and match_flag.value:
                print("🛑 Match found. Exiting main loop.")
                break
    except KeyboardInterrupt:
        print("🔌 Keyboard interrupt received. Terminating...")
    finally:
        for p in processes:
            p.terminate()
        for p in processes:
            p.join()


if __name__ == "__main__":
    main()
