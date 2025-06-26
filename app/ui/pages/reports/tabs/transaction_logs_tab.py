from PyQt5 import QtWidgets, QtCore, QtGui
import mysql.connector
from app.utils.db_manager import DBManager
from datetime import datetime, timedelta
from ..table_factory import TableFactory
from ..style_factory import StyleFactory
from ..control_panel_factory import ControlPanelFactory

class TransactionLogsTab(QtWidgets.QWidget):
    """Tab for displaying transaction logs"""
    
    def __init__(self, parent=None):
        super(TransactionLogsTab, self).__init__()
        self.parent = parent
        self.filter_state = {
            "is_active": False,
            "date_range": "All Time",
            "payment_method": "All Methods",
            "amount_range": "All Amounts",
            "staff": "All Staff"
        }
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(15)
        
        # Header section
        header_layout = QtWidgets.QVBoxLayout()
        
        title_label = QtWidgets.QLabel("Transaction Logs")
        title_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        desc_label = QtWidgets.QLabel("Maintain records of all customer transactions")
        desc_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        header_layout.addWidget(desc_label)
        
        self.layout.addLayout(header_layout)
        
        # Search and filter controls
        self.search_input = QtWidgets.QLineEdit()
        self.control_layout = ControlPanelFactory.create_search_control(
            self.search_input,
            self.filter_transaction_logs,
            self.show_filter_dialog
        )
        
        # Store references
        self.filter_button = self.control_layout.filter_button
        self.filter_indicator = self.control_layout.filter_indicator
        
        self.layout.addLayout(self.control_layout)
        
        # Create table
        self.logs_table = TableFactory.create_table()
        
        # Define column headers
        log_columns = [
            ("Transaction ID", 0.15),
            ("Customer", 0.15),
            ("Service", 0.15),
            ("Amount", 0.10),
            ("Payment Method", 0.10),
            ("Staff", 0.10),
            ("Date/Time", 0.15),
            ("Notes", 0.10)
        ]
        
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.logs_table, log_columns, screen_width)
        
        self.layout.addWidget(self.logs_table)
        self.load_transaction_logs()
        
        # Add filter indicator label
        self.filter_indicator = QtWidgets.QLabel()
        self.filter_indicator.setVisible(False)
        self.filter_indicator.setStyleSheet("""
            QLabel {
                color: #4FC3F7;
                font-style: italic;
                padding-top: 5px;
            }
        """)
        self.layout.addWidget(self.filter_indicator)
    
    def load_transaction_logs(self):
        """Load transaction logs data"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT 
                    t.transaction_id,
                    t.customer_name,
                    s.service_name,
                    t.total_amount,
                    t.payment_method,
                    u.username as staff_name,
                    t.transaction_date,
                    t.notes
                FROM transactions t
                LEFT JOIN services s ON t.service_id = s.service_id
                LEFT JOIN users u ON t.created_by = u.user_id
                ORDER BY t.transaction_date DESC
                LIMIT 1000
            """)
            
            logs = cursor.fetchall()
            self.logs_table.setRowCount(len(logs))
            
            for row, log in enumerate(logs):
                self.logs_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(log.get('transaction_id', ''))))
                self.logs_table.setItem(row, 1, QtWidgets.QTableWidgetItem(log.get('customer_name', '')))
                self.logs_table.setItem(row, 2, QtWidgets.QTableWidgetItem(log.get('service_name', '')))
                
                amount_item = QtWidgets.QTableWidgetItem(f"₱{float(log.get('total_amount', 0)):.2f}")
                amount_item.setTextAlignment(QtCore.Qt.AlignRight)
                self.logs_table.setItem(row, 3, amount_item)
                
                self.logs_table.setItem(row, 4, QtWidgets.QTableWidgetItem(log.get('payment_method', '')))
                self.logs_table.setItem(row, 5, QtWidgets.QTableWidgetItem(log.get('staff_name', '')))
                
                date = log.get('transaction_date')
                date_str = date.strftime('%Y-%m-%d %H:%M') if date else ""
                self.logs_table.setItem(row, 6, QtWidgets.QTableWidgetItem(date_str))
                
                notes = log.get('notes', '') or 'No notes'
                self.logs_table.setItem(row, 7, QtWidgets.QTableWidgetItem(notes[:50] + '...' if len(notes) > 50 else notes))
            
            cursor.close()
            
            # Re-apply any active filters after loading data
            if self.filter_state["is_active"]:
                self.apply_stored_filters()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
    
    def filter_transaction_logs(self):
        """Filter transaction logs based on search input"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.logs_table.rowCount()):
            visible = False
            
            # Search across all columns
            for col in range(self.logs_table.columnCount()):
                item = self.logs_table.item(row, col)
                if item and search_text in item.text().lower():
                    visible = True
                    break
                    
            self.logs_table.setRowHidden(row, not visible)
    
    def show_filter_dialog(self):
        """Show advanced filter dialog for transactions"""
        from ..dialogs import TransactionLogsFilterDialog
        
        filter_dialog = TransactionLogsFilterDialog(self, self.filter_state)
        if filter_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Get the filter state from the dialog
            new_filter_state = filter_dialog.get_filter_state()
            
            # Check if filters were reset
            if not new_filter_state["is_active"] and self.filter_state["is_active"]:
                # Filters were reset
                self.filter_state = new_filter_state
                self.filter_indicator.setVisible(False)
                self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
                
                # Completely reload the table
                QtCore.QTimer.singleShot(50, self.load_transaction_logs)
            else:
                # Regular filter applied
                self.filter_state = new_filter_state
                
                # Apply filters after dialog is closed
                if self.filter_state["is_active"]:
                    QtCore.QTimer.singleShot(50, self.apply_stored_filters)
                    # Update the filter indicator text
                    filter_text = []
                    if self.filter_state["date_range"] != "All Time":
                        filter_text.append(f"Date: {self.filter_state['date_range']}")
                    if self.filter_state["payment_method"] != "All Methods":
                        filter_text.append(f"Payment: {self.filter_state['payment_method']}")
                    if self.filter_state["amount_range"] != "All Amounts":
                        filter_text.append(f"Amount: {self.filter_state['amount_range']}")
                    if self.filter_state["staff"] != "All Staff":
                        filter_text.append(f"Staff: {self.filter_state['staff']}")
                        
                    if filter_text:
                        self.filter_indicator.setText(f"Active filters: {', '.join(filter_text)}")
                        self.filter_indicator.setVisible(True)
                        self.filter_button.setStyleSheet(StyleFactory.get_active_filter_button_style())
                else:
                    self.filter_indicator.setVisible(False)
                    self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
    
    def apply_stored_filters(self):
        """Apply the filters stored in filter_state"""
        if not self.filter_state["is_active"]:
            return
            
        current_date = datetime.now()
        
        # Track if any row is visible
        rows_visible = False
        
        for row in range(self.logs_table.rowCount()):
            visible = True
            
            # Apply date range filter
            if self.filter_state["date_range"] != "All Time":
                date_item = self.logs_table.item(row, 6)
                if date_item and date_item.text():
                    try:
                        transaction_date = datetime.strptime(date_item.text(), '%Y-%m-%d %H:%M')
                        
                        if self.filter_state["date_range"] == "Today":
                            if transaction_date.date() != current_date.date():
                                visible = False
                        elif self.filter_state["date_range"] == "This Week":
                            days_since = (current_date.date() - transaction_date.date()).days
                            if days_since < 0 or days_since >= 7:
                                visible = False
                        elif self.filter_state["date_range"] == "This Month":
                            if (transaction_date.year != current_date.year or 
                                transaction_date.month != current_date.month):
                                visible = False
                        elif self.filter_state["date_range"] == "Last 30 Days":
                            days_since = (current_date.date() - transaction_date.date()).days
                            if days_since < 0 or days_since > 30:
                                visible = False
                        elif self.filter_state["date_range"] == "Last 90 Days":
                            days_since = (current_date.date() - transaction_date.date()).days
                            if days_since < 0 or days_since > 90:
                                visible = False
                    except ValueError:
                        pass
            
            # Apply payment method filter
            if visible and self.filter_state["payment_method"] != "All Methods":
                payment_item = self.logs_table.item(row, 4)
                if payment_item and payment_item.text() != self.filter_state["payment_method"]:
                    visible = False
            
            # Apply staff filter
            if visible and self.filter_state["staff"] != "All Staff":
                staff_item = self.logs_table.item(row, 5)
                if staff_item and staff_item.text() != self.filter_state["staff"]:
                    visible = False
            
            # Apply amount range filter
            if visible and self.filter_state["amount_range"] != "All Amounts":
                amount_item = self.logs_table.item(row, 3)
                if amount_item:
                    try:
                        amount = float(amount_item.text().replace('₱', '').replace(',', ''))
                        amount_range = self.filter_state["amount_range"]
                        
                        if amount_range == "Under ₱500" and amount >= 500:
                            visible = False
                        elif amount_range == "₱500 - ₱1,000" and (amount < 500 or amount > 1000):
                            visible = False
                        elif amount_range == "₱1,000 - ₱2,500" and (amount < 1000 or amount > 2500):
                            visible = False
                        elif amount_range == "₱2,500 - ₱5,000" and (amount < 2500 or amount > 5000):
                            visible = False
                        elif amount_range == "Over ₱5,000" and amount <= 5000:
                            visible = False
                    except ValueError:
                        pass
            
            # Set row visibility
            self.logs_table.setRowHidden(row, not visible)
            
            # Track if at least one row is visible
            if visible:
                rows_visible = True
        
        # Show a message if no results are found
        if not rows_visible and self.logs_table.rowCount() > 0:
            QtWidgets.QMessageBox.information(self, "No Results", 
                "No transactions match the current filters. Try adjusting your filter criteria.")
    
    def refresh_data(self):
        """Refresh the tab data"""
        self.load_transaction_logs()