N = 5

class KnapsackEncryptionAlgorithm:

    def __init__(self, encryption: bool, private_key: list, p: int, q: int):
        self.encryption = encryption
        self.private_key = private_key
        self.p = p
        self.q = q
        self.public_key = []
        self.p_inverted = None

    def transform_private_to_public(self):
        for key in self.private_key:
            self.public_key.append((key * self.p) % self.q)
        return self.public_key

    def encrypt_block(self, plaintext_block):
        indexes = []
        encrypted_value = 0
        for i in range(len(self.private_key)):
            if plaintext_block & (1 << (N - i)):
                indexes.append(i)

        for index in indexes:
            encrypted_value += self.public_key[index]
        print(indexes)
        print(encrypted_value)
        return encrypted_value

    def get_p_inverted(self):
        p_inverted = 0
        while(p_inverted * self.p) % self.q != 1:
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
            print(f"Round{i}: decrypted_value - {decrypted_value}, private_key: {self.private_key[N - i]}")
            if (decrypted_value - self.private_key[N - i]) >= 0:
                decrypted_value -= self.private_key[N - i]
                plaintext |= msb
            print(f"PlainText after round{i}: {format(plaintext, '06b')}")
        return plaintext