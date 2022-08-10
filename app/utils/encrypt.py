from hashlib import sha512


def sha512_hash(content: str, salt: str) -> str:
    password_hash = sha512(f"{content}{salt}".encode("utf-8")).hexdigest()
    return password_hash
