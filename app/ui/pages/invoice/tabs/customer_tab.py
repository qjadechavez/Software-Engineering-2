from PyQt5 import QtWidgets, QtCore
from ..control_panel_factory import ControlPanelFactory

class CustomerTab(QtWidgets.QWidget):
    """Tab for entering customer information"""
    
    def __init__(self, parent=None):
        super(CustomerTab, self).__init__()
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Header
        header_label = QtWidgets.QLabel("Customer Information")
        header_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.layout.addWidget(header_label)
        
        # Description
        desc_label = QtWidgets.QLabel("Enter the customer's details below:")
        desc_label.setStyleSheet("color: #cccccc; font-size: 14px;")
        self.layout.addWidget(desc_label)
        
        # Form container
        form_container = QtWidgets.QWidget()
        form_layout = QtWidgets.QFormLayout(form_container)
        form_layout.setContentsMargins(0, 10, 0, 10)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        form_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        
        # Customer name
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Enter customer name")
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """)
        self.name_input.setMinimumHeight(36)
        name_label = QtWidgets.QLabel("Name:")
        name_label.setStyleSheet("color: white;")
        form_layout.addRow(name_label, self.name_input)
        
        # Gender selection with radio buttons
        gender_label = QtWidgets.QLabel("Gender:")
        gender_label.setStyleSheet("color: white;")
        
        gender_container = QtWidgets.QWidget()
        gender_layout = QtWidgets.QHBoxLayout(gender_container)
        gender_layout.setContentsMargins(0, 0, 0, 0)
        gender_layout.setSpacing(20)
        
        self.male_radio = QtWidgets.QRadioButton("Male")
        self.male_radio.setStyleSheet("color: white;")
        self.female_radio = QtWidgets.QRadioButton("Female")
        self.female_radio.setStyleSheet("color: white;")
        self.other_radio = QtWidgets.QRadioButton("Other")
        self.other_radio.setStyleSheet("color: white;")
        
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        gender_layout.addWidget(self.other_radio)
        gender_layout.addStretch()
        
        form_layout.addRow(gender_label, gender_container)
        
        # Phone number
        self.phone_input = QtWidgets.QLineEdit()
        self.phone_input.setPlaceholderText("Enter phone number")
        self.phone_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """)
        self.phone_input.setMinimumHeight(36)
        phone_label = QtWidgets.QLabel("Phone Number:")
        phone_label.setStyleSheet("color: white;")
        form_layout.addRow(phone_label, self.phone_input)
        
        # City
        self.city_input = QtWidgets.QLineEdit()
        self.city_input.setPlaceholderText("Enter city")
        self.city_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                background-color: #2a2a2a;
                color: white;
                border: 1px solid #444444;
                border-radius: 4px;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
        """)
        self.city_input.setMinimumHeight(36)
        city_label = QtWidgets.QLabel("City:")
        city_label.setStyleSheet("color: white;")
        form_layout.addRow(city_label, self.city_input)
        
        self.layout.addWidget(form_container)
        
        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        back_button = ControlPanelFactory.create_action_button("Back", primary=False)
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)
        
        button_layout.addStretch()
        
        self.continue_button = ControlPanelFactory.create_action_button("Continue to Payment")
        self.continue_button.clicked.connect(self.continue_to_payment)
        button_layout.addWidget(self.continue_button)
        
        self.layout.addLayout(button_layout)
        
        # Add stretch to push everything to the top
        self.layout.addStretch()
        
        # Connect input events
        self.name_input.textChanged.connect(self.validate_inputs)
        self.phone_input.textChanged.connect(self.validate_inputs)
        
        # Initial validation
        self.validate_inputs()
    
    def validate_inputs(self):
        """Validate form inputs and enable/disable continue button"""
        has_name = len(self.name_input.text().strip()) > 0
        has_phone = len(self.phone_input.text().strip()) > 0
        
        self.continue_button.setEnabled(has_name and has_phone)
    
    def get_selected_gender(self):
        """Get the selected gender from radio buttons"""
        if self.male_radio.isChecked():
            return "Male"
        elif self.female_radio.isChecked():
            return "Female"
        elif self.other_radio.isChecked():
            return "Other"
        else:
            return ""
    
    def continue_to_payment(self):
        """Continue to the payment details tab"""
        # Save customer data exactly matching transactions table schema
        self.parent.invoice_data["customer"] = {
            "name": self.name_input.text().strip(),
            "gender": self.get_selected_gender(),
            "phone": self.phone_input.text().strip(),
            "city": self.city_input.text().strip()
        }
        
        self.parent.enable_next_tab(1)
        self.parent.tabs.setCurrentIndex(2)
    
    def go_back(self):
        """Go back to the service selection tab"""
        self.parent.tabs.setCurrentIndex(0)
    
    def reset(self):
        """Reset the tab state"""
        self.name_input.clear()
        self.phone_input.clear()
        self.city_input.clear()
        
        # Uncheck all gender radio buttons
        self.male_radio.setChecked(False)
        self.female_radio.setChecked(False)
        self.other_radio.setChecked(False)
        
        # Reset validation
        self.validate_inputs()