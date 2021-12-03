#!/usr/bin/env python3

import random
import sqlite3
import csv


def generate_random_id(low,high):
    return random.randint(low,high)


class Customer:
    def __init__(self, name: str = "",email:str = "",status:str = ""):
        self.id = generate_random_id(1,100)
        self.name = name
        self.email = email
        self.status = status


class ContactModell(object):
    def __init__(self):
        # Current contact when editing.
        self.current_id = None

        # List of dicts, where each dict contains a single contact, containing
        # name, address, phone, email and notes fields.
        self.customers = []


class ContactModel(object):
    def __init__(self):
        # Create a database in RAM
        self._db = sqlite3.connect(':memory:')
        self._db.row_factory = sqlite3.Row

        # Create the basic contact table.
        self._db.cursor().execute('''
            CREATE TABLE customers(
                id INTEGER PRIMARY KEY,
                id2 INTEGER,
                name TEXT,
                email TEXT,
                status TEXT)
        ''')
        self._db.commit()

        # Current contact when editing.
        self.current_id = None

    def add(self, customer):
        self._db.cursor().execute('''
            INSERT INTO customers(name, email, status)
            VALUES(:name, :email, :status)''',
                                  customer)
        self._db.commit()

    def get_summary(self):
        return self._db.cursor().execute(
            "SELECT name, id from customers").fetchall()

    def get_contact(self, customer_id):
        return self._db.cursor().execute(
            "SELECT * from customers WHERE id=:id", {"id": customer_id}).fetchone()

    def get_current_contact(self):
        if self.current_id is None:
            return {"name": "", "email": "", "status": ""}
        else:
            return self.get_contact(self.current_id)

    def update_current_contact(self, details):
        if self.current_id is None:
            self.add(details)
        else:
            self._db.cursor().execute('''
                UPDATE customer SET name=:name, email=:email, status=:status WHERE id=:id''',
                                      details)
            self._db.commit()

    def delete_contact(self, contact_id):
        self._db.cursor().execute('''
            DELETE FROM customers WHERE id=:id''', {"id": contact_id})
        self._db.commit()


