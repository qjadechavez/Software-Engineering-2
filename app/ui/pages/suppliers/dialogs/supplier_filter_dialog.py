from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
from ..style_factory import StyleFactory

class SupplierFilterDialog(QtWidgets.QDialog):
    """Dialog for filtering suppliers"""
    
    def __init__(self, parent=None, filter_state=None):
        super(SupplierFilterDialog, self).__init__(parent)
        self.parent = parent
        self.filter_state = filter_state or {
            "is_active": False,
            "category": "All Categories",
            "accepts_returns": "All",
            "products_on_the_way": "All",
            "status": "All Statuses"  # Add status to filter state
        }
        self.result_filter_state = self.filter_state.copy()
        
        self.setWindowTitle("Filter Suppliers")
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
        
        # Get unique supplier categories
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT category FROM suppliers WHERE category IS NOT NULL AND category != ''")
            categories = cursor.fetchall()
            for category in categories:
                self.category_combo.addItem(category['category'])
            cursor.close()
        except mysql.connector.Error:
            # Add some defaults if DB connection fails
            self.category_combo.addItem("Electronics")
            self.category_combo.addItem("Food")
            self.category_combo.addItem("Clothing")
            self.category_combo.addItem("Household")
        
        # Set the combo box to match stored filter state
        category_index = self.category_combo.findText(self.filter_state["category"])
        if category_index >= 0:
            self.category_combo.setCurrentIndex(category_index)
            
        form_layout.addRow(category_label, self.category_combo)
        
        # Accepts Returns filter
        accepts_returns_label = QtWidgets.QLabel("Returns Policy:")
        self.returns_combo = QtWidgets.QComboBox()
        self.returns_combo.addItem("All")
        self.returns_combo.addItem("Accepts Returns")
        self.returns_combo.addItem("No Returns")
        
        # Set the combo box to match stored filter state
        returns_index = self.returns_combo.findText(self.filter_state["accepts_returns"])
        if returns_index >= 0:
            self.returns_combo.setCurrentIndex(returns_index)
            
        form_layout.addRow(accepts_returns_label, self.returns_combo)
        
        # Products on the way filter
        on_the_way_label = QtWidgets.QLabel("Products Status:")
        self.on_the_way_combo = QtWidgets.QComboBox()
        self.on_the_way_combo.addItem("All")
        self.on_the_way_combo.addItem("Has Products on the Way")
        self.on_the_way_combo.addItem("No Products on the Way")
        
        # Set the combo box to match stored filter state
        on_the_way_index = self.on_the_way_combo.findText(self.filter_state["products_on_the_way"])
        if on_the_way_index >= 0:
            self.on_the_way_combo.setCurrentIndex(on_the_way_index)
            
        form_layout.addRow(on_the_way_label, self.on_the_way_combo)
        
        # Status filter
        status_label = QtWidgets.QLabel("Supplier Status:")
        self.status_combo = QtWidgets.QComboBox()
        self.status_combo.addItem("All Statuses")
        self.status_combo.addItem("Pending")
        self.status_combo.addItem("Received")
        self.status_combo.addItem("Cancelled")
        
        # Set the combo box to match stored filter state
        status_index = self.status_combo.findText(self.filter_state["status"])
        if status_index >= 0:
            self.status_combo.setCurrentIndex(status_index)
            
        form_layout.addRow(status_label, self.status_combo)
        
        # Filter helper text
        helper_text = QtWidgets.QLabel(
            "Tip: Filter by category and returns policy to find suppliers that best meet your business needs."
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
                min-width: 120px;
                max-width: 120px;
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
        self.result_filter_state["accepts_returns"] = self.returns_combo.currentText()
        self.result_filter_state["products_on_the_way"] = self.on_the_way_combo.currentText()
        self.result_filter_state["status"] = self.status_combo.currentText()  # Save status filter
        
        # Determine if any filters are active
        self.result_filter_state["is_active"] = (
            self.result_filter_state["category"] != "All Categories" or
            self.result_filter_state["accepts_returns"] != "All" or
            self.result_filter_state["products_on_the_way"] != "All" or
            self.result_filter_state["status"] != "All Statuses"  # Check status filter
        )
        
        self.accept()
    
    def reset_filters(self):
        """Reset all filters"""
        self.result_filter_state = {
            "is_active": False,
            "category": "All Categories",
            "accepts_returns": "All",
            "products_on_the_way": "All",
            "status": "All Statuses"  # Reset status filter
        }
        self.accept()
    
    def get_filter_state(self):
        """Return the filter state after dialog is closed"""
        return self.result_filter_state