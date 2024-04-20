import csv
from hashlib import sha256

INPUT_DIR = "data"
HASH_FILE = "password_database.csv"
PASSWORD_FILE = "most_used_passwords.txt"
STUDENT_NUMBER = "A20B0226P"


def load_hash_codes(file_name: str, study_number: str) -> list:
    student_hash_codes = []

    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if row[0] == study_number:
                student_hash_codes.append(row[1])

    return student_hash_codes


def load_most_used_passwords(file_path: str) -> list:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines


def use_most_used_passwords(sha256_code: str, passwords: list):
    for password in passwords:
        if sha256(password.encode('utf-8')).hexdigest() == sha256_code:
            print(f"Hash code: {hash_code} = {password}")


def brute_force(sha256_code: str):
    print()


if __name__ == '__main__':
    hash_codes = load_hash_codes(INPUT_DIR + "/" + HASH_FILE, STUDENT_NUMBER)
    most_used_passwords = load_most_used_passwords(INPUT_DIR + "/" + PASSWORD_FILE)
    for hash_code in hash_codes:
        use_most_used_passwords(hash_code, most_used_passwords)
    print("Finished")
