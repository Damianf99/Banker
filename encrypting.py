from cryptography.fernet import Fernet

def generate():
    key = Fernet.generate_key()
    with open('filekey.key', 'wb') as filekey:
       filekey.write(key)

def encryption(path):
    with open('MonthsBase/filekey.key', 'rb') as filekey:
        key = filekey.read()
    fernet = Fernet(key)
    with open(path, 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)
    with open(path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)


def decryption(path):
    with open('MonthsBase/filekey.key', 'rb') as filekey:
        key = filekey.read()
    fernet = Fernet(key)
    with open(path, 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(path, 'wb') as dec_file:
        dec_file.write(decrypted)

