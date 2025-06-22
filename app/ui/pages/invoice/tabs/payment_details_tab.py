from PyQt5 import QtWidgets, QtCore
from ..factories.panel_factory import PanelFactory
import decimal

class PaymentDetailsTab(QtWidgets.QWidget):
    """Tab for entering payment details"""
    
    def __init__(self, parent=None):
        super(PaymentDetailsTab, self).__init__()
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Header
        header_label = QtWidgets.QLabel("Payment Details")
        header_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.layout.addWidget(header_label)
        
        # Description
        desc_label = QtWidgets.QLabel("Enter the payment details:")
        desc_label.setStyleSheet("color: #cccccc; font-size: 14px;")
        self.layout.addWidget(desc_label)
        
        # Service summary
        self.summary_frame = QtWidgets.QFrame()
        self.summary_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.summary_frame.setStyleSheet("""
            QFrame {
                background-color: #1c1c1c;
                border-radius: 8px;
                border: 1px solid #444444;
                padding: 10px;
            }
        """)
        
        summary_layout = QtWidgets.QVBoxLayout(self.summary_frame)
        
        self.service_name_label = QtWidgets.QLabel()
        self.service_name_label.setStyleSheet("color: white; font-weight: bold;")
        summary_layout.addWidget(self.service_name_label)
        
        self.service_price_label = QtWidgets.QLabel()
        self.service_price_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        summary_layout.addWidget(self.service_price_label)
        
        self.service_customer_label = QtWidgets.QLabel()
        self.service_customer_label.setStyleSheet("color: #cccccc;")
        summary_layout.addWidget(self.service_customer_label)
        
        self.layout.addWidget(self.summary_frame)
        
        # Form container
        form_container = QtWidgets.QWidget()
        form_layout = QtWidgets.QFormLayout(form_container)
        form_layout.setContentsMargins(0, 10, 0, 10)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        form_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        
        # Payment method - changed to display only Cash
        payment_label = QtWidgets.QLabel("Payment Method:")
        payment_label.setStyleSheet("color: white;")
        
        payment_value = QtWidgets.QLabel("Cash")
        payment_value.setStyleSheet("""
            QLabel {
                padding: 8px;
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                min-height: 36px;
            }
        """)
        
        form_layout.addRow(payment_label, payment_value)
        
        # Discount
        discount_label = QtWidgets.QLabel("Discount (%):")
        discount_label.setStyleSheet("color: white;")
        
        self.discount_spin = QtWidgets.QSpinBox()
        self.discount_spin.setRange(0, 50)
        self.discount_spin.setValue(0)
        self.discount_spin.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                min-height: 36px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #3a3a3a;
                width: 20px;
            }
        """)
        self.discount_spin.valueChanged.connect(self.calculate_total)
        
        form_layout.addRow(discount_label, self.discount_spin)
        
        # Coupon code
        coupon_label = QtWidgets.QLabel("Coupon Code:")
        coupon_label.setStyleSheet("color: white;")
        
        coupon_container = QtWidgets.QWidget()
        coupon_layout = QtWidgets.QHBoxLayout(coupon_container)
        coupon_layout.setContentsMargins(0, 0, 0, 0)
        coupon_layout.setSpacing(10)
        
        self.coupon_input = QtWidgets.QLineEdit()
        self.coupon_input.setPlaceholderText("Enter coupon code (optional)")
        self.coupon_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
                min-height: 36px;
            }
        """)
        
        coupon_button = QtWidgets.QPushButton("Apply")
        coupon_button.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        coupon_button.clicked.connect(self.apply_coupon)
        
        coupon_layout.addWidget(self.coupon_input)
        coupon_layout.addWidget(coupon_button)
        
        form_layout.addRow(coupon_label, coupon_container)
        
        self.layout.addWidget(form_container)
        
        # Total amount
        total_container = QtWidgets.QWidget()
        total_layout = QtWidgets.QHBoxLayout(total_container)
        total_layout.setContentsMargins(0, 10, 0, 10)
        
        total_label = QtWidgets.QLabel("Total Amount:")
        total_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        
        self.total_amount_label = QtWidgets.QLabel()
        self.total_amount_label.setStyleSheet("color: #4CAF50; font-size: 18px; font-weight: bold;")
        
        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(self.total_amount_label)
        
        self.layout.addWidget(total_container)
        
        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        back_button = PanelFactory.create_action_button("Back", primary=False)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)
        
        button_layout.addStretch()
        
        self.continue_button = PanelFactory.create_action_button("Continue to Overview")
        self.continue_button.clicked.connect(self.continue_to_overview)
        button_layout.addWidget(self.continue_button)
        
        self.layout.addLayout(button_layout)
        
        # Add stretch to push everything to the top
        self.layout.addStretch()
    
    def showEvent(self, event):
        """Update the UI when the tab is shown"""
        super().showEvent(event)
        self.update_summary()
        self.calculate_total()
    
    def update_summary(self):
        """Update the service summary"""
        service = self.parent.invoice_data.get("service")
        customer = self.parent.invoice_data.get("customer")
        
        if service:
            self.service_name_label.setText(f"Service: {service['service_name']}")
            self.service_price_label.setText(f"Base Price: ₱{float(service['price']):.2f}")
            
            if customer:
                customer_name = customer.get("name", "")
                customer_phone = customer.get("phone", "")
                self.service_customer_label.setText(f"Customer: {customer_name} | Phone: {customer_phone}")
    
    def calculate_total(self):
        """Calculate the total amount with discount"""
        service = self.parent.invoice_data.get("service")
        
        if service:
            price = float(service['price'])
            discount = self.discount_spin.value()
            
            # Apply discount
            discount_amount = price * (discount / 100)
            final_price = price - discount_amount
            
            # Update the total
            self.total_amount_label.setText(f"₱{final_price:.2f}")
            
            # Store the total and discount amounts in invoice data
            self.parent.invoice_data["payment"]["total_amount"] = final_price
            self.parent.invoice_data["payment"]["base_amount"] = price
            self.parent.invoice_data["payment"]["discount_amount"] = discount_amount
    
    def apply_coupon(self):
        """Apply a coupon code"""
        coupon = self.coupon_input.text().strip()
        
        if not coupon:
            return
        
        # For this example, let's simulate some coupon codes
        # In a real application, you would check against the database
        discount = 0
        
        if coupon.upper() == "WELCOME10":
            discount = 10
        elif coupon.upper() == "LOYAL20":
            discount = 20
        elif coupon.upper() == "VIP30":
            discount = 30
        
        if discount > 0:
            self.discount_spin.setValue(discount)
            self.parent.invoice_data["payment"]["coupon_code"] = coupon
            QtWidgets.QMessageBox.information(self, "Coupon Applied", f"Coupon '{coupon}' applied for {discount}% discount!")
        else:
            QtWidgets.QMessageBox.warning(self, "Invalid Coupon", "The coupon code is invalid or expired.")
    
    def continue_to_overview(self):
        """Continue to the overview tab"""
        # Save payment details with Cash as the only payment method
        self.parent.invoice_data["payment"] = {
            "method": "Cash",  # Fixed as Cash
            "discount_percentage": decimal.Decimal(self.discount_spin.value()),
            "discount_amount": decimal.Decimal(str(self.parent.invoice_data["payment"].get("discount_amount", 0))),
            "base_amount": decimal.Decimal(str(self.parent.invoice_data["payment"].get("base_amount", 0))),
            "total_amount": decimal.Decimal(str(self.parent.invoice_data["payment"].get("total_amount", 0))),
            "coupon_code": self.coupon_input.text().strip()
        }
        
        self.parent.enable_next_tab(2)
        self.parent.tabs.setCurrentIndex(3)  # Overview tab
    
    def go_back(self):
        """Go back to the customer tab"""
        self.parent.tabs.setCurrentIndex(1)
    
    def reset(self):
        """Reset the tab state"""
        # No need to reset payment method as it's fixed to Cash
        self.discount_spin.setValue(0)
        self.coupon_input.clear()