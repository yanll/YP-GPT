import base64

from Crypto.Cipher import AES


def decrypt_from_base64(key: str, ciphertext):
    ciphertext = base64.b64decode(ciphertext)
    cipher = AES.new(key.encode("utf-8"), AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    plaintext = plaintext.rstrip(b'\0')
    return plaintext.decode('utf-8')
