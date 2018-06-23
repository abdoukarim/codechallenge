# coding=utf-8
import ast
import hashlib
import logging
import binascii
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random
from Crypto.PublicKey import RSA
import base64

log = logging.getLogger(__name__)


def generate_keys():
    # RSA modulus length must be a multiple of 256 and >= 1024
    modulus_length = 256 * 4  # use larger value in production
    privatekey = RSA.generate(modulus_length, Random.new().read)
    publickey = privatekey.publickey()
    return privatekey, publickey


def export_private_key(privatekey):
    """
    Save private key to disc
    :param privatekey:
    """
    private_key = privatekey.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)
    file_out.close()


def export_public_key(publickey):
    """
    Save public key to disc
    :param privatekey:
    """
    public_key = publickey.publickey().export_key()
    file_out = open("pub.pem", "wb")
    file_out.write(public_key)
    file_out.close()


def import_private_key():
    """
    Import private key from a file
    :return: private key RSA object
    """
    file = open("private.pem", "rb")
    private_key = RSA.import_key(file.read())
    file.close()
    return private_key


def import_public_key():
    """
    Import public key from a file
    :return: public key RSA object
    """
    file = open("pub.pem", "rb")
    public_key = RSA.import_key(file.read())
    file.close()
    return public_key


def encrypt_message(word, publickey):
    """
    Asymmetrical encryption of a given word using public key
    :param word:
    :param publickey:
    :return: encoded_encrypted_msg
    """
    encryptor = PKCS1_OAEP.new(publickey)
    encrypted_msg = encryptor.encrypt(str(word).encode('utf-8'))
    encoded_encrypted_msg = base64.b64encode(encrypted_msg)  # base64 encoded strings are database friendly
    return encoded_encrypted_msg


def decrypt_message(encoded_encrypted_msg, privatekey):
    """
    Asymmetrical decryption of a given encoded and encrypted word using private key
    :param encoded_encrypted_msg:
    :param privatekey:
    :return: decoded_decrypted_msg
    """
    decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
    decryptor = PKCS1_OAEP.new(privatekey)
    decoded_decrypted_msg = decryptor.decrypt(ast.literal_eval(str(decoded_encrypted_msg)))
    return decoded_decrypted_msg


def hash_word(word):
    """
    Hash and salt a word using sha256 algorithm
    :param word:
    :return:
    """
    salt = binascii.hexlify(b"code$challenge")
    value = word + str(salt)
    return 'sha256$' + hashlib.sha256(str(value).encode('utf-8')).hexdigest()
