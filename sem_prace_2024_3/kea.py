N = 5


def split_into_blocks(input_bytes, bits_per_block):
    # Combine bytes into one large integer
    total_bits = len(input_bytes) * 8
    large_int = int.from_bytes(input_bytes, 'big')

    # Prepare blocks
    blocks = []
    for _ in range(0, total_bits, bits_per_block):
        block = large_int & ((1 << bits_per_block) - 1)
        blocks.insert(0, block)
        large_int >>= bits_per_block

    # Check if the last block needs padding (it's the first in the list due to insert(0, block))
    last_block_bits = total_bits % bits_per_block
    if last_block_bits != 0:
        padding_needed = bits_per_block - last_block_bits
        # Pad the last block by shifting
        blocks[0] <<= padding_needed
    else:
        padding_needed = 0  # No padding needed

    return blocks, padding_needed


class KnapsackEncryptionAlgorithm:

    def __init__(self, private_key: list, public_key: list, p: int, q: int):
        self.private_key = private_key
        self.public_key = public_key
        self.p = p
        self.q = q
        self.p_inverted = None

    def transform_private_to_public(self):
        for key in self.private_key:
            self.public_key.append((key * self.p) % self.q)
        return self.public_key

    def encrypt(self, input_bytes):
        blocks, padding = split_into_blocks(input_bytes, len(self.private_key))
        encrypted_blocks = []
        for block in blocks:
            encrypted_blocks.append(self.encrypt_block(block))
        return encrypted_blocks, padding

    def encrypt_block(self, plaintext_block):
        indexes = []
        encrypted_value = 0
        for i in range(len(self.private_key)):
            if plaintext_block & (1 << (len(self.private_key) - 1 - i)):
                indexes.append(i)

        for index in indexes:
            encrypted_value += self.public_key[index]
        #print(indexes)
        #print(encrypted_value)
        return encrypted_value

    def get_p_inverted(self):
        p_inverted = 0
        while (p_inverted * self.p) % self.q != 1:
            p_inverted += 1
        self.p_inverted = p_inverted
        return p_inverted

    def decrypt_block(self, ciphertext_block):
        decrypted_value = (ciphertext_block * self.p_inverted) % self.q
        # rozklad
        plaintext = int('0', 2)
        msb = 1 << (len(self.private_key) - 1)
        for i in range(len(self.private_key)):
            plaintext >>= 1
            #print(f"Round{i}: decrypted_value - {decrypted_value}, private_key: {self.private_key[N - i]}")
            if (decrypted_value - self.private_key[N - i]) >= 0:
                decrypted_value -= self.private_key[N - i]
                plaintext |= msb
            #print(f"PlainText after round{i}: {format(plaintext, '06b')}")
        return plaintext
