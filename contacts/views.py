# -*- coding: utf-8 -*-
#contacts/contacts/views.py

"""This module provides views to manage the contacts table."""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)
from .model import ContactsModel
import frontmatter

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Contacts")
        self.resize(750, 400)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QHBoxLayout()
        self.centralWidget.setLayout(self.layout)
        self.contactsModel = ContactsModel()
        self.setupUI()

    def setupUI(self):
        """Setup the main windows GUI."""
        # Create the table view widget
        self.table = QTableView()
        self.table.setModel(self.contactsModel.model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.resizeColumnsToContents()
        # Create buttons
        self.addButton = QPushButton("Add...")
        self.addButton.clicked.connect(self.openAddDialog)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.clicked.connect(self.deleteContact)
        self.searchButton = QPushButton("Search")
        self.loadButton = QPushButton("Import")
        self.loadButton.clicked.connect(self.getFile)
        self.exportButton = QPushButton("Export")
        self.exportButton.clicked.connect(self.export)
        # Lay out the GUI
        layout = QVBoxLayout()
        layout.addWidget(self.addButton)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.searchButton)
        layout.addStretch()
        layout.addWidget(self.loadButton)
        layout.addWidget(self.exportButton)
        self.layout.addWidget(self.table)
        self.layout.addLayout(layout)

    def openAddDialog(self):
        """Open the Add Contact dialog"""
        dialog = AddDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.contactsModel.addContact(dialog.data)
            self.table.resizeColumnsToContents()

    def deleteContact(self):
        """Delete the selected contact from the database."""
        row = self.table.currentIndex().row()
        if row < 0:
            return
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to remove the selected contact?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )
        if messageBox == QMessageBox.Ok:
            self.contactsModel.deleteContact(row)

    def getFile(self, s):
        print("click", s)
        dlg = CustomDialog(self)
        if dlg.exec_():
            filenames = dlg.selectedFiles()
        
        if dlg.selectedFiles():
            for filePath in filenames:
                with open(filePath) as f:
                    data = frontmatter.loads(f.read())

                contact = []
                for key in data.keys():
                    contact.append(str(data[key]))
                self.contactsModel.addContact(contact)

    def export(self):
        row = self.table.currentIndex().row()
        if row < 0:
            return
        messageBox = QMessageBox.warning(
            self,
            "Warning!",
            "Do you want to export selected contact?",
            QMessageBox.Ok | QMessageBox.Cancel,
        )
        if messageBox == QMessageBox.Ok:
            data = self.contactsModel.retrieveContact(row)
            f=open(f"./export/{data[1]}, {data[0]}.md", "w")
            f.write(f"---\nFirst name: {data[0]}\nLast name: {data[1]}\nAdress: {data[4]}\nZip code: {data[5]}\nTown: {data[6]}\nPhone number: {data[2]}\nBirthday: {data[7]}\n---")
            f.close

class CustomDialog(QFileDialog):
   def __init__(self, *args, **kwargs):
      super(CustomDialog, self).__init__(*args, **kwargs)
      
      self.setWindowTitle("Import")

      QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

      self.buttonBox = QDialogButtonBox(QBtn)
      self.buttonBox.accepted.connect(self.accept)
      self.buttonBox.rejected.connect(self.reject)

      self.layout = QVBoxLayout()
      self.layout.addWidget(self.buttonBox)
      self.setLayout(self.layout)

class AddDialog(QDialog):
    """Add Contact Dialog."""
    def __init__(self, parent= None):
        super().__init__(parent=parent)
        self.setWindowTitle("Add Contact")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.data = None

        self.setupUI()
    
    def setupUI(self):
        """Setup the Add Contacts dialog's GUI."""
        # Create line edits for data fields
        self.firstNameField = QLineEdit()
        self.firstNameField.setObjectName("First name")
        self.lastNameField = QLineEdit()
        self.lastNameField.setObjectName("Last name")
        self.phoneField = QLineEdit()
        self.phoneField.setObjectName("Phone number")
        self.emailField = QLineEdit()
        self.emailField.setObjectName("Email")
        self.adressField = QLineEdit()
        self.adressField.setObjectName("Street Adress")
        self.zipField = QLineEdit()
        self.zipField.setObjectName("Zip code")
        self.townField = QLineEdit()
        self.townField.setObjectName("Town")
        self.birthdayField = QLineEdit()
        self.birthdayField.setObjectName("Birthday")
        #Layout the data fields
        layout = QFormLayout()
        layout.addRow("First Name", self.firstNameField)
        layout.addRow("Last Name", self.lastNameField)
        layout.addRow("Phone No", self.phoneField)
        layout.addRow("Email", self.emailField)
        layout.addRow("Adress", self.adressField)
        layout.addRow("Zip code", self.zipField)
        layout.addRow("Town", self.townField)
        layout.addRow("Birthday", self.birthdayField)
        self.layout.addLayout(layout)
        #Add Standard buttons to the dialog and connect them
        self.buttonsBox = QDialogButtonBox(self)
        self.buttonsBox.setOrientation(Qt.Horizontal)
        self.buttonsBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        self.buttonsBox.accepted.connect(self.accept)
        self.buttonsBox.rejected.connect(self.reject)
        self.layout.addWidget(self.buttonsBox)

    def accept(self):
        """Accept the data provided through the dialog."""
        self.data = []
        for field in (self.firstNameField, self.lastNameField, self.phoneField, self.emailField, self.adressField, self.zipField, self.townField, self.birthdayField):
            if not field.text():
                QMessageBox.critical(
                    self,
                    "Error!",
                    f"You must provide a contact's {field.objectName()}",
                )
                self.data = None  # Reset .data
                return
            self.data.append(field.text())
        super().accept()