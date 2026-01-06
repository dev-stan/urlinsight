import hmac
import hashlib
import os

_SECRET = os.environ["IP_HASH_SECRET"].encode()

def hash_ip(ip: str) -> str:
    return hmac.new(
        _SECRET,
        ip.encode(),
        hashlib.sha256
    ).hexdigest()
