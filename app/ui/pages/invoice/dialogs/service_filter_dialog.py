from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
from ..style_factory import StyleFactory

class ServiceFilterDialog(QtWidgets.QDialog):
    """Dialog for filtering services"""
    
    def __init__(self, parent=None, filter_state=None):
        super(ServiceFilterDialog, self).__init__(parent)
        self.parent = parent
        self.filter_state = filter_state or {
            "is_active": False,
            "category": "All Categories",
            "price_range": "All Prices"
        }
        self.result_filter_state = self.filter_state.copy()
        
        self.setWindowTitle("Filter Services")
        self.setMinimumWidth(400)
        self.setStyleSheet(StyleFactory.get_dialog_style())
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create layout
        layout = QtWidgets.QVBoxLayout(self)
        form_layout = QtWidgets.QFormLayout()
        
        # Category filter
        category_label = QtWidgets.QLabel("Category:")
        self.category_combo = QtWidgets.QComboBox()
        self.category_combo.addItem("All Categories")
        
        # Get unique categories
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT category FROM services WHERE category IS NOT NULL AND category != '' AND availability = 1")
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
            
        form_layout.addRow(category_label, self.category_combo)
        
        # Price range filter
        price_label = QtWidgets.QLabel("Price Range:")
        self.price_combo = QtWidgets.QComboBox()
        self.price_combo.addItem("All Prices")
        self.price_combo.addItem("Under ₱500")
        self.price_combo.addItem("₱500 - ₱1000")
        self.price_combo.addItem("₱1000 - ₱2000")
        self.price_combo.addItem("Over ₱2000")
        
        # Set the combo box to match stored filter state
        price_index = self.price_combo.findText(self.filter_state["price_range"])
        if price_index >= 0:
            self.price_combo.setCurrentIndex(price_index)
            
        form_layout.addRow(price_label, self.price_combo)
        
        # Filter helper text
        helper_text = QtWidgets.QLabel(
            "Tip: Filter by category and price range to find the perfect service for your needs."
        )
        helper_text.setStyleSheet("color: #4FC3F7; font-style: italic; font-size: 12px;")
        helper_text.setWordWrap(True)
        
        # Buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        apply_button = QtWidgets.QPushButton("Apply Filter")
        reset_button = QtWidgets.QPushButton("Reset")
        reset_button.setStyleSheet("""
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
        
        buttons_layout.addWidget(reset_button)
        buttons_layout.addWidget(apply_button)
        
        layout.addLayout(form_layout)
        layout.addWidget(helper_text)
        layout.addSpacing(10)
        layout.addLayout(buttons_layout)
        
        # Connect signals
        apply_button.clicked.connect(self.apply_filters)
        reset_button.clicked.connect(self.reset_filters)
    
    def apply_filters(self):
        """Apply selected filters"""
        # Save filter state
        self.result_filter_state["category"] = self.category_combo.currentText()
        self.result_filter_state["price_range"] = self.price_combo.currentText()
        
        # Determine if any filters are active
        self.result_filter_state["is_active"] = (
            self.result_filter_state["category"] != "All Categories" or
            self.result_filter_state["price_range"] != "All Prices"
        )
        
        self.accept()
    
    def reset_filters(self):
        """Reset all filters"""
        self.result_filter_state = {
            "is_active": False,
            "category": "All Categories",
            "price_range": "All Prices"
        }
        self.accept()
    
    def get_filter_state(self):
        """Return the filter state after dialog is closed"""
        return self.result_filter_state