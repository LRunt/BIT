from tqdm import tqdm

BITS_IN_BYTE = 8

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


class KnapsackEncryptionAlgorithm:
    """
    Implements the Knapsack Encryption Algorithm.
    """

    def __init__(self, private_key: list, public_key: list, p: int, q: int):
        self.private_key = private_key
        self.public_key = public_key
        self.p = p
        self.q = q
        self.p_inverted = None

    def encrypt(self, input_bytes: bytes, file_name: str):
        """
        Encrypts input bytes using knapsack encryption algorithm.

        :param input_bytes: The plaintext data to encrypt.
        :param file_name: Name of the file what is encrypted.
        :return: - encrypted_blocks (list): A list of encrypted blocks.
                 - padding (int): The applied padding.
        """
        blocks, padding = split_into_blocks(input_bytes, len(self.private_key))
        encrypted_blocks = []
        for block in tqdm(blocks, desc=f"Decrypting: {file_name}"):
            encrypted_blocks.append(self.encrypt_block(block))
        return encrypted_blocks, padding

    def encrypt_block(self, plaintext_block: int) -> int:
        """
        Encrypts a single block of plaintext.

        :param plaintext_block: The plaintext block to encrypt.
        :return: The encrypted value of the block.
        """
        indexes = []
        encrypted_value = 0
        for i in range(len(self.private_key)):
            if plaintext_block & (1 << (len(self.private_key) - 1 - i)):
                indexes.append(i)

        for index in indexes:
            encrypted_value += self.public_key[index]
        return encrypted_value

    def get_p_inverted(self) -> int:
        """
        Calculates the modular inverse of p modulo q.

        :return: The modular inverse of p modulo q.
        """
        return pow(self.p, -1, self.q)

    def decrypt(self, input_text: list, padding: int, file_name: str) -> int:
        """
        Decrypts a list of encrypted blocks into plaintext.

        :param input_text: The encrypted blocks.
        :param padding: The padding size applied to the last block.
        :param file_name: Name of the file what is decrypted.
        :return: Decrypted plaintext as binary.
        """
        self.p_inverted = self.get_p_inverted()
        decrypted_value = 0
        for block in tqdm(input_text, desc=f"Decrypting: {file_name}"):
            decrypted_block = self.decrypt_block(block)
            decrypted_value <<= len(self.private_key)
            decrypted_value |= decrypted_block
        decrypted_value >>= int(padding)
        return decrypted_value

    def decrypt_block(self, ciphertext_block: int) -> int:
        """
        Decrypts a single encrypted block.

        :param ciphertext_block: The encrypted block to decrypt.
        :return: The decrypted plaintext block as binary.
        """
        decrypted_value = (ciphertext_block * self.p_inverted) % self.q
        plaintext = int('0', 2)
        msb = 1 << (len(self.private_key) - 1)
        for i in range(len(self.private_key)):
            plaintext >>= 1
            if (decrypted_value - self.private_key[len(self.private_key) - 1 - i]) >= 0:
                decrypted_value -= self.private_key[len(self.private_key) - 1 - i]
                plaintext |= msb
        return plaintext
