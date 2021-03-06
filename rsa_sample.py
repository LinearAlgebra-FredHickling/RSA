import random
import math
from enum import Enum


# A class used to represent common errors I'd like to print out
class Error(Enum):
    invalidPrime = '\n ERROR: Not a prime number \n'


# Dictionary used to hold values for RSA
rsaDict = {'p   ': '',
           'q   ': '',
           'f(n)': '',
           'e   ': '',
           'd   ': ''}


# Recursive Extended Euclidean Algorithm
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        # '%' means modulus. Returns remainder
        g, x, y = extended_gcd(b % a, a)
        # The '//' means Floor division. 9//2 = 4
        return (g, y - (b // a) * x, x)


# Returns the multiplicative inverse if it exist
def multiplicative_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


# This function will ask for two prime numbers and return a tuple of ints
def get_prime_nums():
    primeOne = 0
    primeTwo = 0

    # This is an infinte loop until the number given is prime
    while True:
        primeOne = int(input("Enter the first prime number: "))
        if (is_prime(primeOne)):
            break

        print(Error.invalidPrime.value)

    # Infinte loop until a number that is prime is given
    while True:
        primeTwo = int(input("Enter the second prime number: "))
        if (is_prime(primeTwo)):
            break

        print(Error.invalidPrime.value)

    return (primeOne, primeTwo)


# Checks for a number being prime and returns a boolean
def is_prime(num):
    # First check for 2 because our later checks would
    # rule 2 out of being a prime number
    if num == 2:
        return True
    # Exclude numbers less than 2 and numbers who give
    # a remainder if divided by 2
    if num < 2 or num % 2 == 0:
        return False
    # Loop the numbers from 3 to sqrt(num)
    for n in range(3, int(math.sqrt(num)) + 2, 2):
        # Check if the modular returns 0
        if num % n == 0:
            return False
    return True


# Generates the public and private key pairs for encrypt and decrypt
def generate_keypair(a, b):

    p = a
    q = b

    # Store rsa values in a dictionary to display
    rsaDict['p   '] = a
    rsaDict['q   '] = b

    # Check if p and q are prime
    if not (is_prime(p) and is_prime(q)):
        # Exit with a value error
        raise ValueError('One or more numbers is not prime')
    elif p == q:
        # Exit with a value error
        raise ValueError('p and q cannot be equal')

    # Multiply the two prime numbers if they pass the above test
    n = p * q

    phi = (p - 1) * (q - 1)

    rsaDict['f(n)'] = phi

    e = random.randrange(1, phi)

    g = math.gcd(e, phi)

    # Loop until g does not equal 1
    # if it does equal 1 they're relatively prime
    while g != 1:
        e = random.randrange(1, phi)
        g = math.gcd(e, phi)

    d = multiplicative_inverse(e, phi)

    # If d and e are equal it defeats the point of having a
    # public and private key
    if (d == e):
        raise ValueError('d and e are equal. Use larger prime numbers')

    # Store rsa values in a dictionary to display
    rsaDict['e   '] = e
    rsaDict['d   '] = d

    return ((e, n), (d, n))


# Use the public key to encrypt our messagee
def encrypt(pk, plaintext):
    key, n = pk
    # ord() returns the unicode representation of the character
    cipher = [pow(ord(char), key, n) for char in plaintext]

    return cipher


# Use the private key to decrypt message
def decrypt(pk, ciphertext):
    key, n = pk
    # chr returns the string representing a character represented by Unicode
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return ''.join(plain)


# This code runs everytime the document is called
if __name__ == '__main__':
    print("\nRSA encryption system\n")
    primeOne, primeTwo = get_prime_nums()
    print("\nEstablishing public and private keys... ")
    public, private = generate_keypair(primeOne, primeTwo)

    for k, v in rsaDict.items():
        print(k, ':', v)

    print("Your public key is ", public, " and your private key is ", private)
    message = input("\nEnter a message to be encrypted: ")
    encrypted_msg = encrypt(public, message)
    print("Your encrypted message is: ")
    print(''.join(map(lambda x: str(x), encrypted_msg)))
    print("\nUsing private key ", private, " to decrypt . . .")
    print("Your message is:")
    print(decrypt(private, encrypted_msg))
    print('\n')
