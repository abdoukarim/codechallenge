# coding=utf-8
import ast
import hashlib
import logging

import binascii

from Crypto.Cipher import PKCS1_OAEP

log = logging.getLogger(__name__)

from Crypto import Random
from Crypto.PublicKey import RSA
import base64


def generate_keys():
    # RSA modulus length must be a multiple of 256 and >= 1024
    modulus_length = 256 * 4  # use larger value in production
    privatekey = RSA.generate(modulus_length, Random.new().read)
    publickey = privatekey.publickey()
    return privatekey, publickey


def export_private_key(privatekey):
    private_key = privatekey.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)
    file_out.close()


def export_public_key(publickey):
    public_key = publickey.publickey().export_key()
    file_out = open("pub.pem", "wb")
    file_out.write(public_key)
    file_out.close()


def import_private_key():
    file = open("private.pem", "rb")
    private_key = RSA.import_key(file.read())
    file.close()
    return private_key


def import_public_key():
    file = open("pub.pem", "rb")
    public_key = RSA.import_key(file.read())
    file.close()
    return public_key


def encrypt_message(a_message, publickey):
    # encrypted_msg = publickey.encrypt(a_message, 32)[0]
    encryptor = PKCS1_OAEP.new(publickey)
    encrypted_msg = encryptor.encrypt(str(a_message).encode('utf-8'))
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)  # base64 encoded strings are database friendly
    return encoded_encrypted_msg


def decrypt_message(encoded_encrypted_msg, privatekey):
    decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
    decryptor = PKCS1_OAEP.new(privatekey)
    decoded_decrypted_msg = decryptor.decrypt(ast.literal_eval(str(decoded_encrypted_msg)))
    # decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
    return decoded_decrypted_msg


def hash_word(word):
    salt = binascii.hexlify(b"code$challenge")
    value = word + str(salt)
    return 'sha256$' + hashlib.sha256(str(value).encode('utf-8')).hexdigest()
