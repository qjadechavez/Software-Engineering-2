from PyQt5 import QtWidgets, QtCore
from app.utils.db_manager import DBManager
import mysql.connector
from ..factories.panel_factory import PanelFactory

class SelectServiceTab(QtWidgets.QWidget):
    """Tab for selecting a service"""
    
    def __init__(self, parent=None):
        super(SelectServiceTab, self).__init__()
        self.parent = parent
        self.setup_ui()
        self.load_services()
    
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Header
        header_label = QtWidgets.QLabel("Select a Service")
        header_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.layout.addWidget(header_label)
        
        # Description
        desc_label = QtWidgets.QLabel("Select one of the available services below:")
        desc_label.setStyleSheet("color: #cccccc; font-size: 14px;")
        self.layout.addWidget(desc_label)
        
        # Services container with grid layout
        self.services_container = QtWidgets.QWidget()
        self.services_grid = QtWidgets.QGridLayout(self.services_container)
        self.services_grid.setContentsMargins(0, 0, 0, 0)
        self.services_grid.setSpacing(15)
        
        # Scroll area for services
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.services_container)
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
        
        self.layout.addWidget(scroll_area)
        
        # Selected service info
        self.selected_service_frame = QtWidgets.QFrame()
        self.selected_service_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.selected_service_frame.setStyleSheet("""
            QFrame {
                background-color: #1c1c1c;
                border-radius: 8px;
                border: 1px solid #444444;
            }
        """)
        self.selected_service_frame.setVisible(False)
        
        selected_layout = QtWidgets.QVBoxLayout(self.selected_service_frame)
        
        selected_header = QtWidgets.QLabel("Selected Service")
        selected_header.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        selected_layout.addWidget(selected_header)
        
        self.selected_service_name = QtWidgets.QLabel()
        self.selected_service_name.setStyleSheet("color: white; font-size: 14px;")
        selected_layout.addWidget(self.selected_service_name)
        
        self.selected_service_price = QtWidgets.QLabel()
        self.selected_service_price.setStyleSheet("color: #4CAF50; font-weight: bold;")
        selected_layout.addWidget(self.selected_service_price)
        
        # Products used section
        products_header = QtWidgets.QLabel("Products Used:")
        products_header.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-top: 10px;")
        selected_layout.addWidget(products_header)
        
        self.products_list = QtWidgets.QListWidget()
        self.products_list.setStyleSheet("""
            QListWidget {
                background-color: #232323;
                border: 1px solid #444444;
                border-radius: 4px;
                color: white;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #333333;
            }
        """)
        self.products_list.setMaximumHeight(150)
        selected_layout.addWidget(self.products_list)
        
        # Continue button
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        
        self.continue_button = PanelFactory.create_action_button("Continue to Customer Info")
        self.continue_button.setEnabled(False)
        self.continue_button.clicked.connect(self.continue_to_customer)
        button_layout.addWidget(self.continue_button)
        
        selected_layout.addLayout(button_layout)
        self.layout.addWidget(self.selected_service_frame)
        
        # At the bottom of the page, add a cancel transaction button
        cancel_layout = QtWidgets.QHBoxLayout()
        
        cancel_button = QtWidgets.QPushButton("Cancel Transaction")
        cancel_button.setStyleSheet("""
            QPushButton {
                padding: 8px 15px;
                background-color: #FF5252;
                color: white;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #FF7373;
            }
        """)
        cancel_button.clicked.connect(self.cancel_transaction)
        
        cancel_layout.addStretch()
        cancel_layout.addWidget(cancel_button)
        
        self.layout.addLayout(cancel_layout)

        # Add stretch to push everything to the top
        self.layout.addStretch()
    
    def load_services(self):
        """Load services from the database"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get all services - Updated to fetch all required fields for transactions
            cursor.execute("""
                SELECT service_id, service_name, category, price, description
                FROM services
                WHERE availability = 1
                ORDER BY category, service_name
            """)
            
            services = cursor.fetchall()
            cursor.close()
            
            # Clear existing services
            for i in reversed(range(self.services_grid.count())):
                self.services_grid.itemAt(i).widget().setParent(None)
            
            # Add services to the grid
            row, col = 0, 0
            max_cols = 3  # Number of cards per row
            
            for service in services:
                card = PanelFactory.create_service_card(service, self.select_service)
                self.services_grid.addWidget(card, row, col)
                
                col += 1
                if col >= max_cols:
                    row += 1
                    col = 0
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
    def select_service(self, service):
        """Handle service selection"""
        # Store complete service object with all needed fields for transactions
        self.parent.invoice_data["service"] = service
        
        # Update the selected service info
        self.selected_service_name.setText(f"Service: {service['service_name']} ({service['category']})")
        self.selected_service_price.setText(f"Price: ₱{float(service['price']):.2f}")
        
        # Show the selected service frame
        self.selected_service_frame.setVisible(True)
        
        # Enable the continue button
        self.continue_button.setEnabled(True)
        
        # Load products used for this service
        self.load_service_products(service['service_id'])
        
        # NOW set the transaction in progress and disable navigation
        self.parent.transaction_in_progress = True
        if hasattr(self.parent, 'parent') and self.parent.parent and hasattr(self.parent.parent, 'disable_navigation'):
            self.parent.parent.disable_navigation()
    
    def load_service_products(self, service_id):
        """Load products used for the selected service"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get products used in this service
            cursor.execute("""
                SELECT p.product_name, sp.quantity
                FROM service_products sp
                JOIN products p ON sp.product_id = p.product_id
                WHERE sp.service_id = %s
            """, (service_id,))
            
            products = cursor.fetchall()
            cursor.close()
            
            # Clear existing items
            self.products_list.clear()
            
            # Add products to the list
            for product in products:
                item = QtWidgets.QListWidgetItem(f"{product['product_name']} (Qty: {product['quantity']})")
                self.products_list.addItem(item)
                
            # If no products, add a message
            if not products:
                self.products_list.addItem("No products used for this service")
                
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
    def continue_to_customer(self):
        """Continue to the customer tab"""
        self.parent.enable_next_tab(0)
        self.parent.tabs.setCurrentIndex(1)
    
    def show_error_message(self, message):
        """Show error message dialog"""
        QtWidgets.QMessageBox.critical(self, "Error", message)
    
    def reset(self):
        """Reset the tab state"""
        self.selected_service_frame.setVisible(False)
        self.continue_button.setEnabled(False)
        self.products_list.clear()
    
    def cancel_transaction(self):
        """Cancel the current transaction"""
        # Even if no service is selected, still enable navigation
        if self.parent and hasattr(self.parent, 'cancel_transaction'):
            self.parent.cancel_transaction()
        else:
            # Fallback if parent doesn't have the method
            # Reset the tab state
            self.reset()
            
            # Try to enable navigation in the main window
            main_window = self.parent
            while main_window:
                if hasattr(main_window, 'enable_navigation'):
                    main_window.enable_navigation()
                    break
                if hasattr(main_window, 'parent'):
                    main_window = main_window.parent
                else:
                    break
