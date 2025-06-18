from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
from .base_dialog import BaseDialog

class ProductDialog(BaseDialog):
    """Dialog for adding or editing products"""
    
    def __init__(self, parent=None, product=None):
        super(ProductDialog, self).__init__(parent, product, "Product")
        self.setup_ui()
        self.populate_data()
    
    def setup_ui(self):
        """Set up the product dialog UI"""
        self.setup_base_ui(650)
        
        self.save_button.setText("Save Product")
        self.save_button.clicked.connect(self.save_product)
        
        # Product name input
        name_label = QtWidgets.QLabel("Product Name:")
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Enter product name")
        self.name_input.setMinimumHeight(36)
        self.form_layout.addRow(name_label, self.name_input)
        
        # Category input
        category_label = QtWidgets.QLabel("Category:")
        self.category_input = QtWidgets.QLineEdit()
        self.category_input.setPlaceholderText("Enter product category")
        self.category_input.setMinimumHeight(36)
        self.form_layout.addRow(category_label, self.category_input)
        
        # Price input
        price_label = QtWidgets.QLabel("Price:")
        self.price_input = QtWidgets.QDoubleSpinBox()
        self.price_input.setRange(0, 100000)
        self.price_input.setDecimals(2)
        self.price_input.setSingleStep(0.01)
        self.price_input.setPrefix("₱ ")
        self.price_input.setMinimumHeight(36)
        self.form_layout.addRow(price_label, self.price_input)
        
        # Quantity input
        qty_label = QtWidgets.QLabel("Quantity:")
        self.quantity_input = QtWidgets.QSpinBox()
        self.quantity_input.setRange(0, 100000)
        self.quantity_input.setMinimumHeight(36)
        self.form_layout.addRow(qty_label, self.quantity_input)
        
        # Threshold input
        threshold_label = QtWidgets.QLabel("Threshold Value:")
        self.threshold_input = QtWidgets.QSpinBox()
        self.threshold_input.setRange(0, 10000)
        self.threshold_input.setValue(10)
        self.threshold_input.setMinimumHeight(36)
        self.form_layout.addRow(threshold_label, self.threshold_input)
        
        # Expiry date input
        expiry_label = QtWidgets.QLabel("Expiry Date:")
        self.expiry_date_input = QtWidgets.QDateEdit()
        self.expiry_date_input.setCalendarPopup(True)
        self.expiry_date_input.setDisplayFormat("yyyy-MM-dd")
        self.expiry_date_input.setMinimumHeight(36)
        self.form_layout.addRow(expiry_label, self.expiry_date_input)
        
        # Availability checkbox
        availability_label = QtWidgets.QLabel("Availability:")
        self.availability_checkbox = QtWidgets.QCheckBox("Product is available for sale")
        self.availability_checkbox.setChecked(True)
        self.form_layout.addRow(availability_label, self.availability_checkbox)
        
        # Description input (multiline)
        desc_label = QtWidgets.QLabel("Description:")
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Enter product description")
        self.description_input.setMinimumHeight(120)
        self.form_layout.addRow(desc_label, self.description_input)
    
    def populate_data(self):
        """Populate dialog with product data if editing"""
        if self.item:
            # We're editing an existing product
            self.header_label.setText("Edit Product")
            self.name_input.setText(self.item['product_name'])
            self.category_input.setText(self.item.get('category', ''))
            self.description_input.setText(self.item.get('description', ''))
            self.price_input.setValue(float(self.item['price']))
            self.quantity_input.setValue(self.item['quantity'])
            self.threshold_input.setValue(self.item.get('threshold_value', 10))
            
            # Set expiry date if available
            if self.item.get('expiry_date'):
                expiry_date = QtCore.QDate.fromString(str(self.item['expiry_date']), "yyyy-MM-dd")
                self.expiry_date_input.setDate(expiry_date)
            
            # Set availability
            self.availability_checkbox.setChecked(self.item.get('availability', True))
        else:
            # Adding a new product
            self.header_label.setText("Add New Product")
            default_expiry = QtCore.QDate.currentDate().addYears(1)
            self.expiry_date_input.setDate(default_expiry)
    
    def save_product(self):
        """Save the product to the database"""
        # Validate inputs
        if not self.name_input.text().strip():
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Product name is required.")
            return
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            product_name = self.name_input.text().strip()
            category = self.category_input.text().strip()
            description = self.description_input.toPlainText().strip()
            price = self.price_input.value()
            quantity = self.quantity_input.value()
            threshold = self.threshold_input.value()
            expiry_date = self.expiry_date_input.date().toString("yyyy-MM-dd")
            availability = self.availability_checkbox.isChecked()
            
            if self.item:
                # Update existing product
                cursor.execute(
                    """UPDATE products 
                       SET product_name = %s, 
                           category = %s, 
                           description = %s, 
                           price = %s, 
                           quantity = %s, 
                           threshold_value = %s, 
                           expiry_date = %s, 
                           availability = %s 
                       WHERE product_id = %s""",
                    (product_name, category, description, price, quantity, 
                     threshold, expiry_date, availability, self.item['product_id'])
                )
                
                # Update inventory record if it exists
                cursor.execute(
                    """INSERT INTO inventory (product_id, quantity, status, last_updated) 
                       VALUES (%s, %s, %s, NOW())
                       ON DUPLICATE KEY UPDATE 
                       quantity = VALUES(quantity),
                       last_updated = NOW()""",
                    (self.item['product_id'], quantity, "Updated")
                )
            else:
                # Insert new product
                cursor.execute(
                    """INSERT INTO products 
                       (product_name, category, description, price, quantity, 
                        threshold_value, expiry_date, availability) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (product_name, category, description, price, quantity, 
                     threshold, expiry_date, availability)
                )
                
                # Get the ID of the new product
                product_id = cursor.lastrowid
                
                # Create initial inventory entry
                cursor.execute(
                    "INSERT INTO inventory (product_id, quantity, status) VALUES (%s, %s, %s)",
                    (product_id, quantity, "New")
                )
            
            conn.commit()
            cursor.close()
            
            self.accept()
            
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Error saving product: {err}")