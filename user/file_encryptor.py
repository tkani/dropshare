import os
import io
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class FileEncryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        block_size = algorithms.AES.block_size // 8
        return s + b"\0" * (block_size - len(s) % block_size)

    def encrypt(self, message):
        message = self.pad(message)
        iv = os.urandom(algorithms.AES.block_size // 8)
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(message) + encryptor.finalize()
        return iv + ciphertext

    def custom_encrypt_method(self, file_path):
        with open(file_path, 'rb') as file:
            plaintext = file.read()
        enc = self.encrypt(plaintext)
        with open(file_path, 'wb') as file:
            file.write(enc)

    def decrypt(self, ciphertext):
        iv = ciphertext[:algorithms.AES.block_size // 8]
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext[algorithms.AES.block_size // 8:]) + decryptor.finalize()
        return plaintext.rstrip(b"\0")

    def custom_decrypt_method(self, file_path):
        with open(file_path, 'rb') as file:
            ciphertext = file.read()
        decrypted_content = self.decrypt(ciphertext)
        
        return send_file(
            io.BytesIO(decrypted_content),
            as_attachment=True,
            download_name=f"decrypted_{os.path.basename(file_path[:-4])}"
            )
# =
# # Example usage in a Flask route
# @app.route('/decrypt_and_display/<file_path>')
# def decrypt_and_display(file_path):
#     rendered_html = encryptor.custom_decrypt_method(file_path + ".enc")
#     return rendered_html

