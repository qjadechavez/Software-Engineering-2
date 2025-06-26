from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
from .base_dialog import BaseDialog

class AlertLevelFilterDialog(BaseDialog):
    """Dialog for filtering alert level products"""
    
    def __init__(self, parent=None, filter_state=None):
        super(AlertLevelFilterDialog, self).__init__(parent, None, "Filter Alert Level Report")
        self.parent = parent
        self.filter_state = filter_state or {
            "is_active": False,
            "alert_level": "All Levels",
            "category": "All Categories",
            "status": "All Statuses"
        }
        self.result_filter_state = self.filter_state.copy()
        self.setup_ui()
    
    def setup_ui(self):
        self.setup_base_ui(450)
        
        self.header_label.setText("Filter Alert Level Report")
        
        # Alert level filter
        alert_label = QtWidgets.QLabel("Alert Level:")
        self.alert_combo = QtWidgets.QComboBox()
        self.alert_combo.addItems([
            "All Levels", 
            "Out of Stock", 
            "Critical", 
            "Low Stock", 
            "Overstock", 
            "Normal"
        ])
        
        # Set current selection
        alert_index = self.alert_combo.findText(self.filter_state["alert_level"])
        if alert_index >= 0:
            self.alert_combo.setCurrentIndex(alert_index)
        
        self.form_layout.addRow(alert_label, self.alert_combo)
        
        # Category filter
        category_label = QtWidgets.QLabel("Category:")
        self.category_combo = QtWidgets.QComboBox()
        self.category_combo.addItem("All Categories")
        
        # Get unique categories
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
        
        # Set current selection
        category_index = self.category_combo.findText(self.filter_state["category"])
        if category_index >= 0:
            self.category_combo.setCurrentIndex(category_index)
        
        self.form_layout.addRow(category_label, self.category_combo)
        
        # Status filter
        status_label = QtWidgets.QLabel("Product Status:")
        self.status_combo = QtWidgets.QComboBox()
        self.status_combo.addItems(["All Statuses", "Available", "Unavailable", "Discontinued"])
        
        # Set current selection
        status_index = self.status_combo.findText(self.filter_state["status"])
        if status_index >= 0:
            self.status_combo.setCurrentIndex(status_index)
        
        self.form_layout.addRow(status_label, self.status_combo)
        
        # Helper text
        helper_text = QtWidgets.QLabel(
            "Tip: Filter by alert level to focus on critical inventory issues that need immediate attention."
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
        self.result_filter_state["alert_level"] = self.alert_combo.currentText()
        self.result_filter_state["category"] = self.category_combo.currentText()
        self.result_filter_state["status"] = self.status_combo.currentText()
        
        # Determine if any filters are active
        self.result_filter_state["is_active"] = (
            self.result_filter_state["alert_level"] != "All Levels" or
            self.result_filter_state["category"] != "All Categories" or
            self.result_filter_state["status"] != "All Statuses"
        )
        
        self.accept()
    
    def reset_filters(self):
        """Reset all filters"""
        self.result_filter_state = {
            "is_active": False,
            "alert_level": "All Levels",
            "category": "All Categories",
            "status": "All Statuses"
        }
        self.accept()
    
    def get_filter_state(self):
        """Return the filter state after dialog is closed"""
        return self.result_filter_state