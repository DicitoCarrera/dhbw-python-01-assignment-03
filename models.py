from dataclasses import dataclass
from typing import List, Optional

# Domain Models


class ContactDetail:
    def __init__(self) -> None:
        raise NotImplementedError("This is an abstract class.")


class Telephone(ContactDetail):
    def __init__(self, country_code: str, city_code: str, number: str) -> None:
        self.country_code: str = country_code
        self.city_code: str = city_code
        self.number: str = number

    def __str__(self) -> str:
        return f"Phone: {self.country_code}{self.city_code}{self.number}"


class Email(ContactDetail):
    def __init__(self, address: str) -> None:
        self.address: str = address

    def __str__(self) -> str:
        return f"Email: {self.address}"


class SocialMedia(ContactDetail):
    def __init__(self, platform: str, handle: str) -> None:
        self.platform: str = platform
        self.handle: str = handle

    def __str__(self) -> str:
        return f"{self.platform}: {self.handle}"


class Contact:
    def __init__(self, name: str, details: List[ContactDetail]) -> None:
        self.name: str = name
        self.details: List[ContactDetail] = details

    def __str__(self) -> str:
        details_str = "\n".join(map(str, self.details))
        return f"{self.name}\n{details_str}"


@dataclass
class ContactBook:
    contacts: List[Contact]


# Functional Operations


# Add a new contact to the contact list
def add_contact(new_contact: Contact, contact_book: ContactBook) -> ContactBook:
    # Return a new ContactBook with the updated contacts list
    return ContactBook(contacts=contact_book.contacts + [new_contact])


# List all contacts in a user-friendly format
def list_contacts(contact_book: ContactBook) -> str:
    if not contact_book:
        return "No contacts available."
    return "\n".join(map(str, contact_book.contacts))


# Search for a contact by name
def search_contact(search_name: str, contact_book: ContactBook) -> Optional[Contact]:
    return next(
        (contact for contact in contact_book.contacts if contact.name == search_name),
        None,
    )


# Edit a contact's details by name
def edit_contact(
    search_name: str, new_contact: Contact, contact_book: ContactBook
) -> ContactBook:
    return [
        new_contact if contact.name == search_name else contact
        for contact in contact_book.contacts
    ]


# Delete a contact by name
def delete_contact(search_name: str, contact_book: ContactBook) -> ContactBook:
    return [contact for contact in contact_book.contacts if contact.name != search_name]
