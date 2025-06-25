from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
from ..style_factory import StyleFactory
from .base_dialog import BaseDialog

class SupplierFilterDialog(BaseDialog):
    """Dialog for filtering suppliers"""
    
    def __init__(self, parent=None, filter_state=None):
        super(SupplierFilterDialog, self).__init__(parent, None, "Filter Suppliers")
        self.parent = parent
        self.filter_state = filter_state or {
            "is_active": False,
            "category": "All Categories",
            "accepts_returns": "All",
            "products_on_the_way": "All",
            "status": "All Statuses"
        }
        self.result_filter_state = self.filter_state.copy()
        
        self.setup_ui()
    
    def setup_ui(self):
        self.setup_base_ui(500)
        
        self.header_label.setText("Filter Suppliers")
        
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
        
        # Set the combo box to match stored filter state
        category_index = self.category_combo.findText(self.filter_state["category"])
        if category_index >= 0:
            self.category_combo.setCurrentIndex(category_index)
            
        self.form_layout.addRow(category_label, self.category_combo)
        
        # Status filter
        status_label = QtWidgets.QLabel("Status:")
        self.status_combo = QtWidgets.QComboBox()
        self.status_combo.addItem("All Statuses")
        self.status_combo.addItem("Pending")
        self.status_combo.addItem("Received")
        self.status_combo.addItem("Cancelled")
        
        # Set the combo box to match stored filter state
        status_index = self.status_combo.findText(self.filter_state["status"])
        if status_index >= 0:
            self.status_combo.setCurrentIndex(status_index)
            
        self.form_layout.addRow(status_label, self.status_combo)
        
        # Returns policy filter
        returns_label = QtWidgets.QLabel("Accepts Returns:")
        self.returns_combo = QtWidgets.QComboBox()
        self.returns_combo.addItem("All")
        self.returns_combo.addItem("Accepts Returns")
        self.returns_combo.addItem("No Returns")
        
        # Set the combo box to match stored filter state
        returns_index = self.returns_combo.findText(self.filter_state["accepts_returns"])
        if returns_index >= 0:
            self.returns_combo.setCurrentIndex(returns_index)
            
        self.form_layout.addRow(returns_label, self.returns_combo)
        
        # Products on the way filter
        products_label = QtWidgets.QLabel("Products on the Way:")
        self.products_combo = QtWidgets.QComboBox()
        self.products_combo.addItem("All")
        self.products_combo.addItem("Has Products on the Way")
        self.products_combo.addItem("No Products on the Way")
        
        # Set the combo box to match stored filter state
        products_index = self.products_combo.findText(self.filter_state["products_on_the_way"])
        if products_index >= 0:
            self.products_combo.setCurrentIndex(products_index)
            
        self.form_layout.addRow(products_label, self.products_combo)
        
        # Filter helper text
        helper_text = QtWidgets.QLabel(
            "Tip: Filter by status to see pending orders, by returns policy to find suppliers that accept returns, "
            "or by products on the way to track incoming deliveries."
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
        # Save filter state with correct key names
        self.result_filter_state["category"] = self.category_combo.currentText()
        self.result_filter_state["status"] = self.status_combo.currentText()
        self.result_filter_state["accepts_returns"] = self.returns_combo.currentText()
        self.result_filter_state["products_on_the_way"] = self.products_combo.currentText()
        
        # Determine if any filters are active
        self.result_filter_state["is_active"] = (
            self.result_filter_state["category"] != "All Categories" or
            self.result_filter_state["status"] != "All Statuses" or
            self.result_filter_state["accepts_returns"] != "All" or
            self.result_filter_state["products_on_the_way"] != "All"
        )
        
        self.accept()
    
    def reset_filters(self):
        """Reset all filters"""
        self.result_filter_state = {
            "is_active": False,
            "category": "All Categories",
            "accepts_returns": "All",
            "products_on_the_way": "All",
            "status": "All Statuses"
        }
        self.accept()
    
    def get_filter_state(self):
        """Return the filter state after dialog is closed"""
        return self.result_filter_state