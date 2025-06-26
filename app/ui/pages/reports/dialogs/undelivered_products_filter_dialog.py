from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
from app.ui.pages.inventory.dialogs.base_dialog import BaseDialog

class UndeliveredProductsFilterDialog(BaseDialog):
    """Dialog for filtering undelivered products"""
    
    def __init__(self, parent=None, filter_state=None):
        super(UndeliveredProductsFilterDialog, self).__init__(parent, None, "Filter Undelivered Products")
        self.parent = parent
        self.filter_state = filter_state or {
            "is_active": False,
            "supplier": "All Suppliers",
            "category": "All Categories",
            "status": "All Statuses"
        }
        self.result_filter_state = self.filter_state.copy()
        self.setup_ui()
    
    def setup_ui(self):
        self.setup_base_ui(450)
        
        self.header_label.setText("Filter Undelivered Products")
        
        # Supplier filter
        supplier_label = QtWidgets.QLabel("Supplier:")
        self.supplier_combo = QtWidgets.QComboBox()
        self.supplier_combo.addItem("All Suppliers")
        
        # Get unique suppliers
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT supplier_name FROM suppliers WHERE supplier_name IS NOT NULL AND supplier_name != ''")
            suppliers = cursor.fetchall()
            for supplier in suppliers:
                self.supplier_combo.addItem(supplier['supplier_name'])
            cursor.close()
        except mysql.connector.Error:
            pass
        
        supplier_index = self.supplier_combo.findText(self.filter_state["supplier"])
        if supplier_index >= 0:
            self.supplier_combo.setCurrentIndex(supplier_index)
        
        self.form_layout.addRow(supplier_label, self.supplier_combo)
        
        # Category filter
        category_label = QtWidgets.QLabel("Category:")
        self.category_combo = QtWidgets.QComboBox()
        self.category_combo.addItem("All Categories")
        
        # Get unique categories
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT category FROM suppliers WHERE category IS NOT NULL AND category != ''")
            categories = cursor.fetchall()
            for category in categories:
                self.category_combo.addItem(category['category'])
            cursor.close()
        except mysql.connector.Error:
            pass
        
        category_index = self.category_combo.findText(self.filter_state["category"])
        if category_index >= 0:
            self.category_combo.setCurrentIndex(category_index)
        
        self.form_layout.addRow(category_label, self.category_combo)
        
        # Status filter
        status_label = QtWidgets.QLabel("Status:")
        self.status_combo = QtWidgets.QComboBox()
        self.status_combo.addItems(["All Statuses", "Pending", "Processing", "Delayed"])
        
        status_index = self.status_combo.findText(self.filter_state["status"])
        if status_index >= 0:
            self.status_combo.setCurrentIndex(status_index)
        
        self.form_layout.addRow(status_label, self.status_combo)
        
        # Helper text
        helper_text = QtWidgets.QLabel(
            "Tip: Filter by supplier and status to track specific delivery expectations."
        )
        helper_text.setStyleSheet("color: #4FC3F7; font-style: italic; font-size: 12px;")
        helper_text.setWordWrap(True)
        self.form_layout.addRow(helper_text)
        
        # Update save button to "Apply Filter"
        self.save_button.setText("Apply Filter")
        self.save_button.clicked.connect(self.apply_filters)
        
        # Add reset button next to the cancel button
        self.reset_button = QtWidgets.QPushButton("Reset")
        self.reset_button.setStyleSheet("""
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
        self.reset_button.clicked.connect(self.reset_filters)
        
        # Find the button layout and insert reset button
        button_layout = self.save_button.parent().layout()
        button_layout.insertWidget(button_layout.count() - 2, self.reset_button)
    
    def apply_filters(self):
        """Apply selected filters"""
        self.result_filter_state["supplier"] = self.supplier_combo.currentText()
        self.result_filter_state["category"] = self.category_combo.currentText()
        self.result_filter_state["status"] = self.status_combo.currentText()
        
        # Determine if any filters are active
        self.result_filter_state["is_active"] = (
            self.result_filter_state["supplier"] != "All Suppliers" or
            self.result_filter_state["category"] != "All Categories" or
            self.result_filter_state["status"] != "All Statuses"
        )
        
        self.accept()
    
    def reset_filters(self):
        """Reset all filters"""
        self.result_filter_state = {
            "is_active": False,
            "supplier": "All Suppliers",
            "category": "All Categories",
            "status": "All Statuses"
        }
        self.accept()
    
    def get_filter_state(self):
        """Return the filter state after dialog is closed"""
        return self.result_filter_state