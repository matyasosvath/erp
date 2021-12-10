#!/usr/bin/env python3

import random
# import sqlite3
# import csv

from typing import Type, Union, List
import util
import data_manager

DATAFILE = "hr.csv"
DATAFILE_SALES = "sales.csv"
DATAFILE_CRM = "crm.csv"

HEADERS = ["Id", "Name", "Date of birth", "Department", "Clearance"]

# DATABASE SPECIFIC PARAMTERES
# DO NOT CHANGE
SECURE_ID = 0

NAME = 1
BIRTHDATE = 2
DEPARMENT = 3
CLEARANCE = 4

SALES_CUSTOMER = 1
SALES_PRODUCT = 2
SALES_PRICE = 3
SALES_DATE = 4

class Customer:
    def __init__(self, name: str = "",email:str = "",status:str = ""):
        self.id = util.generate_id()
        self.name = name
        self.email = email
        self.status = status

class CustomerModel(object):
    def __init__(self):

        self.current_id = None
        self.customers = []

    def create(self, vasarlo: Customer):
        self.customers.append(vasarlo)

    def read(self, id):
        for vasarlo in self.customers:
            if id == vasarlo.id:
                return vasarlo

    def update(self, id, name: str = "", email: str = "", status: str = ""):
        for vasarlo in self.customers:
            if vasarlo.id == id:
                vasarlo.name = name
                vasarlo.email = email
                vasarlo.status = status

    def delete(self, id):
        all_ids = [cust.id for cust in self.customers]
        if id in all_ids:
            for i, customer in enumerate(self.customers):
                if customer.id == id:
                    del self.customers[i]


class Worker:
    def __init__(self, name: str = "",birthdate:str = "",department:str = "", clearance: str = ""):
        self.secure_id = util.generate_id()
        self.name = name
        self.birthdate = birthdate
        self.department = department
        self.clearance = clearance

class WorkerModel(object):
    def __init__(self):

        self.current_id = None
        self.workers = self.read_all()

    def read_all(self):

        data = []

        raw_data = data_manager.read_table_from_file(DATAFILE)

        for worker in raw_data:

            name = worker[NAME]
            birthdate = worker[BIRTHDATE]
            department = worker[DEPARMENT]
            clearance = worker[CLEARANCE]

            data.append(Worker(name=name,
                   birthdate=birthdate,
                   department=department,
                   clearance=clearance))

        return data

    def save(self):
        data = []
        for worker in self.workers:
            worker = self.reconstruct_worker_class_to_list(worker)
            data.append(worker)

        data_manager.write_table_to_file(DATAFILE, data)

    def reconstruct_worker_class_to_list(self, munkas: Worker):
        return [munkas.secure_id, munkas.name, munkas.birthdate, munkas.department, munkas.clearance] 


    def create(self, worker: Worker):
        self.workers.append(worker)
        self.save()

    def read(self, secure_id):
        for worker in self.workers:
            if secure_id == worker.secure_id:
                return worker

    def update(self, secure_id, name: str = "", birthdate: str = "", department: str = "", clearance: str = ""):
        for worker in self.workers:
            if worker.secure_id == secure_id:
                worker.name = name
                worker.birthdate = birthdate
                worker.department = department
                worker.clearance = clearance

        self.save()

    def delete(self, secure_id):
        for i, worker in enumerate(self.workers):
                if worker.secure_id == secure_id:
                    del self.workers[i]

        self.save()


################################################
#################### SALES MODEL ###############
################################################

class Transaction:
    def __init__(self, customer: str = "", product:str = "", price: str = "", date: str = ""):
        self.secure_id = util.generate_id()
        self.customer = customer
        self.product = product
        self.price = price
        self.date = date

class TransactionModel(object):
    def __init__(self):

        self.current_id = None
        self.transactions = self.read_all()

    def read_all(self):

        data = []

        raw_data = data_manager.read_table_from_file(DATAFILE_SALES)

        for transaction in raw_data:

            customer = transaction[SALES_CUSTOMER]
            product = transaction[SALES_PRODUCT]
            price = transaction[SALES_PRICE]
            date = transaction[SALES_DATE]

            data.append(Transaction(
                    customer=customer,
                    product=product,
                    price=price,
                    date=date
                ))

        return data

    def save(self):
        data = []
        for transaction in self.transactions:
            transaction = self.reconstruct_transaction_class_to_list(transaction)
            data.append(transaction)

        data_manager.write_table_to_file(DATAFILE, data)

    def reconstruct_transaction_class_to_list(self, transaction: Transaction):
        return [transaction.secure_id, transaction.customer, transaction.product, transaction.price, transaction.date]

    def create(self, transaction: Transaction):
        self.transactions.append(transaction)
        self.save()

    def read(self, secure_id):
        for transaction in self.transactions:
            if secure_id == transaction.secure_id:
                return transaction

    def update(self, secure_id,
               customer: str = "",
               product: str = "",
               price: str = "",
               date: str = ""):

        for transaction in self.transactions:

            if transaction.secure_id == secure_id:

                transaction.customer = customer
                transaction.product = product
                transaction.price = price
                transaction.date = date

        self.save()

    def delete(self, secure_id):
        for i, transaction in enumerate(self.transactions):
                if transaction.secure_id == secure_id:
                    del self.transactions[i]

        self.save()

