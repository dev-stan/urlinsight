from app.core.auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


class TestPasswordHashing:
    def test_hash_returns_string(self):
        h = hash_password("secret")
        assert isinstance(h, str)

    def test_hash_differs_from_plain(self):
        assert hash_password("secret") != "secret"

    def test_verify_correct_password(self):
        h = hash_password("secret")
        assert verify_password("secret", h) is True

    def test_verify_wrong_password(self):
        h = hash_password("secret")
        assert verify_password("wrong", h) is False

    def test_different_inputs_produce_different_hashes(self):
        h1 = hash_password("alpha")
        h2 = hash_password("bravo")
        assert h1 != h2


class TestJWT:
    def test_roundtrip(self):
        token = create_access_token(42)
        assert decode_access_token(token) == 42

    def test_decode_invalid_token(self):
        assert decode_access_token("not.a.jwt") is None

    def test_decode_empty_string(self):
        assert decode_access_token("") is None

    def test_different_user_ids(self):
        t1 = create_access_token(1)
        t2 = create_access_token(2)
        assert decode_access_token(t1) == 1
        assert decode_access_token(t2) == 2
