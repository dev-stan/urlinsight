import hashlib
import hmac

from .config import settings


def hash_ip(ip: str) -> str:
    return hmac.new(str(settings.ip_hash_secret), ip.encode(), hashlib.sha256).hexdigest()