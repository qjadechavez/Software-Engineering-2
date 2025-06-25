from PyQt5 import QtWidgets, QtCore, QtGui
import mysql.connector
from app.utils.db_manager import DBManager
from .base_dialog import BaseDialog

class ServiceDialog(BaseDialog):
    """Dialog for adding or editing services"""
    
    def __init__(self, parent=None, service=None):
        super(ServiceDialog, self).__init__(parent, service, "Service")
        self.setup_ui()
        self.populate_data()
        # Store selected products
        self.selected_products = []
        self.load_products()
        self.load_service_products()
        
    def setup_ui(self):
        """Set up the service dialog UI"""
        self.setup_base_ui(750)  # Increased width for products section
        
        self.save_button.setText("Save Service")
        self.save_button.clicked.connect(self.save_service)
        
        # Service name input
        name_label = QtWidgets.QLabel("Service Name:")
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Enter service name")
        self.name_input.setMinimumHeight(36)
        self.form_layout.addRow(name_label, self.name_input)
        
        # Category input
        category_label = QtWidgets.QLabel("Category:")
        self.category_input = QtWidgets.QLineEdit()
        self.category_input.setPlaceholderText("Enter service category")
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
        
        # Availability checkbox
        availability_label = QtWidgets.QLabel("Availability:")
        self.availability_checkbox = QtWidgets.QCheckBox("Service is available")
        self.availability_checkbox.setChecked(True)
        self.form_layout.addRow(availability_label, self.availability_checkbox)
        
        # Description input (multiline)
        desc_label = QtWidgets.QLabel("Description:")
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Enter service description")
        self.description_input.setMinimumHeight(80)  # Reduced height to make room for products
        self.form_layout.addRow(desc_label, self.description_input)
        
        # Products section
        products_header = QtWidgets.QLabel("Products Used:")
        products_header.setStyleSheet("font-weight: bold; margin-top: 15px;")
        self.form_layout.addRow(products_header)
        
        # Products table
        self.products_table = QtWidgets.QTableWidget()
        self.products_table.setColumnCount(4)  # ID, Name, Quantity, Action
        self.products_table.setHorizontalHeaderLabels(["ID", "Product Name", "Quantity", "Action"])
        self.products_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.products_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.products_table.setMinimumHeight(150)
        self.products_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.products_table.setColumnWidth(0, 50)
        self.products_table.setColumnWidth(2, 70)
        self.products_table.setColumnWidth(3, 100)
        self.form_layout.addRow(self.products_table)
        
        # Add product button
        add_product_layout = QtWidgets.QHBoxLayout()
        self.add_product_button = QtWidgets.QPushButton("+ Add Product")
        self.add_product_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border-radius: 4px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.add_product_button.clicked.connect(self.show_product_selection_dialog)
        add_product_layout.addStretch()
        add_product_layout.addWidget(self.add_product_button)
        self.form_layout.addRow(add_product_layout)

    def load_products(self):
        """Load all available products from database"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT product_id, product_name, category, price FROM products WHERE availability = 1 ORDER BY product_name")
            self.available_products = cursor.fetchall()
            cursor.close()
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load products: {err}")
            self.available_products = []

    def load_service_products(self):
        """Load products associated with this service (if editing)"""
        if not self.item or 'service_id' not in self.item:
            return
            
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT sp.service_product_id, sp.product_id, p.product_name, p.category, sp.quantity
                FROM service_products sp
                JOIN products p ON sp.product_id = p.product_id
                WHERE sp.service_id = %s
            """
            cursor.execute(query, (self.item['service_id'],))
            products = cursor.fetchall()
            cursor.close()
            
            # Clear existing selected products
            self.selected_products = products
            self.update_products_table()
            
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load service products: {err}")

    def update_products_table(self):
        """Update the products table with selected products"""
        self.products_table.setRowCount(0)
        
        for i, product in enumerate(self.selected_products):
            self.products_table.insertRow(i)
            
            # ID column
            id_item = QtWidgets.QTableWidgetItem(str(product['product_id']))
            id_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.products_table.setItem(i, 0, id_item)
            
            # Product name
            self.products_table.setItem(i, 1, QtWidgets.QTableWidgetItem(product['product_name']))
            
            # Quantity
            qty_item = QtWidgets.QTableWidgetItem(str(product['quantity']))
            qty_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.products_table.setItem(i, 2, qty_item)
            
            # Remove button
            remove_btn = QtWidgets.QPushButton("Remove")
            remove_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border-radius: 3px;
                    padding: 3px 8px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            remove_btn.clicked.connect(lambda checked, row=i: self.remove_product(row))
            
            # Set the button as a cell widget
            self.products_table.setCellWidget(i, 3, remove_btn)
    
    def remove_product(self, row):
        """Remove a product from the selected products list"""
        if 0 <= row < len(self.selected_products):
            del self.selected_products[row]
            self.update_products_table()

    def show_product_selection_dialog(self):
        """Show dialog for product selection"""
        product_dialog = ProductSelectionDialog(self, self.available_products, self.selected_products)
        if product_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.selected_products = product_dialog.get_selected_products()
            self.update_products_table()

    def populate_data(self):
        """Populate dialog with service data if editing"""
        if self.item:
            self.header_label.setText("Edit Service")
            self.name_input.setText(self.item['service_name'])
            self.category_input.setText(self.item.get('category', ''))
            self.description_input.setText(self.item.get('description', ''))
            self.price_input.setValue(float(self.item['price']))
            
            self.availability_checkbox.setChecked(self.item.get('availability', True))
        else:
            self.header_label.setText("Add New Service")
    
    def save_service(self):
        """Save the service to the database"""
        # Validate inputs
        if not self.name_input.text().strip():
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Service name is required.")
            return
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            service_name = self.name_input.text().strip()
            category = self.category_input.text().strip()
            description = self.description_input.toPlainText().strip()
            price = self.price_input.value()
            availability = self.availability_checkbox.isChecked()
            
            if self.item:
                # Update existing service
                cursor.execute(
                    """UPDATE services 
                       SET service_name = %s, 
                           category = %s, 
                           description = %s, 
                           price = %s, 
                           availability = %s 
                       WHERE service_id = %s""",
                    (service_name, category, description, price, 
                     availability, self.item['service_id'])
                )
                service_id = self.item['service_id']
                
                # Delete existing product associations
                cursor.execute("DELETE FROM service_products WHERE service_id = %s", (service_id,))
            else:
                # Insert new service
                cursor.execute(
                    """INSERT INTO services 
                       (service_name, category, description, price, availability) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (service_name, category, description, price, availability)
                )
                service_id = cursor.lastrowid
            
            # Insert product associations
            for product in self.selected_products:
                cursor.execute(
                    """INSERT INTO service_products 
                       (service_id, product_id, quantity) 
                       VALUES (%s, %s, %s)""",
                    (service_id, product['product_id'], product['quantity'])
                )
            
            conn.commit()
            cursor.close()
            
            self.accept()
            
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Error saving service: {err}")


class ProductSelectionDialog(QtWidgets.QDialog):
    """Dialog for selecting products to be used in a service"""
    
    def __init__(self, parent, available_products, current_selected):
        super(ProductSelectionDialog, self).__init__(parent)
        self.available_products = available_products
        
        # Create a deep copy of current selected products
        self.selected_products = []
        for product in current_selected:
            self.selected_products.append(product.copy())
            
        self.setup_ui()
        self.setWindowTitle("Select Products")
        
    def setup_ui(self):
        """Set up the UI components"""
        self.setMinimumWidth(600)
        layout = QtWidgets.QVBoxLayout(self)
        
        # Search input
        search_layout = QtWidgets.QHBoxLayout()
        search_label = QtWidgets.QLabel("Search Products:")
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Type to search products...")
        self.search_input.textChanged.connect(self.filter_products)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Products table
        self.products_table = QtWidgets.QTableWidget()
        self.products_table.setColumnCount(5)  # ID, Name, Category, Price, Add
        self.products_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price", "Add"])
        self.products_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.products_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.products_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.products_table.setColumnWidth(0, 50)
        self.products_table.setColumnWidth(2, 100)
        self.products_table.setColumnWidth(3, 80)
        self.products_table.setColumnWidth(4, 100)
        layout.addWidget(self.products_table)
        
        # Load products
        self.populate_products_table()
        
        # Selected products section
        selected_label = QtWidgets.QLabel("Selected Products:")
        selected_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(selected_label)
        
        self.selected_table = QtWidgets.QTableWidget()
        self.selected_table.setColumnCount(5)  # ID, Name, Quantity, Price, Remove
        self.selected_table.setHorizontalHeaderLabels(["ID", "Name", "Quantity", "Price", "Remove"])
        self.selected_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.selected_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.selected_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.selected_table.setColumnWidth(0, 50)
        self.selected_table.setColumnWidth(2, 70)
        self.selected_table.setColumnWidth(3, 80)
        self.selected_table.setColumnWidth(4, 100)
        layout.addWidget(self.selected_table)
        
        # Update selected products table
        self.update_selected_table()
        
        # Buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.save_button = QtWidgets.QPushButton("Save Selection")
        self.save_button.clicked.connect(self.accept)
        self.save_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_button)
        layout.addLayout(buttons_layout)
        
    def populate_products_table(self):
        """Populate the products table"""
        self.products_table.setRowCount(0)
        
        for i, product in enumerate(self.available_products):
            self.products_table.insertRow(i)
            
            # ID column
            id_item = QtWidgets.QTableWidgetItem(str(product['product_id']))
            id_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.products_table.setItem(i, 0, id_item)
            
            # Product name
            self.products_table.setItem(i, 1, QtWidgets.QTableWidgetItem(product['product_name']))
            
            # Category
            self.products_table.setItem(i, 2, QtWidgets.QTableWidgetItem(product['category']))
            
            # Price
            price_item = QtWidgets.QTableWidgetItem(f"₱{float(product['price']):.2f}")
            price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            self.products_table.setItem(i, 3, price_item)
            
            # Add button
            add_btn = QtWidgets.QPushButton("Add")
            add_btn.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    border-radius: 3px;
                    padding: 3px 8px;
                }
                QPushButton:hover {
                    background-color: #0069d9;
                }
            """)
            add_btn.clicked.connect(lambda checked, row=i: self.add_product(row))
            
            self.products_table.setCellWidget(i, 4, add_btn)
            
    def update_selected_table(self):
        """Update the selected products table"""
        self.selected_table.setRowCount(0)
        
        for i, product in enumerate(self.selected_products):
            self.selected_table.insertRow(i)
            
            # ID column
            id_item = QtWidgets.QTableWidgetItem(str(product['product_id']))
            id_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.selected_table.setItem(i, 0, id_item)
            
            # Product name
            self.selected_table.setItem(i, 1, QtWidgets.QTableWidgetItem(product['product_name']))
            
            # Quantity (editable)
            quantity_widget = QtWidgets.QSpinBox()
            quantity_widget.setRange(1, 100)
            quantity_widget.setValue(product.get('quantity', 1))
            quantity_widget.valueChanged.connect(lambda value, index=i: self.update_quantity(index, value))
            self.selected_table.setCellWidget(i, 2, quantity_widget)
            
            # Price
            if 'price' in product:
                price_item = QtWidgets.QTableWidgetItem(f"₱{float(product['price']):.2f}")
                price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.selected_table.setItem(i, 3, price_item)
            
            # Remove button
            remove_btn = QtWidgets.QPushButton("Remove")
            remove_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border-radius: 3px;
                    padding: 3px 8px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                }
            """)
            remove_btn.clicked.connect(lambda checked, row=i: self.remove_selected(row))
            
            self.selected_table.setCellWidget(i, 4, remove_btn)
    
    def update_quantity(self, index, value):
        """Update quantity for a selected product"""
        if 0 <= index < len(self.selected_products):
            self.selected_products[index]['quantity'] = value
    
    def add_product(self, row):
        """Add a product to the selected products list"""
        if 0 <= row < len(self.available_products):
            product = self.available_products[row].copy()
            
            # Check if product is already selected
            for existing in self.selected_products:
                if existing['product_id'] == product['product_id']:
                    # Just increase quantity if already selected
                    existing['quantity'] = existing.get('quantity', 1) + 1
                    self.update_selected_table()
                    return
            
            # Add new product with quantity 1
            product['quantity'] = 1
            self.selected_products.append(product)
            self.update_selected_table()
    
    def remove_selected(self, row):
        """Remove a product from the selected list"""
        if 0 <= row < len(self.selected_products):
            del self.selected_products[row]
            self.update_selected_table()
    
    def filter_products(self):
        """Filter products based on search text"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.products_table.rowCount()):
            match_found = False
            
            # Check name and category columns
            for col in [1, 2]:  # Name and Category columns
                item = self.products_table.item(row, col)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
            
            # Show/hide row based on match
            self.products_table.setRowHidden(row, not match_found)
    
    def get_selected_products(self):
        """Return the list of selected products with quantities"""
        return self.selected_products