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
        # Initialize filter state storage
        self.filter_state = {
            "is_active": False,
            "category": "All Categories",
            "availability": "All",
            "price_sort": "No Sorting"
        }
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
        self.control_layout = ControlPanelFactory.create_search_control(
            self.search_input, 
            "+ Add Product", 
            self.show_add_product_dialog,
            self.filter_products,
            self.show_product_filter_dialog
        )
        self.layout.addLayout(self.control_layout)
        
        # Store reference to filter button
        self.filter_button = self.control_layout.filter_button
        
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
        
        # Add filter indicator label
        self.filter_indicator = QtWidgets.QLabel()
        self.filter_indicator.setStyleSheet("color: #4FC3F7; font-style: italic;")
        self.filter_indicator.setVisible(False)
        self.layout.addWidget(self.filter_indicator)
    
    def load_products(self, preserve_filter=False):
        """Load products from the database and populate the table"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Remember the filter state if needed
            filter_was_active = self.filter_state["is_active"] if preserve_filter else False
            
            # Clear existing items and reset table state completely
            self.products_table.clearContents()
            self.products_table.setRowCount(0)
            
            # Reset search filter (but preserve filter state)
            self.search_input.blockSignals(True)
            self.search_input.clear()
            self.search_input.blockSignals(False)
            
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
            
            # Re-apply filters only if we need to preserve them
            if filter_was_active and preserve_filter:
                self.apply_stored_filters()
            
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
    
    def apply_stored_filters(self):
        """Apply stored filters to the table"""
        category = self.filter_state["category"]
        availability = self.filter_state["availability"]
        price_sort = self.filter_state["price_sort"]
        
        # Update the filter indicator text
        filter_text = []
        if category != "All Categories":
            filter_text.append(f"Category: {category}")
        if availability != "All":
            filter_text.append(f"Status: {availability}")
        if price_sort != "No Sorting":
            filter_text.append(f"Price: {price_sort}")
            
        if filter_text:
            self.filter_indicator.setText(f"Active filters: {', '.join(filter_text)}")
            self.filter_indicator.setVisible(True)
        else:
            self.filter_indicator.setVisible(False)
            
        # First apply filters
        for row in range(self.products_table.rowCount()):
            show_row = True
            
            # Apply category filter
            if category != "All Categories":
                category_cell = self.products_table.item(row, 2)
                if category_cell is None or category_cell.text() != category:
                    show_row = False
            
            # Apply availability filter
            if availability != "All" and show_row:
                availability_cell = self.products_table.item(row, 7)
                if availability_cell is None:
                    show_row = False
                else:
                    availability_text = availability_cell.text()
                    if (availability == "In Stock" and availability_text != "In Stock") or \
                       (availability == "Out of Stock" and availability_text != "Out of Stock"):
                        show_row = False
            
            # Show/hide row based on filters
            self.products_table.setRowHidden(row, not show_row)
        
        # Then apply sorting if selected
        if price_sort != "No Sorting":
            # Use the built-in sort functionality with the correct column and order
            order = QtCore.Qt.AscendingOrder if price_sort == "Lowest - Highest" else QtCore.Qt.DescendingOrder
            self.products_table.sortItems(3, order)
            
        # Update button appearance
        if self.filter_state["is_active"]:
            self.filter_button.setStyleSheet(StyleFactory.get_active_filter_button_style())
        else:
            self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))  # Secondary style
    
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
    
    def rebuild_table(self):
        """Completely rebuild the table with fresh data"""
        # Store current filter state
        was_filtered = self.filter_state["is_active"]
        filter_state_copy = self.filter_state.copy()
        
        # Reset filter state temporarily
        self.filter_state = {
            "is_active": False,
            "category": "All Categories",
            "availability": "All",
            "price_sort": "No Sorting"
        }
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Query for all products
            cursor.execute("SELECT * FROM products ORDER BY product_name")
            products = cursor.fetchall()
            
            # Create and configure a new table from scratch
            new_table = TableFactory.create_table()
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
            screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
            TableFactory.configure_table_columns(new_table, product_columns, screen_width)
            
            # Set up context menu for the new table
            new_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            new_table.customContextMenuRequested.connect(self.show_context_menu)
            
            # Populate the new table
            new_table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                id_item = QtWidgets.QTableWidgetItem(str(product['product_id']))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                new_table.setItem(row, 0, id_item)
                
                new_table.setItem(row, 1, QtWidgets.QTableWidgetItem(product['product_name']))
                new_table.setItem(row, 2, QtWidgets.QTableWidgetItem(product.get('category', '')))
                
                price_item = QtWidgets.QTableWidgetItem(f"₱{product['price']:.2f}")
                price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                new_table.setItem(row, 3, price_item)
                
                qty_item = QtWidgets.QTableWidgetItem(str(product['quantity']))
                qty_item.setTextAlignment(QtCore.Qt.AlignCenter)
                new_table.setItem(row, 4, qty_item)
                
                threshold_item = QtWidgets.QTableWidgetItem(str(product.get('threshold_value', 0)))
                threshold_item.setTextAlignment(QtCore.Qt.AlignCenter)
                new_table.setItem(row, 5, threshold_item)
                
                expiry_date = product.get('expiry_date')
                expiry_str = expiry_date.strftime('%Y-%m-%d') if expiry_date else "N/A"
                expiry_item = QtWidgets.QTableWidgetItem(expiry_str)
                expiry_item.setTextAlignment(QtCore.Qt.AlignCenter)
                new_table.setItem(row, 6, expiry_item)
                
                availability = "In Stock" if product.get('availability', True) else "Out of Stock"
                availability_item = QtWidgets.QTableWidgetItem(availability)
                availability_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                if product.get('availability', True):
                    availability_item.setForeground(QtGui.QColor("#4CAF50"))
                else:
                    availability_item.setForeground(QtGui.QColor("#FF5252"))
                
                new_table.setItem(row, 7, availability_item)
                new_table.setItem(row, 8, QtWidgets.QTableWidgetItem(product.get('description', '')))
        
            # Replace the old table with the new one
            old_table = self.products_table
            self.layout.replaceWidget(old_table, new_table)
            self.products_table = new_table
            old_table.deleteLater()
            
            cursor.close()
            
            # Restore filter state if necessary
            if was_filtered:
                self.filter_state = filter_state_copy
                # Add a short delay before applying filters to ensure table is fully rendered
                QtCore.QTimer.singleShot(5, self.apply_stored_filters)
        
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def show_product_filter_dialog(self):
        """Show advanced filter dialog for products"""
        from ..dialogs import ProductFilterDialog  # Import here to avoid circular imports
        
        filter_dialog = ProductFilterDialog(self, self.filter_state)
        if filter_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Get the filter state from the dialog
            new_filter_state = filter_dialog.get_filter_state()
            
            # Check if filters were reset
            if not new_filter_state["is_active"] and self.filter_state["is_active"]:
                # Filters were reset
                self.filter_state = new_filter_state
                self.filter_indicator.setVisible(False)
                self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
                
                # Completely rebuild the table
                QtCore.QTimer.singleShot(50, self.rebuild_table)
            else:
                # Regular filter applied
                self.filter_state = new_filter_state
                
                # Apply filters after dialog is closed
                if self.filter_state["is_active"]:
                    QtCore.QTimer.singleShot(50, self.apply_stored_filters)
                    # Show filter indicator
                    self.filter_indicator.setVisible(True)
                    # Use the same blue button style
                    self.filter_button.setStyleSheet(StyleFactory.get_active_filter_button_style())
                else:
                    self.filter_indicator.setVisible(False)
                    self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))