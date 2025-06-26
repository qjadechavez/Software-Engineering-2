from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
from ..style_factory import StyleFactory
from .base_dialog import BaseDialog

class ProductFilterDialog(BaseDialog):
    """Dialog for filtering products"""
    
    def __init__(self, parent=None, filter_state=None):
        super(ProductFilterDialog, self).__init__(parent, None, "Filter Products")
        self.parent = parent
        self.filter_state = filter_state or {
            "is_active": False,
            "category": "All Categories",
            "availability": "All",
            "price_sort": "No Sorting"
        }
        self.result_filter_state = self.filter_state.copy()
        
        self.setup_ui()
    
    def setup_ui(self):
        self.setup_base_ui(450)
        
        self.header_label.setText("Filter Products")
        
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
        
        # Set the combo box to match stored filter state
        category_index = self.category_combo.findText(self.filter_state["category"])
        if category_index >= 0:
            self.category_combo.setCurrentIndex(category_index)
            
        self.form_layout.addRow(category_label, self.category_combo)
        
        # Availability filter
        availability_label = QtWidgets.QLabel("Availability:")
        self.availability_combo = QtWidgets.QComboBox()
        self.availability_combo.addItem("All")
        self.availability_combo.addItem("In Stock")
        self.availability_combo.addItem("Out of Stock")
        
        # Set the combo box to match stored filter state
        availability_index = self.availability_combo.findText(self.filter_state["availability"])
        if availability_index >= 0:
            self.availability_combo.setCurrentIndex(availability_index)
            
        self.form_layout.addRow(availability_label, self.availability_combo)
        
        # Price sorting options
        price_sort_label = QtWidgets.QLabel("Price Sort:")
        self.price_sort_combo = QtWidgets.QComboBox()
        self.price_sort_combo.addItem("No Sorting")
        self.price_sort_combo.addItem("Lowest - Highest")
        self.price_sort_combo.addItem("Highest - Lowest")
        
        # Set the combo box to match stored filter state
        price_sort_index = self.price_sort_combo.findText(self.filter_state["price_sort"])
        if price_sort_index >= 0:
            self.price_sort_combo.setCurrentIndex(price_sort_index)
            
        self.form_layout.addRow(price_sort_label, self.price_sort_combo)
        
        # Filter helper text
        helper_text = QtWidgets.QLabel(
            "Tip: Filter by category and availability, then sort by price to find the perfect match."
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
        # Save filter state
        self.result_filter_state["category"] = self.category_combo.currentText()
        self.result_filter_state["availability"] = self.availability_combo.currentText()
        self.result_filter_state["price_sort"] = self.price_sort_combo.currentText()
        
        # Determine if any filters are active
        self.result_filter_state["is_active"] = (
            self.result_filter_state["category"] != "All Categories" or
            self.result_filter_state["availability"] != "All" or
            self.result_filter_state["price_sort"] != "No Sorting"
        )
        
        self.accept()
    
    def reset_filters(self):
        """Reset all filters"""
        self.result_filter_state = {
            "is_active": False,
            "category": "All Categories",
            "availability": "All",
            "price_sort": "No Sorting"
        }
        self.accept()
    
    def get_filter_state(self):
        """Return the filter state after dialog is closed"""
        return self.result_filter_state