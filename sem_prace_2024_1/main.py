import os
from Logger import logger

STEGANOGRAPHY_IMG = "weber.bmp"
DATA_SOURCE = "validation/"
OUTPUT_DIR = "out/"
DECODED_DIR = "decoded/"
first_bit_mask = 0b10000000


def is_file_too_big(steganography_img_size, input_file_size):
    """
    Function determines if the input file is about to fit into STEGANOGRAPHY_IMG
    :param steganography_img_size: number of bytes of STEGANOGRAPHY_IMG
    :param input_file_size: number of bytes of an input file
    :return: True if input file fits, False otherwise
    """
    if steganography_img_size >= input_file_size:
        return True
    else:
        return False


def hide(input_filepath, output_name):
    """
    This procedure performs steganography with the LSB method
    The part of a filepath is a filename and also a file extension
    :param input_filepath: the file which is about to hide into STEGANOGRAPHY IMG
    :param output_name: path to the encoded img with a hidden file
    """

    # TODO read all STEGANOGRAPHY_IMG bytes
    steganography_file_bytes = available_size(STEGANOGRAPHY_IMG)
    logger.info(f"Bytes to store: {steganography_file_bytes}")

    # TODO read all input file bytes from the input_filepath parameter
    input_file_bytes = os.path.getsize(input_filepath)
    logger.info(f"Input file {input_filepath} bytes: {input_file_bytes}")

    if not is_file_too_big(steganography_file_bytes, input_file_bytes):
        print(f"File {input_filepath} is too big for steganography!")
        return

    resulting_bytes = []
    # TODO perform steganography
    steganography(STEGANOGRAPHY_IMG, input_filepath, output_name)

    # TODO write resulting_bytes to the file from the output_name param


def decode(filepath):
    """
    This method decodes a hidden file from a filepath given as parameter and stores it into decoded folder.
    The part of a filepath is a filename and also a file extension
    :param filepath:
    :return:
    """

    # TODO read all bytes from the filepath
    merged_file_bytes = None

    resulting_bytes = []
    # information about filename, extension and size are encoded in a filename
    basename_filepath = os.path.basename(filepath)
    filename_parts = basename_filepath.split("___")
    filename = filename_parts[0]
    extension = filename_parts[1]
    size = int(filename_parts[2])

    # TODO perform decoding (extract bytes from the merged_file_bytes)

    filepath = os.path.join(DECODED_DIR, filename + "." + extension)
    # TODO write resulting_bytes into filepath


def available_size(file_name):
    with open(file_name, 'rb') as bmp:
        bmp.seek(10)
        offset = int.from_bytes(bmp.read(4), 'little')
        logger.info(f"Data starts at: {offset}")
        bmp.seek(18)
        width = int.from_bytes(bmp.read(4), 'little')
        height = int.from_bytes(bmp.read(4), 'little')
        logger.info(f"Width of the data: {width}")
        logger.info(f"Height of the data: {height}")
        num_of_bites = width * height * 3
        return int(num_of_bites / 8)


def steganography(input_file, hide_file, output_file):
    with open(input_file, 'rb') as in_file, open(hide_file, 'rb') as hide_fl:
        header = in_file.read(14)
        offset = int.from_bytes(header[10:14], byteorder='little')
        to_read = offset - 14
        header += in_file.read(to_read)
        data = in_file.read()

    with open(output_file, 'wb') as out:
        out.write(header)
        out.write(data)


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
