from PyQt5 import QtWidgets
import mysql.connector
from app.utils.db_manager import DBManager
from .base_dialog import BaseDialog

class ServiceDialog(BaseDialog):
    """Dialog for adding or editing services"""
    
    def __init__(self, parent=None, service=None):
        super(ServiceDialog, self).__init__(parent, service, "Service")
        self.setup_ui()
        self.populate_data()
    
    def setup_ui(self):
        """Set up the service dialog UI"""
        self.setup_base_ui(550)
        
        self.save_button.setText("Save Service")
        self.save_button.clicked.connect(self.save_service)
        
        # Service name input
        name_label = QtWidgets.QLabel("Service Name:")
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Enter service name")
        self.name_input.setMinimumHeight(36)
        self.form_layout.addRow(name_label, self.name_input)
        
        # Category input
        category_label = QtWidgets.QLabel("Category:")
        self.category_input = QtWidgets.QLineEdit()
        self.category_input.setPlaceholderText("Enter service category")
        self.category_input.setMinimumHeight(36)
        self.form_layout.addRow(category_label, self.category_input)
        
        # Price input
        price_label = QtWidgets.QLabel("Price:")
        self.price_input = QtWidgets.QDoubleSpinBox()
        self.price_input.setRange(0, 100000)
        self.price_input.setDecimals(2)
        self.price_input.setSingleStep(0.01)
        self.price_input.setPrefix("₱ ")
        self.price_input.setMinimumHeight(36)
        self.form_layout.addRow(price_label, self.price_input)
        
        # Availability checkbox
        availability_label = QtWidgets.QLabel("Availability:")
        self.availability_checkbox = QtWidgets.QCheckBox("Service is available")
        self.availability_checkbox.setChecked(True)
        self.form_layout.addRow(availability_label, self.availability_checkbox)
        
        # Description input (multiline)
        desc_label = QtWidgets.QLabel("Description:")
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Enter service description")
        self.description_input.setMinimumHeight(120)
        self.form_layout.addRow(desc_label, self.description_input)
    
    def populate_data(self):
        """Populate dialog with service data if editing"""
        if self.item:
            self.header_label.setText("Edit Service")
            self.name_input.setText(self.item['service_name'])
            self.category_input.setText(self.item.get('category', ''))
            self.description_input.setText(self.item.get('description', ''))
            self.price_input.setValue(float(self.item['price']))
            
            self.availability_checkbox.setChecked(self.item.get('availability', True))
        else:
            self.header_label.setText("Add New Service")
    
    def save_service(self):
        """Save the service to the database"""
        # Validate inputs
        if not self.name_input.text().strip():
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Service name is required.")
            return
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            service_name = self.name_input.text().strip()
            category = self.category_input.text().strip()
            description = self.description_input.toPlainText().strip()
            price = self.price_input.value()
            availability = self.availability_checkbox.isChecked()
            
            if self.item:
                # Update existing service
                cursor.execute(
                    """UPDATE services 
                       SET service_name = %s, 
                           category = %s, 
                           description = %s, 
                           price = %s, 
                           availability = %s 
                       WHERE service_id = %s""",
                    (service_name, category, description, price, 
                     availability, self.item['service_id'])
                )
            else:
                # Insert new service
                cursor.execute(
                    """INSERT INTO services 
                       (service_name, category, description, price, availability) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (service_name, category, description, price, availability)
                )
            
            conn.commit()
            cursor.close()
            
            self.accept()
            
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Error saving service: {err}")