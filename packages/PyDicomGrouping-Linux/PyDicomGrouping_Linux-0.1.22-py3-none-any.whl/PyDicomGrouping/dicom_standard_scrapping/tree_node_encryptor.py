from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import lzma


class Encryptor():
    def key_create(self,
                   password = b"media lab",
                   salt = b"GDPH",
                   kdf = PBKDF2HMAC,
                   length = 32,
                   iterations = 480000,
                   hash = hashes.SHA256):
        kdf = kdf(
            algorithm=hash(),
            length=length,
            salt=salt,
            iterations=iterations
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def file_encrypt(self, key, original_file, encrypted_file):
        f = Fernet(key)
        #load
        with open(original_file, "rb") as file:
            original = file.read()
        #compress
        original = lzma.compress(original)
        encrypted = f.encrypt(original)
        #compression
        with lzma.open(encrypted_file,"wb") as file:
            file.write(encrypted)
    
    def file_decrypt(self, key, encrypted_file, decrypted_file):
        f = Fernet(key)
        
        with open(encrypted_file, "rb") as file:
            encrypted = file.read()
        
        decrypted = f.decrypt(encrypted)

        with open(decrypted_file, "wb") as file:
            file.write(decrypted)
    
    def decrypt(self, key, encrypted_file):
        f = Fernet(key)
        #load
        with lzma.open(encrypted_file, "rb") as file:
            encrypted = file.read()
        
        decrypted = f.decrypt(encrypted)
        decrypted = lzma.decompress(decrypted)

        return decrypted