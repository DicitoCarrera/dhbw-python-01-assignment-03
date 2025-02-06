from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from application import (
    AddContactCommand,
    ContactApplicationService,
    DeleteContactCommand,
    EditContactCommand,
    GetAllContactsQuery,
    GetContactByNameQuery,
)
from models import Contact, Email, SocialMedia, Telephone
from persistence import ContactRepository

# Initialize Rich Console
console = Console()


# Function to display contacts in a table


def display_contacts(contacts):
    if not contacts:
        console.print("No contacts available.", style="bold red")

        return

    table = Table(title="Contacts", show_header=True, header_style="bold green")

    table.add_column("Name", style="dim", width=20)

    table.add_column("Contact Details", width=40)

    for contact in contacts:
        details = "\n".join([str(detail) for detail in contact.details])

        table.add_row(contact.name, details)

    console.print(table)


# CLI Commands


@click.group()
def cli():
    """Simple CLI for managing contacts."""

    pass


# Command to add a new contact


@cli.command()
@click.argument("name")
@click.option(
    "--telephone",
    "-t",
    help="Telephone number in the format: +<country_code><city_code><number>",
)
@click.option("--email", "-e", help="Email address")
@click.option(
    "--social-media",
    "-s",
    help="Social media platform and handle in the format: <platform>:<handle>",
)
def add_contact(
    name: str,
    telephone: Optional[str],
    email: Optional[str],
    social_media: Optional[str],
):
    """Add a new contact."""
    details = []

    if telephone:
        country_code, city_code, number = telephone.split("-", 2)

        details.append(Telephone(country_code, city_code, number))

    if email:
        details.append(Email(email))

    if social_media:
        platform, handle = social_media.split(":", 1)

        details.append(SocialMedia(platform, handle))

    contact = Contact(name=name, details=details)

    add_command = AddContactCommand(contact)

    app_service.handle_add_contact(add_command)

    console.print(f"Contact '{name}' added successfully!", style="bold green")


# Command to list all contacts
@cli.command()
def list_contacts():
    """List all contacts."""

    get_all_query = GetAllContactsQuery()

    contacts = app_service.handle_get_all_contacts(get_all_query)
    display_contacts(contacts)


# Command to search for a contact by name


@cli.command()
@click.argument("name")
def search_contact(name: str):
    """Search for a contact by name."""

    get_contact_query = GetContactByNameQuery(name=name)

    contact = app_service.handle_get_contact_by_name(get_contact_query)

    if contact:
        console.print(f"Found contact: {contact.name}", style="bold blue")

        display_contacts([contact])

    else:
        console.print(f"No contact found with name '{name}'", style="bold red")


# Command to edit a contact


@cli.command()
@click.argument("old_name")
@click.argument("new_name")
@click.option("--telephone", "-t", help="New telephone number")
@click.option("--email", "-e", help="New email address")
@click.option("--social-media", "-s", help="New social media platform and handle")
def edit_contact(
    old_name: str,
    new_name: str,
    telephone: Optional[str],
    email: Optional[str],
    social_media: Optional[str],
):
    """Edit an existing contact."""
    # Gather new details

    details = []

    if telephone:
        country_code, city_code, number = telephone.split("-", 2)

        details.append(Telephone(country_code, city_code, number))

    if email:
        details.append(Email(email))

    if social_media:
        platform, handle = social_media.split(":", 1)
        details.append(SocialMedia(platform, handle))

    updated_contact = Contact(name=new_name, details=details)

    edit_command = EditContactCommand(old_name=old_name, new_contact=updated_contact)

    success = app_service.handle_edit_contact(edit_command)

    if success:
        console.print(
            f"Contact '{old_name}' updated to '{new_name}' successfully!",
            style="bold green",
        )

    else:
        console.print(f"Contact '{old_name}' not found.", style="bold red")


# Command to delete a contact by name


@cli.command()
@click.argument("name")
def delete_contact(name: str):
    """Delete a contact by name."""

    delete_command = DeleteContactCommand(name=name)

    success = app_service.handle_delete_contact(delete_command)

    if success:
        console.print(f"Contact '{name}' deleted successfully!", style="bold green")

    else:
        console.print(f"No contact found with name '{name}'", style="bold red")


if __name__ == "__main__":
    # Initialize the repository and application service

    repo = ContactRepository("contacts.db")

    app_service = ContactApplicationService(repo)

    # Start the CLI

    cli()
