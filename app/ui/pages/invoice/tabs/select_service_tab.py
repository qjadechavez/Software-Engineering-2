from PyQt5 import QtWidgets, QtCore
from app.utils.db_manager import DBManager
import mysql.connector
from ..style_factory import StyleFactory
from ..control_panel_factory import ControlPanelFactory
from ..dialogs.service_filter_dialog import ServiceFilterDialog

class SelectServiceTab(QtWidgets.QWidget):
    """Tab for selecting a service"""
    
    def __init__(self, parent=None):
        super(SelectServiceTab, self).__init__()
        self.parent = parent
        # Initialize filter state
        self.filter_state = {
            "is_active": False,
            "category": "All Categories",
            "price_range": "All Prices"
        }
        self.setup_ui()
        self.load_services()
    
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 10)
        self.layout.setSpacing(10)
        
        # Create search input first
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search services...")
        self.search_input.textChanged.connect(self.filter_services)
        
        # Then use it in the control panel with filter button
        control_layout = ControlPanelFactory.create_search_control(
            self.search_input,
            self.filter_services,  # search_callback parameter
            self.show_service_filter_dialog  # filter_callback parameter
        )
        self.layout.addLayout(control_layout)
        
        # Store reference to filter button
        self.filter_button = control_layout.itemAt(2).widget()
        
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
        
        self.continue_button = ControlPanelFactory.create_action_button("Continue to Customer Info")
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
        
        # Add filter indicator label at the bottom
        self.filter_indicator = QtWidgets.QLabel()
        self.filter_indicator.setStyleSheet("color: #4FC3F7; font-style: italic; padding-top: 5px;")
        self.filter_indicator.setVisible(False)
        self.layout.addWidget(self.filter_indicator)

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
                child = self.services_grid.itemAt(i).widget()
                if child:
                    child.setParent(None)
            
            # Add services to the grid
            row, col = 0, 0
            max_cols = 3  # Number of cards per row
            
            for service in services:
                service_card = self.create_service_card(service)
                self.services_grid.addWidget(service_card, row, col)
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
    def create_service_card(self, service):
        """Create a service card widget"""
        card = QtWidgets.QFrame()
        card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: #1c1c1c;
                border-radius: 8px;
                border: 2px solid #444444;
                padding: 10px;
            }
            QFrame:hover {
                border: 2px solid #007ACC;
                background-color: #252525;
            }
        """)
        card.setFixedSize(200, 120)
        card.setCursor(QtCore.Qt.PointingHandCursor)
        
        # Store service data in the widget
        card.service_data = service
        
        layout = QtWidgets.QVBoxLayout(card)
        
        # Service name
        name_label = QtWidgets.QLabel(service['service_name'])
        name_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        name_label.setWordWrap(True)
        layout.addWidget(name_label)
        
        # Category
        category_label = QtWidgets.QLabel(f"Category: {service['category']}")
        category_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        layout.addWidget(category_label)
        
        # Price
        price_label = QtWidgets.QLabel(f"₱{float(service['price']):.2f}")
        price_label.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 16px;")
        layout.addWidget(price_label)
        
        # Add click event
        card.mousePressEvent = lambda event: self.select_service(service)
        
        return card
    
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
    
    def filter_services(self):
        """Filter services based on search input"""
        search_text = self.search_input.text().lower()
        
        # Loop through all service cards in the grid
        for i in range(self.services_grid.count()):
            item = self.services_grid.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                # Check if service data exists in widget
                if hasattr(widget, 'service_data'):
                    service = widget.service_data
                    # Search in service name, category, and description
                    visible = (search_text in service['service_name'].lower() or
                              search_text in service['category'].lower() or
                              search_text in str(service.get('description', '')).lower())
                    widget.setVisible(visible)
                else:
                    widget.setVisible(True)  # Show if no service data
    
    def show_service_filter_dialog(self):
        """Show advanced filter dialog for services"""
        from ..dialogs.service_filter_dialog import ServiceFilterDialog
        filter_dialog = ServiceFilterDialog(self, self.filter_state)
        if filter_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Get the filter state from the dialog
            new_filter_state = filter_dialog.get_filter_state()
            self.filter_state = new_filter_state
            self.apply_filter()
    
    def apply_filter(self):
        """Apply the filters stored in filter_state"""
        # Get current filter settings
        service_category = self.filter_state["category"]
        price_range = self.filter_state["price_range"]
        
        # Update the filter indicator text
        filter_text = []
        if service_category != "All Categories":
            filter_text.append(f"Category: {service_category}")
        if price_range != "All Prices":
            filter_text.append(f"Price: {price_range}")
            
        if filter_text:
            self.filter_indicator.setText(f"Active filters: {', '.join(filter_text)}")
            self.filter_indicator.setVisible(True)
        else:
            self.filter_indicator.setVisible(False)
        
        # Apply filters to service cards
        for i in range(self.services_grid.count()):
            item = self.services_grid.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if hasattr(widget, 'service_data'):
                    service = widget.service_data
                    visible = True
                    
                    # Apply category filter
                    if service_category != "All Categories" and service['category'] != service_category:
                        visible = False
                    
                    # Apply price range filter
                    if price_range != "All Prices" and visible:
                        price = float(service['price'])
                        if price_range == "Under ₱500" and price >= 500:
                            visible = False
                        elif price_range == "₱500 - ₱1000" and (price < 500 or price > 1000):
                            visible = False
                        elif price_range == "Over ₱1000" and price <= 1000:
                            visible = False
                    
                    widget.setVisible(visible)
                else:
                    widget.setVisible(True)
    
    def get_service_data_from_widget(self, widget):
        """Extract service data from a card widget"""
        # First try to access the stored service data if available (better method)
        if hasattr(widget, "service_data"):
            return widget.service_data
        
        # Fallback to extracting data from labels
        service_data = {}
        for child in widget.findChildren(QtWidgets.QLabel):
            text = child.text()
            if "Category:" in text:
                service_data['category'] = text.replace("Category: ", "")
            elif "₱" in text and "Category" not in text:
                service_data['price'] = text.replace("₱", "")
            elif not any(x in text for x in ["Category:", "₱"]):
                service_data['service_name'] = text
                
        return service_data
