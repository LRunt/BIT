import random
from tqdm import tqdm
import secrets


class Des:
    ROUNDS = 16
    BYTE_BLOCK_SIZE = 8

    ## TODO Here you can specify the pboxes, sboxes and other necessary tables

    def __init__(self, encryption: bool = True):
        self.encryption = encryption

    def create_key(self):
        """
        Generating and saving the 64-bit key to the file key.txt
        """
        return secrets.token_hex(8)

    def perform_des(self, input_bytes, key):
        # TODO perform DES algorithm, dont forget to use padding when encrypting/decrypting files from validations
        raise NotImplementedError

    ### TODO recommend to create small functions that tackles individual operations
