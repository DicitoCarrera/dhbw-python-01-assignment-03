import sqlite3
from typing import List, Optional

from models import Contact, Email, SocialMedia, Telephone

# Database models optimized for persistence (tables)


class ContactRepository:
    def __init__(self, db_file: str):
        self.db_file = db_file

        self.connection = sqlite3.connect(db_file)

        self.cursor = self.connection.cursor()

        self._create_tables()

    def _create_tables(self):
        """Create tables in the database"""

        self._execute_query("""

        CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
            )
        """)

        self._execute_query("""

        CREATE TABLE IF NOT EXISTS contact_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contact_id INTEGER NOT NULL,
        type TEXT NOT NULL,
        value TEXT NOT NULL,
        FOREIGN KEY(contact_id) REFERENCES contacts(id)
        )
        """)

    def _execute_query(self, query: str, params: tuple = ()):
        """Execute a query on the database"""

        self.cursor.execute(query, params)

        self.connection.commit()

    def _fetch_all(self, query: str, params: tuple = ()) -> List[tuple]:
        """Fetch all results for a given query"""

        self.cursor.execute(query, params)

        return self.cursor.fetchall()

    def _fetch_one(self, query: str, params: tuple = ()) -> Optional[tuple]:
        """Fetch a single result for a given query"""

        self.cursor.execute(query, params)

        return self.cursor.fetchone()

    def add_contact(self, contact: Contact) -> Contact:
        """Add a new contact into the database"""

        self._execute_query("INSERT INTO contacts (name) VALUES (?)", (contact.name,))

        contact_id = self.cursor.lastrowid

        # Insert contact details

        for detail in contact.details:
            if isinstance(detail, Telephone):
                self._execute_query(
                    "INSERT INTO contact_details (contact_id, type, value) VALUES (?, ?, ?)",
                    (
                        contact_id,
                        "telephone",
                        f"{detail.country_code},{detail.city_code},{detail.number}",
                    ),
                )

            elif isinstance(detail, Email):
                self._execute_query(
                    "INSERT INTO contact_details (contact_id, type, value) VALUES (?, ?, ?)",
                    (contact_id, "email", detail.address),
                )

            elif isinstance(detail, SocialMedia):
                self._execute_query(
                    "INSERT INTO contact_details (contact_id, type, value) VALUES (?, ?, ?)",
                    (contact_id, "social_media", f"{detail.platform}:{detail.handle}"),
                )

        return contact

    def get_all_contacts(self) -> List[Contact]:
        """Retrieve all contacts from the database"""

        rows = self._fetch_all("SELECT * FROM contacts")

        contacts = []

        for row in rows:
            contact = Contact(name=row[1], details=[])

            contact_id = row[0]

            # Fetch associated details for each contact
            details = self._fetch_all(
                "SELECT type, value FROM contact_details WHERE contact_id = ?",
                (contact_id,),
            )

            for detail in details:
                if detail[0] == "telephone":
                    country_code, city_code, number = detail[1].split(",")
                    contact.details.append(Telephone(country_code, city_code, number))
                elif detail[0] == "email":
                    contact.details.append(Email(detail[1]))
                elif detail[0] == "social_media":
                    platform, handle = detail[1].split(":")
                    contact.details.append(SocialMedia(platform, handle))

            contacts.append(contact)

        return contacts

    def get_contact_by_name(self, name: str):
        """Retrieve a contact by name"""
        row = self._fetch_one("SELECT * FROM contacts WHERE name = ?", (name,))

        if row:
            contact = Contact(name=row[1], details=[])
            contact_id = row[0]

            # Fetch associated details for each contact
            details = self._fetch_all(
                "SELECT type, value FROM contact_details WHERE contact_id = ?",
                (contact_id,),
            )

            for detail in details:
                if detail[0] == "telephone":
                    country_code, city_code, number = detail[1].split(",")
                    contact.details.append(Telephone(country_code, city_code, number))
                elif detail[0] == "email":
                    contact.details.append(Email(detail[1]))
                elif detail[0] == "social_media":
                    platform, handle = detail[1].split(":")
                    contact.details.append(SocialMedia(platform, handle))

            return contact, contact_id

        return None

    def update_contact(self, old_name: str, new_contact: Contact) -> bool:
        """Update an existing contact's details"""

        existing_contact, contact_id = self.get_contact_by_name(name=old_name)

        if existing_contact:
            # Delete old contact details

            self._execute_query(
                "DELETE FROM contact_details WHERE contact_id = ?",
                (contact_id,),
            )

            # Update contact name

            self._execute_query(
                "UPDATE contacts SET name = ? WHERE id = ?",
                (new_contact.name, contact_id),
            )

            # Add new contact details

            for detail in new_contact.details:
                if isinstance(detail, Telephone):
                    self._execute_query(
                        "INSERT INTO contact_details (contact_id, type, value) VALUES (?, ?, ?)",
                        (
                            contact_id,
                            "telephone",
                            f"{detail.country_code},{detail.city_code},{detail.number}",
                        ),
                    )

                elif isinstance(detail, Email):
                    self._execute_query(
                        "INSERT INTO contact_details (contact_id, type, value) VALUES (?, ?, ?)",
                        (contact_id, "email", detail.address),
                    )

                elif isinstance(detail, SocialMedia):
                    self._execute_query(
                        "INSERT INTO contact_details (contact_id, type, value) VALUES (?, ?, ?)",
                        (
                            contact_id,
                            "social_media",
                            f"{detail.platform}:{detail.handle}",
                        ),
                    )

            return True

        return False

    def delete_contact(self, name: str) -> bool:
        """Delete a contact by name"""

        contact, contact_id = self.get_contact_by_name(name)

        if contact:
            self._execute_query(
                "DELETE FROM contact_details WHERE contact_id = ?", (contact_id,)
            )

            self._execute_query("DELETE FROM contacts WHERE id = ?", (contact_id,))

            return True

        return False
