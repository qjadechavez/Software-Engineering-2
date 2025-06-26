from PyQt5 import QtWidgets, QtCore, QtGui
import mysql.connector
from app.utils.db_manager import DBManager
from datetime import datetime, timedelta
from ..table_factory import TableFactory
from ..style_factory import StyleFactory
from ..control_panel_factory import ControlPanelFactory

class SalesReportTab(QtWidgets.QWidget):
    """Tab for displaying sales report - customer service transactions"""
    
    def __init__(self, parent=None):
        super(SalesReportTab, self).__init__()
        self.parent = parent
        self.filter_state = {
            "is_active": False,
            "date_range": "All Time",
            "payment_method": "All Methods",
            "amount_range": "All Amounts",
            "service": "All Services"
        }
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(15)
        
        # Header section
        header_layout = QtWidgets.QVBoxLayout()
        
        title_label = QtWidgets.QLabel("Sales Report")
        title_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        desc_label = QtWidgets.QLabel("Track customer service transactions and revenue analytics")
        desc_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        header_layout.addWidget(desc_label)
        
        self.layout.addLayout(header_layout)
        
        # Search and filter controls
        self.search_input = QtWidgets.QLineEdit()
        self.control_layout = ControlPanelFactory.create_search_control(
            self.search_input,
            self.filter_sales,
            self.show_filter_dialog
        )
        
        # Store references
        self.filter_button = self.control_layout.filter_button
        self.filter_indicator = self.control_layout.filter_indicator
        
        self.layout.addLayout(self.control_layout)
        
        # Sales statistics
        stats_frame = QtWidgets.QFrame()
        stats_frame.setStyleSheet(StyleFactory.get_section_frame_style())
        stats_layout = QtWidgets.QHBoxLayout(stats_frame)
        stats_layout.setContentsMargins(15, 10, 15, 10)
        
        # Create sales statistics cards
        self.total_revenue = self.create_stat_card("Total Revenue", "₱0.00", "#4CAF50")
        self.total_transactions = self.create_stat_card("Total Transactions", "0", "#2196F3")
        self.avg_transaction = self.create_stat_card("Avg. Transaction", "₱0.00", "#FF9800")
        self.today_sales = self.create_stat_card("Today's Sales", "₱0.00", "#9C27B0")
        
        stats_layout.addWidget(self.total_revenue)
        stats_layout.addWidget(self.total_transactions)
        stats_layout.addWidget(self.avg_transaction)
        stats_layout.addWidget(self.today_sales)
        stats_layout.addStretch()
        
        self.layout.addWidget(stats_frame)
        
        # Create sales table
        self.sales_table = TableFactory.create_table()
        
        # Define column headers and their relative widths
        sales_columns = [
            ("Transaction ID", 0.12),
            ("OR Number", 0.10),
            ("Customer", 0.15),
            ("Service", 0.15),
            ("Amount", 0.10),
            ("Discount", 0.08),
            ("Payment Method", 0.10),
            ("Date", 0.12),
            ("Staff", 0.08)
        ]
        
        # Configure the table columns
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.sales_table, sales_columns, screen_width)
        
        # Add context menu
        self.sales_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.sales_table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.layout.addWidget(self.sales_table)
        
        # Load initial data
        self.load_sales_data()
        
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
    
    def create_stat_card(self, title, value, color):
        """Create a sales statistics card widget"""
        card = QtWidgets.QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #333333;
                border: 2px solid {color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout(card)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("color: #cccccc; font-size: 11px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: bold;")
        value_label.setAlignment(QtCore.Qt.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        # Store reference to value label for updates
        card.value_label = value_label
        
        return card
    
    def load_sales_data(self):
        """Load sales data from the database"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.sales_table.clearContents()
            self.sales_table.setRowCount(0)
            
            # Query for sales transactions
            cursor.execute("""
                SELECT 
                    t.transaction_id,
                    t.or_number,
                    t.customer_name,
                    s.service_name,
                    t.total_amount,
                    t.discount_amount,
                    t.payment_method,
                    t.transaction_date,
                    u.username as staff_name
                FROM transactions t
                LEFT JOIN services s ON t.service_id = s.service_id
                LEFT JOIN users u ON t.created_by = u.user_id
                ORDER BY t.transaction_date DESC
            """)
            
            transactions = cursor.fetchall()
            
            # Calculate statistics
            total_revenue = sum(float(t.get('total_amount', 0)) for t in transactions)
            total_count = len(transactions)
            avg_transaction = total_revenue / total_count if total_count > 0 else 0
            
            # Today's sales
            today = datetime.now().date()
            today_sales = sum(float(t.get('total_amount', 0)) for t in transactions 
                            if t.get('transaction_date') and t['transaction_date'].date() == today)
            
            # Populate the table
            self.sales_table.setRowCount(len(transactions))
            
            for row, transaction in enumerate(transactions):
                # Transaction ID
                self.sales_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(transaction.get('transaction_id', ''))))
                
                # OR Number
                self.sales_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(transaction.get('or_number', ''))))
                
                # Customer
                self.sales_table.setItem(row, 2, QtWidgets.QTableWidgetItem(transaction.get('customer_name', '')))
                
                # Service
                self.sales_table.setItem(row, 3, QtWidgets.QTableWidgetItem(transaction.get('service_name', '')))
                
                # Amount
                amount = float(transaction.get('total_amount', 0))
                amount_item = QtWidgets.QTableWidgetItem(f"₱{amount:.2f}")
                amount_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                if amount > 1000:
                    amount_item.setForeground(QtGui.QColor("#4CAF50"))
                self.sales_table.setItem(row, 4, amount_item)
                
                # Discount
                discount = float(transaction.get('discount_amount', 0))
                discount_item = QtWidgets.QTableWidgetItem(f"₱{discount:.2f}")
                discount_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                if discount > 0:
                    discount_item.setForeground(QtGui.QColor("#FF9800"))
                self.sales_table.setItem(row, 5, discount_item)
                
                # Payment Method
                payment_item = QtWidgets.QTableWidgetItem(transaction.get('payment_method', ''))
                payment_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.sales_table.setItem(row, 6, payment_item)
                
                # Date
                date = transaction.get('transaction_date')
                date_str = date.strftime('%Y-%m-%d %H:%M') if date else ""
                date_item = QtWidgets.QTableWidgetItem(date_str)
                date_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.sales_table.setItem(row, 7, date_item)
                
                # Staff
                self.sales_table.setItem(row, 8, QtWidgets.QTableWidgetItem(transaction.get('staff_name', '')))
            
            # Update statistics
            self.total_revenue.value_label.setText(f"₱{total_revenue:.2f}")
            self.total_transactions.value_label.setText(str(total_count))
            self.avg_transaction.value_label.setText(f"₱{avg_transaction:.2f}")
            self.today_sales.value_label.setText(f"₱{today_sales:.2f}")
            
            cursor.close()
            
            # Re-apply any active filters after loading data
            if self.filter_state["is_active"]:
                self.apply_stored_filters()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def filter_sales(self):
        """Filter sales based on search input"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.sales_table.rowCount()):
            visible = False
            
            # Search across all columns
            for col in range(self.sales_table.columnCount()):
                item = self.sales_table.item(row, col)
                if item and search_text in item.text().lower():
                    visible = True
                    break
                    
            self.sales_table.setRowHidden(row, not visible)
    
    def show_filter_dialog(self):
        """Show advanced filter dialog"""
        from ..dialogs import SalesReportFilterDialog
        
        filter_dialog = SalesReportFilterDialog(self, self.filter_state)
        if filter_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Get the filter state from the dialog
            new_filter_state = filter_dialog.get_filter_state()
            
            # Check if filters were reset
            if not new_filter_state["is_active"] and self.filter_state["is_active"]:
                # Filters were reset
                self.filter_state = new_filter_state
                self.filter_indicator.setVisible(False)
                self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
                
                # Completely rebuild the table
                QtCore.QTimer.singleShot(50, self.rebuild_table)
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
                    if self.filter_state["service"] != "All Services":
                        filter_text.append(f"Service: {self.filter_state['service']}")
                        
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
        
        for row in range(self.sales_table.rowCount()):
            visible = True
            
            # Apply date range filter
            if self.filter_state["date_range"] != "All Time":
                date_item = self.sales_table.item(row, 7)
                if date_item and date_item.text() and date_item.text() != "":
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
                    except ValueError:
                        pass
            
            # Apply payment method filter
            if visible and self.filter_state["payment_method"] != "All Methods":
                payment_item = self.sales_table.item(row, 6)
                if payment_item and payment_item.text() != self.filter_state["payment_method"]:
                    visible = False
            
            # Apply amount range filter
            if visible and self.filter_state["amount_range"] != "All Amounts":
                amount_item = self.sales_table.item(row, 4)
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
            
            # Apply service filter
            if visible and self.filter_state["service"] != "All Services":
                service_item = self.sales_table.item(row, 3)
                if service_item and service_item.text() != self.filter_state["service"]:
                    visible = False
            
            # Set row visibility
            self.sales_table.setRowHidden(row, not visible)
            
            # Track if at least one row is visible
            if visible:
                rows_visible = True
        
        # Show a message if no results are found
        if not rows_visible and self.sales_table.rowCount() > 0:
            QtWidgets.QMessageBox.information(self, "No Results", 
                "No sales match the current filters. Try adjusting your filter criteria.")
    
    def rebuild_table(self):
        """Completely rebuild the table with fresh data"""
        # Store current filter state
        was_filtered = self.filter_state["is_active"]
        filter_state_copy = self.filter_state.copy()
        
        # Reset filter state temporarily
        self.filter_state = {
            "is_active": False,
            "date_range": "All Time",
            "payment_method": "All Methods",
            "amount_range": "All Amounts",
            "service": "All Services"
        }
        
        # Reload data
        self.load_sales_data()
        
        # Restore filter state if necessary
        if was_filtered:
            self.filter_state = filter_state_copy
            # Add a short delay before applying filters to ensure table is fully rendered
            QtCore.QTimer.singleShot(50, self.apply_stored_filters)
    
    def show_context_menu(self, position):
        """Show context menu for the table"""
        item = self.sales_table.itemAt(position)
        if item is None:
            return
        
        row = item.row()
        
        menu = QtWidgets.QMenu(self)
        
        view_details_action = menu.addAction("View Transaction Details")
        view_details_action.triggered.connect(lambda: self.view_transaction_details(row))
        
        menu.exec_(self.sales_table.mapToGlobal(position))
    
    def view_transaction_details(self, row):
        """View detailed information for a transaction"""
        transaction_id = self.sales_table.item(row, 0).text()
        QtWidgets.QMessageBox.information(self, "Transaction Details", f"Details for {transaction_id} will be shown here")
    
    def refresh_data(self):
        """Refresh the tab data"""
        self.load_sales_data()