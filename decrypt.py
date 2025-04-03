import cv2
import hashlib
import base64
from Crypto.Cipher import AES

def unpad_message(message):
    return message[:-ord(message[-1])]

def decrypt_aes(encrypted_msg, password):
    key = hashlib.sha256(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_msg = cipher.decrypt(base64.b64decode(encrypted_msg)).decode()
    return unpad_message(decrypted_msg)

def decrypt_message(image_path, password):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Error: Image not found!")
        return

    ascii_values = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            ascii_values.append(img[i, j, 0])

    msg_length = int("".join(chr(ascii_values[i]) for i in range(5)))  # First 5 chars = length
    encrypted_msg = "".join(chr(ascii_values[i]) for i in range(5, 5 + msg_length))

    try:
        decrypted_msg = decrypt_aes(encrypted_msg, password)
        print("\nDecrypted Message:", decrypted_msg)
    except:
        print("Error: Incorrect password or corrupted data!")

if __name__ == "__main__":
    image_path = input("Enter encrypted image path: ")
    password = input("Enter password for decryption: ")
    decrypt_message(image_path, password)
