import os
from Crypto.Cipher import AES, DES, Blowfish
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from cryptography.fernet import Fernet

# 🔹 Function to generate keys
def generate_aes_key():
    return get_random_bytes(16)  # 16-byte key for AES

def generate_rsa_keypair():
    key = RSA.generate(2048)
    return key.export_key(), key.publickey().export_key()

def generate_fernet_key():
    return Fernet.generate_key()

def generate_des_key():
    return get_random_bytes(8)  # DES requires an 8-byte key

def generate_blowfish_key():
    return get_random_bytes(16)  # Blowfish uses variable-length keys

# 🔹 Encryption functions
def aes_encrypt(file_data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    return cipher.nonce + tag + ciphertext

def aes_decrypt(encrypted_data, key):
    nonce, tag, ciphertext = encrypted_data[:16], encrypted_data[16:32], encrypted_data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

def rsa_encrypt(file_data, public_key):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(file_data)

def rsa_decrypt(encrypted_data, private_key):
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(encrypted_data)

def fernet_encrypt(file_data, key):
    cipher = Fernet(key)
    return cipher.encrypt(file_data)

def fernet_decrypt(encrypted_data, key):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data)

def des_encrypt(file_data, key):
    cipher = DES.new(key, DES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    return cipher.nonce + tag + ciphertext

def des_decrypt(encrypted_data, key):
    nonce, tag, ciphertext = encrypted_data[:8], encrypted_data[8:16], encrypted_data[16:]
    cipher = DES.new(key, DES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

def blowfish_encrypt(file_data, key):
    cipher = Blowfish.new(key, Blowfish.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    return cipher.nonce + tag + ciphertext

def blowfish_decrypt(encrypted_data, key):
    nonce, tag, ciphertext = encrypted_data[:8], encrypted_data[8:16], encrypted_data[16:]
    cipher = Blowfish.new(key, Blowfish.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
    

# 🔹 Save encrypted file
def save_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

# 🔹 Main function
def main():
    print("\nWelcome to the File Encryption & Decryption Program!")
    print("1. Encrypt a File")
    print("2. Decrypt a File")
    
    choice = input("Enter your choice (1 for encryption, 2 for decryption): ")

    if choice == '1':  # Encryption
        print("\nSelect an encryption method:")
        print("1. AES")
        print("2. RSA")
        print("3. Fernet")
        print("4. DES")
        print("5. Blowfish")
        
        method = input("Enter your choice: ")
        filename = input("Enter the filename to encrypt: ")
        
        if not os.path.exists(filename):
            print("File not found!")
            return

        with open(filename, 'rb') as f:
            file_data = f.read()

        key = None
        encrypted_data = None
        encrypted_filename = filename + ".enc"

        if method == '1':  # AES
            key = generate_aes_key()
            encrypted_data = aes_encrypt(file_data, key)
        elif method == '2':  # RSA
            private_key, public_key = generate_rsa_keypair()
            key = (private_key, public_key)
            encrypted_data = rsa_encrypt(file_data, public_key)
        elif method == '3':  # Fernet
            key = generate_fernet_key()
            encrypted_data = fernet_encrypt(file_data, key)
            encrypted_filename = filename + ".fernet"
        elif method == '4':  # DES
            key = generate_des_key()
            encrypted_data = des_encrypt(file_data, key)
        elif method == '5':  # Blowfish
            key = generate_blowfish_key()
            encrypted_data = blowfish_encrypt(file_data, key)
        else:
            print("Invalid choice!")
            return

        save_file(encrypted_filename, encrypted_data)
        print(f"Encryption complete! Encrypted file saved as: {encrypted_filename}")
        if method == '2':
            print(f"RSA Private Key (keep safe for decryption):\n{key[0].decode()}")
        elif method == '3':
            print(f"Encryption Key (keep safe for decryption): {key.decode()}")
        else:
            print(f"Encryption Key (keep safe for decryption): {key.hex()}")

    elif choice == '2':  # Decryption
        filename = input("Enter the encrypted filename: ")
        
        if not os.path.exists(filename):
            print("File not found!")
            return

        with open(filename, 'rb') as f:
            encrypted_data = f.read()

        print("\nWhich encryption method was used?")
        print("1. AES")
        print("2. RSA")
        print("3. Fernet")
        print("4. DES")
        print("5. Blowfish")
        
        method = input("Enter your choice: ")
        key_input = input("Enter the decryption key: ")

        try:
            decrypted_data = None
            if method == '1':  # AES
                key = bytes.fromhex(key_input)
                decrypted_data = aes_decrypt(encrypted_data, key)
            elif method == '2':  # RSA
                private_key = key_input.encode()
                decrypted_data = rsa_decrypt(encrypted_data, private_key)
            elif method == '3':  # Fernet
                key = key_input.encode()  # Convert input key to bytes
                decrypted_data = fernet_decrypt(encrypted_data, key)
            elif method == '4':  # DES
                key = bytes.fromhex(key_input)
                decrypted_data = des_decrypt(encrypted_data, key)
            elif method == '5':  # Blowfish
                key = bytes.fromhex(key_input)
                decrypted_data = blowfish_decrypt(encrypted_data, key)
            else:
                print("Invalid choice!")
                return

            decrypted_filename = filename.replace(".enc", ".dec")
            save_file(decrypted_filename, decrypted_data)
            print(f"Decryption complete! Decrypted file saved as: {decrypted_filename}")

        except Exception as e:
            print("Decryption failed! Possible reasons: Wrong key or incorrect encryption type.")
            print(f"Error: {e}")

    else:
        print("Invalid choice! Please enter 1 or 2.")

if __name__ == '__main__':
    main()