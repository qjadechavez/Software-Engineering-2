from PyQt5 import QtWidgets, QtCore, QtGui
from .base_dialog import BaseDialog
from ..style_factory import StyleFactory
from ..table_factory import TableFactory

class ProductSelectionDialog(BaseDialog):
    """Dialog for selecting products to be used in a service"""
    
    def __init__(self, parent, available_products, current_selected):
        super(ProductSelectionDialog, self).__init__(parent, None, "Select Products")
        self.available_products = available_products
        
        # Create a deep copy of current selected products
        self.selected_products = []
        for product in current_selected:
            self.selected_products.append(product.copy())
            
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components"""
        self.setup_base_ui(700)  # Increased height for two tables
        
        self.header_label.setText("Select Products for Service")
        
        # Search input with proper styling
        search_label = QtWidgets.QLabel("Search Products:")
        search_label.setStyleSheet("color: white; font-weight: bold;")
        
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Type to search products...")
        self.search_input.setMinimumHeight(36)
        self.search_input.setStyleSheet(StyleFactory.get_search_input_style())
        self.search_input.textChanged.connect(self.filter_products)
        self.form_layout.addRow(search_label, self.search_input)
        
        # Available products section
        available_header = QtWidgets.QLabel("Available Products:")
        available_header.setStyleSheet("font-weight: bold; margin-top: 15px; color: white; font-size: 14px;")
        self.form_layout.addRow(available_header)
        
        # Create products table using TableFactory - FIXED
        self.products_table = TableFactory.create_table()
        self.products_table.setColumnCount(5)  # ID, Name, Category, Price, Add
        self.products_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price", "Add"])
        self.products_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        
        # Custom column widths
        self.products_table.setColumnWidth(0, 60)   # ID column
        self.products_table.setColumnWidth(2, 120)  # Category column
        self.products_table.setColumnWidth(3, 100)  # Price column
        self.products_table.setColumnWidth(4, 80)   # Add button column
        
        self.products_table.setMinimumHeight(200)
        self.products_table.setMaximumHeight(250)
        # Apply enhanced table styling for better text visibility
        self.products_table.setStyleSheet(self.get_enhanced_table_style())
        self.form_layout.addRow(self.products_table)
        
        # Load products
        self.populate_products_table()
        
        # Selected products section
        selected_header = QtWidgets.QLabel("Selected Products:")
        selected_header.setStyleSheet("font-weight: bold; margin-top: 15px; color: white; font-size: 14px;")
        self.form_layout.addRow(selected_header)
        
        # Create selected products table using TableFactory - FIXED
        self.selected_table = TableFactory.create_table()  # Fixed variable name
        self.selected_table.setColumnCount(5)  # ID, Name, Quantity, Price, Remove
        self.selected_table.setHorizontalHeaderLabels(["ID", "Name", "Quantity", "Price", "Remove"])
        self.selected_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        
        # Custom column widths for selected table
        self.selected_table.setColumnWidth(0, 60)   # ID column
        self.selected_table.setColumnWidth(2, 80)   # Quantity column
        self.selected_table.setColumnWidth(3, 100)  # Price column
        self.selected_table.setColumnWidth(4, 80)   # Remove button column
        
        self.selected_table.setMinimumHeight(150)
        self.selected_table.setMaximumHeight(200)
        # Apply enhanced table styling for better text visibility
        self.selected_table.setStyleSheet(self.get_enhanced_table_style())
        self.form_layout.addRow(self.selected_table)
        
        # Update selected products table
        self.update_selected_table()
        
        # Update save button with proper BaseDialog integration
        self.save_button.setText("Save Selection")
        # Clear any existing connections first
        try:
            self.save_button.clicked.disconnect()
        except:
            pass
        self.save_button.clicked.connect(self.accept)
    
    def get_enhanced_table_style(self):
        """Get enhanced table style with better text visibility"""
        return """
            QTableWidget {
                background-color: #1e1e1e;
                border: 1px solid #444;
                color: white;
                gridline-color: #444;
                font-size: 13px;
                font-weight: normal;
                selection-background-color: #0d7377;
            }
            QTableWidget::item {
                color: white;
                background-color: #1e1e1e;
                border: none;
                padding: 8px;
                border-bottom: 1px solid #333;
            }
            QTableWidget::item:alternate {
                background-color: #252525;
            }
            QTableWidget::item:selected {
                background-color: #0d7377;
                color: white;
            }
            QTableWidget::item:hover {
                background-color: #2a2a2a;
                color: white;
            }
            QHeaderView::section {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #444;
                padding: 10px;
                font-weight: bold;
                font-size: 12px;
            }
            QHeaderView::section:hover {
                background-color: #3d3d3d;
            }
        """
        
    def populate_products_table(self):
        """Populate the products table"""
        self.products_table.setRowCount(0)
        
        for i, product in enumerate(self.available_products):
            self.products_table.insertRow(i)
            
            # ID column with proper white text
            id_item = QtWidgets.QTableWidgetItem(str(product['product_id']))
            id_item.setTextAlignment(QtCore.Qt.AlignCenter)
            id_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))  # Force white text
            id_item.setBackground(QtGui.QBrush(QtGui.QColor(30, 30, 30)))  # Dark background
            self.products_table.setItem(i, 0, id_item)
            
            # Product name with proper white text
            name_item = QtWidgets.QTableWidgetItem(product['product_name'])
            name_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            name_item.setBackground(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
            self.products_table.setItem(i, 1, name_item)
            
            # Category with proper white text
            category_item = QtWidgets.QTableWidgetItem(product['category'])
            category_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            category_item.setBackground(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
            self.products_table.setItem(i, 2, category_item)
            
            # Price with proper white text and green color for amount
            price_item = QtWidgets.QTableWidgetItem(f"₱{float(product['price']):.2f}")
            price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            price_item.setForeground(QtGui.QBrush(QtGui.QColor(76, 175, 80)))  # Green for price
            price_item.setBackground(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
            self.products_table.setItem(i, 3, price_item)
            
            # Add button with improved styling
            add_btn = QtWidgets.QPushButton("Add")
            add_btn.setStyleSheet("""
                QPushButton {
                    background-color: #28a745;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 12px;
                    font-size: 12px;
                    font-weight: bold;
                    min-height: 24px;
                }
                QPushButton:hover {
                    background-color: #218838;
                    transform: translateY(-1px);
                }
                QPushButton:pressed {
                    background-color: #1e7e34;
                    transform: translateY(0px);
                }
            """)
            add_btn.clicked.connect(lambda checked, row=i: self.add_product(row))
            self.products_table.setCellWidget(i, 4, add_btn)
            
    def update_selected_table(self):
        """Update the selected products table"""
        self.selected_table.setRowCount(0)
        
        for i, product in enumerate(self.selected_products):
            self.selected_table.insertRow(i)
            
            # ID column with proper white text
            id_item = QtWidgets.QTableWidgetItem(str(product['product_id']))
            id_item.setTextAlignment(QtCore.Qt.AlignCenter)
            id_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            id_item.setBackground(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
            self.selected_table.setItem(i, 0, id_item)
            
            # Product name with proper white text
            name_item = QtWidgets.QTableWidgetItem(product['product_name'])
            name_item.setForeground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            name_item.setBackground(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
            self.selected_table.setItem(i, 1, name_item)
            
            # Quantity (editable) with improved styling
            quantity_widget = QtWidgets.QSpinBox()
            quantity_widget.setRange(1, 100)
            quantity_widget.setValue(product.get('quantity', 1))
            quantity_widget.setStyleSheet("""
                QSpinBox {
                    color: white;
                    background-color: #2d2d2d;
                    border: 2px solid #444;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 12px;
                    font-weight: bold;
                    min-height: 20px;
                }
                QSpinBox:focus {
                    border: 2px solid #007acc;
                    background-color: #333;
                }
                QSpinBox:hover {
                    background-color: #353535;
                    border: 2px solid #555;
                }
                QSpinBox::up-button, QSpinBox::down-button {
                    background-color: #444;
                    border: 1px solid #666;
                    width: 20px;
                    border-radius: 2px;
                }
                QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                    background-color: #555;
                }
                QSpinBox::up-button:pressed, QSpinBox::down-button:pressed {
                    background-color: #666;
                }
                QSpinBox::up-arrow, QSpinBox::down-arrow {
                    color: white;
                    width: 10px;
                    height: 10px;
                }
            """)
            quantity_widget.valueChanged.connect(lambda value, index=i: self.update_quantity(index, value))
            self.selected_table.setCellWidget(i, 2, quantity_widget)
            
            # Price with proper white text and green color
            if 'price' in product:
                price_item = QtWidgets.QTableWidgetItem(f"₱{float(product['price']):.2f}")
                price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                price_item.setForeground(QtGui.QBrush(QtGui.QColor(76, 175, 80)))  # Green for price
                price_item.setBackground(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
                self.selected_table.setItem(i, 3, price_item)
            
            # Remove button with improved styling
            remove_btn = QtWidgets.QPushButton("Remove")
            remove_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 6px 10px;
                    font-size: 12px;
                    font-weight: bold;
                    min-height: 24px;
                }
                QPushButton:hover {
                    background-color: #c82333;
                    transform: translateY(-1px);
                }
                QPushButton:pressed {
                    background-color: #a71e2a;
                    transform: translateY(0px);
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