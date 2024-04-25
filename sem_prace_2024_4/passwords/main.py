import csv
from hashlib import sha256
import time

INPUT_DIR = "data"
HASH_FILE = "password_database.csv"
PASSWORD_FILE = "most_used_passwords.txt"
STUDENT_NUMBER = "A20B0226P"
PASSWORD_MAX_LENGTH = 6
OUTPUT_FILE = "cracked_results_A20B0226P.csv"
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyz"


def load_hash_codes(file_name: str, study_number: str) -> list:
    """
    Loads hash codes for a specific student number from a CSV file.
    Parameters:
    :param file_name: Path to the CSV file containing sha-256 hash codes.
    :param study_number: The student number to filter hash codes for.
    :return: filtered hash codes associated with the student number.
    """
    student_hash_codes = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0] == study_number:
                student_hash_codes.append(row[1])
    return student_hash_codes


def load_most_used_passwords(file_path: str) -> list:
    """
    Load a list of the most commonly used passwords from a file.
    :param file_path: Path to the file containing commonly used passwords.
    :return: A list of passwords loaded from the file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines


def use_most_used_passwords(sha256_code: str, combination_count: int, passwords: list) -> tuple:
    """
    Check if any of the most used passwords match the given SHA-256 hash code.
    :param sha256_code: The SHA-256 hash code to check against.
    :param combination_count: The number of password attempts made so far.
    :param passwords: A list of commonly used passwords.
    :returns: Returns a tuple containing a boolean indicating if the password was found, the updated combination count,
    and the password itself.
    """
    for password in passwords:
        combination_count += 1
        if sha256(password.encode('utf-8')).hexdigest() == sha256_code:
            print(f"Decoded: {sha256_code} = {password[:-1]}")
            return True, combination_count, password
    return False, combination_count, ""


def generate_strings(prefix: str, length: int, sha256_code: str, combinations: int) -> tuple:
    """
    Recursively generate password strings up to a specified length and check against a SHA-256 hash.
    :param prefix: The current prefix of the password being generated.
    :param length: The remaining length of password to generate.
    :param sha256_code: The SHA-256 hash code to match against.
    :param combinations: The count of combinations tried so far.
    :returns: Returns a tuple containing a boolean indicating
    if the password was found, the password itself, and the total number of combinations tried.
    """
    if length == 0:
        text_with_end_of_line = prefix + '\n'
        combinations += 1
        if sha256(text_with_end_of_line.encode('utf-8')).hexdigest() == sha256_code:
            print(f"Decoded: {sha256_code} = {prefix}")
            return True, prefix, combinations
        else:
            return False, prefix, combinations
    else:
        for char in ALPHABET:
            solved, password, combinations = generate_strings(prefix + char, length - 1, sha256_code, combinations)
            if solved:
                return solved, password, combinations
    return False, password, combinations


if __name__ == '__main__':
    cracked_passwords = []
    hash_codes = load_hash_codes(INPUT_DIR + "/" + HASH_FILE, STUDENT_NUMBER)
    most_used_passwords = load_most_used_passwords(INPUT_DIR + "/" + PASSWORD_FILE)
    for hash_code in hash_codes:
        print(f"Decoding hash code: {hash_code}")
        combination_count = 0
        start_time = time.time()
        found, combination_count, cracked_password = use_most_used_passwords(hash_code, combination_count, most_used_passwords)
        if not found:
            for length in range(1, PASSWORD_MAX_LENGTH + 1):
                found, cracked_password, combination_count = generate_strings("", length, hash_code, combination_count)
                if found:
                    break
        stop_time = time.time()
        cracked_passwords.append(
            f"{hash_code};{cracked_password[:-1]};{combination_count};{(stop_time - start_time):.5f}\n")
    with open(OUTPUT_FILE, 'w') as file:
        file.writelines(cracked_passwords)
