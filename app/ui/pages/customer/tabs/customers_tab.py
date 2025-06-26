from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
import mysql.connector
from app.utils.db_manager import DBManager
from datetime import datetime
from ..table_factory import TableFactory
from ..style_factory import StyleFactory
from ..control_panel_factory import ControlPanelFactory
from ..dialogs import TransactionFilterDialog

class CustomersTab(QtWidgets.QWidget):
    """Tab for displaying customer transaction history"""
    
    def __init__(self, parent=None):
        super(CustomersTab, self).__init__()
        self.parent = parent
        self.filter_state = {
            "is_active": False,
            "date_range": "All Time",
            "payment_method": "All Methods",
            "gender": "All"
        }
        self.setup_ui()
        self.load_transactions()
    
    def setup_ui(self):
        """Set up the UI components for the customers tab"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 10)
        self.layout.setSpacing(10)
        
        # Create search input
        self.search_input = QtWidgets.QLineEdit()
        
        # Create control panel using factory - no add button
        self.control_layout = ControlPanelFactory.create_search_control(
            self.search_input,
            self.filter_transactions,
            self.show_transaction_filter_dialog
        )
        
        # Store reference to filter button and indicator
        self.filter_button = self.control_layout.filter_button
        self.filter_indicator = self.control_layout.filter_indicator
        
        self.layout.addLayout(self.control_layout)
        
        # Create customers table
        self.customers_table = TableFactory.create_table()
        
        # Define column headers and their relative widths
        customer_columns = [
            ("Transaction ID", 0.10), 
            ("OR Number", 0.08),
            ("Customer Name", 0.08),
            ("Phone", 0.07),
            ("Gender", 0.05),
            ("City", 0.08),
            ("Service", 0.10),
            ("Amount", 0.05),
            ("Payment Method", 0.08),
            ("Discount", 0.05),
            ("Date", 0.09),
            ("Staff", 0.05)
        ]
        
        # Configure the table columns to fit horizontally
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.customers_table, customer_columns, screen_width)
        
        # Add context menu to the table
        self.customers_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customers_table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.layout.addWidget(self.customers_table)
        
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
    
    def load_transactions(self):
        """Load customer transactions from the database and populate the table"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.customers_table.clearContents()
            self.customers_table.setRowCount(0)
            
            # Reset search filter
            self.search_input.blockSignals(True)
            self.search_input.clear()
            self.search_input.blockSignals(False)
            
            # Join with users table to get staff name
            cursor.execute("""
                SELECT t.*, u.username as staff_name, s.service_name 
                FROM transactions t
                LEFT JOIN users u ON t.created_by = u.user_id
                LEFT JOIN services s ON t.service_id = s.service_id
                ORDER BY t.transaction_date DESC
            """)
            transactions = cursor.fetchall()
            
            # Populate the table
            self.customers_table.setRowCount(len(transactions))
            
            for row, transaction in enumerate(transactions):
                # Transaction ID
                id_item = QtWidgets.QTableWidgetItem(str(transaction.get('transaction_id', '')))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.customers_table.setItem(row, 0, id_item)
                
                # OR Number
                or_item = QtWidgets.QTableWidgetItem(str(transaction.get('or_number', '')))
                or_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.customers_table.setItem(row, 1, or_item)
                
                # Customer name
                self.customers_table.setItem(row, 2, QtWidgets.QTableWidgetItem(transaction.get('customer_name', '')))
                
                # Phone
                phone_item = QtWidgets.QTableWidgetItem(transaction.get('customer_phone', ''))
                phone_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.customers_table.setItem(row, 3, phone_item)
                
                # Gender
                gender_item = QtWidgets.QTableWidgetItem(transaction.get('customer_gender', ''))
                gender_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.customers_table.setItem(row, 4, gender_item)
                
                # City
                self.customers_table.setItem(row, 5, QtWidgets.QTableWidgetItem(transaction.get('customer_city', '')))
                
                # Service
                self.customers_table.setItem(row, 6, QtWidgets.QTableWidgetItem(transaction.get('service_name', '')))
                
                # Amount with proper formatting
                total = float(transaction.get('total_amount', 0))
                amount_item = QtWidgets.QTableWidgetItem(f"₱{total:.2f}")
                amount_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                
                # Color code based on amount
                if total > 1000:
                    amount_item.setForeground(QtGui.QColor("#4CAF50"))  # Green for high value
                
                self.customers_table.setItem(row, 7, amount_item)
                
                # Payment Method
                payment_item = QtWidgets.QTableWidgetItem(transaction.get('payment_method', ''))
                payment_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.customers_table.setItem(row, 8, payment_item)
                
                # Discount
                discount = float(transaction.get('discount_percentage', 0))
                discount_item = QtWidgets.QTableWidgetItem(f"{discount:.0f}%")
                discount_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                if discount > 0:
                    discount_item.setForeground(QtGui.QColor("#FF9800"))  # Orange for discount
                
                self.customers_table.setItem(row, 9, discount_item)
                
                # Date
                date = transaction.get('transaction_date')
                date_str = date.strftime('%Y-%m-%d %H:%M') if date else ""
                date_item = QtWidgets.QTableWidgetItem(date_str)
                date_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.customers_table.setItem(row, 10, date_item)
                
                # Staff
                self.customers_table.setItem(row, 11, QtWidgets.QTableWidgetItem(transaction.get('staff_name', '')))
            
            cursor.close()
            
            # Re-apply any active filters after loading data
            if self.filter_state["is_active"]:
                self.apply_stored_filters()
                
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def filter_transactions(self):
        """Filter transactions based on search input"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.customers_table.rowCount()):
            visible = False
            
            # Search across all columns
            for col in range(self.customers_table.columnCount()):
                item = self.customers_table.item(row, col)
                if item and search_text in item.text().lower():
                    visible = True
                    break
                    
            self.customers_table.setRowHidden(row, not visible)
    
    def show_transaction_filter_dialog(self):
        """Show advanced filter dialog for transactions"""
        filter_dialog = TransactionFilterDialog(self, self.filter_state)
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
                    if self.filter_state["gender"] != "All":
                        filter_text.append(f"Gender: {self.filter_state['gender']}")
                        
                    if filter_text:
                        self.filter_indicator.setText(f"Active filters: {', '.join(filter_text)}")
                        self.filter_indicator.setVisible(True)
                        # Use the same blue button style as the products tab
                        self.filter_button.setStyleSheet(StyleFactory.get_active_filter_button_style())
                else:
                    self.filter_indicator.setVisible(False)
                    self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
    
    def reset_filters(self, dialog=None):
        """Reset all filters"""
        self.filter_state = {
            "is_active": False,
            "date_range": "All Time",
            "payment_method": "All Methods",
            "gender": "All"
        }
        
        # Show all rows
        for row in range(self.customers_table.rowCount()):
            self.customers_table.setRowHidden(row, False)
        
        # Hide filter indicator
        self.filter_indicator.setVisible(False)
        
        # Reset filter button color
        self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
        
        if dialog:
            dialog.accept()
    
    def apply_stored_filters(self):
        """Apply the filters stored in filter_state"""
        if not self.filter_state["is_active"]:
            return
            
        # Get current date for date range comparisons
        current_date = datetime.now()
        
        # Track if any row is visible
        rows_visible = False
        
        for row in range(self.customers_table.rowCount()):
            visible = True
            
            # Apply date range filter
            if self.filter_state["date_range"] != "All Time":
                date_item = self.customers_table.item(row, 10)
                if date_item and date_item.text():
                    try:
                        transaction_date = datetime.strptime(date_item.text().split()[0], '%Y-%m-%d')
                        
                        if self.filter_state["date_range"] == "Today":
                            if transaction_date.date() != current_date.date():
                                visible = False
                        elif self.filter_state["date_range"] == "This Week":
                            # Calculate days since the start of the week
                            days_since = (current_date.date() - transaction_date.date()).days
                            if days_since < 0 or days_since >= 7:
                                visible = False
                        elif self.filter_state["date_range"] == "This Month":
                            if (transaction_date.year != current_date.year or 
                                transaction_date.month != current_date.month):
                                visible = False
                        elif self.filter_state["date_range"] == "This Year":
                            if transaction_date.year != current_date.year:
                                visible = False
                    except ValueError:
                        # If date parsing fails, keep the row visible
                        pass
            
            # Apply payment method filter
            if visible and self.filter_state["payment_method"] != "All Methods":
                payment_item = self.customers_table.item(row, 8)
                if payment_item and payment_item.text() != self.filter_state["payment_method"]:
                    visible = False
            
            # Apply gender filter
            if visible and self.filter_state["gender"] != "All":
                gender_item = self.customers_table.item(row, 4)
                if gender_item and gender_item.text() != self.filter_state["gender"]:
                    visible = False
            
            # Set row visibility
            self.customers_table.setRowHidden(row, not visible)
            
            # Track if at least one row is visible
            if visible:
                rows_visible = True
        
        # Show a message if no results are found
        if not rows_visible and self.customers_table.rowCount() > 0:
            QtWidgets.QMessageBox.information(self, "No Results", 
                "No transactions match the current filters. Try adjusting your filter criteria.")
    
    def show_context_menu(self, position):
        """Show context menu for the table"""
        item = self.customers_table.itemAt(position)
        if item is None:
            return
        
        row = item.row()
        transaction_id = self.customers_table.item(row, 0).text()
        
        menu = QtWidgets.QMenu(self)
        
        view_action = menu.addAction("View Transaction Details")
        view_action.triggered.connect(lambda: self.view_transaction_details(row))
        
        menu.exec_(self.customers_table.mapToGlobal(position))
    
    def view_transaction_details(self, row):
        """View detailed information for a transaction"""
        transaction_id = self.customers_table.item(row, 0).text()
        customer_name = self.customers_table.item(row, 2).text()
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Query for transaction details
            cursor.execute("""
                SELECT t.*, s.service_name, u.username as staff_name
                FROM transactions t
                LEFT JOIN services s ON t.service_id = s.service_id
                LEFT JOIN users u ON t.created_by = u.user_id
                WHERE t.transaction_id = %s
            """, (transaction_id,))
            
            transaction = cursor.fetchone()
            
            if transaction:
                # Create transaction details dialog
                detail_dialog = QtWidgets.QDialog(self)
                detail_dialog.setWindowTitle(f"Transaction Receipt - {customer_name}")
                detail_dialog.setMinimumSize(550, 700)
                detail_dialog.setStyleSheet("""
                    QDialog {
                        background-color: #232323;
                    }
                """)
                
                layout = QtWidgets.QVBoxLayout(detail_dialog)
                layout.setSpacing(15)
                
                # Create receipt widget
                receipt_content = QtWidgets.QWidget()
                receipt_content.setObjectName("receiptContent")
                receipt_content.setStyleSheet(StyleFactory.get_receipt_style())
                receipt_content.setFixedSize(400, 600)
                
                receipt_layout = QtWidgets.QVBoxLayout(receipt_content)
                receipt_layout.setAlignment(QtCore.Qt.AlignTop)
                receipt_layout.setContentsMargins(20, 20, 20, 20)
                receipt_layout.setSpacing(5)
                
                # HEADER SECTION
                company_name = QtWidgets.QLabel("Miere Beauty Lounge")
                company_name.setObjectName("receiptTitle")
                company_name.setAlignment(QtCore.Qt.AlignCenter)
                receipt_layout.addWidget(company_name)
                
                address = QtWidgets.QLabel("Rainbow St, Marikina City")
                address.setStyleSheet("color: #555555; font-size: 10px;")
                address.setAlignment(QtCore.Qt.AlignCenter)
                receipt_layout.addWidget(address)
                
                contact_details = QtWidgets.QLabel("0962 915 5277 | miere.beautylounge@gmail.com")
                contact_details.setStyleSheet("color: #555555; font-size: 10px;")
                contact_details.setAlignment(QtCore.Qt.AlignCenter)
                receipt_layout.addWidget(contact_details)
                
                # Add space
                receipt_layout.addSpacing(10)
                
                receipt_title = QtWidgets.QLabel("TRANSACTION RECEIPT")
                receipt_title.setObjectName("receiptHeading")
                receipt_title.setAlignment(QtCore.Qt.AlignCenter)
                receipt_layout.addWidget(receipt_title)
                
                # TRANSACTION DETAILS
                transaction_widget = QtWidgets.QWidget()
                transaction_layout = QtWidgets.QGridLayout(transaction_widget)
                transaction_layout.setContentsMargins(0, 5, 0, 5)
                transaction_layout.setSpacing(5)
                
                receipt_label = QtWidgets.QLabel("Receipt No:")
                receipt_label.setObjectName("receiptLabel")
                or_value = QtWidgets.QLabel(str(transaction.get('or_number', '')))
                or_value.setObjectName("receiptValue")
                
                date_label = QtWidgets.QLabel("Date/Time:")
                date_label.setObjectName("receiptLabel")
                date_time_value = QtWidgets.QLabel(
                    transaction.get('transaction_date').strftime('%Y-%m-%d %H:%M:%S') if transaction.get('transaction_date') else ""
                )
                date_time_value.setObjectName("receiptValue")
                
                txn_label = QtWidgets.QLabel("Transaction ID:")
                txn_label.setObjectName("receiptLabel")
                transaction_value = QtWidgets.QLabel(str(transaction.get('transaction_id', '')))
                transaction_value.setObjectName("receiptValue")
                
                transaction_layout.addWidget(receipt_label, 0, 0)
                transaction_layout.addWidget(or_value, 0, 1)
                transaction_layout.addWidget(date_label, 1, 0)
                transaction_layout.addWidget(date_time_value, 1, 1)
                transaction_layout.addWidget(txn_label, 2, 0)
                transaction_layout.addWidget(transaction_value, 2, 1)
                
                receipt_layout.addWidget(transaction_widget)
                
                # CUSTOMER DETAILS
                customer_widget = QtWidgets.QWidget()
                customer_layout = QtWidgets.QGridLayout(customer_widget)
                customer_layout.setContentsMargins(0, 5, 0, 5)
                customer_layout.setSpacing(5)
                
                customer_label = QtWidgets.QLabel("Customer:")
                customer_label.setObjectName("receiptLabel")
                customer_name_value = QtWidgets.QLabel(str(transaction.get('customer_name', '')))
                customer_name_value.setObjectName("receiptValue")
                
                phone_label = QtWidgets.QLabel("Phone:")
                phone_label.setObjectName("receiptLabel")
                customer_phone_value = QtWidgets.QLabel(str(transaction.get('customer_phone', '')))
                customer_phone_value.setObjectName("receiptValue")
                
                gender_label = QtWidgets.QLabel("Gender:")
                gender_label.setObjectName("receiptLabel")
                gender_value = QtWidgets.QLabel(str(transaction.get('customer_gender', '')))
                gender_value.setObjectName("receiptValue")
                
                city_label = QtWidgets.QLabel("City:")
                city_label.setObjectName("receiptLabel")
                city_value = QtWidgets.QLabel(str(transaction.get('customer_city', '')))
                city_value.setObjectName("receiptValue")
                
                customer_layout.addWidget(customer_label, 0, 0)
                customer_layout.addWidget(customer_name_value, 0, 1)
                customer_layout.addWidget(phone_label, 1, 0)
                customer_layout.addWidget(customer_phone_value, 1, 1)
                customer_layout.addWidget(gender_label, 2, 0)
                customer_layout.addWidget(gender_value, 2, 1)
                customer_layout.addWidget(city_label, 3, 0)
                customer_layout.addWidget(city_value, 3, 1)
                
                receipt_layout.addWidget(customer_widget)
                
                # Space instead of divider
                receipt_layout.addSpacing(10)
                
                # SERVICE SECTION
                service_header = QtWidgets.QLabel("SERVICE DETAILS")
                service_header.setObjectName("receiptHeading")
                service_header.setAlignment(QtCore.Qt.AlignLeft)
                receipt_layout.addWidget(service_header)
                
                # ITEMS SECTION HEADER
                items_header = QtWidgets.QWidget()
                items_header_layout = QtWidgets.QHBoxLayout(items_header)
                items_header_layout.setContentsMargins(0, 5, 0, 5)
                items_header_layout.setSpacing(0)
                
                desc_header = QtWidgets.QLabel("Description")
                desc_header.setStyleSheet("color: #333333; font-size: 10px; font-weight: bold;")
                qty_header = QtWidgets.QLabel("Qty")
                qty_header.setStyleSheet("color: #333333; font-size: 10px; font-weight: bold;")
                qty_header.setAlignment(QtCore.Qt.AlignCenter)
                price_header = QtWidgets.QLabel("Amount")
                price_header.setStyleSheet("color: #333333; font-size: 10px; font-weight: bold;")
                price_header.setAlignment(QtCore.Qt.AlignRight)
                
                items_header_layout.addWidget(desc_header, 6)
                items_header_layout.addWidget(qty_header, 1)
                items_header_layout.addWidget(price_header, 3)
                
                receipt_layout.addWidget(items_header)
                
                # SERVICE TABLE
                service_table = QtWidgets.QTableWidget()
                service_table.setColumnCount(3)
                service_table.setStyleSheet("""
                    QTableWidget {
                        border: none;
                        background-color: white;
                        font-size: 10px;
                        color: #333333;
                    }
                    QTableWidget::item {
                        padding: 2px;
                    }
                """)
                service_table.horizontalHeader().setVisible(False)
                service_table.verticalHeader().setVisible(False)
                service_table.setShowGrid(False)
                service_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                service_table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
                service_table.setColumnWidth(0, 230)
                service_table.setColumnWidth(1, 40)
                service_table.setColumnWidth(2, 80)
                
                # Add service to table
                service_table.setRowCount(1)
                service_name_item = QtWidgets.QTableWidgetItem(transaction.get('service_name', ''))
                quantity_item = QtWidgets.QTableWidgetItem("1")
                price_item = QtWidgets.QTableWidgetItem(f"₱{float(transaction.get('base_amount', 0)):.2f}")
                
                service_name_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                quantity_item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                
                service_table.setItem(0, 0, service_name_item)
                service_table.setItem(0, 1, quantity_item)
                service_table.setItem(0, 2, price_item)
                service_table.setRowHeight(0, 20)
                
                receipt_layout.addWidget(service_table)
                
                # Space instead of divider
                receipt_layout.addSpacing(10)
                
                # PAYMENT SUMMARY
                summary_widget = QtWidgets.QWidget()
                summary_layout = QtWidgets.QGridLayout(summary_widget)
                summary_layout.setContentsMargins(0, 5, 0, 5)
                summary_layout.setSpacing(5)
                
                subtotal_label = QtWidgets.QLabel("Subtotal:")
                subtotal_label.setStyleSheet("color: #333333; font-size: 10px;")
                base_price_value = QtWidgets.QLabel(f"₱{float(transaction.get('base_amount', 0)):.2f}")
                base_price_value.setStyleSheet("color: #333333; font-size: 10px;")
                base_price_value.setAlignment(QtCore.Qt.AlignRight)
                
                discount_label = QtWidgets.QLabel("Discount:")
                discount_label.setStyleSheet("color: #333333; font-size: 10px;")
                discount_value = QtWidgets.QLabel(f"-₱{float(transaction.get('discount_amount', 0)):.2f}")
                discount_value.setStyleSheet("color: #333333; font-size: 10px;")
                discount_value.setAlignment(QtCore.Qt.AlignRight)
                
                total_label = QtWidgets.QLabel("Total:")
                total_label.setObjectName("receiptLabel")
                total_amount_value = QtWidgets.QLabel(f"₱{float(transaction.get('total_amount', 0)):.2f}")
                total_amount_value.setObjectName("totalValue")
                total_amount_value.setAlignment(QtCore.Qt.AlignRight)
                
                payment_label = QtWidgets.QLabel("Payment Method:")
                payment_label.setStyleSheet("color: #333333; font-size: 10px;")
                payment_method_value = QtWidgets.QLabel(str(transaction.get('payment_method', '')))
                payment_method_value.setStyleSheet("color: #333333; font-size: 10px;")
                payment_method_value.setAlignment(QtCore.Qt.AlignRight)
                
                coupon_label = QtWidgets.QLabel("Coupon Code:")
                coupon_label.setStyleSheet("color: #333333; font-size: 10px;")
                coupon_value = QtWidgets.QLabel(str(transaction.get('coupon_code', 'None') or 'None'))
                coupon_value.setStyleSheet("color: #333333; font-size: 10px;")
                coupon_value.setAlignment(QtCore.Qt.AlignRight)
                
                summary_layout.addWidget(subtotal_label, 0, 0)
                summary_layout.addWidget(base_price_value, 0, 1)
                summary_layout.addWidget(discount_label, 1, 0)
                summary_layout.addWidget(discount_value, 1, 1)
                summary_layout.addWidget(total_label, 2, 0)
                summary_layout.addWidget(total_amount_value, 2, 1)
                summary_layout.addWidget(payment_label, 3, 0)
                summary_layout.addWidget(payment_method_value, 3, 1)
                summary_layout.addWidget(coupon_label, 4, 0)
                summary_layout.addWidget(coupon_value, 4, 1)
                
                receipt_layout.addWidget(summary_widget)
                
                # Space instead of divider
                receipt_layout.addSpacing(10)
                
                # FOOTER
                footer_widget = QtWidgets.QWidget()
                footer_layout = QtWidgets.QGridLayout(footer_widget)
                footer_layout.setContentsMargins(0, 5, 0, 5)
                footer_layout.setSpacing(5)
                
                staff_label = QtWidgets.QLabel("Served by:")
                staff_label.setStyleSheet("color: #333333; font-size: 10px;")
                served_by_value = QtWidgets.QLabel(str(transaction.get('staff_name', '')))
                served_by_value.setStyleSheet("color: #333333; font-size: 10px; font-weight: bold;")
                
                footer_layout.addWidget(staff_label, 0, 0)
                footer_layout.addWidget(served_by_value, 0, 1)
                
                receipt_layout.addWidget(footer_widget)
                
                # Add receipt to dialog layout
                layout.addWidget(receipt_content, 0, QtCore.Qt.AlignCenter)
                
                # Action buttons
                button_layout = QtWidgets.QHBoxLayout()
                
                # Print button
                print_button = QtWidgets.QPushButton("Print Receipt")
                print_button.setStyleSheet("""
                    QPushButton {
                        background-color: #007ACC;
                        color: white;
                        border-radius: 5px;
                        padding: 8px 15px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #0099FF;
                    }
                """)
                print_button.clicked.connect(lambda: self.print_receipt(receipt_content))
                
                # Save as PDF button
                save_pdf_button = QtWidgets.QPushButton("Save as PDF")
                save_pdf_button.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border-radius: 5px;
                        padding: 8px 15px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #5CBF60;
                    }
                """)
                save_pdf_button.clicked.connect(lambda: self.save_receipt_as_pdf(receipt_content, transaction_id))
                
                # Close button
                close_button = QtWidgets.QPushButton("Close")
                close_button.setStyleSheet("""
                    QPushButton {
                        background-color: #666666;
                        color: white;
                        border-radius: 5px;
                        padding: 8px 15px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #777777;
                    }
                """)
                close_button.clicked.connect(detail_dialog.accept)
                
                button_layout.addWidget(print_button)
                button_layout.addWidget(save_pdf_button)
                button_layout.addStretch()
                button_layout.addWidget(close_button)
                
                layout.addLayout(button_layout)
                
                detail_dialog.exec_()
            
            cursor.close()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def print_receipt(self, receipt_widget):
        """Print the transaction receipt"""
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        printer.setPageSize(QtPrintSupport.QPrinter.A6)
        print_dialog = QtPrintSupport.QPrintDialog(printer, self)
        
        if print_dialog.exec_() == QtWidgets.QDialog.Accepted:
            painter = QtGui.QPainter(printer)
            rect = painter.viewport()
            size = receipt_widget.size()
            scale = min(rect.width() / size.width(), rect.height() / size.height())
            painter.scale(scale, scale)
            receipt_widget.render(painter)
            painter.end()
            QtWidgets.QMessageBox.information(self, "Print Receipt", "Receipt printed successfully!")
    
    def save_receipt_as_pdf(self, receipt_widget, transaction_id):
        """Save the transaction receipt as a PDF file"""
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 
            "Save Receipt as PDF", 
            f"Receipt_{transaction_id}.pdf", 
            "PDF Files (*.pdf)"
        )
        
        if file_name:
            printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
            printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
            printer.setOutputFileName(file_name)
            printer.setPageSize(QtPrintSupport.QPrinter.A6)
            
            painter = QtGui.QPainter(printer)
            rect = painter.viewport()
            size = receipt_widget.size()
            scale = min(rect.width() / size.width(), rect.height() / size.height())
            painter.scale(scale, scale)
            receipt_widget.render(painter)
            painter.end()
            QtWidgets.QMessageBox.information(self, "Save PDF", "Receipt saved as PDF successfully!")
    
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
            "gender": "All"
        }
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Query for all transactions with joined data
            cursor.execute("""
                SELECT t.*, u.username as staff_name, s.service_name 
                FROM transactions t
                LEFT JOIN users u ON t.created_by = u.user_id
                LEFT JOIN services s ON t.service_id = s.service_id
                ORDER BY t.transaction_date DESC
            """)
            transactions = cursor.fetchall()
            
            # Create and configure a new table from scratch
            new_table = TableFactory.create_table()
            customer_columns = [
                ("Transaction ID", 0.10), 
                ("OR Number", 0.08),
                ("Customer Name", 0.08),
                ("Phone", 0.07),
                ("Gender", 0.05),
                ("City", 0.08),
                ("Service", 0.10),
                ("Amount", 0.05),
                ("Payment Method", 0.08),
                ("Discount", 0.05),
                ("Date", 0.09),
                ("Staff", 0.05)
            ]
            
            screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
            TableFactory.configure_table_columns(new_table, customer_columns, screen_width)
            
            # Set up context menu for the new table
            new_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            new_table.customContextMenuRequested.connect(self.show_context_menu)
            
            # Populate the new table
            new_table.setRowCount(len(transactions))
            
            for row, transaction in enumerate(transactions):
                # Transaction ID
                id_item = QtWidgets.QTableWidgetItem(str(transaction.get('transaction_id', '')))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                new_table.setItem(row, 0, id_item)
                
                # OR Number
                or_item = QtWidgets.QTableWidgetItem(str(transaction.get('or_number', '')))
                or_item.setTextAlignment(QtCore.Qt.AlignCenter)
                new_table.setItem(row, 1, or_item)
                
                # Customer name
                new_table.setItem(row, 2, QtWidgets.QTableWidgetItem(transaction.get('customer_name', '')))
                
                # Phone
                phone_item = QtWidgets.QTableWidgetItem(transaction.get('customer_phone', ''))
                phone_item.setTextAlignment(QtCore.Qt.AlignCenter)
                new_table.setItem(row, 3, phone_item)
                
                # Gender
                gender_item = QtWidgets.QTableWidgetItem(transaction.get('customer_gender', ''))
                gender_item.setTextAlignment(QtCore.Qt.AlignCenter)
                new_table.setItem(row, 4, gender_item)
                
                # City
                new_table.setItem(row, 5, QtWidgets.QTableWidgetItem(transaction.get('customer_city', '')))
                
                # Service
                new_table.setItem(row, 6, QtWidgets.QTableWidgetItem(transaction.get('service_name', '')))
                
                # Amount with proper formatting
                total = float(transaction.get('total_amount', 0))
                amount_item = QtWidgets.QTableWidgetItem(f"₱{total:.2f}")
                amount_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                
                # Color code based on amount
                if total > 1000:
                    amount_item.setForeground(QtGui.QColor("#4CAF50"))  # Green for high value
                
                new_table.setItem(row, 7, amount_item)
                
                # Payment Method
                payment_item = QtWidgets.QTableWidgetItem(transaction.get('payment_method', ''))
                payment_item.setTextAlignment(QtCore.Qt.AlignCenter)
                new_table.setItem(row, 8, payment_item)
                
                # Discount
                discount = float(transaction.get('discount_percentage', 0))
                discount_item = QtWidgets.QTableWidgetItem(f"{discount:.0f}%")
                discount_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                if discount > 0:
                    discount_item.setForeground(QtGui.QColor("#FF9800"))  # Orange for discount
                
                new_table.setItem(row, 9, discount_item)
                
                # Date
                date = transaction.get('transaction_date')
                date_str = date.strftime('%Y-%m-%d %H:%M') if date else ""
                date_item = QtWidgets.QTableWidgetItem(date_str)
                date_item.setTextAlignment(QtCore.Qt.AlignCenter)
                new_table.setItem(row, 10, date_item)
                
                # Staff
                new_table.setItem(row, 11, QtWidgets.QTableWidgetItem(transaction.get('staff_name', '')))
            
            # Replace the old table with the new one
            old_table = self.customers_table
            self.layout.replaceWidget(old_table, new_table)
            self.customers_table = new_table
            old_table.deleteLater()
            
            cursor.close()
            
            # Restore filter state if necessary
            if was_filtered:
                self.filter_state = filter_state_copy
                # Add a short delay before applying filters to ensure table is fully rendered
                QtCore.QTimer.singleShot(50, self.apply_stored_filters)
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")