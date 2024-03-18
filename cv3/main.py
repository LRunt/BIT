CIPHER = ""
KEY = "abc"

atbas = {
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'o',
}


def decode_file_ceasar(text: str):
    text = text.replace(" ", "")
    print(text)
    decoded_text = ""
    for i in range(26):
        for j in range(26):
            for char in text:
                decoded_text += decode_char(char, i)
            print(decoded_text)
            decoded_text = ""


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


def decode_char(char, shift):
    return chr((ord(char) - ord('a') - shift) % 26 + ord('a'))


def decode_file(text: str, frequency):
    number_of_appearance = [0] * 26
    for char in text:
        number_of_appearance[ord(char) - ord('a')] += 1
    sorted(number_of_appearance)
    for a in number_of_appearance:
        print()


def parse_frequency(frequency):
    decryption_dict = {}
    char = ord('a')
    for line in frequency:
        splited = line.split(' ')
        decryption_dict[chr(char)] = splited[1]
        char += 1
    return decryption_dict


def map_letters(text_probability, frequency_probability):
    sorted_frequency = {k: v for k, v in sorted(frequency_probability.items(), key=lambda item: item[1], reverse=True)}
    print(sorted_frequency)


def decode_abatas(text: str):
    decoded = ""
    for char in text:
        num = ord(char) - ord('a')
        reverse = 25 - num
        decoded += chr(reverse + ord('a'))
    return decoded


if __name__ == '__main__':
    f1 = open("cipher/sifra1.txt", "r")
    text = f1.read()
    print(text)
    print(decode_abatas(text))
    f = open("cipher/sifra2.txt", "r")
    text = f.read()
    decode_file_ceasar(text)
    # print(decode_abatas(text))
    # frequency_file = open("frequency/frequency_cz_ref.txt")
    # frequency = frequency_file.readlines()
    # print(text)
    # probability = parse_frequency(frequency)
    # frequency_of_letters = decode_file(text)
    # map_letters(frequency_of_letters, probability)
