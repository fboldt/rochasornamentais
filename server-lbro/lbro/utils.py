import hashlib

def encrypt(hash_string):
    '''
    Encrypt a `string`
    '''
    return hashlib.sha256(hash_string.encode()).hexdigest()