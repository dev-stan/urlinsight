import string

from app.services.links.utils import generate_short_code


class TestGenerateShortCode:
    def test_default_length(self):
        code = generate_short_code()
        assert len(code) == 6

    def test_custom_length(self):
        for length in (4, 8, 12):
            code = generate_short_code(length=length)
            assert len(code) == length

    def test_alphanumeric_only(self):
        allowed = set(string.ascii_letters + string.digits)
        for _ in range(50):
            code = generate_short_code()
            assert all(c in allowed for c in code)

    def test_generates_varying_codes(self):
        codes = {generate_short_code() for _ in range(20)}
        # With 62^6 possibilities, 20 random codes should all be unique
        assert len(codes) == 20
