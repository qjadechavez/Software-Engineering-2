from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from ..control_panel_factory import ControlPanelFactory
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
        self.layout.setContentsMargins(15, 15, 15, 15)  # Reduced from 20, 20, 20, 20
        self.layout.setSpacing(10)  # Reduced from 15
        
        # Header
        header_label = QtWidgets.QLabel("Transaction Receipt")
        header_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")  # Reduced from 20px
        self.layout.addWidget(header_label)
        
        desc_label = QtWidgets.QLabel("Transaction completed successfully:")
        desc_label.setStyleSheet("color: #cccccc; font-size: 12px;")  # Reduced from 14px
        self.layout.addWidget(desc_label)
        
        # Receipt content widget (fixed size for printing, no border)
        self.receipt_content = QtWidgets.QWidget()
        self.receipt_content.setStyleSheet("background-color: white;")
        self.receipt_content.setFixedSize(400, 650)  # Increased height from 600 to 650
        self.receipt_layout = QtWidgets.QVBoxLayout(self.receipt_content)
        self.receipt_layout.setAlignment(QtCore.Qt.AlignTop)
        self.receipt_layout.setContentsMargins(15, 15, 15, 15)  # Reduced from 20, 20, 20, 20
        self.receipt_layout.setSpacing(3)  # Reduced from 5
        
        # Setup receipt template
        self.setup_receipt_template()
        
        self.layout.addWidget(self.receipt_content, alignment=QtCore.Qt.AlignCenter)
        
        # Add stretch to push buttons to bottom
        self.layout.addStretch()
        
        # Action buttons at the bottom
        button_layout = QtWidgets.QHBoxLayout()
        
        # Print button
        print_button = ControlPanelFactory.create_action_button("Print Receipt")
        print_button.clicked.connect(self.print_receipt)
        button_layout.addWidget(print_button)
        
        # Save as PDF button
        save_pdf_button = ControlPanelFactory.create_action_button("Save as PDF")
        save_pdf_button.clicked.connect(self.save_as_pdf)
        button_layout.addWidget(save_pdf_button)
        
        button_layout.addStretch()
        
        # New transaction button
        new_transaction_button = ControlPanelFactory.create_action_button("New Transaction", primary=False)
        new_transaction_button.clicked.connect(self.start_new_transaction)
        button_layout.addWidget(new_transaction_button)
        
        # Exit button
        from ..style_factory import StyleFactory
        exit_button = ControlPanelFactory.create_action_button("Exit", primary=False)
        exit_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
        exit_button.clicked.connect(self.exit_transaction)
        button_layout.addWidget(exit_button)
        
        self.layout.addLayout(button_layout)
        
    def setup_receipt_template(self):
        """Set up a professional receipt template"""
        # HEADER SECTION
        company_name = QtWidgets.QLabel("Miere Beauty Lounge")
        company_name.setStyleSheet("color: #333333; font-size: 14px; font-weight: bold;")  # Reduced from 16px
        company_name.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(company_name)
        
        address = QtWidgets.QLabel("Rainbow St, Marikina City")
        address.setStyleSheet("color: #555555; font-size: 9px;")  # Reduced from 10px
        address.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(address)
        
        contact_details = QtWidgets.QLabel("0962 915 5277 | miere.beautylounge@gmail.com")
        contact_details.setStyleSheet("color: #555555; font-size: 9px;")  # Reduced from 10px
        contact_details.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(contact_details)
        
        # Space instead of divider
        self.receipt_layout.addSpacing(6)  # Reduced from 10
        
        receipt_title = QtWidgets.QLabel("OFFICIAL RECEIPT")
        receipt_title.setStyleSheet("color: #333333; font-size: 11px; font-weight: bold;")  # Reduced from 12px
        receipt_title.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(receipt_title)
        
        # TRANSACTION DETAILS
        transaction_widget = QtWidgets.QWidget()
        transaction_layout = QtWidgets.QGridLayout(transaction_widget)
        transaction_layout.setContentsMargins(0, 3, 0, 3)  # Reduced from 0, 5, 0, 5
        transaction_layout.setSpacing(3)  # Reduced from 5
        
        receipt_label = QtWidgets.QLabel("Receipt No:")
        receipt_label.setStyleSheet("color: #333333; font-size: 9px; font-weight: bold;")  # Reduced from 10px
        self.or_value = QtWidgets.QLabel()
        self.or_value.setStyleSheet("color: #333333; font-size: 9px;")  # Reduced from 10px
        
        date_label = QtWidgets.QLabel("Date/Time:")
        date_label.setStyleSheet("color: #333333; font-size: 9px; font-weight: bold;")  # Reduced from 10px
        self.date_time_value = QtWidgets.QLabel()
        self.date_time_value.setStyleSheet("color: #333333; font-size: 9px;")  # Reduced from 10px
        
        txn_label = QtWidgets.QLabel("Transaction ID:")
        txn_label.setStyleSheet("color: #333333; font-size: 9px; font-weight: bold;")  # Reduced from 10px
        self.transaction_value = QtWidgets.QLabel()
        self.transaction_value.setStyleSheet("color: #333333; font-size: 9px;")  # Reduced from 10px
        
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
        customer_layout.setContentsMargins(0, 3, 0, 3)  # Reduced from 0, 5, 0, 5
        customer_layout.setSpacing(3)  # Reduced from 5
        
        customer_label = QtWidgets.QLabel("Customer:")
        customer_label.setStyleSheet("color: #333333; font-size: 9px; font-weight: bold;")  # Reduced from 10px
        self.customer_name_value = QtWidgets.QLabel()
        self.customer_name_value.setStyleSheet("color: #333333; font-size: 9px;")  # Reduced from 10px
        
        phone_label = QtWidgets.QLabel("Phone:")
        phone_label.setStyleSheet("color: #333333; font-size: 9px; font-weight: bold;")  # Reduced from 10px
        self.customer_phone_value = QtWidgets.QLabel()
        self.customer_phone_value.setStyleSheet("color: #333333; font-size: 9px;")  # Reduced from 10px
        
        customer_layout.addWidget(customer_label, 0, 0)
        customer_layout.addWidget(self.customer_name_value, 0, 1)
        customer_layout.addWidget(phone_label, 1, 0)
        customer_layout.addWidget(self.customer_phone_value, 1, 1)
        
        self.receipt_layout.addWidget(customer_widget)
        
        # Space instead of divider
        self.receipt_layout.addSpacing(6)  # Reduced from 10
        
        # ITEMS SECTION HEADER
        items_header = QtWidgets.QWidget()
        items_header_layout = QtWidgets.QHBoxLayout(items_header)
        items_header_layout.setContentsMargins(0, 3, 0, 3)  # Reduced from 0, 5, 0, 5
        items_header_layout.setSpacing(0)
        
        desc_header = QtWidgets.QLabel("Description")
        desc_header.setStyleSheet("color: #333333; font-size: 9px; font-weight: bold;")  # Reduced from 10px
        qty_header = QtWidgets.QLabel("Qty")
        qty_header.setStyleSheet("color: #333333; font-size: 9px; font-weight: bold;")  # Reduced from 10px
        qty_header.setAlignment(QtCore.Qt.AlignCenter)
        price_header = QtWidgets.QLabel("Amount")
        price_header.setStyleSheet("color: #333333; font-size: 9px; font-weight: bold;")  # Reduced from 10px
        price_header.setAlignment(QtCore.Qt.AlignRight)
        
        items_header_layout.addWidget(desc_header, 6)
        items_header_layout.addWidget(qty_header, 1)
        items_header_layout.addWidget(price_header, 3)
        
        self.receipt_layout.addWidget(items_header)
        
        # SERVICES TABLE
        self.service_table = QtWidgets.QTableWidget()
        self.service_table.setColumnCount(3)
        self.service_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                font-size: 9px;
                color: #333333;
            }
            QTableWidget::item {
                padding: 1px;
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
        self.products_header_label.setStyleSheet("color: #555555; font-size: 9px; font-weight: bold;")  # Reduced from 10px
        self.receipt_layout.addWidget(self.products_header_label)
        
        self.products_table = QtWidgets.QTableWidget()
        self.products_table.setColumnCount(3)
        self.products_table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                font-size: 8px;
                color: #555555;
            }
            QTableWidget::item {
                padding: 1px;
            }
        """)
        self.products_table.horizontalHeader().setVisible(False)
        self.products_table.verticalHeader().setVisible(False)
        self.products_table.setShowGrid(False)
        self.products_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.products_table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        self.products_table.setColumnWidth(0, 240)
        self.products_table.setColumnWidth(1, 40)
        self.products_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.receipt_layout.addWidget(self.products_table)
        
        # Space instead of divider
        self.receipt_layout.addSpacing(4)  # Reduced from 10
        
        # NOTES SECTION - New addition
        self.notes_widget = QtWidgets.QWidget()
        notes_layout = QtWidgets.QVBoxLayout(self.notes_widget)
        notes_layout.setContentsMargins(0, 2, 0, 2)  # Reduced from 0, 5, 0, 5
        notes_layout.setSpacing(2)  # Reduced from 5
        
        notes_header = QtWidgets.QLabel("Service Notes:")
        notes_header.setStyleSheet("color: #333333; font-size: 9px; font-weight: bold;")  # Reduced from 10px
        notes_layout.addWidget(notes_header)
        
        self.notes_value = QtWidgets.QLabel()
        self.notes_value.setStyleSheet("color: #333333; font-size: 8px; font-style: italic;")  # Reduced from 9px
        self.notes_value.setWordWrap(True)
        self.notes_value.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        notes_layout.addWidget(self.notes_value)
        
        self.receipt_layout.addWidget(self.notes_widget)
        
        # Space instead of divider
        self.receipt_layout.addSpacing(4)  # Reduced from 10
        
        # PAYMENT SUMMARY
        summary_widget = QtWidgets.QWidget()
        summary_layout = QtWidgets.QGridLayout(summary_widget)
        summary_layout.setContentsMargins(0, 3, 0, 3)  # Reduced from 0, 5, 0, 5
        summary_layout.setSpacing(2)  # Reduced from 5
        
        subtotal_label = QtWidgets.QLabel("Subtotal:")
        subtotal_label.setStyleSheet("color: #333333; font-size: 9px;")  # Reduced from 10px
        self.base_price_value = QtWidgets.QLabel()
        self.base_price_value.setStyleSheet("color: #333333; font-size: 9px;")  # Reduced from 10px
        self.base_price_value.setAlignment(QtCore.Qt.AlignRight)
        
        discount_label = QtWidgets.QLabel("Discount:")
        discount_label.setStyleSheet("color: #333333; font-size: 9px;")  # Reduced from 10px
        self.discount_value = QtWidgets.QLabel()
        self.discount_value.setStyleSheet("color: #333333; font-size: 9px;")  # Reduced from 10px
        self.discount_value.setAlignment(QtCore.Qt.AlignRight)
        
        total_label = QtWidgets.QLabel("Total:")
        total_label.setStyleSheet("color: #333333; font-size: 10px; font-weight: bold;")  # Reduced from 12px
        self.total_amount_value = QtWidgets.QLabel()
        self.total_amount_value.setStyleSheet("color: #333333; font-size: 10px; font-weight: bold;")  # Reduced from 12px
        self.total_amount_value.setAlignment(QtCore.Qt.AlignRight)
        
        payment_label = QtWidgets.QLabel("Payment Method:")
        payment_label.setStyleSheet("color: #333333; font-size: 9px;")  # Reduced from 10px
        self.payment_method_value = QtWidgets.QLabel()
        self.payment_method_value.setStyleSheet("color: #333333; font-size: 9px;")  # Reduced from 10px
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
        self.receipt_layout.addSpacing(4)  # Reduced from 10
        
        # FOOTER
        footer_widget = QtWidgets.QWidget()
        footer_layout = QtWidgets.QGridLayout(footer_widget)
        footer_layout.setContentsMargins(0, 2, 0, 2)  # Reduced from 0, 5, 0, 5
        footer_layout.setSpacing(2)  # Reduced from 5
        
        thank_you = QtWidgets.QLabel("Thank you for your business!")
        thank_you.setStyleSheet("color: #333333; font-size: 9px; font-weight: bold;")  # Reduced from 10px
        staff_label = QtWidgets.QLabel("Served by:")
        staff_label.setStyleSheet("color: #333333; font-size: 8px;")  # Reduced from 10px
        self.served_by_value = QtWidgets.QLabel()
        self.served_by_value.setStyleSheet("color: #333333; font-size: 8px; font-weight: bold;")  # Reduced from 10px
        
        footer_layout.addWidget(thank_you, 0, 0, 1, 2)
        footer_layout.addWidget(staff_label, 1, 0)
        footer_layout.addWidget(self.served_by_value, 1, 1)
        
        self.receipt_layout.addWidget(footer_widget)
        
        policy = QtWidgets.QLabel("No returns or exchanges on services")
        policy.setStyleSheet("color: #555555; font-size: 8px; font-style: italic;")  # Reduced from 9px
        policy.setAlignment(QtCore.Qt.AlignCenter)
        self.receipt_layout.addWidget(policy)
        self.receipt_layout.addStretch()
    
    def generateReceipt(self):
        """Generate the receipt with current invoice data"""
        data = self.parent.invoice_data
        services = data.get("services", [])
        customer = data.get("customer", {})
        payment = data.get("payment", {})
        notes = data.get("notes", "")
        
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
        if services:
            self.service_table.setRowCount(len(services))
            for i, service in enumerate(services):
                service_name_item = QtWidgets.QTableWidgetItem(service.get("service_name", ""))
                quantity_item = QtWidgets.QTableWidgetItem("1")
                price_item = QtWidgets.QTableWidgetItem(f"₱{float(service.get('price', 0)):.2f}")
                
                service_name_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                quantity_item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                
                self.service_table.setItem(i, 0, service_name_item)
                self.service_table.setItem(i, 1, quantity_item)
                self.service_table.setItem(i, 2, price_item)
                self.service_table.setRowHeight(i, 16)  # Reduced from 20
        
        # Update notes section
        if notes and notes.strip():
            self.notes_value.setText(notes.strip())
            self.notes_widget.show()
        else:
            self.notes_widget.hide()
        
        # Update products
        self.products_table.setRowCount(0)
        service_ids = [service.get("service_id") for service in services if service.get("service_id")]
        if service_ids:
            try:
                from app.utils.db_manager import DBManager
                conn = DBManager.get_connection()
                cursor = conn.cursor(dictionary=True)
                
                query = """
                    SELECT p.product_name, sp.quantity, p.price
                    FROM service_products sp
                    JOIN products p ON sp.product_id = p.product_id
                    WHERE sp.service_id IN (%s)
                """ % ','.join(['%s'] * len(service_ids))
                cursor.execute(query, tuple(service_ids))
                products = cursor.fetchall()
                cursor.close()
                
                if products:
                    self.products_table.setRowCount(len(products))
                    self.products_header_label.show()
                    self.products_table.show()
                    for i, product in enumerate(products):
                        name_item = QtWidgets.QTableWidgetItem(f"  {product['product_name']}")
                        quantity_item = QtWidgets.QTableWidgetItem(str(product['quantity']))
                        
                        name_item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                        quantity_item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                        
                        self.products_table.setItem(i, 0, name_item)
                        self.products_table.setItem(i, 1, quantity_item)
                        self.products_table.setRowHeight(i, 14)  # Reduced from 20
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
        if services and payment:
            try:
                base_price = sum(float(service.get('price', 0)) for service in services)
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
        """Save the completed transaction to the database and update inventory"""
        try:
            from app.utils.db_manager import DBManager
            data = self.parent.invoice_data
            services = data.get("services", [])
            customer = data.get("customer", {})
            payment = data.get("payment", {})
            notes = data.get("notes", "")  # Get notes
            
            if not all([services, customer, payment, data.get("or_number")]):
                return
            
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            base_amount = sum(float(service.get('price', 0)) for service in services)
            discount_percentage = float(payment.get('discount_percentage', 0))
            discount_amount = base_amount * (discount_percentage / 100)
            total_amount = float(payment.get('total_amount', base_amount - discount_amount))
            
            user_id = self.parent.user_info.get('user_id') if hasattr(self.parent, 'user_info') and self.parent.user_info else None
            
            # Insert transaction
            cursor.execute("""
                INSERT INTO transactions (
                    transaction_id, or_number, service_id, customer_name, customer_phone,
                    customer_gender, customer_city, payment_method, discount_percentage,
                    discount_amount, base_amount, total_amount, coupon_code, notes, created_by
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                data["transaction_id"],
                data["or_number"],
                services[0].get("service_id"),  # Assuming first service for transaction
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
                notes,  # Add notes to database
                user_id
            ))
            
            # Deduct inventory for products used in services
            service_ids = [service.get("service_id") for service in services if service.get("service_id")]
            if service_ids:
                # Get all products used in the services
                cursor_dict = conn.cursor(dictionary=True)
                query = """
                    SELECT sp.product_id, sp.quantity, p.product_name, p.quantity as current_stock
                    FROM service_products sp
                    JOIN products p ON sp.product_id = p.product_id
                    WHERE sp.service_id IN (%s)
                """ % ','.join(['%s'] * len(service_ids))
                cursor_dict.execute(query, tuple(service_ids))
                products_to_deduct = cursor_dict.fetchall()
                cursor_dict.close()
                
                # Update inventory for each product
                for product in products_to_deduct:
                    new_quantity = max(0, product['current_stock'] - product['quantity'])
                    
                    # Update product quantity
                    cursor.execute("""
                        UPDATE products 
                        SET quantity = %s, 
                            availability = CASE WHEN %s <= 0 THEN 0 ELSE 1 END
                        WHERE product_id = %s
                    """, (new_quantity, new_quantity, product['product_id']))
                    
                    # Update inventory table
                    cursor.execute("""
                        INSERT INTO inventory (product_id, quantity, status, last_updated) 
                        VALUES (%s, %s, %s, NOW())
                        ON DUPLICATE KEY UPDATE 
                        quantity = VALUES(quantity),
                        status = VALUES(status),
                        last_updated = NOW()
                    """, (product['product_id'], new_quantity, "Used in Service"))
                    
                    print(f"Deducted {product['quantity']} units of {product['product_name']} from inventory")
            
            conn.commit()
            cursor.close()
            
            # Refresh inventory display if parent has inventory page reference
            self.refresh_inventory_display()
            
            # Refresh customers table if parent has customers page reference
            self.refresh_customers_display()
            
        except Exception as e:
            print(f"Database error: {e}")
            QtWidgets.QMessageBox.warning(self, "Database Error", f"Failed to save transaction: {e}")
    
    def refresh_inventory_display(self):
        """Refresh inventory displays across the application"""
        try:
            # Get main window reference
            main_window = self.parent
            while main_window and not hasattr(main_window, 'page_manager'):
                main_window = getattr(main_window, 'parent', None)
            
            if main_window and hasattr(main_window, 'page_manager'):
                # Find inventory page and refresh products tab
                for page_name, page_info in main_window.page_manager.pages.items():
                    if 'inventory' in page_name.lower() and hasattr(page_info, 'page') and page_info.page:
                        inventory_page = page_info.page
                        if hasattr(inventory_page, 'products_tab'):
                            inventory_page.products_tab.load_products(preserve_filter=True)
                            print("Refreshed inventory products display")
                        if hasattr(inventory_page, 'inventory_status_tab'):
                            inventory_page.inventory_status_tab.load_inventory_status()
                            print("Refreshed inventory status display")
                        break
        except Exception as e:
            print(f"Error refreshing inventory display: {e}")
    
    def refresh_customers_display(self):
        """Refresh customers table across the application"""
        try:
            # Get main window reference
            main_window = self.parent
            while main_window and not hasattr(main_window, 'page_manager'):
                main_window = getattr(main_window, 'parent', None)
            
            if main_window and hasattr(main_window, 'page_manager'):
                # Find customers page and refresh table
                for page_name, page_info in main_window.page_manager.pages.items():
                    if 'customer' in page_name.lower() and hasattr(page_info, 'page') and page_info.page:
                        customers_page = page_info.page
                        if hasattr(customers_page, 'customers_tab'):
                            customers_page.customers_tab.load_transactions()
                            print("Refreshed customers table display")
                        break
        except Exception as e:
            print(f"Error refreshing customers display: {e}")
    
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
        self.notes_value.setText("")  # Reset notes
        self.notes_widget.hide()  # Hide notes widget

    
    def showEvent(self, event):
        """Called when the tab is shown"""
        super().showEvent(event)
        self.generateReceipt()