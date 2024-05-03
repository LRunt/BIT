import random

STUDENT_NUMBER = "A20B0226P"
PARAMETER_X_FILE = "x.txt"
PARAMETER_Y_FILE = "y.txt"
PARAMETER_G_FILE = "g.txt"
PARAMETER_P_FILE = "p.txt"


def is_prime(number: int) -> bool:
    if number > 1:
        for i in range(2, (number // 2) + 1):
            if (number % i) == 0:
                return False
        else:
            return True
    else:
        return False


def generate_random_number(minimum: int, maximum: int) -> int:
    primes = [i for i in range(minimum, maximum) if is_prime(i)]
    if len(primes) == 0:
        raise ValueError(f"No prime numbers found in the range {minimum} to {maximum}")
    return random.choice(primes)


if __name__ == '__main__':
    p = generate_random_number(1000, 1001)
    print(p)
