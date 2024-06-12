import hashlib

def get_hash(text, prefix="", suffix=""):
    text = prefix + text + suffix
    encoded_string = text.encode('utf-8', errors='ignore')
    hash_value = hashlib.sha256(encoded_string).hexdigest()
    return hash_value
