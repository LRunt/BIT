from tqdm import tqdm
import secrets


class Des:
    ITERATIONS = 16
    BYTE_BLOCK_SIZE = 8

    # PC-1
    KEY_PERMUTATION = [57, 49, 41, 33, 25, 17, 9,
                       1, 58, 50, 42, 34, 26, 18,
                       10, 2, 59, 51, 43, 35, 27,
                       19, 11, 3, 60, 52, 44, 36,
                       63, 55, 47, 39, 31, 23, 15,
                       7, 62, 54, 46, 38, 30, 22,
                       14, 6, 61, 53, 45, 37, 29,
                       21, 13, 5, 28, 20, 12, 4]

    # PC-2
    COMPRESSION_PERMUTATION = [14, 17, 11, 24, 1, 5,
                               3, 28, 15, 6, 21, 10,
                               23, 19, 12, 4, 26, 8,
                               16, 7, 27, 20, 13, 2,
                               41, 52, 31, 37, 47, 55,
                               30, 40, 51, 45, 33, 48,
                               44, 49, 39, 56, 34, 53,
                               46, 42, 50, 36, 29, 32]

    SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    # IP
    INITIAL_PERMUTATION = [58, 50, 42, 34, 26, 18, 10, 2,
                           60, 52, 44, 36, 28, 20, 12, 4,
                           62, 54, 46, 38, 30, 22, 14, 6,
                           64, 56, 48, 40, 32, 24, 16, 8,
                           57, 49, 41, 33, 25, 17, 9, 1,
                           59, 51, 43, 35, 27, 19, 11, 3,
                           61, 53, 45, 37, 29, 21, 13, 5,
                           63, 55, 47, 39, 31, 23, 15, 7]

    # TODO Here you can specify the pboxes, sboxes and other necessary tables

    def __init__(self, encryption: bool = True):
        self.encryption = encryption

    def perform_des(self, input_bytes, key):
        # TODO perform DES algorithm, dont forget to use padding when encrypting/decrypting files from validations
        key = bin(key)[2:]
        print(key)
        print(f"Key 0: {key[0]}")
        keys = self.generate_keys(key)
        print(f"Keys: {keys}")
        return input_bytes

    def create_key(self):
        """
        Generating the 64-bit key
        """
        return secrets.token_hex(8)  # 8 bytes = 64 bits

    # TODO recommend to create small functions that tackles individual operations
    def generate_keys(self, key: str):
        permutate_key = self.get_permutate_key(key, self.KEY_PERMUTATION)
        print(f"Permutate key: {permutate_key}")
        left, right = self.split_in_half(permutate_key)
        print(f"Left: {left}")
        print(f"Right: {right}")
        keys = [None] * self.ITERATIONS
        for i in range(self.ITERATIONS):
            left = self.binary_left_rotation(left, self.SHIFTS[i])
            right = self.binary_left_rotation(right, self.SHIFTS[i])
            print(f"C{i+1}: {left}\nD{i+1}: {right}")
            keys[i] = self.get_permutate_key(left + right, self.COMPRESSION_PERMUTATION)
        return keys

    def get_permutate_key(self, key: str, permutation: list):
        permutate_key = ''
        for position in permutation:
            permutate_key += key[position - 1]
        return permutate_key

    def split_in_half(self, binary: str):
        return binary[:28], binary[28:]

    def binary_left_rotation(self, binary: str, n: int):
        return binary[n:] + binary[:n]
