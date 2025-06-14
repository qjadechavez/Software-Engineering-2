from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage
from app.utils.db_manager import DBManager
import mysql.connector
from datetime import datetime

class StyleFactory:
    """Factory class for consistent styling across components"""
    
    @staticmethod
    def get_tab_style():
        return """
            QTabWidget::pane { 
                border: 1px solid #444; 
                background-color: #232323;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #343434;
                color: #ffffff;
                padding: 10px 30px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                min-width: 120px;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background-color: #1a1a1a;
                border-bottom-color: #1a1a1a;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3a3a3a;
            }
        """
    
    @staticmethod
    def get_search_input_style():
        return """
            QLineEdit {
                border: 1px solid #555;
                border-radius: 18px;
                padding: 8px 15px;
                background: #2a2a2a;
                color: white;
                font-size: 13px;
                min-height: 36px;
            }
            QLineEdit:focus {
                border: 1px solid #0078d7;
                background: #323232;
            }
        """
    
    @staticmethod
    def get_button_style():
        return """
            QPushButton {
                background-color: #007ACC;
                color: white;
                border-radius: 18px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 13px;
                min-width: 150px;
                min-height: 36px;
            }
            QPushButton:hover {
                background-color: #0099FF;
            }
            QPushButton:pressed {
                background-color: #0066BB;
            }
        """
    
    @staticmethod
    def get_table_style():
        return """
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #444;
                color: white;
                border-radius: 5px;
                border: 1px solid #555;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #2c2c2c;
                color: white;
                padding: 8px;
                border: 1px solid #444;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
                background-color: #1e1e1e;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #666;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar:horizontal {
                background: #2a2a2a;
                height: 12px;
            }
            QScrollBar::handle:horizontal {
                background: #666;
                border-radius: 5px;
                min-width: 20px;
            }
        """
    
    @staticmethod
    def get_dialog_style():
        return """
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
                background: transparent;
            }
            QLineEdit, QTextEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #444;
                border-radius: 5px;
                padding: 8px;
                selection-background-color: #007acc;
                font-size: 13px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 1px solid #007acc;
                background-color: #333;
            }
            QCheckBox {
                color: white;
                font-size: 14px;
                background: transparent;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                background: #2d2d2d;
                border: 1px solid #444;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background: #007acc;
                border: none;
                image: url(app/resources/images/check.png);
            }
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 25px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0088e0;
            }
            QPushButton:pressed {
                background-color: #006bb3;
            }
            QPushButton#cancelBtn {
                background-color: #555;
            }
            QPushButton#cancelBtn:hover {
                background-color: #666;
            }
            QPushButton#cancelBtn:pressed {
                background-color: #444;
            }
        """


class TableFactory:
    """Factory class for creating consistent tables"""
    
    @staticmethod
    def create_table():
        """Create a base table with common configuration"""
        table = QtWidgets.QTableWidget()
        table.setStyleSheet(StyleFactory.get_table_style())
        table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.setAlternatingRowColors(False)
        table.verticalHeader().setVisible(False)
        table.setSortingEnabled(True)
        table.setShowGrid(True)
        
        # Make columns and rows not resizable
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        table.horizontalHeader().setStretchLastSection(False)
        
        return table
    
    @staticmethod
    def configure_table_columns(table, column_data, screen_width):
        """Configure table columns with headers and widths
        
        Args:
            table: QTableWidget to configure
            column_data: List of tuples (header, width_percentage)
            screen_width: Total screen width to calculate from
        """
        # Calculate available width (accounting for sidebar and margins)
        table_width = screen_width - 300
        
        # Set column count
        table.setColumnCount(len(column_data))
        
        # Set headers and column widths
        headers = [col[0] for col in column_data]
        table.setHorizontalHeaderLabels(headers)
        
        # Make the table stretch to fill available space
        table.horizontalHeader().setStretchLastSection(True)
        
        # Set the width for all columns except the last one
        for idx, (_, width_pct) in enumerate(column_data[:-1]):
            table.setColumnWidth(idx, int(table_width * width_pct))
        
        # Let the last column stretch to fill remaining space
        # The setStretchLastSection(True) takes care of this


class ControlPanelFactory:
    """Factory class for creating search control panels"""
    
    @staticmethod
    def create_search_control(search_input, add_button_text, add_button_callback, search_callback):
        """Create a consistent search and control panel
        
        Args:
            search_input: QLineEdit for search input
            add_button_text: Text for the add button
            add_button_callback: Callback for the add button
            search_callback: Callback for search input changes
        
        Returns:
            QHBoxLayout containing the search controls
        """
        control_layout = QtWidgets.QHBoxLayout()
        control_layout.setSpacing(10)
        
        # Configure search input
        search_input.setPlaceholderText("Search...")
        search_input.setStyleSheet(StyleFactory.get_search_input_style())
        search_input.textChanged.connect(search_callback)
        
        # Search icon and label
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setSpacing(5)
        
        search_icon = QtWidgets.QLabel()
        search_icon.setPixmap(QtGui.QPixmap("app/resources/images/search.png").scaledToHeight(16) 
                            if QtCore.QFile("app/resources/images/search.png").exists() 
                            else QtGui.QPixmap())
        search_icon.setStyleSheet("color: white; margin-right: 5px;")
        
        search_label = QtWidgets.QLabel("Search:")
        search_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        
        search_layout.addWidget(search_icon)
        search_layout.addWidget(search_label)
        
        # Add button
        add_button = QtWidgets.QPushButton(add_button_text)
        add_button.setStyleSheet(StyleFactory.get_button_style())
        add_button.clicked.connect(add_button_callback)
        
        # Layout for controls
        control_layout.addLayout(search_layout)
        control_layout.addWidget(search_input, 1)
        control_layout.addWidget(add_button)
        
        return control_layout


class BaseDialog(QtWidgets.QDialog):
    """Base dialog class with common functionality for both dialogs"""
    
    def __init__(self, parent=None, item=None, title=""):
        super(BaseDialog, self).__init__(parent)
        self.item = item
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # Common attributes that will be set by child classes
        self.header_label = None
        self.name_input = None
        self.category_input = None
        self.description_input = None
        self.price_input = None
        self.availability_checkbox = None
        
        # Define old_pos for drag support
        self.old_pos = None
    
    def setup_base_ui(self, dialog_height):
        """Set up the base dialog UI with common elements
        
        Args:
            dialog_height: Height of the dialog
        """
        # Set dialog size
        self.resize(550, dialog_height)
        
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create main container with rounded corners
        self.container = QtWidgets.QFrame(self)
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            #container {
                background-color: rgba(35, 35, 35, 0.95);
                border-radius: 12px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }
        """)
        
        # Container layout
        container_layout = QtWidgets.QVBoxLayout(self.container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(15)
        
        # Header with close button
        header_layout = QtWidgets.QHBoxLayout()
        
        self.header_label = QtWidgets.QLabel("Dialog Header")
        self.header_label.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        
        close_button = QtWidgets.QPushButton("×")
        close_button.setFixedSize(35, 35)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #aaa;
                font-size: 20px;
                font-weight: bold;
                border: none;
                border-radius: 15px;
                margin: 0px 0px 0px 0px;
                line-height: 33px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border-radius: 15px;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
            }
        """)
        close_button.clicked.connect(self.reject)
        
        header_layout.addWidget(self.header_label)
        header_layout.addStretch()
        header_layout.addWidget(close_button)
        
        container_layout.addLayout(header_layout)
        
        # Add separator
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        separator.setStyleSheet("background-color: rgba(100, 100, 100, 0.3); margin: 0px 0px 10px 0px;")
        container_layout.addWidget(separator)
        
        # Create a scroll area for the form
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #292929;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Form content will be added by child classes
        self.form_widget = QtWidgets.QWidget()
        self.form_widget.setStyleSheet("background: transparent;")
        self.form_layout = QtWidgets.QFormLayout(self.form_widget)
        self.form_layout.setContentsMargins(5, 5, 5, 5)
        self.form_layout.setSpacing(15)
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.form_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        
        # Apply global styles
        self.setStyleSheet(StyleFactory.get_dialog_style())
        
        self.scroll_area.setWidget(self.form_widget)
        container_layout.addWidget(self.scroll_area, 1)
        
        # Add bottom separator
        bottom_separator = QtWidgets.QFrame()
        bottom_separator.setFrameShape(QtWidgets.QFrame.HLine)
        bottom_separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        bottom_separator.setStyleSheet("background-color: rgba(100, 100, 100, 0.3); margin: 10px 0px 10px 0px;")
        container_layout.addWidget(bottom_separator)
        
        # Button area
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)
        
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.setObjectName("cancelBtn")
        cancel_button.clicked.connect(self.reject)
        
        self.save_button = QtWidgets.QPushButton("Save")
        
        # Add spacer to push buttons to the right
        button_layout.addStretch(1)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(self.save_button)
        
        container_layout.addLayout(button_layout)
        
        # Add container to main layout
        main_layout.addWidget(self.container)
        
        # Enable dragging the dialog
        self.container.mousePressEvent = self.mousePressEvent
        self.container.mouseMoveEvent = self.mouseMoveEvent
        self.container.mouseReleaseEvent = self.mouseReleaseEvent
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPos() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPos()
    
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = None


class ProductDialog(BaseDialog):
    """Dialog for adding or editing products"""
    
    def __init__(self, parent=None, product=None):
        super(ProductDialog, self).__init__(parent, product, "Product")
        self.setup_ui()
        self.populate_data()
    
    def setup_ui(self):
        """Set up the product dialog UI"""
        self.setup_base_ui(650)  # Products need a taller dialog
        
        self.save_button.setText("Save Product")
        self.save_button.clicked.connect(self.save_product)
        
        # Name input
        name_label = QtWidgets.QLabel("Product Name:")
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Enter product name")
        self.name_input.setMinimumHeight(36)
        self.form_layout.addRow(name_label, self.name_input)
        
        # Category input
        category_label = QtWidgets.QLabel("Category:")
        self.category_input = QtWidgets.QLineEdit()
        self.category_input.setPlaceholderText("Enter product category")
        self.category_input.setMinimumHeight(36)
        self.form_layout.addRow(category_label, self.category_input)
        
        # Price input
        price_label = QtWidgets.QLabel("Price:")
        self.price_input = QtWidgets.QDoubleSpinBox()
        self.price_input.setRange(0, 100000)
        self.price_input.setDecimals(2)
        self.price_input.setSingleStep(0.01)
        self.price_input.setPrefix("$ ")
        self.price_input.setMinimumHeight(36)
        self.form_layout.addRow(price_label, self.price_input)
        
        # Quantity input
        qty_label = QtWidgets.QLabel("Quantity:")
        self.quantity_input = QtWidgets.QSpinBox()
        self.quantity_input.setRange(0, 100000)
        self.quantity_input.setMinimumHeight(36)
        self.form_layout.addRow(qty_label, self.quantity_input)
        
        # Threshold input
        threshold_label = QtWidgets.QLabel("Threshold Value:")
        self.threshold_input = QtWidgets.QSpinBox()
        self.threshold_input.setRange(0, 10000)
        self.threshold_input.setValue(10)  # Default threshold
        self.threshold_input.setMinimumHeight(36)
        self.form_layout.addRow(threshold_label, self.threshold_input)
        
        # Expiry date input
        expiry_label = QtWidgets.QLabel("Expiry Date:")
        self.expiry_date_input = QtWidgets.QDateEdit()
        self.expiry_date_input.setCalendarPopup(True)
        self.expiry_date_input.setDisplayFormat("yyyy-MM-dd")
        self.expiry_date_input.setMinimumHeight(36)
        self.form_layout.addRow(expiry_label, self.expiry_date_input)
        
        # Availability checkbox
        availability_label = QtWidgets.QLabel("Availability:")
        self.availability_checkbox = QtWidgets.QCheckBox("Product is available for sale")
        self.availability_checkbox.setChecked(True)
        self.form_layout.addRow(availability_label, self.availability_checkbox)
        
        # Description input (multiline)
        desc_label = QtWidgets.QLabel("Description:")
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setPlaceholderText("Enter product description")
        self.description_input.setMinimumHeight(120)
        self.form_layout.addRow(desc_label, self.description_input)
    
    def populate_data(self):
        """Populate dialog with product data if editing"""
        if self.item:
            # We're editing an existing product
            self.header_label.setText("Edit Product")
            self.name_input.setText(self.item['product_name'])
            self.category_input.setText(self.item.get('category', ''))
            self.description_input.setText(self.item.get('description', ''))
            self.price_input.setValue(float(self.item['price']))
            self.quantity_input.setValue(self.item['quantity'])
            self.threshold_input.setValue(self.item.get('threshold_value', 10))
            
            # Set expiry date if available
            if self.item.get('expiry_date'):
                expiry_date = QtCore.QDate.fromString(str(self.item['expiry_date']), "yyyy-MM-dd")
                self.expiry_date_input.setDate(expiry_date)
            
            # Set availability
            self.availability_checkbox.setChecked(self.item.get('availability', True))
        else:
            # We're adding a new product
            self.header_label.setText("Add New Product")
            # Set default expiry date to one year from now
            default_expiry = QtCore.QDate.currentDate().addYears(1)
            self.expiry_date_input.setDate(default_expiry)
    
    def save_product(self):
        """Save the product to the database"""
        # Validate inputs
        if not self.name_input.text().strip():
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Product name is required.")
            return
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            product_name = self.name_input.text().strip()
            category = self.category_input.text().strip()
            description = self.description_input.toPlainText().strip()
            price = self.price_input.value()
            quantity = self.quantity_input.value()
            threshold = self.threshold_input.value()
            expiry_date = self.expiry_date_input.date().toString("yyyy-MM-dd")
            availability = self.availability_checkbox.isChecked()
            
            if self.item:
                # Update existing product
                cursor.execute(
                    """UPDATE products 
                       SET product_name = %s, 
                           category = %s, 
                           description = %s, 
                           price = %s, 
                           quantity = %s, 
                           threshold_value = %s, 
                           expiry_date = %s, 
                           availability = %s 
                       WHERE product_id = %s""",
                    (product_name, category, description, price, quantity, 
                     threshold, expiry_date, availability, self.item['product_id'])
                )
                
                # Update inventory record if it exists
                cursor.execute(
                    """INSERT INTO inventory (product_id, quantity, status, last_updated) 
                       VALUES (%s, %s, %s, NOW())
                       ON DUPLICATE KEY UPDATE 
                       quantity = VALUES(quantity),
                       last_updated = NOW()""",
                    (self.item['product_id'], quantity, "Updated")
                )
            else:
                # Insert new product
                cursor.execute(
                    """INSERT INTO products 
                       (product_name, category, description, price, quantity, 
                        threshold_value, expiry_date, availability) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (product_name, category, description, price, quantity, 
                     threshold, expiry_date, availability)
                )
                
                # Get the ID of the new product
                product_id = cursor.lastrowid
                
                # Create initial inventory entry
                cursor.execute(
                    "INSERT INTO inventory (product_id, quantity, status) VALUES (%s, %s, %s)",
                    (product_id, quantity, "New")
                )
            
            conn.commit()
            cursor.close()
            
            self.accept()
            
        except mysql.connector.Error as err:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Error saving product: {err}")


class ServiceDialog(BaseDialog):
    """Dialog for adding or editing services"""
    
    def __init__(self, parent=None, service=None):
        super(ServiceDialog, self).__init__(parent, service, "Service")
        self.setup_ui()
        self.populate_data()
    
    def setup_ui(self):
        """Set up the service dialog UI"""
        self.setup_base_ui(550)  # Services need a shorter dialog
        
        self.save_button.setText("Save Service")
        self.save_button.clicked.connect(self.save_service)
        
        # Name input
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
        self.price_input.setPrefix("$ ")
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
            # We're editing an existing service
            self.header_label.setText("Edit Service")
            self.name_input.setText(self.item['service_name'])
            self.category_input.setText(self.item.get('category', ''))
            self.description_input.setText(self.item.get('description', ''))
            self.price_input.setValue(float(self.item['price']))
            
            # Set availability
            self.availability_checkbox.setChecked(self.item.get('availability', True))
        else:
            # We're adding a new service
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


class InventoryPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(InventoryPage, self).__init__(parent, title="Inventory", user_info=user_info)
        self.load_products()
        self.load_services()
    
    def createContent(self):
        # Content area with reduced margins for more space
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(8)
        
        # Create tabs for Products and Inventory with improved styling
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet(StyleFactory.get_tab_style())
        
        # Create and configure tabs
        self.setup_products_tab()
        self.setup_services_tab()
        self.setup_inventory_status_tab()
        
        # Add the tab widget to the main layout
        self.content_layout.addWidget(self.tabs)
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
        
        # Connect the tab change signal
        self.tabs.currentChanged.connect(self.handle_tab_change)
    
    def setup_products_tab(self):
        """Setup the Products tab"""
        self.products_tab = QtWidgets.QWidget()
        self.products_layout = QtWidgets.QVBoxLayout(self.products_tab)
        self.products_layout.setContentsMargins(10, 15, 10, 10)
        self.products_layout.setSpacing(10)
        
        # Create search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search products...")
        
        # Create control panel using factory
        control_layout = ControlPanelFactory.create_search_control(
            self.search_input, 
            "+ Add Product", 
            self.show_add_product_dialog,
            self.filter_products
        )
        self.products_layout.addLayout(control_layout)
        
        # Create products table
        self.products_table = TableFactory.create_table()
        
        # Define column headers and their relative widths
        product_columns = [
            ("ID", 0.05),
            ("Name", 0.15),
            ("Category", 0.10),
            ("Price", 0.07),
            ("Quantity", 0.07),
            ("Threshold", 0.07),
            ("Expiry Date", 0.11),
            ("Availability", 0.10),
            ("Description", 0.28)  # Slightly reduced to ensure total is ~1.0
        ]
        
        # Configure the table columns
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.products_table, product_columns, screen_width)
        
        # Add context menu to the table
        self.products_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.products_table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.products_layout.addWidget(self.products_table)
        
        # Add Products tab to the tab widget
        self.tabs.addTab(self.products_tab, "Products")

    def setup_services_tab(self):
        """Setup the Services tab"""
        self.services_tab = QtWidgets.QWidget()
        self.services_layout = QtWidgets.QVBoxLayout(self.services_tab)
        self.services_layout.setContentsMargins(10, 15, 10, 10)
        self.services_layout.setSpacing(10)
        
        # Create search input
        self.services_search_input = QtWidgets.QLineEdit()
        self.services_search_input.setPlaceholderText("Search services...")
        
        # Create control panel using factory
        services_control_layout = ControlPanelFactory.create_search_control(
            self.services_search_input,
            "+ Add Service",
            self.show_add_service_dialog,
            self.filter_services
        )
        self.services_layout.addLayout(services_control_layout)
        
        # Create services table
        self.services_table = TableFactory.create_table()
        
        # Define column headers and their relative widths
        service_columns = [
            ("ID", 0.05),
            ("Name", 0.20),
            ("Category", 0.15),
            ("Price", 0.10),
            ("Availability", 0.12),
            ("Description", 0.38)  # Increased to use remaining space
        ]
        
        # Configure the table columns
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.services_table, service_columns, screen_width)
        
        # Add context menu to the services table
        self.services_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.services_table.customContextMenuRequested.connect(self.show_service_context_menu)
        
        self.services_layout.addWidget(self.services_table)
        
        # Add Services tab to the tab widget
        self.tabs.addTab(self.services_tab, "Services")

    def setup_inventory_status_tab(self):
        """Setup the Inventory Status tab"""
        self.inventory_tab = QtWidgets.QWidget()
        self.inventory_layout = QtWidgets.QVBoxLayout(self.inventory_tab)
        self.inventory_layout.setContentsMargins(10, 15, 10, 10)
        self.inventory_layout.setSpacing(15)
        
        # Add inventory analytics section
        analytics_layout = QtWidgets.QHBoxLayout()
        analytics_layout.setSpacing(15)
        
        # Create info cards
        low_stock_card = self.create_info_card("Low Stock Items", "0", "#FF5252", "warning")
        expired_card = self.create_info_card("Expired Items", "0", "#FF9800", "expired")
        total_card = self.create_info_card("Total Products", "0", "#4CAF50", "products")
        
        analytics_layout.addWidget(low_stock_card)
        analytics_layout.addWidget(expired_card)
        analytics_layout.addWidget(total_card)
        
        self.inventory_layout.addLayout(analytics_layout)
        
        # Create inventory table
        self.inventory_table = TableFactory.create_table()
        
        # Define column headers and their relative widths
        inventory_columns = [
            ("ID", 0.05),
            ("Product Name", 0.35),  # Increased
            ("Quantity", 0.15),
            ("Status", 0.20),
            ("Last Updated", 0.25)
        ]
        
        # Configure the table columns
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.inventory_table, inventory_columns, screen_width)
        
        self.inventory_layout.addWidget(self.inventory_table)
        
        # Add Inventory tab to the tab widget
        self.tabs.addTab(self.inventory_tab, "Inventory Status")
    
    def create_info_card(self, title, value, color, icon_type=None):
        """Create an info card for the inventory dashboard with icons"""
        card = QtWidgets.QFrame()
        card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #232323;
                border-radius: 10px;
                border-left: 5px solid {color};
                padding: 10px;
                min-height: 100px;
            }}
        """)
        
        card_layout = QtWidgets.QHBoxLayout(card)
        card_layout.setContentsMargins(15, 10, 15, 10)
        
        # Add icon based on card type
        icon_label = QtWidgets.QLabel()
        icon_path = ""
        
        if icon_type == "warning":
            icon_path = "app/resources/images/warning.png"
        elif icon_type == "expired":
            icon_path = "app/resources/images/expired.png"
        elif icon_type == "products":
            icon_path = "app/resources/images/products.png"
        
        # If icon exists, show it
        if icon_path and QtCore.QFile(icon_path).exists():
            icon_label.setPixmap(QtGui.QPixmap(icon_path).scaledToHeight(40))
        else:
            # Create a colored circle if icon doesn't exist
            icon_label.setText("●")
            icon_label.setStyleSheet(f"""
                color: {color};
                font-size: 40px;
            """)
        
        icon_label.setFixedSize(50, 50)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Text content
        text_layout = QtWidgets.QVBoxLayout()
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            color: #AAAAAA;
            font-size: 14px;
            font-weight: bold;
        """)
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet(f"""
            color: {color};
            font-size: 28px;
            font-weight: bold;
        """)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        
        # Add icon and text to card layout
        card_layout.addWidget(icon_label)
        card_layout.addLayout(text_layout, 1)
        
        # Store the value label to update it later
        card.value_label = value_label
        
        return card
    
    def handle_tab_change(self, index):
        """Handle changing between tabs"""
        if index == 1:  # Services tab
            self.load_services()
        elif index == 2:  # Inventory Status tab
            self.load_inventory()
            self.update_inventory_analytics()
    
    def load_products(self):
        """Load products from the database and populate the table"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.products_table.setRowCount(0)
            
            # Reset search filter
            self.search_input.clear()
            
            # Query for all products
            cursor.execute("SELECT * FROM products ORDER BY product_name")
            products = cursor.fetchall()
            
            # Populate the table
            self.products_table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                # Set item with proper alignment
                id_item = QtWidgets.QTableWidgetItem(str(product['product_id']))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.products_table.setItem(row, 0, id_item)
                
                self.products_table.setItem(row, 1, QtWidgets.QTableWidgetItem(product['product_name']))
                self.products_table.setItem(row, 2, QtWidgets.QTableWidgetItem(product.get('category', '')))
                
                # Price with better formatting and alignment
                price_item = QtWidgets.QTableWidgetItem(f"${product['price']:.2f}")
                price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.products_table.setItem(row, 3, price_item)
                
                # Quantity with center alignment
                qty_item = QtWidgets.QTableWidgetItem(str(product['quantity']))
                qty_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.products_table.setItem(row, 4, qty_item)
                
                # Threshold with center alignment
                threshold_item = QtWidgets.QTableWidgetItem(str(product.get('threshold_value', 0)))
                threshold_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.products_table.setItem(row, 5, threshold_item)
                
                # Format expiry date
                expiry_date = product.get('expiry_date')
                expiry_str = expiry_date.strftime('%Y-%m-%d') if expiry_date else "N/A"
                expiry_item = QtWidgets.QTableWidgetItem(expiry_str)
                expiry_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.products_table.setItem(row, 6, expiry_item)
                
                # Format availability with color indicators
                availability = "In Stock" if product.get('availability', True) else "Out of Stock"
                availability_item = QtWidgets.QTableWidgetItem(availability)
                availability_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                # Set color based on availability
                if product.get('availability', True):
                    availability_item.setForeground(QtGui.QColor("#4CAF50"))  # Green for in stock
                else:
                    availability_item.setForeground(QtGui.QColor("#FF5252"))  # Red for out of stock
                    
                self.products_table.setItem(row, 7, availability_item)
                
                # Description
                self.products_table.setItem(row, 8, QtWidgets.QTableWidgetItem(product.get('description', '')))
            
            cursor.close()
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
    def load_services(self):
        """Load services from the database and populate the table"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.services_table.setRowCount(0)
            
            # Reset search filter
            self.services_search_input.clear()
            
            # Query for all services
            cursor.execute("SELECT * FROM services ORDER BY service_name")
            services = cursor.fetchall()
            
            # Populate the table
            self.services_table.setRowCount(len(services))
            
            for row, service in enumerate(services):
                # Set item with proper alignment
                id_item = QtWidgets.QTableWidgetItem(str(service['service_id']))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.services_table.setItem(row, 0, id_item)
                
                self.services_table.setItem(row, 1, QtWidgets.QTableWidgetItem(service['service_name']))
                self.services_table.setItem(row, 2, QtWidgets.QTableWidgetItem(service.get('category', '')))
                
                # Price with better formatting and alignment
                price_item = QtWidgets.QTableWidgetItem(f"${service['price']:.2f}")
                price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.services_table.setItem(row, 3, price_item)
                
                # Availability
                availability_status = "Available" if service.get('availability', 0) else "Unavailable"
                availability_item = QtWidgets.QTableWidgetItem(availability_status)
                availability_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                # Set color based on availability
                if service.get('availability', 0):
                    availability_item.setForeground(QtGui.QColor(0, 170, 0))  # Green for available
                else:
                    availability_item.setForeground(QtGui.QColor(200, 0, 0))  # Red for unavailable
                
                self.services_table.setItem(row, 4, availability_item)
                
                # Description
                self.services_table.setItem(row, 5, QtWidgets.QTableWidgetItem(service.get('description', '')))
        
            cursor.close()
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
    def load_inventory(self):
        """Load inventory data from the database"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.inventory_table.setRowCount(0)
            
            # Query for inventory items with product names
            cursor.execute("""
                SELECT i.inventory_id, p.product_name, i.quantity, i.status, i.last_updated
                FROM inventory i
                JOIN products p ON i.product_id = p.product_id
                ORDER BY i.last_updated DESC
            """)
            
            inventory_items = cursor.fetchall()
            
            # Populate the table
            self.inventory_table.setRowCount(len(inventory_items))
            
            for row, item in enumerate(inventory_items):
                self.inventory_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item['inventory_id'])))
                self.inventory_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item['product_name']))
                self.inventory_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item['quantity'])))
                self.inventory_table.setItem(row, 3, QtWidgets.QTableWidgetItem(item['status'] or "N/A"))
                
                # Format last updated date
                last_updated = item.get('last_updated')
                last_updated_str = last_updated.strftime('%Y-%m-%d %H:%M') if last_updated else "N/A"
                self.inventory_table.setItem(row, 4, QtWidgets.QTableWidgetItem(last_updated_str))
            
            cursor.close()
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
    def update_inventory_analytics(self):
        """Update inventory analytics cards"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get total products count
            cursor.execute("SELECT COUNT(*) as count FROM products")
            total_count = cursor.fetchone()['count']
            
            # Get low stock items count
            cursor.execute("""
                SELECT COUNT(*) as count FROM products 
                WHERE quantity <= threshold_value
            """)
            low_stock_count = cursor.fetchone()['count']
            
            # Get expired items count
            cursor.execute("""
                SELECT COUNT(*) as count FROM products 
                WHERE expiry_date IS NOT NULL AND expiry_date < CURDATE()
            """)
            expired_count = cursor.fetchone()['count']
            
            # Update the info cards
            for card in self.findChildren(QtWidgets.QFrame):
                if hasattr(card, 'value_label'):
                    # Get the text layout which is the second item (index 1) in card layout
                    text_layout = card.layout().itemAt(1).layout()
                    if text_layout:
                        # Get the title label which is the first widget in the text layout
                        title_label = text_layout.itemAt(0).widget()
                        if title_label.text() == "Low Stock Items":
                            card.value_label.setText(str(low_stock_count))
                        elif title_label.text() == "Expired Items":
                            card.value_label.setText(str(expired_count))
                        elif title_label.text() == "Total Products":
                            card.value_label.setText(str(total_count))
        
            cursor.close()
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
    def filter_items(self, table, search_text):
        """Generic function to filter items in a table based on search text"""
        search_text = search_text.lower()
        
        for row in range(table.rowCount()):
            match_found = False
            
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
            
            # Show/hide row based on match
            table.setRowHidden(row, not match_found)
    
    def filter_products(self):
        """Filter products based on search input"""
        self.filter_items(self.products_table, self.search_input.text())
    
    def filter_services(self):
        """Filter services based on search input"""
        self.filter_items(self.services_table, self.services_search_input.text())
    
    def show_context_menu(self, position):
        """Show context menu for product actions"""
        self.show_item_context_menu(self.products_table, position, self.edit_product, self.delete_product)
    
    def show_service_context_menu(self, position):
        """Show context menu for service actions"""
        self.show_item_context_menu(self.services_table, position, self.edit_service, self.delete_service)
    
    def show_item_context_menu(self, table, position, edit_callback, delete_callback):
        """Generic function to show context menu for table actions"""
        context_menu = QtWidgets.QMenu()
        
        # Get the current row
        current_row = table.currentRow()
        
        if current_row >= 0:
            edit_action = context_menu.addAction("Edit")
            delete_action = context_menu.addAction("Delete")
            
            # Show the context menu
            action = context_menu.exec_(table.mapToGlobal(position))
            
            if action == edit_action:
                edit_callback(current_row)
            elif action == delete_action:
                delete_callback(current_row)
    
    def show_add_product_dialog(self):
        """Show dialog to add a new product"""
        dialog = ProductDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_products()
            # Reset row visibility
            for row in range(self.products_table.rowCount()):
                self.products_table.setRowHidden(row, False)
    
    def show_add_service_dialog(self):
        """Show dialog to add a new service"""
        dialog = ServiceDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_services()
            # Reset row visibility
            for row in range(self.services_table.rowCount()):
                self.services_table.setRowHidden(row, False)

    def edit_product(self, row):
        """Edit the selected product"""
        product_id = int(self.products_table.item(row, 0).text())
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            product = cursor.fetchone()
            
            if product:
                dialog = ProductDialog(self, product)
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    self.load_products()
                    
            # Reset row visibility
            for row in range(self.products_table.rowCount()):
                self.products_table.setRowHidden(row, False)
            
            cursor.close()
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
    def edit_service(self, row):
        """Edit the selected service"""
        service_id = int(self.services_table.item(row, 0).text())
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM services WHERE service_id = %s", (service_id,))
            service = cursor.fetchone()
            
            if service:
                dialog = ServiceDialog(self, service)
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    self.load_services()
                
            # Reset row visibility
            for row in range(self.services_table.rowCount()):
                self.services_table.setRowHidden(row, False)
        
            cursor.close()
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")

    def delete_item(self, table, row, id_column, name_column, confirm_message, delete_query, success_message, reload_callback):
        """Generic function to delete an item"""
        item_id = int(table.item(row, 0).text())
        item_name = table.item(row, name_column).text()
        
        # Confirm deletion
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Deletion",
            confirm_message.format(item_name),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if confirm == QtWidgets.QMessageBox.Yes:
            try:
                conn = DBManager.get_connection()
                cursor = conn.cursor()
                
                # Delete the item
                cursor.execute(delete_query, (item_id,))
                
                conn.commit()
                cursor.close()
                
                # Refresh the list
                reload_callback()
                
                # Show success message
                QtWidgets.QMessageBox.information(
                    self,
                    "Success",
                    success_message.format(item_name)
                )
                
            except mysql.connector.Error as err:
                self.show_error_message(f"Database error: {err}")

    def delete_product(self, row):
        """Delete the selected product"""
        product_id = int(self.products_table.item(row, 0).text())
        product_name = self.products_table.item(row, 1).text()
        
        # Confirm deletion
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete product: {product_name}?\n\nThis will also delete all inventory records for this product.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if confirm == QtWidgets.QMessageBox.Yes:
            try:
                conn = DBManager.get_connection()
                cursor = conn.cursor()
                
                # First delete inventory records
                cursor.execute("DELETE FROM inventory WHERE product_id = %s", (product_id,))
                
                # Then delete the product
                cursor.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
                
                conn.commit()
                cursor.close()
                
                # Refresh the product list
                self.load_products()
                
                # Show success message
                QtWidgets.QMessageBox.information(
                    self,
                    "Success",
                    f"Product '{product_name}' has been deleted successfully."
                )
                
            except mysql.connector.Error as err:
                self.show_error_message(f"Database error: {err}")
    
    def delete_service(self, row):
        """Delete the selected service"""
        # Use the generic delete_item function
        self.delete_item(
            table=self.services_table,
            row=row,
            id_column=0,
            name_column=1,
            confirm_message="Are you sure you want to delete service: {}?",
            delete_query="DELETE FROM services WHERE service_id = %s",
            success_message="Service '{}' has been deleted successfully.",
            reload_callback=self.load_services
        )
    
    def show_error_message(self, message):
        """Show error message dialog"""
        QtWidgets.QMessageBox.critical(self, "Error", message)