BITS_IN_BYTE = 8
# Initializing vector
INIT_A = 54
INIT_B = 88
INIT_C = 72
INIT_D = 123
A = 0
B = 1
C = 2
D = 3
# Keys
KEYS = [131, 12, 26, 92]
# Rotation
ROTATION = [3, 1, 5, 2]
ITERATIONS = 4


def split_into_blocks(input_bytes: bytes, bits_per_block: int):
    """
    Splits input bytes into the blocks of specified size.
    Applying padding if it is necessary to align last block.

    :param input_bytes: The input data to be split into blocks.
    :param bits_per_block: The size of each block
    :return: - blocks (list): List of blocks represented in binary (integer)
             - padding (int): The number of bits used to padding the last block.
    """
    total_bits = len(input_bytes) * BITS_IN_BYTE
    padding = (bits_per_block - (total_bits % bits_per_block)) % bits_per_block
    large_int = int.from_bytes(input_bytes, 'big')
    large_int <<= padding

    # Extract blocks of the specified size.
    blocks = []
    for i in range(0, total_bits + padding, bits_per_block):
        block = large_int & ((1 << bits_per_block) - 1)
        blocks.insert(0, block)
        large_int >>= bits_per_block

    return blocks, padding


def add_padding(string):
    padding = 4 - (len(string) % 4) % 4
    for i in range(padding):
        string += " "
    return string


def rotate_left(value, shift):
    return ((value << shift) | (value >> (8 - shift))) & 0xFF


def md5(P: str):
    vector = [INIT_A, INIT_B, INIT_C, INIT_D]
    split_P = [P[i:i + 4] for i in range(0, len(P), 4)]
    print(split_P)
    for k in range(len(split_P)):
        message_vector = [ord(split_P[k][A]), ord(split_P[k][B]), ord(split_P[k][C]), ord(split_P[k][D])]
        print(f"letters {message_vector}")
        for i in range(ITERATIONS):
            if i % 4 == 0:
                function_res = (vector[B] & vector[D]) | (vector[C] & (vector[D] ^ 255))
            elif i % 4 == 1:
                function_res = (vector[B] & vector[C]) | ((vector[B] ^ 255) & vector[D])
            elif i % 4 == 2:
                function_res = vector[C] ^ (vector[B] | (vector[D] ^ 255))
            elif i % 4 == 3:
                function_res = vector[B] ^ vector[C] ^ vector[D]
            vector[A] = (vector[A] + function_res) % 255
            vector[A] = (vector[A] + message_vector[i]) % 255
            vector[A] = (vector[A] + KEYS[i % 4])
            vector[A] = rotate_left(vector[A], ROTATION[i % 4])
            vector[A] = (vector[A] + vector[B]) % 255
            help_num = vector[A]
            vector[A] = vector[D]
            vector[D] = vector[C]
            vector[C] = vector[B]
            vector[B] = help_num
            print(f"Iteration {i + k * 4}, vector: {vector}")
    return vector


def transform_result(result_vector: list):
    result_int = 0
    for i in result_vector:
        result_int <<= 8
        result_int |= i
    return result_int


if __name__ == '__main__':
    P = "Kdo implementuje prvni, dostava 3 body, druhy 2 body, treti 1 bod."
    P = add_padding(P)
    result = md5(P)
    print(result)
    print(f"{result[A]:02x} {result[B]:02x} {result[C]:02x} {result[D]:02x}")
    result = transform_result(result)
    print(f"{result:08x}")
