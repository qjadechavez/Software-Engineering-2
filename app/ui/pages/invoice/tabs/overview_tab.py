from PyQt5 import QtWidgets, QtCore, QtGui
from ..factories.panel_factory import PanelFactory
import random
from datetime import datetime

class OverviewTab(QtWidgets.QWidget):
    """Tab for reviewing the invoice before finalizing"""
    
    def __init__(self, parent=None):
        super(OverviewTab, self).__init__()
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Header
        header_label = QtWidgets.QLabel("Invoice Overview")
        header_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.layout.addWidget(header_label)
        
        # Description
        desc_label = QtWidgets.QLabel("Review the invoice details before finalizing:")
        desc_label.setStyleSheet("color: #cccccc; font-size: 14px;")
        self.layout.addWidget(desc_label)
        
        # Create scrollable container
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #555;
                border-radius: 5px;
            }
        """)
        
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 10, 0)
        scroll_layout.setSpacing(15)
        
        # Service details section
        service_details = QtWidgets.QFrame()
        service_details.setFrameShape(QtWidgets.QFrame.StyledPanel)
        service_details.setStyleSheet("""
            QFrame {
                background-color: #1c1c1c;
                border-radius: 8px;
                border: 1px solid #444444;
            }
        """)
        
        service_layout = QtWidgets.QVBoxLayout(service_details)
        
        service_title = QtWidgets.QLabel("Service Details")
        service_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        service_layout.addWidget(service_title)
        
        self.service_name = QtWidgets.QLabel()
        self.service_name.setStyleSheet("color: white;")
        service_layout.addWidget(self.service_name)
        
        self.service_price = QtWidgets.QLabel()
        self.service_price.setStyleSheet("color: #4CAF50;")
        service_layout.addWidget(self.service_price)
        
        scroll_layout.addWidget(service_details)
        
        # Customer details section
        customer_details = QtWidgets.QFrame()
        customer_details.setFrameShape(QtWidgets.QFrame.StyledPanel)
        customer_details.setStyleSheet("""
            QFrame {
                background-color: #1c1c1c;
                border-radius: 8px;
                border: 1px solid #444444;
            }
        """)
        
        customer_layout = QtWidgets.QVBoxLayout(customer_details)
        
        customer_title = QtWidgets.QLabel("Customer Details")
        customer_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        customer_layout.addWidget(customer_title)
        
        self.customer_name = QtWidgets.QLabel()
        self.customer_name.setStyleSheet("color: white;")
        customer_layout.addWidget(self.customer_name)
        
        self.customer_phone = QtWidgets.QLabel()
        self.customer_phone.setStyleSheet("color: white;")
        customer_layout.addWidget(self.customer_phone)
        
        self.customer_gender = QtWidgets.QLabel()
        self.customer_gender.setStyleSheet("color: white;")
        customer_layout.addWidget(self.customer_gender)
        
        self.customer_city = QtWidgets.QLabel()
        self.customer_city.setStyleSheet("color: white;")
        customer_layout.addWidget(self.customer_city)
        
        scroll_layout.addWidget(customer_details)
        
        # Payment details section
        payment_details = QtWidgets.QFrame()
        payment_details.setFrameShape(QtWidgets.QFrame.StyledPanel)
        payment_details.setStyleSheet("""
            QFrame {
                background-color: #1c1c1c;
                border-radius: 8px;
                border: 1px solid #444444;
            }
        """)
        
        payment_layout = QtWidgets.QVBoxLayout(payment_details)
        
        payment_title = QtWidgets.QLabel("Payment Details")
        payment_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        payment_layout.addWidget(payment_title)
        
        self.payment_method = QtWidgets.QLabel()
        self.payment_method.setStyleSheet("color: white;")
        payment_layout.addWidget(self.payment_method)
        
        self.payment_discount = QtWidgets.QLabel()
        self.payment_discount.setStyleSheet("color: white;")
        payment_layout.addWidget(self.payment_discount)
        
        self.payment_coupon = QtWidgets.QLabel()
        self.payment_coupon.setStyleSheet("color: white;")
        payment_layout.addWidget(self.payment_coupon)
        
        scroll_layout.addWidget(payment_details)
        
        # Total amount section
        total_details = QtWidgets.QFrame()
        total_details.setFrameShape(QtWidgets.QFrame.StyledPanel)
        total_details.setStyleSheet("""
            QFrame {
                background-color: #1c1c1c;
                border-radius: 8px;
                border: 1px solid #444444;
            }
        """)
        
        total_layout = QtWidgets.QVBoxLayout(total_details)
        
        total_title = QtWidgets.QLabel("Total")
        total_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        total_layout.addWidget(total_title)
        
        total_grid = QtWidgets.QGridLayout()
        total_grid.setColumnStretch(0, 1)
        total_grid.setColumnStretch(1, 0)
        
        base_price_label = QtWidgets.QLabel("Base Price:")
        base_price_label.setStyleSheet("color: white;")
        self.base_price_value = QtWidgets.QLabel()
        self.base_price_value.setStyleSheet("color: white; font-weight: bold;")
        self.base_price_value.setAlignment(QtCore.Qt.AlignRight)
        
        total_grid.addWidget(base_price_label, 0, 0)
        total_grid.addWidget(self.base_price_value, 0, 1)
        
        discount_label = QtWidgets.QLabel("Discount:")
        discount_label.setStyleSheet("color: white;")
        self.discount_value = QtWidgets.QLabel()
        self.discount_value.setStyleSheet("color: #FF5252; font-weight: bold;")
        self.discount_value.setAlignment(QtCore.Qt.AlignRight)
        
        total_grid.addWidget(discount_label, 1, 0)
        total_grid.addWidget(self.discount_value, 1, 1)
        
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        separator.setStyleSheet("background-color: #444444;")
        
        final_label = QtWidgets.QLabel("Final Total:")
        final_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        self.final_value = QtWidgets.QLabel()
        self.final_value.setStyleSheet("color: #4CAF50; font-size: 16px; font-weight: bold;")
        self.final_value.setAlignment(QtCore.Qt.AlignRight)
        
        total_grid.addWidget(separator, 2, 0, 1, 2)
        total_grid.addWidget(final_label, 3, 0)
        total_grid.addWidget(self.final_value, 3, 1)
        
        total_layout.addLayout(total_grid)
        
        scroll_layout.addWidget(total_details)
        
        # Add scroll area to layout
        scroll_area.setWidget(scroll_content)
        self.layout.addWidget(scroll_area)
        
        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        back_button = PanelFactory.create_action_button("Back", primary=False)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)
        
        button_layout.addStretch()
        
        finalize_button = PanelFactory.create_action_button("Finalize Invoice")
        finalize_button.clicked.connect(self.finalize_invoice)
        button_layout.addWidget(finalize_button)
        
        self.layout.addLayout(button_layout)
    
    def updateOverview(self):
        """Update the overview with current invoice data"""
        data = self.parent.invoice_data
        service = data.get("service", {})
        customer = data.get("customer", {})
        payment = data.get("payment", {})
        
        # Update service details
        if service:
            self.service_name.setText(f"Service: {service.get('service_name', '')}")
            self.service_price.setText(f"Base Price: ₱{float(service.get('price', 0)):.2f}")
        
        # Update customer details
        if customer:
            self.customer_name.setText(f"Name: {customer.get('name', '')}")
            self.customer_phone.setText(f"Phone: {customer.get('phone', '')}")
            self.customer_gender.setText(f"Gender: {customer.get('gender', '')}")
            self.customer_city.setText(f"City: {customer.get('city', '')}")
        
        # Update payment details
        if payment:
            self.payment_method.setText(f"Payment Method: {payment.get('method', 'Cash')}")
            discount = payment.get('discount_percentage', 0)
            self.payment_discount.setText(f"Discount: {discount}%")
            
            coupon = payment.get('coupon_code', '')
            if coupon:
                self.payment_coupon.setText(f"Coupon: {coupon}")
            else:
                self.payment_coupon.setText("Coupon: None")
        
        # Update total calculation
        if service and payment:
            base_price = float(service.get('price', 0))
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
        self.service_name.setText("")
        self.service_price.setText("")
        self.customer_name.setText("")
        self.customer_phone.setText("")
        self.customer_gender.setText("")
        self.customer_city.setText("")
        self.payment_method.setText("")
        self.payment_discount.setText("")
        self.payment_coupon.setText("")
        self.base_price_value.setText("")
        self.discount_value.setText("")
        self.final_value.setText("")