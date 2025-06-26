from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
from .base_dialog import BaseDialog

class DeliveredProductsFilterDialog(BaseDialog):
    """Dialog for filtering delivered products"""
    
    def __init__(self, parent=None, filter_state=None):
        super(DeliveredProductsFilterDialog, self).__init__(parent, None, "Filter Delivered Products")
        self.parent = parent
        self.filter_state = filter_state or {
            "is_active": False,
            "date_range": "All Time",
            "supplier": "All Suppliers",
            "status": "All Statuses"
        }
        self.result_filter_state = self.filter_state.copy()
        self.setup_ui()
    
    def setup_ui(self):
        self.setup_base_ui(450)
        
        self.header_label.setText("Filter Delivered Products")
        
        # Date range filter
        date_label = QtWidgets.QLabel("Date Range:")
        self.date_combo = QtWidgets.QComboBox()
        self.date_combo.addItems([
            "All Time",
            "Today", 
            "This Week",
            "This Month",
            "Last 30 Days",
            "Last 90 Days"
        ])
        
        # Set current selection
        date_index = self.date_combo.findText(self.filter_state["date_range"])
        if date_index >= 0:
            self.date_combo.setCurrentIndex(date_index)
        
        self.form_layout.addRow(date_label, self.date_combo)
        
        # Supplier filter
        supplier_label = QtWidgets.QLabel("Supplier:")
        self.supplier_combo = QtWidgets.QComboBox()
        self.supplier_combo.addItem("All Suppliers")
        
        # Get unique suppliers from inventory_status
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT DISTINCT supplier_name 
                FROM inventory_status 
                WHERE supplier_name IS NOT NULL AND supplier_name != '' AND status = 'Received'
            """)
            suppliers = cursor.fetchall()
            for supplier in suppliers:
                if supplier['supplier_name']:
                    self.supplier_combo.addItem(supplier['supplier_name'])
            cursor.close()
        except mysql.connector.Error:
            pass
        
        # Set current selection
        supplier_index = self.supplier_combo.findText(self.filter_state["supplier"])
        if supplier_index >= 0:
            self.supplier_combo.setCurrentIndex(supplier_index)
        
        self.form_layout.addRow(supplier_label, self.supplier_combo)
        
        # Status filter
        status_label = QtWidgets.QLabel("Status:")
        self.status_combo = QtWidgets.QComboBox()
        self.status_combo.addItems(["All Statuses", "Received", "Processed", "Verified"])
        
        # Set current selection
        status_index = self.status_combo.findText(self.filter_state["status"])
        if status_index >= 0:
            self.status_combo.setCurrentIndex(status_index)
        
        self.form_layout.addRow(status_label, self.status_combo)
        
        # Helper text
        helper_text = QtWidgets.QLabel(
            "Tip: Filter by date range and supplier to track specific delivery patterns and supplier performance."
        )
        helper_text.setStyleSheet("color: #4FC3F7; font-style: italic; font-size: 12px;")
        helper_text.setWordWrap(True)
        self.form_layout.addRow(helper_text)
        
        # Update button text
        self.save_button.setText("Apply Filter")
        self.save_button.clicked.connect(self.apply_filters)
        
        # Add reset button
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
        
        # Insert reset button into layout
        self.button_layout.insertWidget(self.button_layout.count() - 2, self.reset_button)
    
    def apply_filters(self):
        """Apply selected filters"""
        self.result_filter_state["date_range"] = self.date_combo.currentText()
        self.result_filter_state["supplier"] = self.supplier_combo.currentText()
        self.result_filter_state["status"] = self.status_combo.currentText()
        
        # Determine if any filters are active
        self.result_filter_state["is_active"] = (
            self.result_filter_state["date_range"] != "All Time" or
            self.result_filter_state["supplier"] != "All Suppliers" or
            self.result_filter_state["status"] != "All Statuses"
        )
        
        self.accept()
    
    def reset_filters(self):
        """Reset all filters"""
        self.result_filter_state = {
            "is_active": False,
            "date_range": "All Time",
            "supplier": "All Suppliers",
            "status": "All Statuses"
        }
        self.accept()
    
    def get_filter_state(self):
        """Return the filter state after dialog is closed"""
        return self.result_filter_state