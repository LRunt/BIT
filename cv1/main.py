"""
Author: Lukas Runt
Email: lrunt@students.zcu.cz
Date: February 27, 2024,
Version: 1.0.0
Description: Program to extract hidden information form the .bmp image
"""
if __name__ == '__main__':
    with open('data/obr2.bmp', 'rb') as file:
        bmp_header = file.read(14)

        pixel_array_offset = int.from_bytes(bmp_header[10:14], byteorder='little')

        file.seek(pixel_array_offset)

        char = ''
        bin = 0b00000001
        print(bin)
        letter = 0b0000000
        i = 0
        sentence = ""
        while char != '\n':
            for i in range(8):
                byte = file.read(1)
                last_bit = byte[0] & bin
                letter = (letter << 1) | last_bit
                print(letter)
            sentence += chr(letter)
            char = chr(letter)
            letter = letter & 0
            print(sentence)
