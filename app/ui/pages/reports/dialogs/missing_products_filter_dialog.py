from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
from app.ui.pages.inventory.dialogs.base_dialog import BaseDialog

class MissingProductsFilterDialog(BaseDialog):
    """Dialog for filtering missing products"""
    
    def __init__(self, parent=None, filter_state=None):
        super(MissingProductsFilterDialog, self).__init__(parent, None, "Filter Missing Products")
        self.parent = parent
        self.filter_state = filter_state or {
            "is_active": False,
            "status": "All",
            "severity": "All",
            "category": "All Categories"
        }
        self.result_filter_state = self.filter_state.copy()
        self.setup_ui()
    
    def setup_ui(self):
        self.setup_base_ui(450)
        
        self.header_label.setText("Filter Missing Products")
        
        # Status filter
        status_label = QtWidgets.QLabel("Status:")
        self.status_combo = QtWidgets.QComboBox()
        self.status_combo.addItems(["All", "Missing", "Excess"])
        
        status_index = self.status_combo.findText(self.filter_state["status"])
        if status_index >= 0:
            self.status_combo.setCurrentIndex(status_index)
        
        self.form_layout.addRow(status_label, self.status_combo)
        
        # Severity filter
        severity_label = QtWidgets.QLabel("Severity:")
        self.severity_combo = QtWidgets.QComboBox()
        self.severity_combo.addItems(["All", "Critical (>10)", "Moderate (5-10)", "Minor (<5)"])
        
        severity_index = self.severity_combo.findText(self.filter_state["severity"])
        if severity_index >= 0:
            self.severity_combo.setCurrentIndex(severity_index)
        
        self.form_layout.addRow(severity_label, self.severity_combo)
        
        # Category filter
        category_label = QtWidgets.QLabel("Category:")
        self.category_combo = QtWidgets.QComboBox()
        self.category_combo.addItem("All Categories")
        
        # Get unique categories from products
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL AND category != ''")
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
        
        # Helper text
        helper_text = QtWidgets.QLabel(
            "Tip: Filter by severity and status to prioritize inventory investigations and reconciliation tasks."
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
        self.result_filter_state["status"] = self.status_combo.currentText()
        self.result_filter_state["severity"] = self.severity_combo.currentText()
        self.result_filter_state["category"] = self.category_combo.currentText()
        
        # Determine if any filters are active
        self.result_filter_state["is_active"] = (
            self.result_filter_state["status"] != "All" or
            self.result_filter_state["severity"] != "All" or
            self.result_filter_state["category"] != "All Categories"
        )
        
        self.accept()
    
    def reset_filters(self):
        """Reset all filters"""
        self.result_filter_state = {
            "is_active": False,
            "status": "All",
            "severity": "All",
            "category": "All Categories"
        }
        self.accept()
    
    def get_filter_state(self):
        """Return the filter state after dialog is closed"""
        return self.result_filter_state