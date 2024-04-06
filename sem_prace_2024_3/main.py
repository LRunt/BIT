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

DEBUG = False


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


def modular_inverse_exists(p, q):
    # Check if n and m are coprime
    if gcd(p, q) == 1:
        # n and m are coprime, so n^-1 exists
        return True, pow(p, -1, q)
    else:
        # n and m are not coprime, so n^-1 does not exist
        return False, None


def save_key_to_file(file_name: str, key: list):
    with open(file_name, "w") as file:
        file.write(', '.join(map(str, key)))
        file.close()


def load_key_from_file(file_name: str) -> list:
    with open(file_name, "r") as file:
        key_string = file.read()
        # Split the string by commas and convert each part back to an integer
        key = list(map(int, key_string.split(', ')))
    return key


def save_param_to_file(file_name: str, parameter_value: int):
    with open(file_name, 'w') as file:
        file.write(str(parameter_value))
        file.close()


def load_param_from_file(file_name: str) -> int:
    with open(file_name, 'r') as file:
        parameter_value = int(file.read())
    return parameter_value


def generate_parameter():
    p_inverted_exists = False
    while not p_inverted_exists:
        private_key = generate_super_increasing_sequence(min_bits=100, max_bits=400, length=KEY_LENGTH)
        while not private_key:
            private_key = generate_super_increasing_sequence(min_bits=100, max_bits=400, length=KEY_LENGTH)
        q = generate_q(min_bits=100, max_bits=400)
        p = generate_p(q=q)
        p_inverted_exists = modular_inverse_exists(p, q)
    save_key_to_file(file_name=PRIVATE_KEY_FILE, key=private_key)
    save_param_to_file(file_name=Q_FILE, parameter_value=q)
    save_param_to_file(file_name=P_FILE, parameter_value=p)
    public_key = transform_private_to_public_key(private_key=private_key, q=q, p=p)
    save_key_to_file(file_name=PUBLIC_KEY_FILE, key=public_key)
    return private_key, q, p, public_key


def load_parameter():
    private_key = load_key_from_file(PRIVATE_KEY_FILE)
    public_key = load_key_from_file(PUBLIC_KEY_FILE)
    p = load_param_from_file(P_FILE)
    q = load_param_from_file(Q_FILE)
    print(f"Private key: {private_key}")
    print(f"Public key: {public_key}")
    print(f"P: {p}")
    print(f"Q: {q}")
    return private_key, public_key, p, q


def save_encrypted_file(name: str, extension: str, padding: int, encrypted_blocks: list):
    # Controls if output dir exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    with open(OUTPUT_DIR + "/" + str(padding) + "_" + name + "_" + extension + ".kna", "w") as file:
        for block in encrypted_blocks:
            file.write(f"{str(block)}\n")
        file.close()


def save_decrypted_file(name: str, extension: str, data: int):
    if not os.path.exists(DECODED_DIR):
        os.makedirs(DECODED_DIR)
    byte_length = (data.bit_length() + 7) // 8
    byte_data = data.to_bytes(byte_length, byteorder='big')
    with open(DECODED_DIR + "/" + name + extension, 'wb') as output:
        output.write(byte_data)
        output.close()


if __name__ == '__main__':
    if DEBUG:
        private_key = [2, 3, 6, 13, 27, 52]
        p = 31
        q = 105
        public_key = transform_private_to_public_key(private_key=private_key, p=p, q=q)
        print(f"Public key: {public_key}")
        message = int("01100011010110111001100011001101", 2)
        print(f"Input message: {format(message, '024b')}")
        num_bytes = (message.bit_length() + 7) // 8
        message_bytes = message.to_bytes(num_bytes, byteorder='big')
        knapsackAlgo = KnapsackEncryptionAlgorithm(private_key=private_key, public_key=public_key, p=p, q=q)
        encrypted_text, padding = knapsackAlgo.encrypt(message_bytes)
        save_encrypted_file(name='debug', extension='.txt', padding=padding,
                            encrypted_blocks=encrypted_text)
        print(f"Encrypted message: {encrypted_text}")
        file = "4_debug_.txt.kna"
        print(f"Padding: {padding}")
        with open(OUTPUT_DIR + "/" + file, 'r') as f:
            input_data = f.read()
            f.close()
        input_blocks = [int(block) for block in input_data.strip().split('\n')]
        decrypted_text = knapsackAlgo.decrypt(input_blocks, padding)
        print(f"Decrypted message: {format(decrypted_text, '024b')}")

    else:
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
                        save_encrypted_file(name=file_name, extension=file_extension, padding=padding,
                                            encrypted_blocks=encrypted_blocks)


            elif mode == "-d":
                print("Decryption mode")
                private_key, public_key, p, q = load_parameter()
                knapsackAlgo = KnapsackEncryptionAlgorithm(private_key=private_key, public_key=public_key, p=p, q=q)

                if os.path.exists(OUTPUT_DIR):
                    files = sorted(os.listdir(OUTPUT_DIR))
                    print(f"{len(files)} files found in {OUTPUT_DIR}")
                    for file in files:
                        print(f"Decrypting file: {file}")
                        file_name, extension = os.path.splitext(os.path.basename(file))
                        file_parameters = file_name.split('_')
                        padding = file_parameters[0]
                        decoded_file_name = file_parameters[1]
                        decoded_file_extension = file_parameters[2]
                        print(f"Padding: {padding}")
                        print(f"File name: {decoded_file_name}")
                        print(f"File extension: {decoded_file_extension}")

                        with open(OUTPUT_DIR + "/" + file, 'r') as f:
                            input_data = f.read()
                            f.close()

                        input_blocks = [int(block) for block in input_data.strip().split('\n')]
                        decrypted_text = knapsackAlgo.decrypt(input_text=input_blocks, padding=padding)
                        save_decrypted_file(decoded_file_name, decoded_file_extension, decrypted_text)

            else:
                print("Unknown mode... Choices are [-e, -d]")
                exit(1)
