# -*- coding: utf-8 -*-

# contacts/contacts/database.py

"""This module provides a database connection."""

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

def _createContactsTable():
    """Create the contacts table in the database."""
    createTableQuery = QSqlQuery()
    return createTableQuery.exec(
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id integer PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            firstname VARCHAR(40) NOT NULL,
            lastname VARCHAR(40) NOT NULL,
            phone VARCHAR(15),
            email VARCHAR(40),
            streetadress VARCHAR(40),
            zip VARCHAR(5),
            town VARCHAR(40),
            birthday VARCAR(12)
        )
        """
    )

def createConnection(databaseName):
    """Create and open a database connection."""
    connection = QSqlDatabase.addDatabase("QSQLITE")
    connection.setDatabaseName(databaseName)
    if not connection.open():
        QMessageBox.warning(
            None,
            "RP Contact",
            f"Database Error: {connection.lastError().text()}",
        )
        return False
    _createContactsTable()
    return True