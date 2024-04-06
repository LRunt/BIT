import sys
from kea import KnapsackEncryptionAlgorithm

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

if __name__ == '__main__':
    kna = KnapsackEncryptionAlgorithm(encryption=True, private_key=PRIVATE_KEY, p=P, q=Q)
    public_key = kna.transform_private_to_public()
    print(public_key)
    print("Encoding")
    kna.encrypt(MESSAGE)
    """block1 = kna.encrypt_block(int('011000', 2))
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