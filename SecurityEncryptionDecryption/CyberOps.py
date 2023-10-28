# -*- coding: utf-8.
"""
Created on Sat Oct 28 16:13:42 2023

@author: Sanchez-Cisneros
"""

import re
import hashlib
import random
import string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode

#use directory to path of file you want to scan

import random
import string
import hashlib

def generate_mock_hash():
    """
    Generate a mock hash.
    """
    mock_data = ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))
    return hashlib.sha256(mock_data.encode()).hexdigest()

# Generate 1000 mock hashes (adding newly updated list of fake malware hashes)
MOCK_MALWARE_HASH_DB = [generate_mock_hash() for _ in range(1000)]

# List of fake malware file hashes (for demonstrative purposes only)
MALWARE_HASHES = [
    "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
    "abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef",
    # Adding generated mock hashes
    *MOCK_MALWARE_HASH_DB
]

def check_for_malware(file_path):
    """
    Check if a file contains malware by comparing its SHA-256 hash to a list of fake malware hashes.
    """
    with open(file_path, 'rb') as f:
        file_content = f.read()
        file_hash = hashlib.sha256(file_content).hexdigest()
        return file_hash in MALWARE_HASHES

import hashlib

def hash_string(input_string):
    """
    Hashes the input string using SHA-256 algorithm.
    """
    return hashlib.sha256(input_string.encode()).hexdigest()


def generate_strong_password(length=16):
    """
    Generates a strong password of specified length.
    """
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for i in range(length))
    return password


def encrypt_message(message: str, key: bytes) -> tuple:
    """
    Encrypts a message using AES encryption with a given key.
    """
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return (b64encode(nonce).decode('utf-8'), b64encode(ciphertext).decode('utf-8'))

def decrypt_message(nonce, ciphertext, key):
    """
    Decrypts a message using AES encryption with the given nonce, ciphertext, and key.
    """
    nonce = b64decode(nonce.encode('utf-8'))
    ciphertext = b64decode(ciphertext.encode('utf-8'))
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    return plaintext

def generate_filename(length=16):
    """
    Generates a random filename of specified length.
    """
    chars = string.ascii_letters + string.digits
    filename = ''.join(random.choice(chars) for i in range(length))
    return filename

def main():
    """
    This function provides a menu-driven interface for various security-related tasks, including:
    The user is prompted to choose an option from the menu, and the corresponding function is executed.
    """
    while True:
        print("""
        1. Check file for malware using hash
        2. Hash a string using SHA-256
        3. Encrypt a message
        4. Decrypt a message
        5. Exit
        """)
        
        choice = input("Enter your choice: ")

        if choice == "1":
            file_path = input("Enter the path to the file to check: ")
            if check_for_malware(file_path):
                print(f"The file {file_path} might be malicious!")
            else:
                print(f"The file {file_path} seems clean (based on our limited hash list).")

        elif choice == "2":
            s = input("Enter string to hash: ")
            print("Hashed String:", hash_string(s))

        elif choice == "3":
            print("""
            a. Use a specific key
            b. Generate a strong password as key
            """)
            sub_choice = input("Choose an option: ")
            if sub_choice == "a":
                key = input("Enter your key (in base64 format): ").encode('utf-8')
                key = b64decode(key)
            elif sub_choice == "b":
                key = generate_strong_password().encode('utf-8')
                print("Generated Key (in base64 format):", b64encode(key).decode('utf-8'))
            else:
                print("Invalid choice.")
                continue
            
            message = input("Enter message to encrypt: ")
            nonce, ciphertext = encrypt_message(message, key)

            # Using the sanitized filename instead of the key
            filename = generate_filename()
            with open(f"{filename}.txt", "w") as f:
                f.write(ciphertext)

            print("Nonce:", nonce)
            print("Encrypted Message:", ciphertext)  # Display the encrypted message
            print(f"Encrypted Message saved to file: {filename}.txt")

        elif choice == "4":
            nonce = input("Enter the nonce: ")
            ciphertext = input("Enter the encrypted message (the gibberish string, not the original text): ")
            key = input("Enter the key (in base64 format): ")
            key = b64decode(key.encode('utf-8'))
            try:
                print("Decrypted Message:", decrypt_message(nonce, ciphertext, key))
            except Exception as e:
                print("Error during decryption:", str(e))

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
