import os.path
import sys
from kea import KnapsackEncryptionAlgorithm
import random
from math import gcd

DATA_SOURCE = "validation"
OUTPUT_DIR = "out"
DECODED_DIR = "decoded"

P_FILE = "p.txt"
Q_FILE = "q.txt"
PRIVATE_KEY_FILE = "private_key.txt"
PUBLIC_KEY_FILE = "public_key.txt"

KEY_LENGTH = 250

PRIVATE_KEY = [2, 3, 6, 13, 27, 52]
P = 31
Q = 105
MESSAGE = int("011000110101101110", 2)


def transform_private_to_public_key(private_key: list, q: int, p: int) -> list:
    public_key = []
    for key in private_key:
        public_key.append((key * p) % q)
    return public_key


def generate_super_increasing_sequence(min_bits: int, max_bits: int, length: int) -> list:
    first_num = random.randint(2 ** (min_bits - 1), 2 ** min_bits - 1)
    sequence = [first_num]

    for i in range(length):
        next_num = sum(sequence) + random.randint(1, 2 ** min_bits)
        if next_num.bit_length() > max_bits:
            return False
        sequence.append(next_num)
    return sequence


def generate_q(min_bits: int, max_bits: int) -> int:
    return random.randint(2 ** (min_bits - 1), 2 ** max_bits - 1)


def generate_p(q: int) -> int:
    while True:
        r = random.randint(2, q - 1)
        if gcd(q, r) == 1:
            return r


def save_key_to_file(file_name: str, key: list):
    with open(file_name, "w") as file:
        file.write(', '.join(map(str, key)))
        file.close()


def save_param_to_file(file_name: str, parameter_value: int):
    with open(file_name, 'w') as file:
        file.write(str(parameter_value))
        file.close()


def generate_parameter():
    private_key = generate_super_increasing_sequence(min_bits=100, max_bits=400, length=KEY_LENGTH)
    while not private_key:
        private_key = generate_super_increasing_sequence(min_bits=100, max_bits=400, length=KEY_LENGTH)
    save_key_to_file(file_name=PRIVATE_KEY_FILE, key=private_key)
    q = generate_q(min_bits=100, max_bits=200)
    save_param_to_file(file_name=Q_FILE, parameter_value=q)
    p = generate_p(q=q)
    save_param_to_file(file_name=P_FILE, parameter_value=p)
    public_key = transform_private_to_public_key(private_key=private_key, q=q, p=p)
    save_key_to_file(file_name=PUBLIC_KEY_FILE, key=public_key)
    return private_key, q, p, public_key

def save_encrypted_file(name: str, extension: str, padding: int, encrypted_blocks: list):
    # Controls if output dir exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(OUTPUT_DIR + "/" + str(padding) + "_" + name + "_" + extension + ".kna", "w") as file:
        for block in encrypted_blocks:
            file.write(f"{str(block)}\n")
        file.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Exactly one argument is expected (either -e or -d)")
        exit(1)
    else:
        mode = sys.argv[1]

        if mode == "-e":
            print("Encryption mode")
            source_folder = DATA_SOURCE
            output_folder = OUTPUT_DIR
            # generating private key, q, p, public_key
            private_key, q, p, public_key = generate_parameter()

            knapsackAlgo = KnapsackEncryptionAlgorithm(private_key=private_key, public_key=public_key, p=p, q=q)

            # Start to encrypt the files
            if os.path.exists(DATA_SOURCE):
                files = sorted(os.listdir(DATA_SOURCE))
                print(f"{len(files)} files found in {DATA_SOURCE}")
                for file in files:
                    print(f"Encrypting file: {file}")
                    # Saving filename and extension
                    file_name, file_extension = os.path.splitext(os.path.basename(file))
                    # Loading file
                    with open(DATA_SOURCE + "/" + file, 'rb') as f:
                        input_bytes = f.read()
                        f.close()
                    encrypted_blocks, padding = knapsackAlgo.encrypt(input_bytes)
                    save_encrypted_file(name=file_name, extension=file_extension, padding=padding, encrypted_blocks=encrypted_blocks)


        elif mode == "-d":
            print("Decryption mode")


        else:
            print("Unknown mode... Choices are [-e, -d]")
            exit(1)

    """super_increasing_sequence = generate_super_increasing_sequence(100, 400, 250)
       print(super_increasing_sequence)
       q = generate_q(100, 200)
       print(f"q: {q}")
       p = generate_p(q)
       print(f"p: {p}")

       kna = KnapsackEncryptionAlgorithm(encryption=True, private_key=PRIVATE_KEY, p=P, q=Q)
       public_key = kna.transform_private_to_public()
       print(public_key)"""

    """print("Encoding")
    #kna.encrypt(MESSAGE)
    block1 = kna.encrypt_block(int('011000', 2))
    block2 = kna.encrypt_block(int('110101', 2))
    block3 = kna.encrypt_block(int('101110', 2))
    p_inverted = kna.get_p_inverted()
    print(f"P-inverted: {p_inverted}")
    print("Decoding")
    decrypted1 = kna.decrypt_block(block1)
    print(f"Block1: {format(decrypted1, '06b')}")
    decrypted2 = kna.decrypt_block(block2)
    print(f"Block2: {format(decrypted2, '06b')}")
    decrypted3 = kna.decrypt_block(block3)
    print(f"Block3: {format(decrypted3, '06b')}")"""
