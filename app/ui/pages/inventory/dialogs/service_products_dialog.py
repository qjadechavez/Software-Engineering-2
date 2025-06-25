from PyQt5 import QtWidgets, QtCore, QtGui
from ..style_factory import StyleFactory
from .base_dialog import BaseDialog

class ServiceProductsDialog(BaseDialog):
    """Dialog for displaying products used in a service"""
    
    def __init__(self, parent, service_name, products):
        super(ServiceProductsDialog, self).__init__(parent, None, "Service Products")
        self.service_name = service_name
        self.products = products
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components"""
        self.setup_base_ui(450)
        
        self.header_label.setText(f"Products Used in Service")
        
        # Service name
        service_label = QtWidgets.QLabel(f"<b>Service:</b> {self.service_name}")
        service_label.setStyleSheet("color: white; font-size: 14px; margin-bottom: 10px;")
        self.form_layout.addRow(service_label)
        
        # Products table
        self.products_table = QtWidgets.QTableWidget()
        self.products_table.setColumnCount(5)  # ID, Name, Category, Price, Quantity
        self.products_table.setHorizontalHeaderLabels(["ID", "Product Name", "Category", "Price", "Quantity"])
        self.products_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.products_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.products_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.products_table.setColumnWidth(0, 50)
        self.products_table.setColumnWidth(2, 100)
        self.products_table.setColumnWidth(3, 100)
        self.products_table.setColumnWidth(4, 80)
        self.products_table.setMinimumHeight(250)
        self.form_layout.addRow(self.products_table)
        
        # Counter label showing number of products
        product_count_label = QtWidgets.QLabel(f"Total Products: {len(self.products)}")
        product_count_label.setStyleSheet("color: #4FC3F7; font-size: 13px;")
        self.form_layout.addRow(product_count_label)
        
        # Populate products
        self.populate_products_table()
        
        # Update save button to "Close"
        self.save_button.setText("Close")
        self.save_button.clicked.connect(self.accept)
        
        # Hide cancel button since we only need close
        for i in range(self.save_button.parent().layout().count()):
            widget = self.save_button.parent().layout().itemAt(i).widget()
            if widget and hasattr(widget, 'objectName') and widget.objectName() == "cancelBtn":
                widget.hide()
                break
        
    def populate_products_table(self):
        """Populate the products table"""
        self.products_table.setRowCount(len(self.products))
        
        for i, product in enumerate(self.products):
            # ID column
            id_item = QtWidgets.QTableWidgetItem(str(product['product_id']))
            id_item.setTextAlignment(QtCore.Qt.AlignCenter)
            id_item.setForeground(QtGui.QColor("white"))
            self.products_table.setItem(i, 0, id_item)
            
            # Name
            name_item = QtWidgets.QTableWidgetItem(product['product_name'])
            name_item.setForeground(QtGui.QColor("white"))
            self.products_table.setItem(i, 1, name_item)
            
            # Category
            category_item = QtWidgets.QTableWidgetItem(product['category'])
            category_item.setForeground(QtGui.QColor("white"))
            self.products_table.setItem(i, 2, category_item)
            
            # Price
            price_item = QtWidgets.QTableWidgetItem(f"₱{float(product['price']):.2f}")
            price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            price_item.setForeground(QtGui.QColor("white"))
            self.products_table.setItem(i, 3, price_item)
            
            # Quantity
            qty_item = QtWidgets.QTableWidgetItem(str(product['quantity']))
            qty_item.setTextAlignment(QtCore.Qt.AlignCenter)
            qty_item.setForeground(QtGui.QColor("white"))
            self.products_table.setItem(i, 4, qty_item)