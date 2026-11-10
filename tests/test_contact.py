import pytest

from models.contact import Contact


class TestContact:
    def test_create_contact_with_name_with_spaces(self):
        # 1. arrange (preparar)
        name = " Cielo "
        phone = "989356231"
        email = "sky@example.com"

        # 2. act (actuar)
        contact = Contact(name, phone, email)

        # 3. assert (afirmar)
        assert contact.name == "Cielo"

    def test_create_contact_with_name_two_characters(self):
        # 1. arrange (preparar)
        name = "Ci"
        phone = "989356231"
        email = "sky@gmail.com"

        with pytest.raises(ValueError):
            Contact(name, phone, email)
