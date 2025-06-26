from PyQt5 import QtWidgets, QtCore
import mysql.connector
from app.utils.db_manager import DBManager
from app.ui.pages.inventory.dialogs.base_dialog import BaseDialog

class TransactionFilterDialog(BaseDialog):
    """Dialog for filtering customer transactions"""
    
    def __init__(self, parent=None, filter_state=None):
        super(TransactionFilterDialog, self).__init__(parent, None, "Filter Transactions")
        self.parent = parent
        self.filter_state = filter_state or {
            "is_active": False,
            "date_range": "All Time",
            "payment_method": "All Methods",
            "gender": "All"
        }
        self.result_filter_state = self.filter_state.copy()
        
        self.setup_ui()
    
    def setup_ui(self):
        self.setup_base_ui(450)
        
        self.header_label.setText("Filter Transactions")
        
        date_label = QtWidgets.QLabel("Date Range:")
        self.date_combo = QtWidgets.QComboBox()
        self.date_combo.addItems(["All Time", "Today", "This Week", "This Month", "This Year"])
        
        date_index = self.date_combo.findText(self.filter_state["date_range"])
        if date_index >= 0:
            self.date_combo.setCurrentIndex(date_index)
            
        self.form_layout.addRow(date_label, self.date_combo)
        
        payment_label = QtWidgets.QLabel("Payment Method:")
        self.payment_combo = QtWidgets.QComboBox()
        self.payment_combo.addItem("All Methods")
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT payment_method FROM transactions WHERE payment_method IS NOT NULL AND payment_method != ''")
            methods = cursor.fetchall()
            for method in methods:
                self.payment_combo.addItem(method['payment_method'])
            cursor.close()
        except mysql.connector.Error:
            self.payment_combo.addItem("Cash")
        
        payment_index = self.payment_combo.findText(self.filter_state["payment_method"])
        if payment_index >= 0:
            self.payment_combo.setCurrentIndex(payment_index)
            
        self.form_layout.addRow(payment_label, self.payment_combo)
        
        gender_label = QtWidgets.QLabel("Gender:")
        self.gender_combo = QtWidgets.QComboBox()
        self.gender_combo.addItem("All")
        
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
            self.gender_combo.addItems(["Male", "Female", "Other"])
        
        gender_index = self.gender_combo.findText(self.filter_state["gender"])
        if gender_index >= 0:
            self.gender_combo.setCurrentIndex(gender_index)
            
        self.form_layout.addRow(gender_label, self.gender_combo)
        
        # Filter helper text
        helper_text = QtWidgets.QLabel(
            "Tip: Filter by date range and gender to find patterns in customer transactions."
        )
        helper_text.setStyleSheet("color: #4FC3F7; font-style: italic; font-size: 12px;")
        helper_text.setWordWrap(True)
        self.form_layout.addRow(helper_text)
        
        self.save_button.setText("Apply Filters")
        self.save_button.clicked.connect(self.apply_filters)
        
        self.reset_button = QtWidgets.QPushButton("Reset Filters")
        self.reset_button.setObjectName("resetButton")
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
        
        button_layout = self.save_button.parent().layout()
        button_layout.insertWidget(button_layout.count() - 2, self.reset_button)
    
    def apply_filters(self):
        """Apply selected filters"""
        self.result_filter_state["date_range"] = self.date_combo.currentText()
        self.result_filter_state["payment_method"] = self.payment_combo.currentText()
        self.result_filter_state["gender"] = self.gender_combo.currentText()
        
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