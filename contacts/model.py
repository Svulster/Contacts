# -*- coding: utf-8 -*-
# contacts/contacts/model.py

"""This module provides a model to manage the contacts table."""

from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel

class ContactsModel:
    def __init__(self):
        self.model = self._createModel()

    @staticmethod
    def _createModel():
        """Create and set up the model"""
        tableModel = QSqlTableModel()
        tableModel.setTable("contacts")
        tableModel.setEditStrategy(QSqlTableModel.OnFieldChange)
        tableModel.select()
        headers = ("ID", "First name", "Last name", "Phone", "Email", "Adress", "Zip code", "Town", "Birthday")
        for columnindex, header in enumerate(headers):
            tableModel.setHeaderData(columnindex, Qt.Horizontal, header)
        return tableModel
    
    def addContact(self, data):
        """Add a contact to the database."""
        rows = self.model.rowCount()
        self.model.insertRows(rows,1)
        for column, field in enumerate(data):
            self.model.setData(self.model.index(rows, column+1), field)
        self.model.submitAll()
        self.model.select()

    def deleteContact(self, row):
        """Remove a contact from the database."""
        self.model.removeRow(row)
        self.model.submitAll()
        self.model.select()

    def retrieveContact(self, row):
        """Retrieves contact data from the database"""
        data = []
        columns = self.model.columnCount()-1
        for column in range(columns):
            data.append(self.model.index(row, column+1).data())
        return data