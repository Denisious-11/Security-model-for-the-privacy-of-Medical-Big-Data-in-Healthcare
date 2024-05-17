from .blowfish_algo import *
import base64



def encrypt_msg(msg,encryption_key):
    #cipher = Cipher(b"%s"%(encryption_key))
    cipher=Cipher(encryption_key.encode())
    msg = str.encode(msg)
    cipher_text = b"".join(cipher.encrypt_ecb_cts(msg))
    cipher_text = base64.b64encode(cipher_text)
    return cipher_text.decode('utf-8')

def decrypt_msg(msg,decryption_key):
    cipher = Cipher(decryption_key.encode())
    msg = str.encode(msg)
    cipher_text = base64.b64decode(msg)
    plain_text = b"".join(cipher.decrypt_ecb_cts(cipher_text))
    return plain_text.decode('utf-8')

if __name__ == "__main__":
    msg = "Testing Blowfish: Success \u2713"
    val = encrypt_msg(msg)
    print(val)
    val = decrypt_msg(val)
    print(val)