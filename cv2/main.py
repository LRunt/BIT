"""
Author: Lukas Runt
Email: lrunt@students.zcu.cz
Date: February 27, 2024,
Version: 1.0.0
Description: Program to encode and decode the text
"""

SHIFT = 3
KEY = "hanoutwr"


def encode_ceasar(input_text: str):
    """
    Method for encode the text with Ceasar encryption
    :param input_text: text what will be encoded
    :return: encoded text
    """
    encrypted_text = ""
    for letter in input_text:
        encrypted_text += encode_char(letter, SHIFT)
    return encrypted_text


def decode_ceasar(encoded_text: str):
    """
    Mehod to decode the encoded text with the Ceasar encryption
    :param encoded_text: text what is encrypted
    :return: decoded text
    """
    decoded_text = ""
    for letter in encoded_text:
        decoded_text += decode_char(letter, SHIFT)
    return decoded_text


def encode_viegner(text: str):
    """
    Method to encrypt the text with Viegner algorithm
    :param text: the text what will be encrypted
    :return: encoded text
    """
    i = 0
    encoded_text = ""
    for letter in text:
        shift = ord(KEY[i % len(KEY)]) - ord('a')
        encoded_text += encode_char(letter, shift % 26)
        i += 1
    return encoded_text


def decode_viegner(encoded_text: str):
    """
    Method to decode the text what is encoded with Viegner algorithm
    :param encoded_text: text what is encoded with Viegner algorithm
    :return: decoded text
    """
    i = 0
    decoded_text = ""
    for letter in encoded_text:
        shift = ord(KEY[i % len(KEY)]) - ord('a')
        decoded_text += decode_char(letter, shift % 26)
        i += 1
    return decoded_text


def encode_char(char, shift: int):
    """
    Encode one char with given shift
    :param char: char what will be encoded
    :param shift: number of how many chars will be the char shifted
    :return: encoded character
    """
    return chr((ord(char) - ord('a') + shift) % 26 + ord('a'))


def decode_char(char, shift):
    return chr((ord(char) - ord('a') - shift) % 26 + ord('a'))


def getTranspositionKey():
    return sorted(KEY)


def transposition(input_text):
    sorted_key = getTranspositionKey()
    print(len(input_text))
    encrypted_text = [None] * len(input_text)
    for i in range(int(len(input_text) / len(KEY))):
        j = 0
        for char in KEY:
            index = sorted_key.index(char)
            encrypted_text[i * len(KEY) + j] = input_text[i * len(KEY) + index]
            j += 1
    for i in range(int(len(input_text) % len(KEY))):
        encrypted_text[int(len(input_text) / len(KEY)) * len(KEY) + i] = input_text[
            int(len(input_text) / len(KEY)) * len(KEY) + i]
    return encrypted_text


def print_transposition(encrypt):
    for i in range(int(len(encrypt) / len(KEY))):
        row = ""
        for j in range(len(KEY)):
            row += encrypt[i * len(KEY) + j]
        print(row)
    row = ""
    for i in range(len(encrypt) % len(KEY)):
        row += encrypt[int(len(encrypt) / len(KEY)) * len(KEY) + i]
    print(row)


if __name__ == '__main__':
    text = "zeptaslisebudespetminutvypadatjakoblbecnezeptaslisebudesblbcempocelyzivot"
    encoded_text = encode_ceasar(text)
    print(f"Ceasarova šifra:\t\t\t\t {encoded_text}")
    decoded_text = decode_ceasar(encoded_text)
    print(f"Dekodovana Ceasarova šifra: \t {decoded_text}")
    print("--------------------------------------------------------------------------------------")
    encoded_text = encode_viegner(text)
    print(f"Viegnerova šifra:\t\t\t\t {encoded_text}")
    decoded_text = decode_viegner(encoded_text)
    print(f"Dekodovana Viegnerova šifra: \t {decoded_text}")
    print_transposition(transposition(text))
