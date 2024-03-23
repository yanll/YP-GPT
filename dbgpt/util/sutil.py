import base64


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


def ncssourl():
    return decrypt("cHx8eEI3N8KBa212azbCgW1teGnCgTZrd3VCOzg8Ojo3woF9cWk1e216fnFrbTVqd3t7N2l9fHA3eHpxdmtxeGl0")


def innerssourl():
    return decrypt("cHx8eEI3N8KBfXFpNntten5xa202and7ezbCgXhCOzg8Ojo3woF9cWk1e216fnFrbTVqd3t7N2l9fHA3eHpxdmtxeGl0")


def ssourl():
    return innerssourl() if True else ncssourl()


def ak():
    return decrypt("a3RxZ0FuPmo/QWlBbT87P0E4OGo=")


def sk():
    return decrypt("a8KBS0BpPlh6ckBaSzxaUVdOa39aYWtJecKAdXJxaklQPQ==")


def enabledsso():
    return True
