from tqdm import tqdm
import secrets


class Des:
    ITERATIONS = 16
    BYTE_BLOCK_SIZE = 8
    LENGTH_OF_KEY = 8  # in bytes
    BITS_IN_S_BOX = 6
    S_BOX_SIZE = 64
    S_BOX_ROWS = 4
    S_BOX_COLUMNS = 16
    NUMBER_OF_S_BOXES = 8

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

    # E bit-selection table
    EXPAND_PERMUTATION = [32, 1, 2, 3, 4, 5,
                          4, 5, 6, 7, 8, 9,
                          8, 9, 10, 11, 12, 13,
                          12, 13, 14, 15, 16, 17,
                          16, 17, 18, 19, 20, 21,
                          20, 21, 22, 23, 24, 25,
                          24, 25, 26, 27, 28, 29,
                          28, 29, 30, 31, 32, 1]

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

    # All s-boxes in one array
    S_BOXES = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
               0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
               4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
               15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13,
               15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
               3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
               0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
               13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9,
               10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
               13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
               13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
               1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12,
               7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
               13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
               10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
               3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14,
               2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
               14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
               4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
               11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3,
               12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
               10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
               9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
               4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13,
               4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
               13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
               1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
               6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12,
               13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
               1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
               7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
               2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11
               ]

    # Permutation in the function
    FUNCTION_PERMUTATION = [16, 7, 20, 21,
                            29, 12, 28, 17,
                            1, 15, 23, 26,
                            5, 18, 31, 10,
                            2, 8, 24, 14,
                            32, 27, 3, 9,
                            19, 13, 30, 6,
                            22, 11, 4, 25]

    # The final permutation
    FINAL_PERMUTATION = [40, 8, 48, 16, 56, 24, 64, 32,
                         39, 7, 47, 15, 55, 23, 63, 31,
                         38, 6, 46, 14, 54, 22, 62, 30,
                         37, 5, 45, 13, 53, 21, 61, 29,
                         36, 4, 44, 12, 52, 20, 60, 28,
                         35, 3, 43, 11, 51, 19, 59, 27,
                         34, 2, 42, 10, 50, 18, 58, 26,
                         33, 1, 41, 9, 49, 17, 57, 25]

    def __init__(self, encryption: bool = True):
        self.encryption = encryption

    def perform_des(self, input_bytes: bytes, key: int, description: str):
        """
        Performing the DES (Data Encryption Standard) encryption or decryption
        :param input_bytes: Bytes what will be encrypted
        :param key: Key which will be used to encrypt or decrypt.
        :param description: Description of the action.
        :return: Encoded or decoded bytes.
        """
        coded_bytes = bytearray()
        key = format(key, '064b')
        #print(key)
        #print(f"Key 0: {key[0]}")
        keys = self.generate_keys(key)
        if not self.encryption:
            keys.reverse()
            padded_input_bytes = input_bytes
        else:
            padded_input_bytes = self.add_zero_padding(input_bytes)
        #print(f"Keys: {keys}")
        num_blocks = len(padded_input_bytes) // self.BYTE_BLOCK_SIZE
        actual_block = 0
        for i in tqdm(range(num_blocks), desc=description):
            actual_block += 1
            #print(f"Actual block: {actual_block} of {num_blocks}")
            start = i * self.BYTE_BLOCK_SIZE
            coded_bytes += self.encode_block(padded_input_bytes[start:start + self.BYTE_BLOCK_SIZE], keys)
        if not self.encryption:
            coded_bytes = self.remove_zero_padding(coded_bytes)
        return coded_bytes


    def create_key(self):
        """
        Generating the 64-bit key.
        """
        return secrets.token_hex(self.LENGTH_OF_KEY)

    def generate_keys(self, key: str):
        """
        Method generating keys for all iterations.
        :param key: Key value from witch are the keys generated.
        :return: List of keys for every iteration.
        """
        permutate_key = self.get_permutatation(key, self.KEY_PERMUTATION)
        #print(f"Permutate key: {permutate_key}")
        left, right = self.split_in_half(permutate_key)
        #print(f"Left: {left}")
        #print(f"Right: {right}")
        keys = [None] * self.ITERATIONS
        for i in range(self.ITERATIONS):
            left = self.binary_left_rotation(left, self.SHIFTS[i])
            right = self.binary_left_rotation(right, self.SHIFTS[i])
            #print(f"C{i + 1}: {left}\nD{i + 1}: {right}")
            keys[i] = self.get_permutatation(left + right, self.COMPRESSION_PERMUTATION)
        return keys

    def get_permutatation(self, binary: str, permutation_rules: list):
        """
        Returns a permutation of string
        :param binary: Binary what will be permuted.
        :param permutation_rules: Rules of the permutation.
        :return: Permuted binary.
        """
        permutation = ''
        for position in permutation_rules:
            permutation += binary[position - 1]
        return permutation

    def split_in_half(self, binary: str):
        """
        Returns binary split in half.
        :param binary: Binary what will be split.
        :return: Left and right half of the binary.
        """
        half = len(binary) // 2
        return binary[:half], binary[half:]

    def binary_left_rotation(self, binary: str, n: int):
        """
        Returns binary rotation of the binary.
        :param binary: Binary what will be rotated.
        :param n: Number of shift positions.
        :return: Rotated binary.
        """
        return binary[n:] + binary[:n]

    def add_zero_padding(self, input_bytes: bytes):
        """
        Adding zero padding bytes to align the file size to the desired length.
        Adding zeros and number of added bytes on last position of the array.
        :param input_bytes: Bytes where will be the zero padding performed.
        :return: Bytes with zero padding.
        """
        num_of_padding_bytes = self.BYTE_BLOCK_SIZE - (len(input_bytes) % self.BYTE_BLOCK_SIZE)
        #print(f"Adding padding: {num_of_padding_bytes}")
        padding = bytes([0x00] * (num_of_padding_bytes - 1)) + bytes([num_of_padding_bytes])
        input_bytes += padding
        return input_bytes

    def remove_zero_padding(self, decoded_bytes: bytes):
        """
        Removes the zero padding form the byte array.
        :param decoded_bytes: Decoded bytes with zero padding.
        :return: Bytes without zero padding.
        """
        num_of_padding_bytes = decoded_bytes[-1]
        return decoded_bytes[:-num_of_padding_bytes]

    def encode_block(self, bytes_block: bytes, keys: list):
        """
        Encoding or decoding the block of bytes.
        :param bytes_block: Block of bytes what will be encoded.
        :param keys: Keys for each iteration
        :return: Encoded or decoded bytes.
        """
        binary_block = ''.join(format(byte, '08b') for byte in bytes_block)
        # Initial permutation
        permuted_block = self.get_permutatation(binary_block, self.INITIAL_PERMUTATION)
        # Split into two half
        left, right = self.split_in_half(permuted_block)
        for i in range(self.ITERATIONS):
            left_previous = left
            right_previous = right
            # Ln = Rn - 1
            left = right_previous
            # Rn
            # Expanding R
            right = self.get_permutatation(right, self.EXPAND_PERMUTATION)
            right = self.xor_operation(right, keys[i])
            right = self.s_box_operation(right)
            # Permutation
            right = self.get_permutatation(right, self.FUNCTION_PERMUTATION)
            # xor with left side
            right = self.xor_operation(left_previous, right)
        encrypted_block = right + left
        encrypted_block = self.get_permutatation(encrypted_block, self.FINAL_PERMUTATION)
        encrypted_block = int(encrypted_block, 2).to_bytes(8, byteorder='big')
        return encrypted_block

    def xor_operation(self, first_binary: str, second_binary: str):
        """
        The operation of xor of two binaries.
        :param first_binary: The first binary (in string).
        :param second_binary: The second binary (in string).
        :return: Result of XOR operation.
        """
        if len(first_binary) != len(second_binary):
            raise ValueError("Binary strings must be of the same length")
        num_bits = len(first_binary)
        result = int(first_binary, 2) ^ int(second_binary, 2)
        return format(result, f'0{num_bits}b')

    def s_box_operation(self, binary: str):
        """
        Operation of S-Boxes performing a substitution from 48-bits to 32-bits
        :param binary: Binary on which the substitution will be performed.
        :return: Substituted binary.
        """
        result = ''
        for i in range(self.NUMBER_OF_S_BOXES):
            # get 6 bits
            start_index = i * self.BITS_IN_S_BOX
            end_index = start_index + self.BITS_IN_S_BOX
            segment = binary[start_index:end_index]
            # get row
            row = int(segment[0] + segment[5], 2)
            # get column
            column = int(segment[1] + segment[2] + segment[3] + segment[4], 2)
            s_box_value = self.S_BOXES[i * self.S_BOX_SIZE + row * self.S_BOX_COLUMNS + column]
            result += format(s_box_value, '04b')
        return result
