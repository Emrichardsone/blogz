import hashlib
import random
import os
import base64

def make_salt():
 #this fn makes bytes characters for readibility and makes salt
    raw_salt = os.urandom(5) #get random characters
    return base64.b64encode(raw_salt).decode() #

def make_pw_hash(password, salt=None):
    #salt = None means that it will figure
    # out a salt for you
    hasher = hashlib.sha512()
    if salt is None:
        salt = make_salt()
    hasher.update(str.encode(password))
    hasher.update(str.encode(salt))
    hash = hasher.hexdigest() #makes your code hexidecimal
    return hash + ":" + salt #gives you coded password and salt 
    #a colon is good because it wont occur elsewhere



def check_pw_hash (password, hash_and_salt):
    salt = hash_and_salt.split (":")[1]
    provided_hash = make_pw_hash(password, salt)
    return hash_and_salt == provided_hash