# tests/test_repository_contacts.py
# from ..src.repository.contacts import create_contact, get_contacts, get_contact, update_contact, remove_contact

import sys
import os

# Цей рядок програмно додає кореневу папку проєкту до шляху Python.
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
# Тепер ці імпорти мають працювати без помилок.
from repository.contacts import create_contact, get_contacts, get_contact, update_contact, remove_contact
from schemas import ContactCreate, ContactUpdate
from database.models import Contact, User

class TestContacts(unittest.TestCase):
    def setUp(self):
        """
        Sets up a mock database session and user for testing.
        """
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, username="test_user", email="test@example.com")

    def tearDown(self):
        """
        Cleans up resources after each test.
        """
        self.session.reset_mock()

    # Тут будуть тестові методи
    def test_create_contact(self):
        """
        Tests the successful creation of a contact.
        """
        body = ContactCreate(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="1234567890",
            birthday="1990-01-01"
        )
        result = create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertTrue(hasattr(result, "id"))

    def test_get_contacts(self):
        """
        Tests retrieving all contacts for a user.
        """
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = get_contacts(user=self.user, db=self.session)
        self.assertEqual(result, contacts)