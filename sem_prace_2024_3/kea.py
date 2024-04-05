N = 5

class KnapsackEncryptionAlgorithm:

    def __init__(self, encryption: bool, private_key: list, p: int, q: int):
        self.encryption = encryption
        self.private_key = private_key
        self.p = p
        self.q = q
        self.public_key = []

    def transform_private_to_public(self):
        for key in self.private_key:
            self.public_key.append((key * self.p) % self.q)
        return self.public_key

    def encrypt_block(self, message):
        indexes = []
        encrypted_value = 0
        for i in range(len(self.private_key)):
            if message & (1 << (N - i)):
                indexes.append(i)

        for index in indexes:
            encrypted_value += self.public_key[index]
        print(indexes)
        print(encrypted_value)