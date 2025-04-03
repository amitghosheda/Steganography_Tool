import cv2
import hashlib
import numpy as np
from Crypto.Cipher import AES
import base64

def pad_message(message):
    return message + (16 - len(message) % 16) * chr(16 - len(message) % 16)

def encrypt_aes(message, password):
    key = hashlib.sha256(password.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_msg = cipher.encrypt(pad_message(message).encode())
    return base64.b64encode(encrypted_msg).decode()

def encrypt_message(image_path, message, password, output_path):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        print("Error: Image not found!")
        return

    encrypted_msg = encrypt_aes(message, password)
    msg_len = len(encrypted_msg)

    if msg_len > img.shape[0] * img.shape[1]:
        print("Error: Message is too long for this image!")
        return

    # Store message length in first 5 pixels
    encrypted_msg = str(msg_len).zfill(5) + encrypted_msg  
    ascii_values = [ord(c) for c in encrypted_msg]

    index = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if index < len(ascii_values):
                img[i, j, 0] = ascii_values[index]  # Store in Blue channel
                index += 1
            else:
                break

    cv2.imwrite(output_path, img)
    print(f"Message encrypted successfully! Saved as {output_path}")

if __name__ == "__main__":
    image_path = input("Enter image path: ")
    message = input("Enter secret message: ")
    password = input("Set a password: ")
    output_path = "encrypted_image.png"
    encrypt_message(image_path, message, password, output_path)
