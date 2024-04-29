import base64
import os

from dbgpt.util import envutils


def encrypt(text):
    encrypted_text = ""
    for char in text:
        encrypted_char = chr(ord(char) + 8)
        encrypted_text += encrypted_char
    encrypted_text = base64.b64encode(encrypted_text.encode()).decode()
    return encrypted_text


def decrypt(encrypted_text):
    decrypted_text = base64.b64decode(encrypted_text).decode()
    decrypted_result = ""
    for char in decrypted_text:
        decrypted_char = chr(ord(char) - 8)
        decrypted_result += decrypted_char
    return decrypted_result


def ssourl():
    url = envutils.getenv("SSO_SERVER_ENDPOINT") + "/auth/principal"
    return url


def enabledsso():
    return False if envutils.getenv("DEPLOY_ENV") == "LOCAL" else True
