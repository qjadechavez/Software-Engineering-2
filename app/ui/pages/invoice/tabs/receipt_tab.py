from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from ..factories.panel_factory import PanelFactory
import datetime
import random

class ReceiptTab(QtWidgets.QWidget):
    """Tab for displaying and printing the final receipt"""
    
    def __init__(self, parent=None):
        super(ReceiptTab, self).__init__(parent)
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)
        
        # Header
        header_label = QtWidgets.QLabel("Transaction Receipt")
        header_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.layout.addWidget(header_label)
        
        desc_label = QtWidgets.QLabel("Transaction completed successfully:")
        desc_label.setStyleSheet("color: #cccccc; font-size: 14px;")
        self.layout.addWidget(desc_label)
        
        # Receipt content widget (fixed size for printing, no border)
        self.receipt_content = QtWidgets.QWidget()
        self.receipt_content.setStyleSheet("background-color: white;")
        self.receipt_content.setFixedSize(400, 600)  # Standard receipt size (approx. A6)
        self.receipt_layout = QtWidgets.QVBoxLayout(self.receipt_content)
        self.receipt_layout.setAlignment(QtCore.Qt.AlignTop)
        self.receipt_layout.setContentsMargins(20, 20, 20, 20)
        self.receipt_layout.setSpacing(5)
        
        # Setup receipt template
        self.setup_receipt_template()
        
        self.layout.addWidget(self.receipt_content, alignment=QtCore.Qt.AlignCenter)
        self.layout.addStretch()
        
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
        
        # Exit button
        exit_button = PanelFactory.create_action_button("Exit", primary=False)
        exit_button.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
        """)
        exit_button.clicked.connect(self.exit_transaction)
        button_layout.addWidget(exit_button)
        
        self.layout.addLayout(button_layout)
        
    def setup_receipt_template(self):
        """Set up a professional receipt template"""
        # HEADER SECTION
        company_name = QtWidgets.QLabel("Miere Beauty Lounge")
        company_name.setStyleSheet("color: #333333; font-size: 16px; font-weight: bold;")
        company_name.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(company_name)
        
        address = QtWidgets.QLabel("Rainbow St, Marikina City")
        address.setStyleSheet("color: #555555; font-size: 10px;")
        address.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(address)
        
        contact_details = QtWidgets.QLabel("0962 915 5277 | miere.beautylounge@gmail.com")
        contact_details.setStyleSheet("color: #555555; font-size: 10px;")
        contact_details.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(contact_details)
        
        # Space instead of divider
        self.receipt_layout.addSpacing(10)
        
        receipt_title = QtWidgets.QLabel("OFFICIAL RECEIPT")
        receipt_title.setStyleSheet("color: #333333; font-size: 12px; font-weight: bold;")
        receipt_title.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(receipt_title)
        
        # TRANSACTION DETAILS
        transaction_widget = QtWidgets.QWidget()
        transaction_layout = QtWidgets.QGridLayout(transaction_widget)
        transaction_layout.setContentsMargins(0, 5, 0, 5)
        transaction_layout.setSpacing(5)
        
        receipt_label = QtWidgets.QLabel("Receipt No:")
        receipt_label.setStyleSheet("color: #333333; font-size: 10px; font-weight: bold;")
        self.or_value = QtWidgets.QLabel()
        self.or_value.setStyleSheet("color: #333333; font-size: 10px;")
        
        date_label = QtWidgets.QLabel("Date/Time:")
        date_label.setStyleSheet("color: #333333; font-size: 10px; font-weight: bold;")
        self.date_time_value = QtWidgets.QLabel()
        self.date_time_value.setStyleSheet("color: #333333; font-size: 10px;")
        
        txn_label = QtWidgets.QLabel("Transaction ID:")
        txn_label.setStyleSheet("color: #333333; font-size: 10px; font-weight: bold;")
        self.transaction_value = QtWidgets.QLabel()
        self.transaction_value.setStyleSheet("color: #333333; font-size: 10px;")
        
        transaction_layout.addWidget(receipt_label, 0, 0)
        transaction_layout.addWidget(self.or_value, 0, 1)
        transaction_layout.addWidget(date_label, 1, 0)
        transaction_layout.addWidget(self.date_time_value, 1, 1)
        transaction_layout.addWidget(txn_label, 2, 0)
        transaction_layout.addWidget(self.transaction_value, 2, 1)
        
        self.receipt_layout.addWidget(transaction_widget)
        
        # CUSTOMER DETAILS
        customer_widget = QtWidgets.QWidget()
        customer_layout = QtWidgets.QGridLayout(customer_widget)
        customer_layout.setContentsMargins(0, 5, 0, 5)
        customer_layout.setSpacing(5)
        
        customer_label = QtWidgets.QLabel("Customer:")
        customer_label.setStyleSheet("color: #333333; font-size: 10px; font-weight: bold;")
        self.customer_name_value = QtWidgets.QLabel()
        self.customer_name_value.setStyleSheet("color: #333333; font-size: 10px;")
        
        phone_label = QtWidgets.QLabel("Phone:")
        phone_label.setStyleSheet("color: #333333; font-size: 10px; font-weight: bold;")
        self.customer_phone_value = QtWidgets.QLabel()
        self.customer_phone_value.setStyleSheet("color: #333333; font-size: 10px;")
        
        customer_layout.addWidget(customer_label, 0, 0)
        customer_layout.addWidget(self.customer_name_value, 0, 1)
        customer_layout.addWidget(phone_label, 1, 0)
        customer_layout.addWidget(self.customer_phone_value, 1, 1)
        
        self.receipt_layout.addWidget(customer_widget)
        
        # Space instead of divider
        self.receipt_layout.addSpacing(10)
        
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
        
        self.receipt_layout.addWidget(items_header)
        
        # SERVICE TABLE
        self.service_table = QtWidgets.QTableWidget()
        self.service_table.setColumnCount(3)
        self.service_table.setStyleSheet("""
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
        self.service_table.horizontalHeader().setVisible(False)
        self.service_table.verticalHeader().setVisible(False)
        self.service_table.setShowGrid(False)
        self.service_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.service_table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        self.service_table.setColumnWidth(0, 240)
        self.service_table.setColumnWidth(1, 40)
        self.service_table.setColumnWidth(2, 80)
        self.service_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.receipt_layout.addWidget(self.service_table)
        
        # PRODUCTS TABLE
        self.products_header_label = QtWidgets.QLabel("Products Used:")
        self.products_header_label.setStyleSheet("color: #555555; font-size: 10px; font-weight: bold;")
        self.receipt_layout.addWidget(self.products_header_label)
        
        self.products_table = QtWidgets.QTableWidget()
        self.products_table.setColumnCount(3)
        self.products_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                font-size: 10px;
                color: #555555;
            }
            QTableWidget::item {
                padding: 2px;
            }
        """)
        self.products_table.horizontalHeader().setVisible(False)
        self.products_table.verticalHeader().setVisible(False)
        self.products_table.setShowGrid(False)
        self.products_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.products_table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        self.products_table.setColumnWidth(0, 240)
        self.products_table.setColumnWidth(1, 40)
        self.products_table.setColumnWidth(2, 80)
        self.products_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.receipt_layout.addWidget(self.products_table)
        
        # Space instead of divider
        self.receipt_layout.addSpacing(10)
        
        # PAYMENT SUMMARY
        summary_widget = QtWidgets.QWidget()
        summary_layout = QtWidgets.QGridLayout(summary_widget)
        summary_layout.setContentsMargins(0, 5, 0, 5)
        summary_layout.setSpacing(5)
        
        subtotal_label = QtWidgets.QLabel("Subtotal:")
        subtotal_label.setStyleSheet("color: #333333; font-size: 10px;")
        self.base_price_value = QtWidgets.QLabel()
        self.base_price_value.setStyleSheet("color: #333333; font-size: 10px;")
        self.base_price_value.setAlignment(QtCore.Qt.AlignRight)
        
        discount_label = QtWidgets.QLabel("Discount:")
        discount_label.setStyleSheet("color: #333333; font-size: 10px;")
        self.discount_value = QtWidgets.QLabel()
        self.discount_value.setStyleSheet("color: #333333; font-size: 10px;")
        self.discount_value.setAlignment(QtCore.Qt.AlignRight)
        
        total_label = QtWidgets.QLabel("Total:")
        total_label.setStyleSheet("color: #333333; font-size: 12px; font-weight: bold;")
        self.total_amount_value = QtWidgets.QLabel()
        self.total_amount_value.setStyleSheet("color: #333333; font-size: 12px; font-weight: bold;")
        self.total_amount_value.setAlignment(QtCore.Qt.AlignRight)
        
        payment_label = QtWidgets.QLabel("Payment Method:")
        payment_label.setStyleSheet("color: #333333; font-size: 10px;")
        self.payment_method_value = QtWidgets.QLabel()
        self.payment_method_value.setStyleSheet("color: #333333; font-size: 10px;")
        self.payment_method_value.setAlignment(QtCore.Qt.AlignRight)
        
        summary_layout.addWidget(subtotal_label, 0, 0)
        summary_layout.addWidget(self.base_price_value, 0, 1)
        summary_layout.addWidget(discount_label, 1, 0)
        summary_layout.addWidget(self.discount_value, 1, 1)
        summary_layout.addWidget(total_label, 2, 0)
        summary_layout.addWidget(self.total_amount_value, 2, 1)
        summary_layout.addWidget(payment_label, 3, 0)
        summary_layout.addWidget(self.payment_method_value, 3, 1)
        
        self.receipt_layout.addWidget(summary_widget)
        
        # Space instead of divider
        self.receipt_layout.addSpacing(10)
        
        # FOOTER
        footer_widget = QtWidgets.QWidget()
        footer_layout = QtWidgets.QGridLayout(footer_widget)
        footer_layout.setContentsMargins(0, 5, 0, 5)
        footer_layout.setSpacing(5)
        
        thank_you = QtWidgets.QLabel("Thank you for your business!")
        thank_you.setStyleSheet("color: #333333; font-size: 10px; font-weight: bold;")
        staff_label = QtWidgets.QLabel("Served by:")
        staff_label.setStyleSheet("color: #333333; font-size: 10px;")
        self.served_by_value = QtWidgets.QLabel()
        self.served_by_value.setStyleSheet("color: #333333; font-size: 10px; font-weight: bold;")
        
        footer_layout.addWidget(thank_you, 0, 0, 1, 2)
        footer_layout.addWidget(staff_label, 1, 0)
        footer_layout.addWidget(self.served_by_value, 1, 1)
        
        self.receipt_layout.addWidget(footer_widget)
        
        policy = QtWidgets.QLabel("No returns or exchanges on services")
        policy.setStyleSheet("color: #555555; font-size: 9px; font-style: italic;")
        policy.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(policy)
        self.receipt_layout.addStretch()
    
    def generateReceipt(self):
        """Generate the receipt with current invoice data"""
        data = self.parent.invoice_data
        service = data.get("service", {})
        customer = data.get("customer", {})
        payment = data.get("payment", {})
        
        # Generate transaction ID if not present
        if not data.get("transaction_id"):
            data["transaction_id"] = f"TXN-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(10000, 99999)}"
        
        # Update receipt information
        current_datetime = datetime.datetime.now()
        self.or_value.setText(data.get("or_number", ""))
        self.date_time_value.setText(current_datetime.strftime('%m/%d/%Y %H:%M'))
        self.transaction_value.setText(data.get("transaction_id", ""))
        
        # Update customer information
        self.customer_name_value.setText(customer.get("name", ""))
        self.customer_phone_value.setText(customer.get("phone", ""))
        
        # Update service details
        self.service_table.setRowCount(0)
        if service and service.get("service_name") and service.get("price"):
            self.service_table.setRowCount(1)
            service_name_item = QtWidgets.QTableWidgetItem(service.get("service_name"))
            quantity_item = QtWidgets.QTableWidgetItem("1")
            price_item = QtWidgets.QTableWidgetItem(f"₱{float(service.get('price')):.2f}")
            
            service_name_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            quantity_item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
            price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
            
            self.service_table.setItem(0, 0, service_name_item)
            self.service_table.setItem(0, 1, quantity_item)
            self.service_table.setItem(0, 2, price_item)
            self.service_table.setRowHeight(0, 20)
        
        # Update products
        self.products_table.setRowCount(0)
        service_id = service.get("service_id")
        if service_id:
            try:
                from app.utils.db_manager import DBManager
                conn = DBManager.get_connection()
                cursor = conn.cursor(dictionary=True)
                
                query = """
                    SELECT p.product_name, sp.quantity, p.price
                    FROM service_products sp
                    JOIN products p ON sp.product_id = p.product_id
                    WHERE sp.service_id = %s
                """
                cursor.execute(query, (service_id,))
                products = cursor.fetchall()
                cursor.close()
                
                if products:
                    self.products_table.setRowCount(len(products))
                    self.products_header_label.show()
                    self.products_table.show()
                    for i, product in enumerate(products):
                        name_item = QtWidgets.QTableWidgetItem(f"  {product['product_name']}")
                        quantity_item = QtWidgets.QTableWidgetItem(str(product['quantity']))
                        price_item = QtWidgets.QTableWidgetItem(f"₱{float(product['price']):.2f}")
                        
                        name_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        quantity_item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                        price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                        
                        self.products_table.setItem(i, 0, name_item)
                        self.products_table.setItem(i, 1, quantity_item)
                        self.products_table.setItem(i, 2, price_item)
                        self.products_table.setRowHeight(i, 20)
                else:
                    self.products_header_label.hide()
                    self.products_table.hide()
            except Exception as e:
                print(f"Error loading products: {str(e)}")
                self.products_header_label.hide()
                self.products_table.hide()
        else:
            self.products_header_label.hide()
            self.products_table.hide()
        
        # Update payment summary
        if service and payment:
            try:
                base_price = float(service.get('price', 0))
                discount_percentage = float(payment.get('discount_percentage', 0))
                discount_amount = base_price * (discount_percentage / 100)
                final_price = float(payment.get('total_amount', base_price - discount_amount))
                
                self.base_price_value.setText(f"₱{base_price:.2f}")
                self.discount_value.setText(f"-₱{discount_amount:.2f}")
                self.total_amount_value.setText(f"₱{final_price:.2f}")
                self.payment_method_value.setText(payment.get('method', 'Cash'))
            except (ValueError, TypeError) as e:
                print(f"Error calculating payment values: {e}")
        
        # Update staff information
        self.served_by_value.setText(
            self.parent.user_info.get('full_name', self.parent.user_info.get('username', 'Staff'))
            if hasattr(self.parent, 'user_info') and self.parent.user_info else "Staff"
        )
    
    def print_receipt(self):
        """Print the receipt"""
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
        printer.setPageSize(QtPrintSupport.QPrinter.A6)
        print_dialog = QtPrintSupport.QPrintDialog(printer, self)
        
        if print_dialog.exec_() == QtWidgets.QDialog.Accepted:
            painter = QtGui.QPainter(printer)
            rect = painter.viewport()
            size = self.receipt_content.size()
            scale = min(rect.width() / size.width(), rect.height() / size.height())
            painter.scale(scale, scale)
            self.receipt_content.render(painter)
            painter.end()
            QtWidgets.QMessageBox.information(self, "Print Receipt", "Receipt printed successfully!")
    
    def save_as_pdf(self):
        """Save the receipt as a PDF file"""
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, 
            "Save Receipt as PDF", 
            f"Receipt_{self.parent.invoice_data.get('or_number', '')}.pdf", 
            "PDF Files (*.pdf)"
        )
        
        if file_name:
            printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
            printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
            printer.setOutputFileName(file_name)
            printer.setPageSize(QtPrintSupport.QPrinter.A6)
            
            painter = QtGui.QPainter(printer)
            rect = painter.viewport()
            size = self.receipt_content.size()
            scale = min(rect.width() / size.width(), rect.height() / size.height())
            painter.scale(scale, scale)
            self.receipt_content.render(painter)
            painter.end()
            QtWidgets.QMessageBox.information(self, "Save PDF", "Receipt saved as PDF successfully!")
    
    def start_new_transaction(self):
        """Start a new transaction by resetting the invoice data"""
        reply = QtWidgets.QMessageBox.question(
            self,
            "New Transaction",
            "Are you sure you want to start a new transaction?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            self.save_transaction_to_db()
            self.parent.reset_invoice()
    
    def save_transaction_to_db(self):
        """Save the completed transaction to the database"""
        try:
            from app.utils.db_manager import DBManager
            data = self.parent.invoice_data
            service = data.get("service", {})
            customer = data.get("customer", {})
            payment = data.get("payment", {})
            
            if not all([service, customer, payment, data.get("or_number")]):
                return
            
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            base_amount = float(service.get('price', 0))
            discount_percentage = float(payment.get('discount_percentage', 0))
            discount_amount = base_amount * (discount_percentage / 100)
            total_amount = float(payment.get('total_amount', base_amount - discount_amount))
            
            user_id = self.parent.user_info.get('user_id') if hasattr(self.parent, 'user_info') and self.parent.user_info else None
            
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
        except Exception as e:
            print(f"Database error: {e}")
            QtWidgets.QMessageBox.warning(self, "Database Error", f"Failed to save transaction: {e}")
    
    def exit_transaction(self):
        """Save the transaction and exit to main dashboard"""
        self.save_transaction_to_db()
        QtWidgets.QMessageBox.information(
            self,
            "Transaction Complete",
            "Transaction has been saved and completed successfully."
        )
        self.parent.reset_invoice()
        if hasattr(self.parent, 'parent') and self.parent.parent:
            self.parent.invoice_completed = True
            if hasattr(self.parent.parent, 'enable_navigation'):
                self.parent.parent.enable_navigation()
    
    def reset(self):
        """Reset the tab state"""
        self.or_value.setText("")
        self.date_time_value.setText("")
        self.transaction_value.setText("")
        self.customer_name_value.setText("")
        self.customer_phone_value.setText("")
        self.service_table.setRowCount(0)
        self.products_table.setRowCount(0)
        self.base_price_value.setText("")
        self.discount_value.setText("")
        self.total_amount_value.setText("")
        self.payment_method_value.setText("")
        self.served_by_value.setText("")
    
    def showEvent(self, event):
        """Called when the tab is shown"""
        super().showEvent(event)
        self.generateReceipt()