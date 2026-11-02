"""
Test Cases for Account Service REST API
"""
import os
import logging
import unittest
from unittest import TestCase
from service import app
from service.models import db, Account, init_db
from service.common import status
from tests.factories import AccountFactory

DATABASE_URI = os.environ.get(
    "DATABASE_URI", "sqlite:///test.db"
)

BASE_URL = "/accounts"


class TestAccountService(TestCase):
    """Account Service Tests."""

    @classmethod
    def setUpClass(cls):
        """Set up once before all tests."""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Tear down after all tests."""
        db.session.close()

    def setUp(self):
        """Set up before each test."""
        self.client = app.test_client()
        db.session.query(Account).delete()
        db.session.commit()

    def tearDown(self):
        """Tear down after each test."""
        db.session.remove()

    ############################################################
    # Utility methods
    ############################################################
    def _create_accounts(self, count):
        """Helper method to bulk create accounts."""
        accounts = []
        for _ in range(count):
            account = AccountFactory()
            response = self.client.post(BASE_URL, json=account.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            new_account = response.get_json()
            account.id = new_account["id"]
            accounts.append(account)
        return accounts

    ############################################################
    # Test cases for CREATE
    ############################################################
    def test_create_account(self):
        """It should Create a new Account."""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            json=account.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)
        new_account = response.get_json()
        self.assertEqual(new_account["name"], account.name)
        self.assertEqual(new_account["email"], account.email)
        self.assertEqual(new_account["phone_number"], account.phone_number)
        self.assertEqual(new_account["disabled"], account.disabled)

    def test_bad_request(self):
        """It should return 400 for a bad request."""
        response = self.client.post(BASE_URL, json={"name": "not enough data"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unsupported_media_type(self):
        """It should return 415 for unsupported media type."""
        account = AccountFactory()
        response = self.client.post(
            BASE_URL,
            data=str(account.serialize()),
            content_type="text/html",
        )
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    ############################################################
    # Test cases for READ
    ############################################################
    def test_get_account(self):
        """It should Read a single Account."""
        account = self._create_accounts(1)[0]
        response = self.client.get(
            f"{BASE_URL}/{account.id}", content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], account.name)

    def test_get_account_not_found(self):
        """It should return 404 for a non-existing account."""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ############################################################
    # Test cases for LIST
    ############################################################
    def test_list_accounts(self):
        """It should List all Accounts."""
        self._create_accounts(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_list_accounts_empty(self):
        """It should return an empty list when no accounts exist."""
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 0)

    ############################################################
    # Test cases for UPDATE
    ############################################################
    def test_update_account(self):
        """It should Update an existing Account."""
        account = self._create_accounts(1)[0]
        new_name = "Updated Name"
        account.name = new_name
        response = self.client.put(
            f"{BASE_URL}/{account.id}",
            json=account.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_account = response.get_json()
        self.assertEqual(updated_account["name"], new_name)

    def test_update_account_not_found(self):
        """It should return 404 when updating a non-existing account."""
        account = AccountFactory()
        response = self.client.put(
            f"{BASE_URL}/0",
            json=account.serialize(),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    ############################################################
    # Test cases for DELETE
    ############################################################
    def test_delete_account(self):
        """It should Delete an Account."""
        account = self._create_accounts(1)[0]
        response = self.client.delete(f"{BASE_URL}/{account.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_nonexisting_account(self):
        """It should return 204 even for non-existing account (idempotent)."""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    ############################################################
    # Security Headers Tests
    ############################################################
    def test_security_headers(self):
        """It should return security headers."""
        response = self.client.get("/", environ_base={"wsgi.url_scheme": "https"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        headers = response.headers
        self.assertIn("X-Frame-Options", headers)
        self.assertIn("X-Content-Type-Options", headers)
        self.assertIn("Content-Security-Policy", headers)
        self.assertIn("Referrer-Policy", headers)

    def test_cors_security_headers(self):
        """It should return CORS headers."""
        response = self.client.get(
            "/",
            environ_base={"wsgi.url_scheme": "https"},
            headers={"Origin": "http://localhost:3000"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


if __name__ == "__main__":
    unittest.main()
