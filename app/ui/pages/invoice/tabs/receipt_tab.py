from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from ..factories.panel_factory import PanelFactory
import datetime
import random

class ReceiptTab(QtWidgets.QWidget):
    """Tab for displaying and printing the final receipt"""
    
    def __init__(self, parent=None):
        super(ReceiptTab, self).__init__()
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Header
        header_label = QtWidgets.QLabel("Receipt")
        header_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.layout.addWidget(header_label)
        
        # Description
        desc_label = QtWidgets.QLabel("The transaction has been completed successfully!")
        desc_label.setStyleSheet("color: #4CAF50; font-size: 14px; font-weight: bold;")
        self.layout.addWidget(desc_label)
        
        # Receipt preview container
        receipt_container = QtWidgets.QScrollArea()
        receipt_container.setWidgetResizable(True)
        receipt_container.setStyleSheet("""
            QScrollArea {
                border: 1px solid #444444;
                background-color: white;
                border-radius: 4px;
            }
            QScrollBar:vertical {
                background: #f0f0f0;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #c1c1c1;
                border-radius: 5px;
            }
        """)
        
        # Receipt content widget (white background for the receipt)
        self.receipt_content = QtWidgets.QWidget()
        self.receipt_content.setStyleSheet("background-color: white;")
        self.receipt_layout = QtWidgets.QVBoxLayout(self.receipt_content)
        self.receipt_layout.setAlignment(QtCore.Qt.AlignTop)
        self.receipt_layout.setContentsMargins(30, 30, 30, 30)
        self.receipt_layout.setSpacing(8)
        
        # Receipt elements will be added in generateReceipt()
        self.setup_receipt_template()
        
        receipt_container.setWidget(self.receipt_content)
        self.layout.addWidget(receipt_container)
        
        # Action buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        # Print button
        print_button = PanelFactory.create_action_button("Print Receipt")
        print_button.clicked.connect(self.print_receipt)
        button_layout.addWidget(print_button)
        
        # Save as PDF button
        save_pdf_button = PanelFactory.create_action_button("Save as PDF")
        save_pdf_button.clicked.connect(self.save_as_pdf)
        button_layout.addWidget(save_pdf_button)
        
        button_layout.addStretch()
        
        # New transaction button
        new_transaction_button = PanelFactory.create_action_button("New Transaction", primary=False)
        new_transaction_button.clicked.connect(self.start_new_transaction)
        button_layout.addWidget(new_transaction_button)
        
        # Exit button - ADD THIS NEW BUTTON
        exit_button = PanelFactory.create_action_button("Exit", primary=False)
        exit_button.setStyleSheet("""
            QPushButton {
                padding: 10px 15px;
                background-color: #FF5252;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #FF7373;
            }
            QPushButton:pressed {
                background-color: #D32F2F;
            }
            QPushButton:disabled {
                background-color: #888888;
            }
        """)
        exit_button.clicked.connect(self.exit_transaction)
        button_layout.addWidget(exit_button)
        
        self.layout.addLayout(button_layout)
        
    def setup_receipt_template(self):
        """Set up the receipt template structure"""
        # Company header
        company_name = QtWidgets.QLabel("Miere Beauty Lounge")
        company_name.setStyleSheet("color: black; font-size: 18px; font-weight: bold; text-align: center;")
        company_name.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(company_name)
        
        address = QtWidgets.QLabel("Rainbow Street, Marikina City, Philippines, 1811")
        address.setStyleSheet("color: black; font-size: 12px; text-align: center;")
        address.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(address)
        
        contact = QtWidgets.QLabel("0962 915 5277 | Email: miere.beautylounge@gmail.com")
        contact.setStyleSheet("color: black; font-size: 12px; text-align: center;")
        contact.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(contact)
        
        # Horizontal line
        line1 = QtWidgets.QFrame()
        line1.setFrameShape(QtWidgets.QFrame.HLine)
        line1.setFrameShadow(QtWidgets.QFrame.Sunken)
        line1.setStyleSheet("background-color: black;")
        self.receipt_layout.addWidget(line1)
        
        # Receipt title
        receipt_title = QtWidgets.QLabel("OFFICIAL RECEIPT")
        receipt_title.setStyleSheet("color: black; font-size: 16px; font-weight: bold; text-align: center;")
        receipt_title.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(receipt_title)
        
        # Receipt information section
        receipt_info_layout = QtWidgets.QGridLayout()
        receipt_info_layout.setColumnStretch(0, 0)
        receipt_info_layout.setColumnStretch(1, 1)
        receipt_info_layout.setColumnStretch(2, 0)
        receipt_info_layout.setColumnStretch(3, 1)
        
        # Receipt number
        or_label = QtWidgets.QLabel("OR Number:")
        or_label.setStyleSheet("color: black; font-weight: bold;")
        self.or_value = QtWidgets.QLabel()
        self.or_value.setStyleSheet("color: black;")
        
        # Date
        date_label = QtWidgets.QLabel("Date:")
        date_label.setStyleSheet("color: black; font-weight: bold;")
        self.date_value = QtWidgets.QLabel()
        self.date_value.setStyleSheet("color: black;")
        
        # Time
        time_label = QtWidgets.QLabel("Time:")
        time_label.setStyleSheet("color: black; font-weight: bold;")
        self.time_value = QtWidgets.QLabel()
        self.time_value.setStyleSheet("color: black;")
        
        # Transaction ID
        transaction_label = QtWidgets.QLabel("Transaction ID:")
        transaction_label.setStyleSheet("color: black; font-weight: bold;")
        self.transaction_value = QtWidgets.QLabel()
        self.transaction_value.setStyleSheet("color: black;")
        
        receipt_info_layout.addWidget(or_label, 0, 0)
        receipt_info_layout.addWidget(self.or_value, 0, 1)
        receipt_info_layout.addWidget(date_label, 0, 2)
        receipt_info_layout.addWidget(self.date_value, 0, 3)
        receipt_info_layout.addWidget(time_label, 1, 0)
        receipt_info_layout.addWidget(self.time_value, 1, 1)
        receipt_info_layout.addWidget(transaction_label, 1, 2)
        receipt_info_layout.addWidget(self.transaction_value, 1, 3)
        
        self.receipt_layout.addLayout(receipt_info_layout)
        
        # Customer section
        customer_frame = QtWidgets.QFrame()
        customer_frame.setStyleSheet("background-color: #f5f5f5; border-radius: 4px; padding: 8px;")
        customer_layout = QtWidgets.QFormLayout(customer_frame)
        customer_layout.setVerticalSpacing(4)
        
        # Customer name
        customer_name_label = QtWidgets.QLabel("Customer:")
        customer_name_label.setStyleSheet("color: black; font-weight: bold;")
        self.customer_name_value = QtWidgets.QLabel()
        self.customer_name_value.setStyleSheet("color: black;")
        customer_layout.addRow(customer_name_label, self.customer_name_value)
        
        # Customer phone
        customer_phone_label = QtWidgets.QLabel("Phone:")
        customer_phone_label.setStyleSheet("color: black; font-weight: bold;")
        self.customer_phone_value = QtWidgets.QLabel()
        self.customer_phone_value.setStyleSheet("color: black;")
        customer_layout.addRow(customer_phone_label, self.customer_phone_value)
        
        self.receipt_layout.addWidget(customer_frame)
        
        # Service details
        self.receipt_layout.addSpacing(10)
        
        service_header_label = QtWidgets.QLabel("SERVICE DETAILS")
        service_header_label.setStyleSheet("color: black; font-size: 14px; font-weight: bold;")
        self.receipt_layout.addWidget(service_header_label)
        
        # Service table
        self.service_table = QtWidgets.QTableWidget()
        self.service_table.setColumnCount(3)
        self.service_table.setHorizontalHeaderLabels(["Service", "Price", "Quantity"])
        self.service_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #dddddd;
                border: 1px solid #dddddd;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: black;
                padding: 6px;
                border: 1px solid #dddddd;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        self.service_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.service_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.service_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.service_table.verticalHeader().setVisible(False)
        self.service_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.service_table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        
        self.receipt_layout.addWidget(self.service_table)
        
        # Products used
        self.products_header_label = QtWidgets.QLabel("PRODUCTS USED")
        self.products_header_label.setStyleSheet("color: black; font-size: 14px; font-weight: bold;")
        self.receipt_layout.addWidget(self.products_header_label)
        
        # Products table
        self.products_table = QtWidgets.QTableWidget()
        self.products_table.setColumnCount(3)
        self.products_table.setHorizontalHeaderLabels(["Product", "Quantity", "Price"])
        self.products_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: black;
                gridline-color: #dddddd;
                border: 1px solid #dddddd;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: black;
                padding: 6px;
                border: 1px solid #dddddd;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        self.products_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.products_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        self.products_table.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.products_table.verticalHeader().setVisible(False)
        self.products_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.products_table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        
        self.receipt_layout.addWidget(self.products_table)
        
        # Payment summary section
        payment_summary = QtWidgets.QFrame()
        payment_summary.setStyleSheet("background-color: #f5f5f5; border-radius: 4px; padding: 8px;")
        payment_layout = QtWidgets.QGridLayout(payment_summary)
        payment_layout.setColumnStretch(0, 1)
        payment_layout.setColumnStretch(1, 0)
        
        # Base price
        base_label = QtWidgets.QLabel("Base Price:")
        base_label.setStyleSheet("color: black; text-align: right;")
        base_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.base_price_value = QtWidgets.QLabel()
        self.base_price_value.setStyleSheet("color: black; font-weight: bold;")
        self.base_price_value.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        # Discount
        discount_label = QtWidgets.QLabel("Discount:")
        discount_label.setStyleSheet("color: black; text-align: right;")
        discount_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.discount_value = QtWidgets.QLabel()
        self.discount_value.setStyleSheet("color: #FF5252; font-weight: bold;")
        self.discount_value.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        # Total
        total_label = QtWidgets.QLabel("TOTAL:")
        total_label.setStyleSheet("color: black; font-size: 14px; font-weight: bold; text-align: right;")
        total_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.total_value = QtWidgets.QLabel()
        self.total_value.setStyleSheet("color: black; font-size: 14px; font-weight: bold;")
        self.total_value.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        # Payment method
        payment_method_label = QtWidgets.QLabel("Payment Method:")
        payment_method_label.setStyleSheet("color: black; text-align: right;")
        payment_method_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.payment_method_value = QtWidgets.QLabel()
        self.payment_method_value.setStyleSheet("color: black;")
        self.payment_method_value.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        
        payment_layout.addWidget(base_label, 0, 0)
        payment_layout.addWidget(self.base_price_value, 0, 1)
        payment_layout.addWidget(discount_label, 1, 0)
        payment_layout.addWidget(self.discount_value, 1, 1)
        
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setStyleSheet("background-color: black;")
        payment_layout.addWidget(line, 2, 0, 1, 2)
        
        payment_layout.addWidget(total_label, 3, 0)
        payment_layout.addWidget(self.total_value, 3, 1)
        payment_layout.addWidget(payment_method_label, 4, 0)
        payment_layout.addWidget(self.payment_method_value, 4, 1)
        
        self.receipt_layout.addWidget(payment_summary)
        
        # Thank you note
        self.receipt_layout.addSpacing(10)
        thank_you = QtWidgets.QLabel("Thank you for availing our service!")
        thank_you.setStyleSheet("color: black; font-weight: bold; text-align: center;")
        thank_you.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(thank_you)
        
        note = QtWidgets.QLabel("We appreciate your support.")
        note.setStyleSheet("color: black; text-align: center;")
        note.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(note)
        
        # Served by
        served_by_layout = QtWidgets.QHBoxLayout()
        served_by_layout.addStretch()
        
        served_by_label = QtWidgets.QLabel("Served by:")
        served_by_label.setStyleSheet("color: black;")
        served_by_layout.addWidget(served_by_label)
        
        self.served_by_value = QtWidgets.QLabel()
        self.served_by_value.setStyleSheet("color: black; font-weight: bold;")
        served_by_layout.addWidget(self.served_by_value)
        
        served_by_layout.addStretch()
        self.receipt_layout.addLayout(served_by_layout)
        
    def generateReceipt(self):
        """Generate the receipt with current invoice data"""
        data = self.parent.invoice_data
        service = data.get("service", {})
        customer = data.get("customer", {})
        payment = data.get("payment", {})
        
        # If there's no transaction ID yet, generate one
        if not data["transaction_id"]:
            data["transaction_id"] = f"TXN-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(10000, 99999)}"
        
        # Update receipt information
        current_datetime = datetime.datetime.now()
        
        self.or_value.setText(data["or_number"])
        self.date_value.setText(current_datetime.strftime("%Y-%m-%d"))
        self.time_value.setText(current_datetime.strftime("%H:%M:%S"))
        self.transaction_value.setText(data["transaction_id"])
        
        # Update customer information
        self.customer_name_value.setText(customer.get("name", ""))
        self.customer_phone_value.setText(customer.get("phone", ""))
        
        # Update service details
        if service:
            self.service_table.setRowCount(1)
            
            service_name_item = QtWidgets.QTableWidgetItem(service.get("service_name", ""))
            price_item = QtWidgets.QTableWidgetItem(f"₱{float(service.get('price', 0)):.2f}")
            quantity_item = QtWidgets.QTableWidgetItem("1")
            
            price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            quantity_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            
            self.service_table.setItem(0, 0, service_name_item)
            self.service_table.setItem(0, 1, price_item)
            self.service_table.setItem(0, 2, quantity_item)
            
            # Fetch and display products used for this service
            self.load_service_products(service['service_id'])
        
        # Update payment summary
        if service and payment:
            # Convert to the same type (float) for calculations
            base_price = float(service.get('price', 0))
            discount_percentage = float(payment.get('discount_percentage', 0))
            discount_amount = base_price * (discount_percentage / 100)
            final_price = float(payment.get('total_amount', base_price - discount_amount))
            
            self.base_price_value.setText(f"₱{base_price:.2f}")
            self.discount_value.setText(f"-₱{discount_amount:.2f}")
            self.total_value.setText(f"₱{final_price:.2f}")
            self.payment_method_value.setText(payment.get('method', 'Cash'))
        
        # Update staff information
        user_info = self.parent.user_info
        if user_info:
            self.served_by_value.setText(user_info.get('full_name', user_info.get('username', 'Staff')))
    
    def load_service_products(self, service_id):
        """Load products used for the selected service"""
        try:
            from app.utils.db_manager import DBManager
            import mysql.connector
            
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get products used in this service
            cursor.execute("""
                SELECT p.product_name, sp.quantity, p.price
                FROM service_products sp
                JOIN products p ON sp.product_id = p.product_id
                WHERE sp.service_id = %s
            """, (service_id,))
            
            products = cursor.fetchall()
            cursor.close()
            
            # Add products to the table
            if products:
                self.products_table.setRowCount(len(products))
                
                for i, product in enumerate(products):
                    name_item = QtWidgets.QTableWidgetItem(product['product_name'])
                    quantity_item = QtWidgets.QTableWidgetItem(str(product['quantity']))
                    price_item = QtWidgets.QTableWidgetItem(f"₱{float(product['price']):.2f}")
                    
                    quantity_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                    price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                    
                    self.products_table.setItem(i, 0, name_item)
                    self.products_table.setItem(i, 1, quantity_item)
                    self.products_table.setItem(i, 2, price_item)
                
                self.products_header_label.show()
                self.products_table.show()
            else:
                self.products_header_label.hide()
                self.products_table.hide()
                
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            self.products_header_label.hide()
            self.products_table.hide()
    
    def print_receipt(self):
        """Print the receipt"""
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        print_dialog = QtPrintSupport.QPrintDialog(printer, self)
        
        if print_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Create a painter to paint on the printer
            painter = QtGui.QPainter()
            painter.begin(printer)
            
            # Get the receipt widget's content
            screen = self.receipt_content.grab()
            
            # Scale the image to fit the printer's page
            page_rect = printer.pageRect()
            scale_factor = min(page_rect.width() / screen.width(), page_rect.height() / screen.height())
            
            # Calculate new dimensions
            new_width = int(screen.width() * scale_factor)
            new_height = int(screen.height() * scale_factor)
            
            # Calculate position to center the receipt
            x_position = int((page_rect.width() - new_width) / 2)
            y_position = int((page_rect.height() - new_height) / 2)
            
            # Draw the scaled image
            painter.drawImage(
                QtCore.QRect(x_position, y_position, new_width, new_height),
                screen.toImage()
            )
            
            painter.end()
            
            QtWidgets.QMessageBox.information(self, "Print Receipt", "Receipt printed successfully!")
    
    def save_as_pdf(self):
        """Save the receipt as a PDF file"""
        file_dialog = QtWidgets.QFileDialog()
        file_name, _ = file_dialog.getSaveFileName(
            self, 
            "Save Receipt as PDF", 
            f"Receipt_{self.parent.invoice_data['or_number']}.pdf", 
            "PDF Files (*.pdf)"
        )
        
        if file_name:
            # Create a PDF printer
            printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
            printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
            printer.setOutputFileName(file_name)
            
            # Create a painter to paint on the printer
            painter = QtGui.QPainter()
            painter.begin(printer)
            
            # Get the receipt widget's content
            screen = self.receipt_content.grab()
            
            # Scale the image to fit the printer's page
            page_rect = printer.pageRect()
            scale_factor = min(page_rect.width() / screen.width(), page_rect.height() / screen.height())
            
            # Calculate new dimensions
            new_width = int(screen.width() * scale_factor)
            new_height = int(screen.height() * scale_factor)
            
            # Calculate position to center the receipt
            x_position = int((page_rect.width() - new_width) / 2)
            y_position = int((page_rect.height() - new_height) / 2)
            
            # Draw the scaled image
            painter.drawImage(
                QtCore.QRect(x_position, y_position, new_width, new_height),
                screen.toImage()
            )
            
            painter.end()
            
            QtWidgets.QMessageBox.information(self, "Save PDF", "Receipt saved as PDF successfully!")
    
    def start_new_transaction(self):
        """Start a new transaction by resetting the invoice data"""
        # Confirm with the user
        reply = QtWidgets.QMessageBox.question(
            self,
            "New Transaction",
            "Are you sure you want to start a new transaction?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            # First save the transaction to database if needed
            self.save_transaction_to_db()
            
            # Reset the invoice data and all tabs
            self.parent.reset_invoice()
    
    def save_transaction_to_db(self):
        """Save the completed transaction to the database"""
        try:
            from app.utils.db_manager import DBManager
            import mysql.connector
            
            data = self.parent.invoice_data
            service = data.get("service", {})
            customer = data.get("customer", {})
            payment = data.get("payment", {})
            
            if not service or not customer or not payment or not data["or_number"]:
                return
            
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            # Calculate amounts - convert to float for consistent calculation
            base_amount = float(service.get('price', 0))
            discount_percentage = float(payment.get('discount_percentage', 0))
            discount_amount = base_amount * (discount_percentage / 100)
            total_amount = float(payment.get('total_amount', base_amount - discount_amount))
            
            # Get user ID
            user_id = None
            if self.parent.user_info:
                user_id = self.parent.user_info.get('user_id')
            
            # Insert transaction
            cursor.execute("""
                INSERT INTO transactions (
                    transaction_id, or_number, service_id, customer_name, customer_phone,
                    customer_gender, customer_city, payment_method, discount_percentage,
                    discount_amount, base_amount, total_amount, coupon_code, created_by
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                data["transaction_id"],
                data["or_number"],
                service.get("service_id"),
                customer.get("name"),
                customer.get("phone"),
                customer.get("gender"),
                customer.get("city"),
                payment.get("method"),
                discount_percentage,
                discount_amount,
                base_amount,
                total_amount,
                payment.get("coupon_code"),
                user_id
            ))
            
            conn.commit()
            cursor.close()
            
            print("Transaction saved successfully!")
            
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
            QtWidgets.QMessageBox.warning(self, "Database Error", f"Failed to save transaction: {err}")
    
    def exit_transaction(self):
        """Save the transaction and exit to main dashboard"""
        # First save the transaction to database if needed
        self.save_transaction_to_db()
        
        # Show confirmation to the user
        QtWidgets.QMessageBox.information(
            self,
            "Transaction Complete",
            "Transaction has been saved and completed successfully."
        )
        
        # Reset the invoice data
        self.parent.reset_invoice()
        
        # Signal to the main window to allow navigation again
        if hasattr(self.parent, 'parent') and self.parent.parent:
            # Notify the parent (main window) that the transaction is completed
            self.parent.invoice_completed = True
            if hasattr(self.parent.parent, 'enable_navigation'):
                self.parent.parent.enable_navigation()
    
    def reset(self):
        """Reset the tab state"""
        # Clear all the receipt information
        self.or_value.setText("")
        self.date_value.setText("")
        self.time_value.setText("")
        self.transaction_value.setText("")
        self.customer_name_value.setText("")
        self.customer_phone_value.setText("")
        self.service_table.setRowCount(0)
        self.products_table.setRowCount(0)
        self.base_price_value.setText("")
        self.discount_value.setText("")
        self.total_value.setText("")
        self.payment_method_value.setText("")
        self.served_by_value.setText("")