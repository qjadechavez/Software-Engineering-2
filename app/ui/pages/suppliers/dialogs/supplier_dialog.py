from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
from .base_dialog import BaseDialog

class SupplierDialog(BaseDialog):
    """Dialog for adding or editing suppliers"""
    
    def __init__(self, parent=None, supplier=None):
        super(SupplierDialog, self).__init__(parent, supplier, "Supplier")
        self.setup_ui()
        self.populate_data()

    def setup_ui(self):
        """Set up the supplier dialog UI"""
        self.setup_base_ui(650)
        
        self.save_button.setText("Save Supplier")
        self.save_button.clicked.connect(self.save_supplier)
        
        # Supplier name input
        name_label = QtWidgets.QLabel("Supplier Name:")
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Enter supplier name")
        self.name_input.setMinimumHeight(36)
        self.form_layout.addRow(name_label, self.name_input)
        
        # Product name input
        product_label = QtWidgets.QLabel("Product Name:")
        self.product_input = QtWidgets.QLineEdit()
        self.product_input.setPlaceholderText("Enter product name")
        self.product_input.setMinimumHeight(36)
        self.form_layout.addRow(product_label, self.product_input)
        
        # Category input
        category_label = QtWidgets.QLabel("Category:")
        self.category_input = QtWidgets.QLineEdit()
        self.category_input.setPlaceholderText("Enter product category")
        self.category_input.setMinimumHeight(36)
        self.form_layout.addRow(category_label, self.category_input)
        
        # Contact number input
        contact_label = QtWidgets.QLabel("Contact Number:")
        self.contact_input = QtWidgets.QLineEdit()
        self.contact_input.setPlaceholderText("Enter contact number")
        self.contact_input.setMinimumHeight(36)
        self.form_layout.addRow(contact_label, self.contact_input)
        
        # Email input
        email_label = QtWidgets.QLabel("Email:")
        self.email_input = QtWidgets.QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        self.email_input.setMinimumHeight(36)
        self.form_layout.addRow(email_label, self.email_input)
        
        # Accepts returns checkbox
        returns_label = QtWidgets.QLabel("Returns Policy:")
        self.returns_checkbox = QtWidgets.QCheckBox("Supplier accepts returns")
        self.returns_checkbox.setChecked(False)
        self.form_layout.addRow(returns_label, self.returns_checkbox)
        
        # Products on the way input
        on_the_way_label = QtWidgets.QLabel("Products on the Way:")
        self.on_the_way_input = QtWidgets.QSpinBox()
        self.on_the_way_input.setRange(0, 100000)
        self.on_the_way_input.setMinimumHeight(36)
        self.form_layout.addRow(on_the_way_label, self.on_the_way_input)

    def populate_data(self):
        """Populate dialog with supplier data if editing"""
        if self.item:
            self.header_label.setText("Edit Supplier")
            self.name_input.setText(self.item['supplier_name'])
            self.product_input.setText(self.item['product_name'])
            self.category_input.setText(self.item.get('category', ''))
            self.contact_input.setText(self.item.get('contact_number', ''))
            self.email_input.setText(self.item.get('email', ''))
            
            self.returns_checkbox.setChecked(self.item.get('accepts_returns', False))
            self.on_the_way_input.setValue(self.item.get('products_on_the_way', 0))
        else:
            self.header_label.setText("Add New Supplier")

    def save_supplier(self):
        """Save the supplier to the database"""
        # Validate inputs
        if not self.name_input.text().strip():
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Supplier name is required.")
            return
        
        if not self.product_input.text().strip():
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Product name is required.")
            return
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            supplier_name = self.name_input.text().strip()
            product_name = self.product_input.text().strip()
            category = self.category_input.text().strip()
            contact_number = self.contact_input.text().strip()
            email = self.email_input.text().strip()
            accepts_returns = self.returns_checkbox.isChecked()
            products_on_the_way = self.on_the_way_input.value()
            
            if self.item:
                # Update existing supplier
                cursor.execute(
                    """UPDATE suppliers 
                       SET supplier_name = %s, 
                           product_name = %s, 
                           category = %s, 
                           contact_number = %s, 
                           email = %s, 
                           accepts_returns = %s, 
                           products_on_the_way = %s 
                       WHERE supplier_id = %s""",
                    (supplier_name, product_name, category, contact_number, 
                     email, accepts_returns, products_on_the_way, self.item['supplier_id'])
                )
            else:
                # Insert new supplier
                cursor.execute(
                    """INSERT INTO suppliers 
                       (supplier_name, product_name, category, contact_number, email, accepts_returns, products_on_the_way) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (supplier_name, product_name, category, contact_number, 
                     email, accepts_returns, products_on_the_way)
                )
            
            conn.commit()
            cursor.close()
            
            self.accept()
            
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Error saving supplier: {err}")