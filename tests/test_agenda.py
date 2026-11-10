from models.agenda import Agenda
from models.category import Category
from models.contact import Contact


class TestAgenda:
    def test_update_contact_name(self):
        # Test updating a contact's name
        agenda = Agenda()

        contact = Contact("John Doe", "989356231", "john.doe@example.com")

        agenda.add_contact(contact)

        agenda.update_contact(contact.contact_id, {"name": "Purihuaman"})

        assert contact.name == "Purihuaman"
        assert contact.phone == "989356231"
        assert contact.email == "john.doe@example.com"
        assert contact.category == Category.OTHER

    def test_update_contact_phone(self):
        # Test updating a contact's phone number
        agenda = Agenda()

        contact = Contact("John Doe", "989356231", "john.doe@example.com")

        agenda.add_contact(contact)

        new_phone = "989356232"
        agenda.update_contact(contact.contact_id, {"phone": new_phone})

        assert contact.phone == new_phone
        assert contact.name == "John Doe"
        assert contact.email == "john.doe@example.com"
        assert contact.category == Category.OTHER

    def test_update_contact_email(self):
        # Test updating a contact's email
        agenda = Agenda()

        contact = Contact("Cielo", "989356231", "chelito@gmail.com")

        agenda.add_contact(contact)
        new_email = "sky@gmail.com"
        agenda.update_contact(contact.contact_id, {"email": new_email})

        assert contact.email == new_email
        assert contact.name == contact.name
        assert contact.phone == contact.phone
        assert contact.category == Category.OTHER

    def test_update_contact_category(self):
        # Test updating a contact's category
        agenda = Agenda()

        contact = Contact("John Doe", "989356231", "doe@example.com", Category.FAMILY)
        agenda.add_contact(contact)
        new_category = Category.FRIENDS
        agenda.update_contact(contact.contact_id, {"category": new_category})

        assert contact.category == new_category
        assert contact.email == "doe@example.com"
        assert contact.name == contact.name
        assert contact.phone == contact.phone

    def test_update_contact_updated_at_when_phone_not_updated(self):
        # Test that updated_at is not changed when the phone number is not updated
        agenda = Agenda()

        contact = Contact("Cielo Fernandez", "989356231", "sky@gmail.com")
        agenda.add_contact(contact)
        old_updated_at = contact.updated_at

        equal_phone = "989356231"
        agenda.update_contact(contact.contact_id, {"phone": equal_phone})

        assert contact.name == contact.name
        assert contact.email == contact.email
        assert contact.phone == equal_phone
        assert contact.category == Category.OTHER
        assert contact.updated_at == old_updated_at

    def test_update_contact_updated_at_when_email_is_updated(self):
        # Test update contact's updated_at timestamp
        agenda = Agenda()

        contact = Contact("Daniela", "989356231", "dani@gmail.com")
        agenda.add_contact(contact)
        old_updated_at = contact.updated_at

        new_email = "dani@example.com"
        agenda.update_contact(contact.contact_id, {"email": new_email})

        assert contact.name == contact.name
        assert contact.email == new_email
        assert contact.phone == contact.phone
        assert contact.category == Category.OTHER
        assert contact.updated_at != old_updated_at
