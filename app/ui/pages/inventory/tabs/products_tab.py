from PyQt5 import QtWidgets, QtCore, QtGui
from app.utils.db_manager import DBManager
import mysql.connector
from ..style_factory import StyleFactory
from ..table_factory import TableFactory
from ..control_panel_factory import ControlPanelFactory
from ..dialogs import ProductDialog

class ProductsTab(QtWidgets.QWidget):
    """Tab for managing products in inventory"""
    
    def __init__(self, parent=None):
        super(ProductsTab, self).__init__()
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components for the products tab"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 10)
        self.layout.setSpacing(10)
        
        # Create search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search products...")
        
        # Create control panel using factory
        control_layout = ControlPanelFactory.create_search_control(
            self.search_input, 
            "+ Add Product", 
            self.show_add_product_dialog,
            self.filter_products,
            self.show_product_filter_dialog
        )
        self.layout.addLayout(control_layout)
        
        # Create products table
        self.products_table = TableFactory.create_table()
        
        # Define column headers and their relative widths
        product_columns = [
            ("ID", 0.05),
            ("Name", 0.17),
            ("Category", 0.10),
            ("Price", 0.07),
            ("Quantity", 0.07),
            ("Threshold", 0.07),
            ("Expiry Date", 0.11),
            ("Availability", 0.10),
            ("Description", 0.26)
        ]
        
        # Configure the table columns
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.products_table, product_columns, screen_width)
        
        # Add context menu to the table
        self.products_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.products_table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.layout.addWidget(self.products_table)
    
    def load_products(self):
        """Load products from the database and populate the table"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.products_table.setRowCount(0)
            
            # Reset search filter
            self.search_input.clear()
            
            # Query for all products
            cursor.execute("SELECT * FROM products ORDER BY product_name")
            products = cursor.fetchall()
            
            # Populate the table
            self.products_table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                # Set item with proper alignment
                id_item = QtWidgets.QTableWidgetItem(str(product['product_id']))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.products_table.setItem(row, 0, id_item)
                
                self.products_table.setItem(row, 1, QtWidgets.QTableWidgetItem(product['product_name']))
                self.products_table.setItem(row, 2, QtWidgets.QTableWidgetItem(product.get('category', '')))
                
                price_item = QtWidgets.QTableWidgetItem(f"₱{product['price']:.2f}")
                price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.products_table.setItem(row, 3, price_item)
                
                # Quantity with center alignment
                qty_item = QtWidgets.QTableWidgetItem(str(product['quantity']))
                qty_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.products_table.setItem(row, 4, qty_item)
                
                # Threshold with center alignment
                threshold_item = QtWidgets.QTableWidgetItem(str(product.get('threshold_value', 0)))
                threshold_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.products_table.setItem(row, 5, threshold_item)
                
                # Format expiry date
                expiry_date = product.get('expiry_date')
                expiry_str = expiry_date.strftime('%Y-%m-%d') if expiry_date else "N/A"
                expiry_item = QtWidgets.QTableWidgetItem(expiry_str)
                expiry_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.products_table.setItem(row, 6, expiry_item)
                
                # Format availability with color indicators
                availability = "In Stock" if product.get('availability', True) else "Out of Stock"
                availability_item = QtWidgets.QTableWidgetItem(availability)
                availability_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                # Set color based on availability
                if product.get('availability', True):
                    availability_item.setForeground(QtGui.QColor("#4CAF50")) 
                else:
                    availability_item.setForeground(QtGui.QColor("#FF5252")) 
                    
                self.products_table.setItem(row, 7, availability_item)
                
                # Description
                self.products_table.setItem(row, 8, QtWidgets.QTableWidgetItem(product.get('description', '')))
            
            cursor.close()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def filter_products(self):
        """Filter products based on search input"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.products_table.rowCount()):
            match_found = False
            
            for col in range(self.products_table.columnCount()):
                item = self.products_table.item(row, col)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
            
            # Show/hide row based on match
            self.products_table.setRowHidden(row, not match_found)
    
    def show_context_menu(self, position):
        """Show context menu for product actions"""
        context_menu = QtWidgets.QMenu()
        
        # Get the current row
        current_row = self.products_table.currentRow()
        
        if current_row >= 0:
            edit_action = context_menu.addAction("Edit")
            delete_action = context_menu.addAction("Delete")
            
            # Show the context menu
            action = context_menu.exec_(self.products_table.mapToGlobal(position))
            
            if action == edit_action:
                self.edit_product(current_row)
            elif action == delete_action:
                self.delete_product(current_row)
    
    def show_add_product_dialog(self):
        """Show dialog to add a new product"""
        dialog = ProductDialog(self.parent or self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_products()
            # Reset row visibility
            for row in range(self.products_table.rowCount()):
                self.products_table.setRowHidden(row, False)
    
    def edit_product(self, row):
        """Edit the selected product"""
        product_id = int(self.products_table.item(row, 0).text())
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()
            
            if product:
                dialog = ProductDialog(self.parent or self, product)
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    self.load_products()
                    
            # Reset row visibility
            for row in range(self.products_table.rowCount()):
                self.products_table.setRowHidden(row, False)
            
            cursor.close()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def delete_product(self, row):
        """Delete the selected product"""
        product_id = int(self.products_table.item(row, 0).text())
        product_name = self.products_table.item(row, 1).text()
        
        # Confirm deletion
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete product: {product_name}?\n\nThis will also delete all inventory records for this product.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if confirm == QtWidgets.QMessageBox.Yes:
            try:
                conn = DBManager.get_connection()
                cursor = conn.cursor()
                
                # First delete inventory records
                cursor.execute("DELETE FROM inventory WHERE product_id = %s", (product_id,))
                
                # Then delete the product
                cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
                
                conn.commit()
                cursor.close()
                
                # Refresh the product list
                self.load_products()
                
                # Show success message
                QtWidgets.QMessageBox.information(
                    self,
                    "Success",
                    f"Product '{product_name}' has been deleted successfully."
                )
                
                # Notify parent to update overview tab if it exists
                if self.parent and hasattr(self.parent, "update_overview_tab"):
                    self.parent.update_overview_tab()
                
            except mysql.connector.Error as err:
                if self.parent:
                    self.parent.show_error_message(f"Database error: {err}")
                else:
                    QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def show_product_filter_dialog(self):
        """Show advanced filter dialog for products"""
        # Create a dialog
        filter_dialog = QtWidgets.QDialog(self)
        filter_dialog.setWindowTitle("Filter Products")
        filter_dialog.setMinimumWidth(400)
        filter_dialog.setStyleSheet(StyleFactory.get_dialog_style())
        
        # Create layout
        layout = QtWidgets.QVBoxLayout(filter_dialog)
        form_layout = QtWidgets.QFormLayout()
        
        # Category filter
        category_label = QtWidgets.QLabel("Category:")
        category_combo = QtWidgets.QComboBox()
        category_combo.addItem("All Categories")
        
        # Get unique categories
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL AND category != ''")
            categories = cursor.fetchall()
            for category in categories:
                category_combo.addItem(category['category'])
            cursor.close()
        except mysql.connector.Error:
            pass
        
        form_layout.addRow(category_label, category_combo)
        
        # Availability filter
        availability_label = QtWidgets.QLabel("Availability:")
        availability_combo = QtWidgets.QComboBox()
        availability_combo.addItem("All")
        availability_combo.addItem("In Stock")
        availability_combo.addItem("Out of Stock")
        form_layout.addRow(availability_label, availability_combo)
        
        # Price range filter
        price_range_label = QtWidgets.QLabel("Price Range:")
        price_range_layout = QtWidgets.QHBoxLayout()
        min_price = QtWidgets.QDoubleSpinBox()
        min_price.setPrefix("₱ ")
        min_price.setMaximum(1000000)
        max_price = QtWidgets.QDoubleSpinBox()
        max_price.setPrefix("₱ ")
        max_price.setMaximum(1000000)
        max_price.setValue(1000000)
        price_range_layout.addWidget(min_price)
        price_range_layout.addWidget(QtWidgets.QLabel(" to "))
        price_range_layout.addWidget(max_price)
        form_layout.addRow(price_range_label, price_range_layout)
        
        # Buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        apply_button = QtWidgets.QPushButton("Apply Filter")
        reset_button = QtWidgets.QPushButton("Reset")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        
        buttons_layout.addWidget(reset_button)
        buttons_layout.addWidget(apply_button)
        
        layout.addLayout(form_layout)
        layout.addLayout(buttons_layout)
        
        # Connect signals
        def apply_filters():
            category = category_combo.currentText()
            availability = availability_combo.currentText()
            min_price_val = min_price.value()
            max_price_val = max_price.value()
            
            for row in range(self.products_table.rowCount()):
                show_row = True
                
                # Apply category filter
                if category != "All Categories":
                    category_cell = self.products_table.item(row, 2).text()
                    if category_cell != category:
                        show_row = False
                
                # Apply availability filter
                if availability != "All" and show_row:
                    availability_cell = self.products_table.item(row, 7).text()
                    if (availability == "In Stock" and availability_cell != "In Stock") or \
                       (availability == "Out of Stock" and availability_cell != "Out of Stock"):
                        show_row = False
                
                # Apply price filter
                if show_row:
                    price_text = self.products_table.item(row, 3).text().replace("₱", "")
                    try:
                        price = float(price_text)
                        if price < min_price_val or price > max_price_val:
                            show_row = False
                    except ValueError:
                        pass
                
                self.products_table.setRowHidden(row, not show_row)
            
            filter_dialog.accept()
        
        def reset_filters():
            # Show all rows
            for row in range(self.products_table.rowCount()):
                self.products_table.setRowHidden(row, False)
            filter_dialog.accept()
        
        apply_button.clicked.connect(apply_filters)
        reset_button.clicked.connect(reset_filters)
        
        filter_dialog.exec_()