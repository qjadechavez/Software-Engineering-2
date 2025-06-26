from PyQt5 import QtWidgets, QtCore, QtGui
import mysql.connector
from app.utils.db_manager import DBManager
from .base_dialog import BaseDialog

class SupplierDialog(BaseDialog):
    """Dialog for adding or editing suppliers"""
    
    def __init__(self, parent=None, item=None):
        super(SupplierDialog, self).__init__(parent, item, "Supplier")
        
        # Check if this is a received supplier
        self.is_received = False
        if item and item.get('status', '').lower() == 'received':
            self.is_received = True
        
        self.setup_ui()
        self.populate_data()
        
        # Make dialog read-only if supplier is received
        if self.is_received:
            self.make_readonly()

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
        self.on_the_way_input = QtWidgets.QLineEdit()
        self.on_the_way_input.setPlaceholderText("Enter number of products")
        self.on_the_way_input.setMinimumHeight(36)
        # Optional: Add validator to ensure only numbers are entered
        self.on_the_way_input.setValidator(QtGui.QIntValidator(0, 100000))
        self.form_layout.addRow(on_the_way_label, self.on_the_way_input)
        
        # Status selection - NEW
        status_label = QtWidgets.QLabel("Status:")
        self.status_combo = QtWidgets.QComboBox()
        self.status_combo.addItem("Pending")
        self.status_combo.addItem("Received")
        self.status_combo.addItem("Cancelled")
        self.status_combo.setMinimumHeight(36)
        self.form_layout.addRow(status_label, self.status_combo)

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
            self.on_the_way_input.setText(str(self.item.get('products_on_the_way', 0)))
            
            # Set status if available, default to "Active"
            status = self.item.get('status', 'Active')
            status_index = self.status_combo.findText(status)
            if status_index >= 0:
                self.status_combo.setCurrentIndex(status_index)
        else:
            self.header_label.setText("Add New Supplier")
            # Auto-select status based on products on the way
            self.on_the_way_input.textChanged.connect(self.update_status_based_on_products)

    def update_status_based_on_products(self, text):
        """Update status based on products on the way"""
        if text and int(text) > 0:
            self.status_combo.setCurrentText("Pending")
        else:
            self.status_combo.setCurrentText("Received")

    def make_readonly(self):
        """Make the dialog read-only for received suppliers"""
        # Update title
        self.setWindowTitle("Supplier Details (Read-Only)")
        self.header_label.setText("Supplier Details - Cannot Edit (Already Received)")
        self.header_label.setStyleSheet("color: #FF9800; font-weight: bold; font-size: 16px;")
        
        # Disable all input fields
        self.name_input.setReadOnly(True)
        self.product_input.setReadOnly(True)
        self.category_input.setReadOnly(True)
        self.contact_input.setReadOnly(True)
        self.email_input.setReadOnly(True)
        self.returns_checkbox.setEnabled(False)
        self.on_the_way_input.setReadOnly(True)
        self.status_combo.setEnabled(False)
        
        # Change button text and disconnect save functionality
        self.save_button.setText("Close")
        self.save_button.clicked.disconnect()
        self.save_button.clicked.connect(self.accept)
        
        # Add warning message
        warning_label = QtWidgets.QLabel("⚠️ This supplier has been marked as 'Received' and cannot be modified.")
        warning_label.setStyleSheet("color: #FF9800; font-weight: bold; background-color: #FFF3E0; padding: 10px; border-radius: 5px; margin: 10px 0;")
        warning_label.setWordWrap(True)
        self.form_layout.insertRow(0, warning_label)

    def save_supplier(self):
        """Save the supplier to the database and update inventory if needed"""
        # Prevent saving if supplier is received
        if self.is_received:
            QtWidgets.QMessageBox.warning(
                self,
                "Cannot Save",
                "This supplier has been marked as 'Received' and cannot be modified."
            )
            return
        
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
            products_on_the_way = int(self.on_the_way_input.text()) if self.on_the_way_input.text() else 0
            status = self.status_combo.currentText().lower()
            
            # Check if this is a status change from something else to "received"
            old_status = None
            if self.item:
                old_status = self.item.get('status', '').lower()
            
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
                           products_on_the_way = %s,
                           status = %s
                       WHERE supplier_id = %s""",
                    (supplier_name, product_name, category, contact_number, 
                     email, accepts_returns, products_on_the_way, status, self.item['supplier_id'])
                )
            else:
                # Insert new supplier
                cursor.execute(
                    """INSERT INTO suppliers 
                       (supplier_name, product_name, category, contact_number, email, accepts_returns, products_on_the_way, status) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (supplier_name, product_name, category, contact_number, 
                     email, accepts_returns, products_on_the_way, status)
                )
            
            # If status changed to "received", update inventory
            if status == 'received' and (old_status != 'received' or not self.item):
                self.update_inventory_on_received(cursor, product_name, category, products_on_the_way)
            
            conn.commit()
            cursor.close()
            
            # Show success message with inventory update info
            if status == 'received' and products_on_the_way > 0:
                QtWidgets.QMessageBox.information(
                    self, 
                    "Success", 
                    f"Supplier saved successfully!\n{products_on_the_way} units of '{product_name}' have been added to inventory."
                )
            else:
                QtWidgets.QMessageBox.information(self, "Success", "Supplier saved successfully!")
            
            self.accept()
            
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Error saving supplier: {err}")

    def update_inventory_on_received(self, cursor, product_name, category, quantity):
        """Update inventory when supplier status changes to received"""
        if quantity <= 0:
            return
        
        try:
            # Check if product already exists in inventory
            cursor.execute(
                "SELECT product_id, quantity FROM products WHERE product_name = %s",
                (product_name,)
            )
            existing_product = cursor.fetchone()
            
            if existing_product:
                # Update existing product quantity
                new_quantity = existing_product[1] + quantity
                cursor.execute(
                    "UPDATE products SET quantity = %s WHERE product_id = %s",
                    (new_quantity, existing_product[0])
                )
                product_id = existing_product[0]
            else:
                # Create new product entry with default values
                cursor.execute(
                    """INSERT INTO products (product_name, category, quantity, price, threshold_value, availability) 
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (product_name, category, quantity, 0.00, 10, True)
                )
                product_id = cursor.lastrowid
            
            # Update inventory status with "Received" status
            cursor.execute("""
                INSERT INTO inventory_status (product_id, product_name, quantity, status, last_updated)
                VALUES (%s, %s, %s, %s, NOW())
                ON DUPLICATE KEY UPDATE
                    quantity = %s,
                    status = 'Received',
                    last_updated = NOW()
            """, (product_id, product_name, quantity, 'Received', quantity))
            
            # Log the inventory transaction
            cursor.execute(
                """INSERT INTO inventory_transactions (product_name, transaction_type, quantity, notes, transaction_date) 
                   VALUES (%s, %s, %s, %s, NOW())""",
                (product_name, 'Stock In', quantity, f'Received from supplier: {product_name}')
            )
            
            print(f"✓ Updated inventory status for {product_name}: {quantity} units received")
            
        except mysql.connector.Error as err:
            print(f"Error updating inventory: {err}")
            raise