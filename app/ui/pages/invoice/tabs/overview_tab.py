from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QSizePolicy      # << add this
from ..control_panel_factory import ControlPanelFactory
from ..style_factory import StyleFactory
from ..dialogs.payment_dialog import PaymentDialog
import random
from datetime import datetime

class OverviewTab(QtWidgets.QWidget):
    """Tab for reviewing the invoice before finalizing"""
    
    def __init__(self, parent=None):
        super(OverviewTab, self).__init__()
        self.parent = parent
        self.payment_completed = False
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)
        
        # Header
        header_label = QtWidgets.QLabel("Invoice Overview")
        header_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        self.layout.addWidget(header_label)
        
        # Description
        desc_label = QtWidgets.QLabel("Review all invoice details before finalizing the transaction:")
        desc_label.setStyleSheet("color: #cccccc; font-size: 14px;")
        self.layout.addWidget(desc_label)
        
        # Main content container - Single unified container
        main_container = QtWidgets.QFrame()
        # company-standard main card
        main_container.setStyleSheet(
            StyleFactory.get_main_container_style() +
            StyleFactory.get_standard_font()
        )

        # Single layout for all content
        content_layout = QtWidgets.QVBoxLayout(main_container)
        content_layout.setContentsMargins(10, 10, 10, 10)
        content_layout.setSpacing(8)
        
        # TRANSACTION HEADER - in its own box
        transaction_frame = QtWidgets.QFrame()
        # transaction header sub-card
        transaction_frame.setStyleSheet(
            StyleFactory.get_section_frame_style() +
            StyleFactory.get_standard_font()
        )
        tx_layout = QtWidgets.QHBoxLayout(transaction_frame)
        tx_layout.setContentsMargins(8, 8, 8, 8)
        tx_layout.setSpacing(10)
        
        # Transaction ID / Date / Staff
        self.transaction_id_label = QtWidgets.QLabel()
        self.transaction_id_label.setStyleSheet("color: #4FC3F7; font-size: 14px; font-weight: bold;")
        
        self.transaction_date_label = QtWidgets.QLabel()
        self.transaction_date_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        
        # Staff info
        self.staff_label = QtWidgets.QLabel()
        self.staff_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        self.staff_label.setAlignment(QtCore.Qt.AlignRight)
        
        tx_layout.addWidget(self.transaction_id_label)
        tx_layout.addWidget(self.transaction_date_label)
        tx_layout.addStretch()
        tx_layout.addWidget(self.staff_label)
        content_layout.addWidget(transaction_frame)
        
        # CUSTOMER AND SERVICES - in a box
        customer_services_frame = QtWidgets.QFrame()
        customer_services_frame.setStyleSheet(
            StyleFactory.get_section_frame_style() +
            StyleFactory.get_standard_font()
        )
        cs_layout = QtWidgets.QHBoxLayout(customer_services_frame)
        cs_layout.setContentsMargins(8, 8, 8, 8)
        cs_layout.setSpacing(20)
        
        # LEFT SIDE - Customer Information
        customer_layout = QtWidgets.QVBoxLayout()
        
        customer_title = QtWidgets.QLabel("Customer Information")
        customer_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        customer_layout.addWidget(customer_title)
        
        # Customer details in compact format
        self.customer_name = QtWidgets.QLabel()
        self.customer_name.setStyleSheet("color: white; font-size: 13px;")
        customer_layout.addWidget(self.customer_name)
        
        self.customer_phone = QtWidgets.QLabel()
        self.customer_phone.setStyleSheet("color: #cccccc; font-size: 12px;")
        customer_layout.addWidget(self.customer_phone)
        
        self.customer_gender = QtWidgets.QLabel()
        self.customer_gender.setStyleSheet("color: #cccccc; font-size: 12px;")
        customer_layout.addWidget(self.customer_gender)
        
        self.customer_city = QtWidgets.QLabel()
        self.customer_city.setStyleSheet("color: #cccccc; font-size: 12px;")
        customer_layout.addWidget(self.customer_city)
        
        customer_layout.addStretch()
        cs_layout.addLayout(customer_layout, 1)
        
        # RIGHT SIDE - Services Information
        services_layout = QtWidgets.QVBoxLayout()
        
        services_title = QtWidgets.QLabel("Selected Services")
        services_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        services_layout.addWidget(services_title)
        
        # Services list - more compact
        self.services_list_widget = QtWidgets.QListWidget()
        # use unified list style
        self.services_list_widget.setStyleSheet(StyleFactory.get_selected_services_list_style())
        self.services_list_widget.setMaximumHeight(70)
        self.services_list_widget.setMinimumHeight(50)
        services_layout.addWidget(self.services_list_widget)
        
        # Services total
        self.services_total_label = QtWidgets.QLabel()
        self.services_total_label.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 14px;")
        self.services_total_label.setAlignment(QtCore.Qt.AlignRight)
        services_layout.addWidget(self.services_total_label)
        
        cs_layout.addLayout(services_layout, 1)
        content_layout.addWidget(customer_services_frame)
        
        # separator
        sep1 = QtWidgets.QFrame()
        sep1.setFrameShape(QtWidgets.QFrame.HLine)
        sep1.setStyleSheet(StyleFactory.get_separator_style())

        content_layout.addWidget(sep1)
        
        # PAYMENT AND TOTAL - in a box
        payment_frame = QtWidgets.QFrame()
        payment_frame.setStyleSheet(
            StyleFactory.get_section_frame_style() +
            StyleFactory.get_standard_font()
        )
        pay_layout = QtWidgets.QHBoxLayout(payment_frame)
        pay_layout.setContentsMargins(8, 8, 8, 8)
        pay_layout.setSpacing(20)
        
        # LEFT SIDE - Payment Details
        payment_info_layout = QtWidgets.QVBoxLayout()
        
        payment_title = QtWidgets.QLabel("Payment Details")
        payment_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        payment_info_layout.addWidget(payment_title)
        
        self.payment_method = QtWidgets.QLabel()
        self.payment_method.setStyleSheet("color: white; font-size: 13px;")
        payment_info_layout.addWidget(self.payment_method)
        
        self.payment_coupon = QtWidgets.QLabel()
        self.payment_coupon.setStyleSheet("color: #cccccc; font-size: 12px;")
        payment_info_layout.addWidget(self.payment_coupon)
        
        payment_info_layout.addStretch()
        pay_layout.addLayout(payment_info_layout, 1)
        
        # RIGHT SIDE - Total Calculation
        total_layout = QtWidgets.QVBoxLayout()
        
        total_title = QtWidgets.QLabel("Total Summary")
        total_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        total_layout.addWidget(total_title)
        
        # Total calculation in compact format
        total_details_layout = QtWidgets.QGridLayout()
        total_details_layout.setVerticalSpacing(2)
        total_details_layout.setHorizontalSpacing(8)
        
        # Base price
        base_label = QtWidgets.QLabel("Base Price:")
        base_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        self.base_price_value = QtWidgets.QLabel()
        self.base_price_value.setStyleSheet("color: white; font-size: 12px; font-weight: bold;")
        self.base_price_value.setAlignment(QtCore.Qt.AlignRight)
        
        total_details_layout.addWidget(base_label, 0, 0)
        total_details_layout.addWidget(self.base_price_value, 0, 1)
        
        # Discount
        discount_label = QtWidgets.QLabel("Discount:")
        discount_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        self.discount_value = QtWidgets.QLabel()
        self.discount_value.setStyleSheet("color: #FF5252; font-size: 12px; font-weight: bold;")
        self.discount_value.setAlignment(QtCore.Qt.AlignRight)
        
        total_details_layout.addWidget(discount_label, 1, 0)
        total_details_layout.addWidget(self.discount_value, 1, 1)
        
        total_layout.addLayout(total_details_layout)
        
        # Final total - prominent
        final_total_layout = QtWidgets.QHBoxLayout()
        final_label = QtWidgets.QLabel("Final Total:")
        final_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.final_value = QtWidgets.QLabel()
        self.final_value.setStyleSheet("color: #4CAF50; font-size: 18px; font-weight: bold;")
        self.final_value.setAlignment(QtCore.Qt.AlignRight)
        
        final_total_layout.addWidget(final_label)
        final_total_layout.addWidget(self.final_value)
        
        total_layout.addLayout(final_total_layout)
        pay_layout.addLayout(total_layout, 1)
        content_layout.addWidget(payment_frame)
        
        self.layout.addWidget(main_container, 1)
        
        # final separator before action buttons
        sep2 = QtWidgets.QFrame()
        sep2.setFrameShape(QtWidgets.QFrame.HLine)
        sep2.setStyleSheet(StyleFactory.get_separator_style())

        self.layout.addWidget(sep2)
        
        # Buttons at the bottom
        button_layout = QtWidgets.QHBoxLayout()
        
        back_button = ControlPanelFactory.create_action_button("Back", primary=False)
        back_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)
        
        button_layout.addStretch()
        
        # Payment button
        self.payment_button = ControlPanelFactory.create_action_button("Payment")
        # (primary button uses default StyleFactory.get_button_style())
        self.payment_button.clicked.connect(self.open_payment_dialog)
        button_layout.addWidget(self.payment_button)
        
        # Finalize Invoice button (initially disabled)
        self.finalize_button = ControlPanelFactory.create_action_button("Finalize Invoice")
        self.finalize_button.setEnabled(False)
        self.finalize_button.clicked.connect(self.finalize_invoice)
        button_layout.addWidget(self.finalize_button)
        
        self.layout.addLayout(button_layout)
    
    def open_payment_dialog(self):
        """Open the payment dialog"""
        total_amount = float(self.parent.invoice_data["payment"].get("total_amount", 0))
        
        dialog = PaymentDialog(self, total_amount)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Payment completed successfully
            self.payment_completed = True
            self.finalize_button.setEnabled(True)
            self.payment_button.setEnabled(False)
            self.payment_button.setText("Payment Completed ✓")
            QtWidgets.QMessageBox.information(self, "Payment Complete", "Payment has been processed successfully!")
    
    def showEvent(self, event):
        """Update the overview when the tab is shown"""
        super().showEvent(event)
        self.updateOverview()
    
    def updateOverview(self):
        """Update the overview with current invoice data"""
        data = self.parent.invoice_data
        services = data.get("services", [])
        customer = data.get("customer", {})
        payment = data.get("payment", {})
        
        # Update transaction info
        transaction_id = data.get("transaction_id", "")
        if not transaction_id:
            # Generate if not exists
            now = datetime.now()
            transaction_id = f"TXN-{now.strftime('%Y%m%d')}-{random.randint(10000, 99999)}"
            data["transaction_id"] = transaction_id
        
        self.transaction_id_label.setText(f"ID: {transaction_id}")
        
        # Current date and time
        now = datetime.now()
        self.transaction_date_label.setText(f"{now.strftime('%b %d, %Y at %I:%M %p')}")
        
        # Staff info
        staff_name = "Staff Member"
        if hasattr(self.parent, 'user_info') and self.parent.user_info:
            staff_name = self.parent.user_info.get('name', 'Staff Member')
        self.staff_label.setText(f"Served by: {staff_name}")
        
        # Update customer details
        if customer:
            self.customer_name.setText(f"Name: {customer.get('name', '')}")
            self.customer_phone.setText(f"Phone: {customer.get('phone', '')}")
            self.customer_gender.setText(f"Gender: {customer.get('gender', '')}")
            self.customer_city.setText(f"City: {customer.get('city', '')}")
        
        # Update services details
        self.services_list_widget.clear()
        total_services_price = 0
        
        for service in services:
            price = float(service.get('price', 0))
            total_services_price += price
            item_text = f"{service.get('service_name', '')} - ₱{price:.2f}"
            self.services_list_widget.addItem(item_text)
        
        self.services_total_label.setText(f"Subtotal: ₱{total_services_price:.2f}")
        
        # Update payment details
        if payment:
            self.payment_method.setText(f"Method: {payment.get('method', 'Cash')}")
            
            coupon = payment.get('coupon_code', '')
            if coupon:
                self.payment_coupon.setText(f"Coupon: {coupon}")
            else:
                self.payment_coupon.setText("Coupon: None")
        
        # Update total calculation
        if services and payment:
            base_price = total_services_price
            discount_amount = float(payment.get('discount_amount', 0))
            final_price = float(payment.get('total_amount', 0))
            
            self.base_price_value.setText(f"₱{base_price:.2f}")
            self.discount_value.setText(f"-₱{discount_amount:.2f}")
            self.final_value.setText(f"₱{final_price:.2f}")
    
    def go_back(self):
        """Go back to the payment details tab"""
        self.parent.tabs.setCurrentIndex(2)
    
    def finalize_invoice(self):
        """Finalize the invoice and generate OR number"""
        if not self.payment_completed:
            QtWidgets.QMessageBox.warning(self, "Payment Required", "Please complete the payment process first.")
            return
            
        # Generate a simple OR number (in a real system, this would be more sophisticated)
        now = datetime.now()
        or_number = f"OR-{now.strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        # Save OR number to invoice data
        self.parent.invoice_data["or_number"] = or_number
        
        # Generate transaction ID if not already generated
        if not self.parent.invoice_data.get("transaction_id"):
            self.parent.invoice_data["transaction_id"] = f"TXN-{now.strftime('%Y%m%d')}-{random.randint(10000, 99999)}"
        
        # Enable receipt tab and switch to it
        self.parent.enable_next_tab(3)
        self.parent.tabs.setCurrentIndex(4)
    
    def reset(self):
        """Reset the tab state"""
        self.payment_completed = False
        self.finalize_button.setEnabled(False)
        self.payment_button.setEnabled(True)
        self.payment_button.setText("Payment")
        
        self.transaction_id_label.setText("")
        self.transaction_date_label.setText("")
        self.staff_label.setText("")
        self.services_list_widget.clear()
        self.services_total_label.setText("")
        self.customer_name.setText("")
        self.customer_phone.setText("")
        self.customer_gender.setText("")
        self.customer_city.setText("")
        self.payment_method.setText("")
        self.payment_coupon.setText("")
        self.base_price_value.setText("")
        self.discount_value.setText("")
        self.final_value.setText("")