import sys
from kea import KnapsackEncryptionAlgorithm
import random
from math import gcd

DATA_SOURCE = "validation"
OUTPUT_DIR = "out"
DECODED_DIR = "decoded"

PRIVATE_KEY = [2, 3, 6, 13, 27, 52]
P = 31
Q = 105
MESSAGE = int("011000110101101110", 2)


def transform_private_to_public():
    public_key = []
    for key in PRIVATE_KEY:
        public_key.append((key * P) % Q)
    print(public_key)


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


if __name__ == '__main__':
    super_increasing_sequence = generate_super_increasing_sequence(100, 400, 250)
    print(super_increasing_sequence)
    q = generate_q(100, 200)
    print(f"q: {q}")
    p = generate_p(q)
    print(f"p: {p}")

    kna = KnapsackEncryptionAlgorithm(encryption=True, private_key=PRIVATE_KEY, p=P, q=Q)
    public_key = kna.transform_private_to_public()
    print(public_key)

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

    """if len(sys.argv) != 2:
        print("Exactly one argument is expected (either -e or -d)")
        exit(1)
    else:
        mode = sys.argv[1]

        if mode == "-e":
            print("Encryption mode")

        elif mode == "-d":
            print("Decryption mode")
        else:
            print("Unknown mode... Choices are [-e, -d]")
            exit(1)"""
