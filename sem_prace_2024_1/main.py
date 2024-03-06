import os

STEGANOGRAPHY_IMG = "weber.bmp"
DATA_SOURCE = "validation/"
OUTPUT_DIR = "out/"
DECODED_DIR = "decoded/"
RGB = 3
MASK = 0b11111110
MASK_LAST = 0b00000001
BYTE = 8


def is_file_too_big(steganography_img_size: int, input_file_size: int):
    """
    Function determines if the input file is about to fit into STEGANOGRAPHY_IMG
    :param steganography_img_size: number of bytes of STEGANOGRAPHY_IMG
    :param input_file_size: number of bytes of an input file
    :return: True if input file is bigger than available space, False otherwise
    """
    return steganography_img_size < input_file_size


def hide(input_filepath: str, output_name: str):
    """
    This procedure performs steganography with the LSB method
    The part of a filepath is a filename and also a file extension
    :param input_filepath: the file which is about to hide into STEGANOGRAPHY IMG
    :param output_name: path to the encoded img with a hidden file
    """

    # read all STEGANOGRAPHY_IMG bytes
    with open(STEGANOGRAPHY_IMG, 'rb') as steg_img:
        steganography_img_bytes = steg_img.read();

    # read all input file bytes from the input_filepath parameter
    with open(input_filepath, 'rb') as input_file:
        input_file_bytes = input_file.read()
        input_file_bits = [int(bit) for byte in input_file_bytes for bit in format(byte, '08b')]

    encoded_string = output_name.encode('utf-8')
    size_of_text = len(encoded_string)
    #print(f"Output_name: {output_name}")
    #print(f"Size of name: {size_of_text}")

    start_of_pixels, width, height = get_bmp_parameters(STEGANOGRAPHY_IMG)

    if is_file_too_big(width * height * 3, len(input_file_bits)):
        print(f"File {input_filepath} is too big for steganography!")
        return

    resulting_bytes = []
    # perform steganography

    for i in range(start_of_pixels):
        resulting_bytes.append(steganography_img_bytes[i])
    written_bits = 0
    while written_bits < len(input_file_bits):
        resulting_bytes.append(steganography_img_bytes[start_of_pixels + written_bits] & MASK | int(input_file_bits[written_bits]))
        written_bits += 1
    while written_bits + start_of_pixels < len(steganography_img_bytes):
        resulting_bytes.append(steganography_img_bytes[start_of_pixels + written_bits])
        written_bits += 1

    # write resulting_bytes to the file from the output_name param
    with open(output_name, 'wb') as output_file:
        output_file.write(bytes(resulting_bytes))


def decode(file_path: str):
    """
    This method decodes a hidden file from a filepath given as parameter and stores it into decoded folder.
    The part of a filepath is a filename and also a file extension
    :param file_path:
    :return:
    """

    # read all bytes from the filepath
    with open(file_path, 'rb') as input_file:
        merged_file_bytes = input_file.read()

    resulting_bytes = []
    # information about filename, extension and size are encoded in a filename
    basename_filepath = os.path.basename(file_path)
    filename_parts = basename_filepath.split("___")
    file_name = filename_parts[0]
    extension = filename_parts[1]
    size = int(filename_parts[2])

    start_of_pixels, width, height = get_bmp_parameters(file_path)

    # perform decoding (extract bytes from the merged_file_bytes)
    extracted_bits = 0
    final_byte = 0
    while len(resulting_bytes) < size:
        for i in range(BYTE):
            byte = merged_file_bytes[start_of_pixels + extracted_bits]
            last_bit = byte & MASK_LAST
            final_byte = (final_byte << 1) | last_bit
            extracted_bits += 1
        resulting_bytes.append(final_byte)
        final_byte = 0

    output_path = os.path.join(DECODED_DIR, file_name + "." + extension)

    # write resulting_bytes into filepath
    with open(output_path, 'wb') as output_file:
        output_file.write(bytes(resulting_bytes))


def get_bmp_parameters(file_name: str):
    """
    Getting information (offset, height and width) about bmp image
    :param file_name: name of the bmp file
    :return: offset (where pixels start), width of the image, height of the image
    """
    with open(file_name, 'rb') as bmp:
        bmp.seek(10)
        offset = int.from_bytes(bmp.read(4), 'little')
        bmp.seek(18)
        width = int.from_bytes(bmp.read(4), 'little')
        height = int.from_bytes(bmp.read(4), 'little')
        return offset, width, height


if __name__ == '__main__':
    if not os.path.exists(DECODED_DIR):
        os.makedirs(DECODED_DIR)

    # 1. phase hiding (encoding) -- steganography
    if os.path.exists(DATA_SOURCE):
        files = sorted(os.listdir(DATA_SOURCE))
        for file in files:
            filepath = os.path.join(DATA_SOURCE, file)
            print(f"Hiding file {filepath} into {STEGANOGRAPHY_IMG}")
            filename, extension = file.split(".")
            size = os.stat(filepath).st_size
            output_filename = os.path.join(OUTPUT_DIR,
                                           filename + "___" + extension + "___" + str(size) + "___" + STEGANOGRAPHY_IMG)
            hide(filepath, output_name=output_filename)

    # 2. phase Decoding
    if os.path.exists(OUTPUT_DIR):
        files = sorted(os.listdir(OUTPUT_DIR))
        for file in files:
            filepath = os.path.join(OUTPUT_DIR, file)
            print(f"Decoding a hidden file from {filepath}")
            decode(filepath)
