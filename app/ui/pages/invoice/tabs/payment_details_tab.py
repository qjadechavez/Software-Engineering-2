from PyQt5 import QtWidgets, QtCore
from ..control_panel_factory import ControlPanelFactory
from ..style_factory import StyleFactory
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
        
        # Main content area - 2 column layout
        main_content_layout = QtWidgets.QHBoxLayout()
        main_content_layout.setSpacing(20)
        
        # LEFT COLUMN - Services summary
        left_column = QtWidgets.QVBoxLayout()
        
        self.summary_frame = QtWidgets.QFrame()
        self.summary_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.summary_frame.setStyleSheet("""
            QFrame {
                background-color: #1c1c1c;
                border-radius: 8px;
                border: 1px solid #444444;
                padding: 15px;
            }
        """)
        
        summary_layout = QtWidgets.QVBoxLayout(self.summary_frame)
        
        # Services header
        services_header = QtWidgets.QLabel("Selected Services:")
        services_header.setStyleSheet("color: white; font-weight: bold; font-size: 16px; border: none;")
        summary_layout.addWidget(services_header)
        
        # Services list
        self.services_list_widget = QtWidgets.QListWidget()
        self.services_list_widget.setStyleSheet("""
            QListWidget {
                background-color: #2a2a2a;
                border: 1px solid #444444;
                border-radius: 4px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #444444;
                border-radius: 4px;
                margin: 2px;
            }
            QListWidget::item:hover {
                background-color: #3a3a3a;
            }
        """)
        self.services_list_widget.setMinimumHeight(150)
        self.services_list_widget.setMaximumHeight(200)
        summary_layout.addWidget(self.services_list_widget)
        
        # Total services price
        self.total_services_price_label = QtWidgets.QLabel()
        self.total_services_price_label.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 16px; margin: 10px 0; border: none;")
        summary_layout.addWidget(self.total_services_price_label)
        
        # Customer info
        self.service_customer_label = QtWidgets.QLabel()
        self.service_customer_label.setStyleSheet("color: #cccccc; font-size: 14px; border: none;")
        summary_layout.addWidget(self.service_customer_label)
        
        left_column.addWidget(self.summary_frame)
        left_column.addStretch()
        
        # RIGHT COLUMN - Form container
        right_column = QtWidgets.QVBoxLayout()
        
        form_container = QtWidgets.QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background-color: #1c1c1c;
                border-radius: 8px;
                border: 1px solid #444444;
                padding: 15px;
            }
        """)
        form_layout = QtWidgets.QFormLayout(form_container)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(20)
        form_layout.setLabelAlignment(QtCore.Qt.AlignLeft)
        form_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        
        # Payment method - changed to display only Cash
        payment_label = QtWidgets.QLabel("Payment Method:")
        payment_label.setStyleSheet("color: white; font-weight: bold; border: none;")
        
        payment_value = QtWidgets.QLabel("Cash")
        payment_value.setStyleSheet("""
            QLabel {
                padding: 12px;
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #444444;
                border-radius: 6px;
                min-height: 20px;
                font-size: 14px;
            }
        """)
        
        form_layout.addRow(payment_label, payment_value)
        
        # Discount
        discount_label = QtWidgets.QLabel("Discount (%):")
        discount_label.setStyleSheet("color: white; font-weight: bold; border: none;")
        
        self.discount_spin = QtWidgets.QSpinBox()
        self.discount_spin.setRange(0, 50)
        self.discount_spin.setEnabled(False)
        self.discount_spin.setValue(0)
        self.discount_spin.setStyleSheet("""
            QSpinBox {
                padding: 12px;
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #444444;
                border-radius: 6px;
                min-height: 20px;
                font-size: 14px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #3a3a3a;
                width: 20px;
                border-radius: 3px;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #4a4a4a;
            }
        """)
        self.discount_spin.valueChanged.connect(self.calculate_total)
        
        form_layout.addRow(discount_label, self.discount_spin)
        
        # Coupon code
        coupon_label = QtWidgets.QLabel("Coupon Code:")
        coupon_label.setStyleSheet("color: white; font-weight: bold; border: none;")
        
        coupon_container = QtWidgets.QWidget()
        coupon_layout = QtWidgets.QHBoxLayout(coupon_container)
        coupon_layout.setContentsMargins(0, 0, 0, 0)
        coupon_layout.setSpacing(10)
        
        self.coupon_input = QtWidgets.QLineEdit()
        self.coupon_input.setPlaceholderText("Enter coupon code (optional)")
        self.coupon_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                background-color: #2a2a2a;
                color: white;
                border-radius: 6px;
                min-height: 20px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """)
        
        coupon_button = QtWidgets.QPushButton("Apply")
        coupon_button.setStyleSheet("""
            QPushButton {
                padding: 12px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        coupon_button.clicked.connect(self.apply_coupon)
        
        coupon_layout.addWidget(self.coupon_input)
        coupon_layout.addWidget(coupon_button)
        
        form_layout.addRow(coupon_label, coupon_container)
        
        # Total amount
        total_label = QtWidgets.QLabel("Total Amount:")
        total_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none;")
        
        self.total_amount_label = QtWidgets.QLabel("₱0.00")
        self.total_amount_label.setStyleSheet("""
            QLabel {
                color: #4CAF50; 
                font-size: 24px; 
                font-weight: bold;
                padding: 12px;
                background-color: #2a2a2a;
                border: 2px solid #4CAF50;
                border-radius: 6px;
                min-height: 20px;
            }
        """)
        
        form_layout.addRow(total_label, self.total_amount_label)
        
        right_column.addWidget(form_container)
        right_column.addStretch()
        
        # Add columns to main content layout (50% left, 50% right)
        main_content_layout.addLayout(left_column, 1)
        main_content_layout.addLayout(right_column, 1)
        
        self.layout.addLayout(main_content_layout)
        
        # Add stretch to push buttons to bottom
        self.layout.addStretch()
        
        # Buttons at the bottom
        button_layout = QtWidgets.QHBoxLayout()
        
        back_button = ControlPanelFactory.create_action_button("Back", primary=False)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)
        
        button_layout.addStretch()
        
        self.continue_button = ControlPanelFactory.create_action_button("Continue", primary=True)
        self.continue_button.clicked.connect(self.continue_to_overview)
        button_layout.addWidget(self.continue_button)
        
        self.layout.addLayout(button_layout)
    
    def showEvent(self, event):
        """Update the UI when the tab is shown"""
        super().showEvent(event)
        self.update_summary()
        self.calculate_total()
    
    def update_summary(self):
        """Update the services summary"""
        services = self.parent.invoice_data.get("services", [])
        customer = self.parent.invoice_data.get("customer")
        
        # Clear and update services list
        self.services_list_widget.clear()
        total_price = 0
        
        for service in services:
            price = float(service['price'])
            total_price += price
            item_text = f"{service['service_name']} - ₱{price:.2f}"
            self.services_list_widget.addItem(item_text)
        
        # Update total services price
        self.total_services_price_label.setText(f"Services Total: ₱{total_price:.2f}")
        
        # Update customer info
        if customer:
            customer_name = customer.get("name", "")
            customer_phone = customer.get("phone", "")
            self.service_customer_label.setText(f"Customer: {customer_name} | Phone: {customer_phone}")
    
    def calculate_total(self):
        """Calculate the total amount with discount"""
        services = self.parent.invoice_data.get("services", [])
        
        if services:
            # Calculate total price of all services
            total_price = sum(float(service['price']) for service in services)
            discount = self.discount_spin.value()
            
            # Apply discount
            discount_amount = total_price * (discount / 100)
            final_price = total_price - discount_amount
            
            # Update the total
            self.total_amount_label.setText(f"₱{final_price:.2f}")
            
            # Store the total and discount amounts in invoice data
            self.parent.invoice_data["payment"]["total_amount"] = final_price
            self.parent.invoice_data["payment"]["base_amount"] = total_price
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
        self.services_list_widget.clear()
        self.total_services_price_label.setText("")
        self.service_customer_label.setText("")
        self.total_amount_label.setText("")