import random
from Crypto.Util import number

from cryptozero.attacks.scanner import scan_vulnerabilities
from cryptozero.attacks.rsa.fermat_attack import FermatAttack
from cryptozero.ciphers.rsa import RSA


def generate_weak_rsa(bit_length=1024, delta_bits=16, e=65537):
    """
    Generates RSA parameters (n, e, d, p, q) vulnerable to Fermat's factorization.
    p and q are chosen such that q - p is small (around 2^delta_bits).
    bit_length: total bits for modulus n.
    delta_bits: bits of difference between q and p.
    e: public exponent.
    """
    half_bits = bit_length // 2

    # Generate first prime p of half bit length
    p = number.getPrime(half_bits)

    # Choose small offset k, so q = p + k is prime
    # k is roughly in range [2^(delta_bits-1), 2^delta_bits)
    min_k = 1 << (delta_bits - 1)
    max_k = (1 << delta_bits) - 1
    k = random.randrange(min_k, max_k)

    # Ensure q is prime; if not, keep incrementing by 2
    q = p + k
    if q % 2 == 0:
        q += 1
    while not number.isPrime(q):
        q += 2
        # If gap becomes too large, restart generation
        if q - p > max_k:
            return generate_weak_rsa(bit_length, delta_bits, e)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Compute private exponent d
    d = number.inverse(e, phi)
    return {
        'n': n,
        'e': e,
        'd': d,
        'p': p,
        'q': q,
        'gap': q - p
    }


if __name__ == '__main__':
    params = generate_weak_rsa(bit_length=1024, delta_bits=16)
    print("Test RSA parameters:")
    print(f"p = {params['p']}")
    print(f"q = {params['q']}")
    print(f"Gap (q - p) = {params['gap']}")
    print(f"n = {params['n']}")
    print(f"e = {params['e']}")
    print(f"d = {params['d']}")
    print("\n\n")

    print("Vulnerabilities found by scan:")
    print(scan_vulnerabilities("rsa", params))
    print("\n\n")

    print("Performing Fermat Attack")
    plaintext = "Very super omega secret unfindable message!!"

    rsa = RSA(params["n"], params["e"])
    ciphertext = rsa.encrypt(plaintext.encode("utf-8"))

    attack = FermatAttack(**params)
    print(attack.is_vulnerable())

    decrypted_message = attack.run(ciphertext)
    print(decrypted_message.decode("utf-8"))