from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
from ..style_factory import StyleFactory

class TransactionFilterDialog(QtWidgets.QDialog):
    """Dialog for filtering customer transactions"""
    
    def __init__(self, parent=None, filter_state=None):
        super(TransactionFilterDialog, self).__init__(parent)
        self.parent = parent
        self.filter_state = filter_state or {
            "is_active": False,
            "date_range": "All Time",
            "payment_method": "All Methods",
            "gender": "All"
        }
        self.result_filter_state = self.filter_state.copy()
        
        self.setWindowTitle("Filter Transactions")
        self.setMinimumWidth(400)
        self.setStyleSheet(StyleFactory.get_dialog_style())
        
        self.setup_ui()
    
    def setup_ui(self):
        # Create layout
        layout = QtWidgets.QVBoxLayout(self)
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(15)
        
        # Date range filter
        date_label = QtWidgets.QLabel("Date Range:")
        self.date_combo = QtWidgets.QComboBox()
        self.date_combo.addItems(["All Time", "Today", "This Week", "This Month", "This Year"])
        
        # Set the combo box to match stored filter state
        date_index = self.date_combo.findText(self.filter_state["date_range"])
        if date_index >= 0:
            self.date_combo.setCurrentIndex(date_index)
            
        form_layout.addRow(date_label, self.date_combo)
        
        # Payment method filter
        payment_label = QtWidgets.QLabel("Payment Method:")
        self.payment_combo = QtWidgets.QComboBox()
        self.payment_combo.addItem("All Methods")
        
        # Get unique payment methods
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT payment_method FROM transactions WHERE payment_method IS NOT NULL AND payment_method != ''")
            methods = cursor.fetchall()
            for method in methods:
                self.payment_combo.addItem(method['payment_method'])
            cursor.close()
        except mysql.connector.Error:
            # Add default if DB connection fails
            self.payment_combo.addItem("Cash")
        
        # Set the combo box to match stored filter state
        payment_index = self.payment_combo.findText(self.filter_state["payment_method"])
        if payment_index >= 0:
            self.payment_combo.setCurrentIndex(payment_index)
            
        form_layout.addRow(payment_label, self.payment_combo)
        
        # Gender filter
        gender_label = QtWidgets.QLabel("Gender:")
        self.gender_combo = QtWidgets.QComboBox()
        self.gender_combo.addItem("All")
        
        # Get unique gender values
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT customer_gender FROM transactions WHERE customer_gender IS NOT NULL AND customer_gender != ''")
            genders = cursor.fetchall()
            for gender in genders:
                if gender['customer_gender'] not in ["All"]:  # Avoid duplicates
                    self.gender_combo.addItem(gender['customer_gender'])
            cursor.close()
        except mysql.connector.Error:
            # Add defaults if DB connection fails
            self.gender_combo.addItems(["Male", "Female", "Other"])
        
        # Set the combo box to match stored filter state
        gender_index = self.gender_combo.findText(self.filter_state["gender"])
        if gender_index >= 0:
            self.gender_combo.setCurrentIndex(gender_index)
            
        form_layout.addRow(gender_label, self.gender_combo)
        
        # Filter helper text
        helper_text = QtWidgets.QLabel(
            "Tip: Filter by date range and gender to find patterns in customer transactions."
        )
        helper_text.setStyleSheet("color: #4FC3F7; font-style: italic; font-size: 12px;")
        helper_text.setWordWrap(True)
        
        # Buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        reset_button = QtWidgets.QPushButton("Reset Filters")
        reset_button.setObjectName("resetButton")
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
        
        apply_button = QtWidgets.QPushButton("Apply Filters")
        
        buttons_layout.addWidget(reset_button)
        buttons_layout.addStretch()
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
        self.result_filter_state["date_range"] = self.date_combo.currentText()
        self.result_filter_state["payment_method"] = self.payment_combo.currentText()
        self.result_filter_state["gender"] = self.gender_combo.currentText()
        
        # Determine if any filters are active
        self.result_filter_state["is_active"] = (
            self.result_filter_state["date_range"] != "All Time" or
            self.result_filter_state["payment_method"] != "All Methods" or
            self.result_filter_state["gender"] != "All"
        )
        
        self.accept()
    
    def reset_filters(self):
        """Reset all filters"""
        self.result_filter_state = {
            "is_active": False,
            "date_range": "All Time",
            "payment_method": "All Methods",
            "gender": "All"
        }
        self.accept()
    
    def get_filter_state(self):
        """Return the filter state after dialog is closed"""
        return self.result_filter_state