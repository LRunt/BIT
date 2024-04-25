import csv
import time

INPUT_DIR = "data"
INPUT_FILE = "diffie_hellman_keys.csv"
OUTPUT_FILE = "alices_private_keys_A20B0226P.csv"


class Diffie_Hellman_key:
    """
    A class to represent a Diffie-Hellman key.

    Attributes
    ----------
    p_length (int): The length of the prime p.
    key_length (int): The length of the key.
    p (int): The prime number.
    g (int): The base generator.
    g_mod_p (int): The generator raised to a private exponent mod p.
    """

    def __init__(self, p_length: str, key_length: str, p: str, g: str, g_mod_p: str):
        """
        Constructor of class Diffie_Hellman_key
        """
        self.p_length = int(p_length)
        self.key_length = int(key_length)
        self.p = int(p)
        self.g = int(g)
        self.g_mod_p = int(g_mod_p)

    def __str__(self) -> str:
        """
        Text representation of class
        """
        return f"Diffie-Hellman, p: {self.p}, g: {self.g}, g_mod_p: {self.g_mod_p}"


def load_dh_keys(file_name: str) -> list:
    """
    Load Diffie-Hellman keys from a CSV file.
    :param file_name: The name of the file to read from.
    :return: A list of Diffie_Hellman_key objects.
    """
    diffie_hellman_keys = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            key = Diffie_Hellman_key(row[0], row[1], row[2], row[3], row[4])
            diffie_hellman_keys.append(key)
    return diffie_hellman_keys


def brute_force(parameters: Diffie_Hellman_key) -> tuple:
    """
    Attempt to determine the private exponent using brute force method.
    :param parameters: The Diffie-Hellman key containing necessary parameters.
    :return: A tuple containing the discovered private key and the time taken to find it.
    """
    start_time = time.time()
    # 15 minutes timeout
    timeout = 15 * 60

    for i in range(parameters.p):
        if time.time() - start_time > timeout:
            print("Timeout: Key not found within 15 minutes.")
            return None, time.time() - start_time
        g_inverted = pow(parameters.g, i, parameters.p)
        if g_inverted == parameters.g_mod_p:
            stop_time = time.time()
            execution_time = stop_time - start_time
            print(f"Found in time {execution_time:.5f}")
            return i, execution_time


if __name__ == '__main__':
    results = []
    keys_to_found = load_dh_keys(INPUT_DIR + "/" + INPUT_FILE);
    for key in keys_to_found:
        print(f"Searching: {key}")
        alice_key, measured_time = brute_force(key)
        results.append(f"{alice_key};{measured_time:.5f}\n")
    with open(OUTPUT_FILE, 'w') as file:
        file.writelines(results)
