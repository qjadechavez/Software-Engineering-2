from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage
from app.utils.db_manager import DBManager
import mysql.connector
from datetime import datetime

class InventoryPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(InventoryPage, self).__init__(parent, title="Inventory", user_info=user_info)
        self.load_products()
    
    def createContent(self):
        # Content area with reduced margins for more space
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(8)
        
        # Create tabs for Products and Inventory with improved styling
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #444; 
                background-color: #232323;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #343434;
                color: #ffffff;
                padding: 10px 30px;  /* Increased padding for wider tabs */
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                min-width: 120px;  /* Set minimum width for tabs */
                font-size: 13px;  /* Ensure text is properly sized */
            }
            QTabBar::tab:selected {
                background-color: #1a1a1a;
                border-bottom-color: #1a1a1a;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3a3a3a;
            }
        """)
        
        # Create Products tab
        self.products_tab = QtWidgets.QWidget()
        self.products_layout = QtWidgets.QVBoxLayout(self.products_tab)
        self.products_layout.setContentsMargins(10, 15, 10, 10)
        self.products_layout.setSpacing(10)
        
        # Create search and control area with better spacing
        control_layout = QtWidgets.QHBoxLayout()
        control_layout.setSpacing(10)
        
        # Search input with improved styling
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search products...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #555;
                border-radius: 18px;
                padding: 8px 15px;
                background: #2a2a2a;
                color: white;
                font-size: 13px;
                min-height: 36px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d7;
                background: #323232;
            }
        """)
        self.search_input.textChanged.connect(self.filter_products)
        
        # Search icon and label
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setSpacing(5)
        
        search_icon = QtWidgets.QLabel()
        search_icon.setPixmap(QtGui.QPixmap("app/resources/images/search.png").scaledToHeight(16) if QtCore.QFile("app/resources/images/search.png").exists() else QtGui.QPixmap())
        search_icon.setStyleSheet("color: white; margin-right: 5px;")
        
        search_label = QtWidgets.QLabel("Search:")
        search_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        
        search_layout.addWidget(search_icon)
        search_layout.addWidget(search_label)
        
        # Add product button with improved contrast and styling
        self.add_product_btn = QtWidgets.QPushButton("+ Add Product")
        self.add_product_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;  /* Brighter blue for better contrast */
                color: white;
                border-radius: 18px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 13px;
                min-width: 150px;
                min-height: 36px;
            }
            QPushButton:hover {
                background-color: #0099FF;
            }
            QPushButton:pressed {
                background-color: #0066BB;
            }
        """)
        self.add_product_btn.clicked.connect(self.show_add_product_dialog)
        
        # Layout for controls
        control_layout.addLayout(search_layout)
        control_layout.addWidget(self.search_input, 1)
        control_layout.addWidget(self.add_product_btn)
        
        self.products_layout.addLayout(control_layout)
        
        # Create products table with optimized column widths
        self.products_table = QtWidgets.QTableWidget()
        self.products_table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #444;
                color: white;
                border-radius: 5px;
                border: 1px solid #555;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #2c2c2c;
                color: white;
                padding: 8px;
                border: 1px solid #444;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
                background-color: #1e1e1e;  /* Force all rows to have same background */
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #666;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar:horizontal {
                background: #2a2a2a;
                height: 12px;
            }
            QScrollBar::handle:horizontal {
                background: #666;
                border-radius: 5px;
                min-width: 20px;
            }
        """)
        
        # Set up the table columns with optimized widths
        self.products_table.setColumnCount(9)
        self.products_table.setHorizontalHeaderLabels([
            "ID", "Name", "Category", "Price", "Quantity", 
            "Threshold", "Expiry Date", "Availability", "Description"
        ])
        
        # Set column widths - optimized to use available space
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        table_width = screen_width - 300  # Accounting for sidebar and margins
        
        # Calculate column widths as percentages of available space
        self.products_table.setColumnWidth(0, int(table_width * 0.05))  # ID (5%)
        self.products_table.setColumnWidth(1, int(table_width * 0.18))  # Name (18%)
        self.products_table.setColumnWidth(2, int(table_width * 0.12))  # Category (12%)
        self.products_table.setColumnWidth(3, int(table_width * 0.08))  # Price (8%)
        self.products_table.setColumnWidth(4, int(table_width * 0.08))  # Quantity (8%)
        self.products_table.setColumnWidth(5, int(table_width * 0.08))  # Threshold (8%)
        self.products_table.setColumnWidth(6, int(table_width * 0.11))  # Expiry Date (11%)
        self.products_table.setColumnWidth(7, int(table_width * 0.10))  # Availability (10%)
        self.products_table.setColumnWidth(8, int(table_width * 0.20))  # Description (20%)
        
        # Adjust table properties
        self.products_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.products_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.products_table.setAlternatingRowColors(False)  # Change this line
        self.products_table.verticalHeader().setVisible(False)
        self.products_table.setSortingEnabled(True)
        self.products_table.setShowGrid(True)
        
        # Set table to take all available space
        self.products_table.horizontalHeader().setStretchLastSection(True)
        self.products_table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Interactive)
        
        # Add context menu to the table
        self.products_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.products_table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.products_layout.addWidget(self.products_table)
        
        # Add Products tab to the tab widget
        self.tabs.addTab(self.products_tab, "Products")
        
        # Create Inventory tab with improved styling
        self.inventory_tab = QtWidgets.QWidget()
        self.inventory_layout = QtWidgets.QVBoxLayout(self.inventory_tab)
        self.inventory_layout.setContentsMargins(10, 15, 10, 10)
        self.inventory_layout.setSpacing(15)
        
        # Add inventory analytics section with better spacing
        analytics_layout = QtWidgets.QHBoxLayout()
        analytics_layout.setSpacing(15)
        
        # Low stock items card with improved visualization
        low_stock_card = self.create_info_card("Low Stock Items", "0", "#FF5252", "warning")
        analytics_layout.addWidget(low_stock_card)
        
        # Expired items card
        expired_card = self.create_info_card("Expired Items", "0", "#FF9800", "expired")
        analytics_layout.addWidget(expired_card)
        
        # Total products card
        total_card = self.create_info_card("Total Products", "0", "#4CAF50", "products")
        analytics_layout.addWidget(total_card)
        
        self.inventory_layout.addLayout(analytics_layout)
        
        # Add inventory table (simplified version of product table)
        self.inventory_table = QtWidgets.QTableWidget()
        self.inventory_table.setStyleSheet(self.products_table.styleSheet())
        
        # Set up inventory columns
        self.inventory_table.setColumnCount(5)
        self.inventory_table.setHorizontalHeaderLabels([
            "ID", "Product Name", "Quantity", "Status", "Last Updated"
        ])
        
        # Set column widths - optimized for inventory view
        self.inventory_table.setColumnWidth(0, int(table_width * 0.08))    # ID
        self.inventory_table.setColumnWidth(1, int(table_width * 0.32))    # Product Name
        self.inventory_table.setColumnWidth(2, int(table_width * 0.15))    # Quantity
        self.inventory_table.setColumnWidth(3, int(table_width * 0.20))    # Status
        self.inventory_table.setColumnWidth(4, int(table_width * 0.25))    # Last Updated
        
        # Adjust table properties
        self.inventory_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.inventory_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.inventory_table.setAlternatingRowColors(False)  # Also for inventory table
        self.inventory_table.verticalHeader().setVisible(False)
        self.inventory_table.setSortingEnabled(True)
        self.inventory_table.horizontalHeader().setStretchLastSection(True)
        
        self.inventory_layout.addWidget(self.inventory_table)
        
        # Add Inventory tab to the tab widget
        self.tabs.addTab(self.inventory_tab, "Inventory Status")
        
        # Add the tab widget to the main layout
        self.content_layout.addWidget(self.tabs)
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
        
        # Connect the tab change signal
        self.tabs.currentChanged.connect(self.handle_tab_change)
    
    def create_info_card(self, title, value, color, icon_type=None):
        """Create an info card for the inventory dashboard with icons"""
        card = QtWidgets.QFrame()
        card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #232323;
                border-radius: 10px;
                border-left: 5px solid {color};
                padding: 10px;
                min-height: 100px;
            }}
        """)
        
        card_layout = QtWidgets.QHBoxLayout(card)
        card_layout.setContentsMargins(15, 10, 15, 10)
        
        # Add icon based on card type
        icon_label = QtWidgets.QLabel()
        icon_path = ""
        
        if icon_type == "warning":
            icon_path = "app/resources/images/warning.png"
        elif icon_type == "expired":
            icon_path = "app/resources/images/expired.png"
        elif icon_type == "products":
            icon_path = "app/resources/images/products.png"
        
        # If icon exists, show it
        if icon_path and QtCore.QFile(icon_path).exists():
            icon_label.setPixmap(QtGui.QPixmap(icon_path).scaledToHeight(40))
        else:
            # Create a colored circle if icon doesn't exist
            icon_label.setText("●")
            icon_label.setStyleSheet(f"""
                color: {color};
                font-size: 40px;
            """)
        
        icon_label.setFixedSize(50, 50)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Text content
        text_layout = QtWidgets.QVBoxLayout()
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            color: #AAAAAA;
            font-size: 14px;
            font-weight: bold;
        """)
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet(f"""
            color: {color};
            font-size: 28px;
            font-weight: bold;
        """)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        
        # Add icon and text to card layout
        card_layout.addWidget(icon_label)
        card_layout.addLayout(text_layout, 1)
        
        # Store the value label to update it later
        card.value_label = value_label
        
        return card
    
    def handle_tab_change(self, index):
        """Handle changing between tabs"""
        if index == 1:  # Inventory Status tab
            self.load_inventory()
            self.update_inventory_analytics()
    
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
                
                # Price with better formatting and alignment
                price_item = QtWidgets.QTableWidgetItem(f"${product['price']:.2f}")
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
                    availability_item.setForeground(QtGui.QColor("#4CAF50"))  # Green for in stock
                else:
                    availability_item.setForeground(QtGui.QColor("#FF5252"))  # Red for out of stock
                    
                self.products_table.setItem(row, 7, availability_item)
                
                # Description
                self.products_table.setItem(row, 8, QtWidgets.QTableWidgetItem(product.get('description', '')))
            
            cursor.close()
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
    def load_inventory(self):
        """Load inventory data from the database"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.inventory_table.setRowCount(0)
            
            # Query for inventory items with product names
            cursor.execute("""
                SELECT i.inventory_id, p.product_name, i.quantity, i.status, i.last_updated
                FROM inventory i
                JOIN products p ON i.product_id = p.product_id
                ORDER BY i.last_updated DESC
            """)
            
            inventory_items = cursor.fetchall()
            
            # Populate the table
            self.inventory_table.setRowCount(len(inventory_items))
            
            for row, item in enumerate(inventory_items):
                self.inventory_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item['inventory_id'])))
                self.inventory_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item['product_name']))
                self.inventory_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item['quantity'])))
                self.inventory_table.setItem(row, 3, QtWidgets.QTableWidgetItem(item['status'] or "N/A"))
                
                # Format last updated date
                last_updated = item.get('last_updated')
                last_updated_str = last_updated.strftime('%Y-%m-%d %H:%M') if last_updated else "N/A"
                self.inventory_table.setItem(row, 4, QtWidgets.QTableWidgetItem(last_updated_str))
            
            cursor.close()
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
    def update_inventory_analytics(self):
        """Update inventory analytics cards"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get total products count
            cursor.execute("SELECT COUNT(*) as count FROM products")
            total_count = cursor.fetchone()['count']
            
            # Get low stock items count
            cursor.execute("""
                SELECT COUNT(*) as count FROM products 
                WHERE quantity <= threshold_value
            """)
            low_stock_count = cursor.fetchone()['count']
            
            # Get expired items count
            cursor.execute("""
                SELECT COUNT(*) as count FROM products 
                WHERE expiry_date IS NOT NULL AND expiry_date < CURDATE()
            """)
            expired_count = cursor.fetchone()['count']
            
            # Update the info cards
            for card in self.findChildren(QtWidgets.QFrame):
                if hasattr(card, 'value_label'):
                    # Get the text layout which is the second item (index 1) in card layout
                    text_layout = card.layout().itemAt(1).layout()
                    if text_layout:
                        # Get the title label which is the first widget in the text layout
                        title_label = text_layout.itemAt(0).widget()
                        if title_label.text() == "Low Stock Items":
                            card.value_label.setText(str(low_stock_count))
                        elif title_label.text() == "Expired Items":
                            card.value_label.setText(str(expired_count))
                        elif title_label.text() == "Total Products":
                            card.value_label.setText(str(total_count))
        
            cursor.close()
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
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
        dialog = ProductDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_products()
    
    def edit_product(self, row):
        """Edit the selected product"""
        product_id = int(self.products_table.item(row, 0).text())
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()
            
            if product:
                dialog = ProductDialog(self, product)
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    self.load_products()
                    
            for row in range(self.products_table.rowCount()):
                self.products_table.setRowHidden(row, False)
            
            cursor.close()
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
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
                
            except mysql.connector.Error as err:
                self.show_error_message(f"Database error: {err}")
    
    def show_error_message(self, message):
        """Show error message dialog"""
        QtWidgets.QMessageBox.critical(self, "Error", message)


class ProductDialog(QtWidgets.QDialog):
    """Dialog for adding or editing products"""
    
    def __init__(self, parent=None, product=None):
        super(ProductDialog, self).__init__(parent)
        
        self.product = product
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # Remove window frame
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Enable translucent background
        self.setup_ui()
        
        if product:
            # We're editing an existing product
            self.header_label.setText("Edit Product")
            self.name_input.setText(product['product_name'])
            self.category_input.setText(product.get('category', ''))
            self.description_input.setText(product.get('description', ''))
            self.price_input.setValue(float(product['price']))
            self.quantity_input.setValue(product['quantity'])
            self.threshold_input.setValue(product.get('threshold_value', 10))
            
            # Set expiry date if available
            if product.get('expiry_date'):
                expiry_date = QtCore.QDate.fromString(str(product['expiry_date']), "yyyy-MM-dd")
                self.expiry_date_input.setDate(expiry_date)
            
            # Set availability
            self.availability_checkbox.setChecked(product.get('availability', True))
        else:
            # We're adding a new product
            self.header_label.setText("Add New Product")
            # Set default expiry date to one year from now
            default_expiry = QtCore.QDate.currentDate().addYears(1)
            self.expiry_date_input.setDate(default_expiry)
    
    def setup_ui(self):
        """Set up the dialog UI with improved design"""
        # Set dialog size
        self.resize(550, 650)
        
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create main container with rounded corners
        self.container = QtWidgets.QFrame(self)
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            #container {
                background-color: rgba(35, 35, 35, 0.95);
                border-radius: 12px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }
        """)
        
        # Container layout
        container_layout = QtWidgets.QVBoxLayout(self.container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)
        
        # Header with close button
        header_layout = QtWidgets.QHBoxLayout()
        
        self.header_label = QtWidgets.QLabel("Add Product")
        self.header_label.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        
        self.close_button = QtWidgets.QPushButton("×")
        self.close_button.setFixedSize(35, 35)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #aaa;
                font-size: 20px;
                font-weight: bold;
                border: none;
                border-radius: 15px;
                margin: 0px 0px 0px 0px;
                line-height: 33px;
                
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border-radius: 15px;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
            }
        """)
        self.close_button.clicked.connect(self.reject)
        
        header_layout.addWidget(self.header_label)
        header_layout.addStretch()
        header_layout.addWidget(self.close_button)
        
        container_layout.addLayout(header_layout)
        
        # Add separator
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        separator.setStyleSheet("background-color: rgba(100, 100, 100, 0.3); margin: 0px 0px 10px 0px;")
        container_layout.addWidget(separator)
        
        # Scroll area for form
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #292929;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Form content
        form_widget = QtWidgets.QWidget()
        form_widget.setStyleSheet("background: transparent;")
        form_layout = QtWidgets.QFormLayout(form_widget)
        form_layout.setContentsMargins(5, 5, 5, 5)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        form_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        
        # Apply global styles
        self.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
                background: transparent;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #007acc;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 1px solid #007acc;
                background-color: #333;
            }
            QCheckBox {
                color: white;
                font-size: 14px;
                background: transparent;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                background: #2d2d2d;
                border: 1px solid #444;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background: #007acc;
                border: none;
                image: url(app/resources/images/check.png);
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 25px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0088e0;
            }
            QPushButton:pressed {
                background-color: #006bb3;
            }
            QPushButton#cancelBtn {
                background-color: #555;
            }
            QPushButton#cancelBtn:hover {
                background-color: #666;
            }
            QPushButton#cancelBtn:pressed {
                background-color: #444;
            }
            QSpinBox::up-button, QDoubleSpinBox::up-button, QDateEdit::up-button {
                subcontrol-origin: border;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #444;
                border-bottom: 1px solid #444;
                border-top-right-radius: 5px;
                background: #333;
            }
            QSpinBox::down-button, QDoubleSpinBox::down-button, QDateEdit::down-button {
                subcontrol-origin: border;
                subcontrol-position: bottom right;
                width: 20px;
                border-left: 1px solid #444;
                border-top: 1px solid #444;
                border-bottom-right-radius: 5px;
                background: #333;
            }
            QDateEdit::drop-down {
                subcontrol-origin: border;
                subcontrol-position: center right;
                width: 20px;
                border-left: 1px solid #444;
                background: #333;
            }
        """)
        
        # Name input
        name_label = QtWidgets.QLabel("Product Name:")
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Enter product name")
        self.name_input.setMinimumHeight(36)
        form_layout.addRow(name_label, self.name_input)
        
        # Category input
        category_label = QtWidgets.QLabel("Category:")
        self.category_input = QtWidgets.QLineEdit()
        self.category_input.setPlaceholderText("Enter product category")
        self.category_input.setMinimumHeight(36)
        form_layout.addRow(category_label, self.category_input)
        
        # Price input
        price_label = QtWidgets.QLabel("Price:")
        self.price_input = QtWidgets.QDoubleSpinBox()
        self.price_input.setRange(0, 100000)
        self.price_input.setDecimals(2)
        self.price_input.setSingleStep(0.01)
        self.price_input.setPrefix("$ ")
        self.price_input.setMinimumHeight(36)
        form_layout.addRow(price_label, self.price_input)
        
        # Quantity input
        qty_label = QtWidgets.QLabel("Quantity:")
        self.quantity_input = QtWidgets.QSpinBox()
        self.quantity_input.setRange(0, 100000)
        self.quantity_input.setMinimumHeight(36)
        form_layout.addRow(qty_label, self.quantity_input)
        
        # Threshold input
        threshold_label = QtWidgets.QLabel("Threshold Value:")
        self.threshold_input = QtWidgets.QSpinBox()
        self.threshold_input.setRange(0, 10000)
        self.threshold_input.setValue(10)  # Default threshold
        self.threshold_input.setMinimumHeight(36)
        form_layout.addRow(threshold_label, self.threshold_input)
        
        # Expiry date input
        expiry_label = QtWidgets.QLabel("Expiry Date:")
        self.expiry_date_input = QtWidgets.QDateEdit()
        self.expiry_date_input.setCalendarPopup(True)
        self.expiry_date_input.setDisplayFormat("yyyy-MM-dd")
        self.expiry_date_input.setMinimumHeight(36)
        form_layout.addRow(expiry_label, self.expiry_date_input)
        
        # Availability checkbox
        availability_label = QtWidgets.QLabel("Availability:")
        self.availability_checkbox = QtWidgets.QCheckBox("Product is available for sale")
        self.availability_checkbox.setChecked(True)
        form_layout.addRow(availability_label, self.availability_checkbox)
        
        # Description input (multiline)
        desc_label = QtWidgets.QLabel("Description:")
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Enter product description")
        self.description_input.setMinimumHeight(120)
        form_layout.addRow(desc_label, self.description_input)
        
        scroll_area.setWidget(form_widget)
        container_layout.addWidget(scroll_area, 1)
        
        # Add bottom separator
        bottom_separator = QtWidgets.QFrame()
        bottom_separator.setFrameShape(QtWidgets.QFrame.HLine)
        bottom_separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        bottom_separator.setStyleSheet("background-color: rgba(100, 100, 100, 0.3); margin: 10px 0px 10px 0px;")
        container_layout.addWidget(bottom_separator)
        
        # Button area
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setObjectName("cancelBtn")
        self.cancel_button.clicked.connect(self.reject)
        
        self.save_button = QtWidgets.QPushButton("Save Product")
        self.save_button.clicked.connect(self.save_product)
        
        # Add spacer to push buttons to the right
        button_layout.addStretch(1)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        
        container_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(self.container)
        
        # Enable dragging the dialog
        self.old_pos = None
        self.container.mousePressEvent = self.mousePressEvent
        self.container.mouseMoveEvent = self.mouseMoveEvent
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()
    
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = None
    
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
            
            if self.product:
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
                     threshold, expiry_date, availability, self.product['product_id'])
                )
                
                # Update inventory record if it exists
                cursor.execute(
                    """INSERT INTO inventory (product_id, quantity, status, last_updated) 
                       VALUES (%s, %s, %s, NOW())
                       ON DUPLICATE KEY UPDATE 
                       quantity = VALUES(quantity),
                       last_updated = NOW()""",
                    (self.product['product_id'], quantity, "Updated")
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