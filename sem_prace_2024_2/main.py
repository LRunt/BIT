import sys
import os
from des import Des

DATA_SOURCE = "validation"
OUTPUT_DIR = "out"
DECODED_DIR = "decoded"
KEY_FILEPATH = "key.txt"

DEBUG = True


if __name__ == '__main__':
    if DEBUG:
        ## The purpose of this is to make sure that DES algorithm is correct
        # example is from https://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm

        print("WARNING: running in DEBUG mode!")
        debug_input: int = 81985529216486895
        debug_input_hex = "12345690abcdef"
        debug_key: int = 1383827165325090801
        # debug_key_hex = 0x133457799bbcdff1

        # print(f"Input bytes hexa: {hex(debug_input)}")
        key = debug_key
        des_encrypt = Des(encryption=True)
        debug_output_bytes = des_encrypt.perform_des(input_bytes=bytes.fromhex(debug_input_hex), key=key)

        ## decryption
        des_decrypt = Des(encryption=False)
        decoded_bytes = des_decrypt.perform_des(debug_output_bytes, key=key)

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

                ##key genaration 64-bit length
                # TODO call Des function to create a key and store it to the KEY_FILEPATH

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

                    # TODO Load file and save its filename and extension
                    input_bytes = None

                    # TODO Load key
                    key = None

                    print(f"Processing file {file}")
                    output_bytes = des.perform_des(input_bytes=input_bytes, key=key)

                    if des.encryption:
                        # TODO build output_filename
                        pass
                    else:
                        # TODO build original filename from the filename of .des file
                        pass

                    # TODO save output bytes to the proper file based on encryption or decryption