import math
import random
from hashlib import sha256

STUDENT_NUMBER = "A20B0226P"
PARAMETER_X_FILE = "x.txt"
PARAMETER_Y_FILE = "y.txt"
PARAMETER_G_FILE = "g.txt"
PARAMETER_P_FILE = "p.txt"
SIGNATURE_FILE = "signature.txt"


def is_prime(number: int) -> bool:
    """
    Check if numer is a prime number.
    :param number: Integer to be checked.
    :return: True - number is prime number, False - number is not prime.
    """
    if number > 1:
        for i in range(2, (number // 2) + 1):
            if (number % i) == 0:
                return False
        else:
            return True
    else:
        return False


def generate_random_prime_number(minimum: int, maximum: int) -> int:
    """
    Generate a random prime number within a specified range.
    :param minimum: The lower bound of the range.
    :param maximum: The upper bound of the range.
    :return: A prime number within the range.
    :raises ValueError: If no prime numbers are found in the specified range.
    """
    primes = [i for i in range(minimum, maximum) if is_prime(i)]
    if len(primes) == 0:
        raise ValueError(f"No prime numbers found in the range {minimum} to {maximum}")
    return random.choice(primes)


def generate_random_number(minimum: int, maximum: int) -> int:
    """
    Generate a random integer within a specified range.

    :param minimum: The lower bound of the range.
    :param maximum: The upper bound of the range.
    :return: A random integer within the range.
    """
    return random.randint(minimum, maximum)


def generate_k(p: int) -> int:
    """
    Generate a random number k that is relatively prime to p-1.
    :param p: The prime number p.
    :return: A random integer k such that is relatively prime to p-1.
    """
    while True:
        k = random.randint(2, p - 1)
        if math.gcd(k, p - 1) == 1:
            return k


def save_to_file(file_name: str, value: int) -> None:
    """
    Save an integer parameter value to a file.
    :param file_name: The name of the file.
    :param value: The integer value to save.
    """
    with open(file_name, 'w') as file:
        file.write(str(value))
        file.close()


def mod_inverse(k: int, p_minus_1: int) -> int:
    """
    Compute the modular inverse of k modulo p-1 using the extended Euclidean algorithm.
    :param k: The integer to find the inverse of.
    :param p_minus_1: p-1, where p is a prime number.
    :return: The modular inverse of k.
    :raises ValueError: If the inverse does not exist.
    """
    g, x, y = extended_euclidean_algorithm(k, p_minus_1)
    if g != 1:
        raise ValueError("Inverse doesn't exist")
    return x % p_minus_1


def extended_euclidean_algorithm(a: int, b: int):
    """
    Compute the greatest common divisor of a and b and coefficients x and y using the extended Euclidean algorithm.
    :param a: First integer.
    :param b: Second integer.
    :return: Tuple containing gcd(a, b), coefficient x, and coefficient y.
    """
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_euclidean_algorithm(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def signature(sha256_hash: str, p: int, g: int) -> [int, int]:
    """
    Generate an ElGamal signature for a given message hash.
    :param sha256_hash: The SHA-256 hash of the message to be signed.
    :param p: The prime number p.
    :param y: The public key y.
    :param g: The generator g.
    :return: Tuple containing the signature components a and b.
    """
    k = generate_k(p)
    a = pow(g, k, p)
    b = (mod_inverse(k, p - 1) * (int(sha256_hash, 16) - x * a)) % (p - 1)
    return a, b


def verify_signature(sha256_hash: str, a: int, b: int, p: int, g: int, y: int) -> bool:
    """
    Verify an ElGamal digital signature using the provided hash and signature components.
    :param sha256_hash: The SHA-256 hash of the signed message, represented as a hexadecimal string.
    :param a: The first component of the signature.
    :param b: The second component of the signature.
    :param p: The prime number used in the ElGamal scheme.
    :param g: The generator used in the ElGamal scheme.
    :param y: The public key component derived from the private key.
    :return: True if the signature is valid, False otherwise.
    """
    left = (pow(y, a) * pow(a, b)) % p
    right = pow(g, int(sha256_hash, 16), p)
    return left == right


if __name__ == '__main__':
    # Generating parameters
    p = generate_random_prime_number(1000, 10000)
    save_to_file(PARAMETER_P_FILE, p)
    g = generate_random_number(500, p)
    save_to_file(PARAMETER_G_FILE, g)
    x = generate_random_number(500, p)
    save_to_file(PARAMETER_X_FILE, x)
    y = pow(g, x, p)
    save_to_file(PARAMETER_Y_FILE, y)
    # signature a student number
    student_number_hash = sha256(STUDENT_NUMBER.encode('utf-8')).hexdigest()
    a, b = signature(student_number_hash, p, g)
    with open(SIGNATURE_FILE, 'w') as f:
        f.write(f"{a},{b}")
        f.close()
    # Validate signature
    valid = verify_signature(student_number_hash, a, b, p, g, y)
    print(f"Signature is valid: {valid}")
