import pytest

from models.category import Category
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

    def test_create_contact_with_name_three_character(self):
        # 1. arrange (preparar)
        name = "Joa"
        phone = "989356231"
        email = "joa@example.com"

        # 2. act (actuar)
        contact = Contact(name, phone, email)

        # 3. assert (afirmar)
        assert contact.name == "Joa"

    def test_create_contact_with_phone_of_eight_characters(self):
        # 1. arrange (preparar)
        name = "Cielo"
        phone = "98935623"
        email = "sky@gmail.com"

        # 2. act (actuar) + 3. assert (afirmar)
        with pytest.raises(ValueError):
            Contact(name, phone, email)

    def test_create_contact_with_phone_of_nine_characters(self):
        # 1. arrange (preparar)
        name = "Daniela"
        phone = "989356230"
        email = "dani@gmail.com"

        # 2. act (actuar)
        contact = Contact(name, phone, email)

        # 3. assert (afirmar)
        assert len(contact.phone) == 9

    def test_create_contact_with_short_email(self):
        # 1. arrange (preparar)
        name = "Cielo"
        phone = "989356231"
        email = "sky@gmail"

        # 2. act (actuar) + 3. assert (afirmar)
        with pytest.raises(ValueError):
            Contact(name, phone, email)

    def test_create_contact_with_valid_email(self):
        # 1. arrange (preparar)
        name = "Cielo"
        phone = "989356231"
        email = "sky@example.com"

        # 2. act (actuar)
        contact = Contact(name, phone, email)

        # 3. assert (afirmar)
        assert contact.email == email

    def test_create_contact_with_invalid_category(self):
        # 1. arrange (preparar)
        name = "Joa"
        phone = "989356231"
        email = "joa@gmail.com"
        category = "ADMIN"

        # 2. act (actuar) + 3. assert (afirmar)
        with pytest.raises(ValueError):
            Contact(name, phone, email, category)

    def test_create_contact_uses_other_category_by_default(self):
        # 1. arrange (preparar)
        name = "Daniela"
        phone = "989356231"
        email = "dani@example.com"

        # 2. act (actuar)
        contact = Contact(name, phone, email)

        # 3. assert (afirmar)
        assert contact.category == Category.OTHER
