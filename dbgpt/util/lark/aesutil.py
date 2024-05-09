from binascii import a2b_base64

from Crypto.Cipher import AES

unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def decrypt_from_base64(key, text):
    key = key.encode('UTF-8')
    mode = AES.MODE_ECB
    cryptor = AES.new(key, mode)
    plain_text = cryptor.decrypt(a2b_base64(text))
    return unpad(plain_text.rstrip(b'\0')).decode('UTF-8')
