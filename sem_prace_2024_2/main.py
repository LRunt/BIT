import sys
import os
from des import Des

DATA_SOURCE = "validation"
OUTPUT_DIR = "out"
DECODED_DIR = "decoded"
KEY_FILEPATH = "key.txt"

DEBUG = False

if __name__ == '__main__':
    if DEBUG:
        # The purpose of this is to make sure that DES algorithm is correct
        # example is from https://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm

        print("WARNING: running in DEBUG mode!")
        # debug_input: int = 81985529216486895
        debug_input_hex = "12345690abcdef"
        # debug_key: int = 1383827165325090801
        debug_key_hex = 0x133457799bbcdff1

        # print(f"Input bytes hexa: {hex(debug_input)}")
        key = debug_key_hex
        des_encrypt = Des(encryption=True)
        debug_output_bytes = des_encrypt.perform_des(input_bytes=bytes.fromhex(debug_input_hex), key=key,
                                                     description='Debug encryption')

        # decryption
        des_decrypt = Des(encryption=False)
        decoded_bytes = des_decrypt.perform_des(debug_output_bytes, key=key, description='Debug decryption')

        # decoded must be equal to the debug_input if DES works correctly
        assert decoded_bytes == bytes.fromhex(debug_input_hex)
        print("DEBUG mode, DES correct")
        print("DES exit")

    else:
        if len(sys.argv) != 2:
            print("Exactly one argument is expected (either -e or -d)")
            exit(1)
        else:
            mode = sys.argv[1]
            data_folder = None

            if mode == "-e":
                print("Encryption mode")
                des = Des(encryption=True)
                data_folder = DATA_SOURCE
                output_folder = OUTPUT_DIR
                # key generation 64-bit length
                key = des.create_key()
                with open(KEY_FILEPATH, 'w') as file:
                    file.write(key)

            elif mode == "-d":
                print("Decryption mode")
                des = Des(encryption=False)
                data_folder = OUTPUT_DIR
                output_folder = DECODED_DIR
            else:
                print("Unknown mode... Choices are [-e, -d]")
                exit(1)

            if os.path.exists(data_folder):
                files = sorted(os.listdir(data_folder))
                print(f"{len(files)} files found in {data_folder}")
                for file in files:

                    # Saving filename and extension
                    file_name, file_extension = os.path.splitext(os.path.basename(file))
                    # Loading file
                    with open(data_folder + "/" + file, 'rb') as f:
                        input_bytes = f.read()

                    # Loading key
                    with open(KEY_FILEPATH, 'r') as key_file:
                        key_string = key_file.read()
                    key = int(key_string, 16)

                    output_bytes = des.perform_des(input_bytes=input_bytes, key=key, description=f"Processing {file}")

                    if des.encryption:
                        # building output_filename
                        output_filename = file_name + '_' + file_extension[1:] + '.des'
                        pass
                    else:
                        # building output_name
                        name_and_extension = file_name.split('_')
                        output_filename = name_and_extension[0] + '.' + name_and_extension[1]
                        pass

                    if des.encryption:
                        output_filepath = OUTPUT_DIR + '/' + output_filename
                    else:
                        output_filepath = DECODED_DIR + '/' + output_filename
                    # saving output bytes
                    with open(output_filepath, 'wb') as output_file:
                        output_file.write(output_bytes)
