import hashlib
import hmac

from app.core.security import hash_ip


class TestHashIp:
    def test_returns_hex_string(self):
        result = hash_ip("127.0.0.1")
        assert isinstance(result, str)
        assert all(c in "0123456789abcdef" for c in result)

    def test_returns_64_char_sha256_digest(self):
        result = hash_ip("127.0.0.1")
        assert len(result) == 64

    def test_deterministic(self):
        assert hash_ip("192.168.1.1") == hash_ip("192.168.1.1")

    def test_different_ips_produce_different_hashes(self):
        assert hash_ip("10.0.0.1") != hash_ip("10.0.0.2")

    def test_consistent_with_stdlib_hmac(self):
        """Verify our function produces a valid HMAC-SHA256 output."""
        from app.core.config import settings

        ip = "203.0.113.42"
        expected = hmac.new(
            str(settings.ip_hash_secret).encode(),
            ip.encode(),
            hashlib.sha256,
        ).hexdigest()
        assert hash_ip(ip) == expected
