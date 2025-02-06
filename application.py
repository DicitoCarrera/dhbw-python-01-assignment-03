from dataclasses import dataclass

from models import (
    Contact,
    ContactBook,
    add_contact,
    delete_contact,
    edit_contact,
    search_contact,
)
from persistence import ContactRepository

# Command Handlers


@dataclass
class AddContactCommand:
    contact: Contact


@dataclass
class EditContactCommand:
    old_name: str
    new_contact: Contact


@dataclass
class DeleteContactCommand:
    name: str


# Query Handlers


@dataclass
class GetAllContactsQuery:
    pass


@dataclass
class GetContactByNameQuery:
    name: str


# Application Layer


class ContactApplicationService:
    def __init__(self, repository: ContactRepository) -> None:
        self.repository: ContactRepository = repository

    # Command Handlers

    def handle_add_contact(self, command: AddContactCommand) -> Contact:
        """
        Handle the command to add a new contact using domain functionality.
        """
        current_contacts: ContactBook = self.repository.get_all_contacts()

        updated_contact_book: ContactBook = add_contact(
            new_contact=command.contact,
            contact_book=current_contacts,
        )

        self.repository.add_contact(contact=updated_contact_book.contacts[-1])

        return command.contact

    def handle_edit_contact(self, command: EditContactCommand) -> bool:
        """
        Handle the command to edit an existing contact using domain functionality.
        """

        current_contacts: ContactBook = self.repository.get_all_contacts()

        updated_contacts: ContactBook = edit_contact(
            search_name=command.old_name,
            new_contact=command.new_contact,
            contact_book=current_contacts,
        )

        if updated_contacts != current_contacts:
            self.repository.update_contact(
                old_name=command.old_name, new_contact=command.new_contact
            )

            return True

        return False

    def handle_delete_contact(self, command: DeleteContactCommand) -> bool:
        """
        Handle the command to delete an existing contact using domain functionality.
        """

        current_contacts: ContactBook = self.repository.get_all_contacts()

        updated_contacts: ContactBook = delete_contact(
            search_name=command.name,
            contact_book=current_contacts,
        )

        if updated_contacts != current_contacts:
            self.repository.delete_contact(name=command.name)

            return True

        return False

    # Query Handlers

    def handle_get_all_contacts(self, query: GetAllContactsQuery) -> list[Contact]:
        """
        Handle the query to retrieve all contacts using domain functionality.
        """

        contacts: ContactBook = self.repository.get_all_contacts()

        return contacts

    def handle_get_contact_by_name(
        self, query: GetContactByNameQuery
    ) -> Contact | None:
        """
        Handle the query to retrieve a contact by name using domain functionality.
        """

        current_contacts: ContactBook = self.repository.get_all_contacts()

        contact: Contact | None = search_contact(
            search_name=query.name, contact_book=current_contacts
        )

        return contact
