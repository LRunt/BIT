import constants
from hashlib import sha256


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


def load_parameter(file_name: str) -> int:
    """
    Load a parameter from a file.
    :param file_name: The name of the file containing the parameter.
    :return: The parameter read from the file.
    """
    with open(file_name, 'r') as f:
        parameter = int(f.read())
        f.close()
    return parameter


def load_signature(file_name: str) -> (int, int):
    """
    Load an ElGamal digital signature from a file.
    :param file_name: The name of the file containing the signature.
    :return: A tuple containing the two components of the signature.
    """
    with open(file_name, 'r') as f:
        signature = f.read()
    a, b = map(int, signature.split(','))
    return a, b


if __name__ == '__main__':
    # Load public key
    p = load_parameter(constants.PARAMETER_P_FILE)
    g = load_parameter(constants.PARAMETER_G_FILE)
    y = load_parameter(constants.PARAMETER_Y_FILE)
    a, b = load_signature(constants.SIGNATURE_FILE)
    print(f"p: {p}, g: {g}, y: {y}, a: {a}, b: {b}")
    student_number_hash = sha256(constants.STUDENT_NUMBER.encode('utf-8')).hexdigest()
    # verify signature
    valid = verify_signature(student_number_hash, a, b, p, g, y)
    print(f"Signature is valid: {valid}")
