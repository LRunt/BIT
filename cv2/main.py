
SHIFT = 3
KEY = "cba"

def encode_ceasar(text):
    encrypted_text = ""
    for letter in text:
        encrypted_text += encode_char(letter, SHIFT)
    return encrypted_text

def decode_ceasar(encoded_text):
    decoded_text = ""
    for letter in encoded_text:
        decoded_text += decode_char(letter, SHIFT)
    return decoded_text

def encode_viegner(text):
    i = 0
    encoded_text = ""
    for letter in text:
        shift = ord(KEY[i % len(KEY)]) - ord('a')
        encoded_text += encode_char(letter, shift % 26)
        i += 1
    return encoded_text

def decode_viegner(encoded_text):
    i = 0
    decoded_text = ""
    for letter in encoded_text:
        shift = ord(KEY[i%len(KEY)]) - ord('a')
        decoded_text += decode_char(letter, shift % 26)
        i += 1
    return decoded_text

def encode_char(char, shift):
    return chr((ord(char) - ord('a') + shift) % 26 + ord('a'))

def decode_char(char, shift):
    return chr((ord(char) - ord('a') - shift) % 26 + ord('a'))

def getTranspositionKey():
    return sorted(KEY)

def transposition(input_text):
    sorted_key = getTranspositionKey()
    print(len(input_text))
    encrypted_text = [None] * len(input_text)
    for i in range(int(len(input_text)/len(KEY))):
        j = 0
        for char in KEY:
            index = sorted_key.index(char)
            encrypted_text[i * len(KEY) + j] = input_text[i * len(KEY) + index]
            j += 1
    for i in range(int(len(input_text)%len(KEY))):
        encrypted_text[int(len(input_text)/len(KEY)) * len(KEY) + i] = input_text[int(len(input_text)/len(KEY)) * len(KEY) + i]
    return encrypted_text

def print_transposition(encrypt):
    for i in range(int(len(encrypt)/len(KEY))):
        row = ""
        for j in range(len(KEY)):
            row += encrypt[i * len(KEY) + j]
        print(row)
    row = ""
    for i in range(len(encrypt)%len(KEY)):
        row += encrypt[int(len(encrypt)/len(KEY)) * len(KEY) + i]
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
