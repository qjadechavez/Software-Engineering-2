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
        # Track selected services (max 3)
        self.selected_services = []
        self.max_services = 3
        self.setup_ui()
        self.load_services()
    
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 10)
        self.layout.setSpacing(10)
        
        # Create search input first
        self.search_input = QtWidgets.QLineEdit()
        
        # Then use it in the control panel with filter button
        self.control_layout = ControlPanelFactory.create_search_control(
            self.search_input,
            self.filter_services,
            self.show_service_filter_dialog 
        )
        
        self.filter_button = self.control_layout.filter_button
        self.filter_indicator = self.control_layout.filter_indicator
        
        self.layout.addLayout(self.control_layout)
        
        # Header
        header_label = QtWidgets.QLabel("Select Services (Up to 3)")
        header_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.layout.addWidget(header_label)
        
        # Description
        desc_label = QtWidgets.QLabel("Select up to 3 services from the available options below:")
        desc_label.setStyleSheet("color: #cccccc; font-size: 14px;")
        self.layout.addWidget(desc_label)
        
        # Main content area - 2 column layout
        main_content_layout = QtWidgets.QHBoxLayout()
        main_content_layout.setSpacing(20)
        
        # LEFT COLUMN - Services grid
        left_column = QtWidgets.QVBoxLayout()
        
        # Services container with background and improved grid layout
        self.services_container = QtWidgets.QWidget()
        # use the top‐level StyleFactory import
        self.services_container.setStyleSheet(StyleFactory.get_services_grid_style())
        self.services_grid = QtWidgets.QGridLayout(self.services_container)
        self.services_grid.setContentsMargins(20, 20, 20, 20)
        self.services_grid.setSpacing(15)  # Reduced spacing to fit more cards
        self.services_grid.setAlignment(QtCore.Qt.AlignTop)
        
        # Scroll area for services
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.services_container)
        scroll_area.setStyleSheet(StyleFactory.get_scroll_area_style())
        scroll_area.setMinimumHeight(400)
        
        left_column.addWidget(scroll_area)
        
        # Add filter indicator to left column
        self.filter_indicator = QtWidgets.QLabel()
        self.filter_indicator.setStyleSheet("color: #4FC3F7; font-style: italic; padding-top: 5px;")
        self.filter_indicator.setVisible(False)
        left_column.addWidget(self.filter_indicator)
        
        # RIGHT COLUMN - Selected services info (always visible but content changes)
        right_column = QtWidgets.QVBoxLayout()
        
        # Selected services info frame
        self.selected_services_frame = QtWidgets.QFrame()
        self.selected_services_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.selected_services_frame.setStyleSheet(StyleFactory.get_selected_services_frame_style())
        self.selected_services_frame.setMinimumWidth(350)
        self.selected_services_frame.setMaximumWidth(400)
        self.selected_services_frame.setMinimumHeight(400)
        
        
        # Selected services layout
        selected_layout = QtWidgets.QVBoxLayout(self.selected_services_frame)
        selected_layout.setSpacing(15)
        selected_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        selected_header = QtWidgets.QLabel("Selected Services")
        selected_header.setStyleSheet("color: white; font-size: 18px; font-weight: bold; border: none;")
        selected_layout.addWidget(selected_header)
        
        # Services counter
        self.services_counter = QtWidgets.QLabel("0 / 3 services selected")
        self.services_counter.setStyleSheet("color: #4FC3F7; font-size: 14px; border: none;")
        selected_layout.addWidget(self.services_counter)
        
        # Selected services list widget
        self.selected_services_list = QtWidgets.QListWidget()
        self.selected_services_list.setStyleSheet(StyleFactory.get_selected_services_list_style())
        self.selected_services_list.setMinimumHeight(150) 
        self.selected_services_list.setMaximumHeight(200)
        selected_layout.addWidget(self.selected_services_list)
        
        # Total price
        self.total_price_label = QtWidgets.QLabel("Total: ₱0.00")
        self.total_price_label.setStyleSheet("color: #4CAF50; font-weight: bold; font-size: 20px; margin: 10px 0; border: none;")
        selected_layout.addWidget(self.total_price_label)
        
        # Products used section
        products_header = QtWidgets.QLabel("Products Required:")
        products_header.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-top: 10px; border: none;")
        selected_layout.addWidget(products_header)
        
        self.products_list = QtWidgets.QListWidget()
        self.products_list.setStyleSheet(StyleFactory.get_products_list_style())
        self.products_list.setMinimumHeight(100)
        self.products_list.setMaximumHeight(150)
        selected_layout.addWidget(self.products_list)
        
        # Continue button
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        
        self.continue_button = ControlPanelFactory.create_action_button("Continue")
        self.continue_button.setEnabled(False)
        self.continue_button.clicked.connect(self.continue_to_customer)
        button_layout.addWidget(self.continue_button)
        
        selected_layout.addLayout(button_layout)
        selected_layout.addStretch()
        
        right_column.addWidget(self.selected_services_frame)
        right_column.addStretch()
        
        # Add columns to main content layout (70% left, 30% right)
        main_content_layout.addLayout(left_column, 7)
        main_content_layout.addLayout(right_column, 3)
        
        self.layout.addLayout(main_content_layout)
        
        
        # At the bottom of the page, add a cancel transaction button
        cancel_layout = QtWidgets.QHBoxLayout()

         # unified secondary button style
        self.close_button = QtWidgets.QPushButton("Cancel Transaction")
        self.close_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
        self.close_button.clicked.connect(self.cancel_transaction)
         
        cancel_layout.addStretch()
        cancel_layout.addWidget(self.close_button)
        self.layout.addLayout(cancel_layout)
        
        # Initialize with empty state message
        self.show_empty_state()
    
    def show_empty_state(self):
        """Show message when no services are selected"""
        self.selected_services_list.clear()
        empty_item = QtWidgets.QListWidgetItem("No services selected yet...")
        empty_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.selected_services_list.addItem(empty_item)
        
        self.products_list.clear()
        empty_products_item = QtWidgets.QListWidgetItem("Select services to see required products")
        empty_products_item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.products_list.addItem(empty_products_item)
    
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
            
            # Add services to the grid (5 columns for better space utilization)
            row, col = 0, 0
            max_cols = 6  # Increased to 5 columns to use more space
            
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
        """Create a service card widget with improved design - no inner borders"""
        card = QtWidgets.QFrame()
        card.setFrameShape(QtWidgets.QFrame.NoFrame)  # Remove frame shape
        
        # Check if service is already selected
        is_selected = any(s['service_id'] == service['service_id'] for s in self.selected_services)
        
        if is_selected:
            card.setStyleSheet(StyleFactory.get_service_card_selected_style())
        else:
            card.setStyleSheet(StyleFactory.get_service_card_style())
            
        card.setFixedSize(180, 140)  # Adjusted size for 5-column layout
        card.setCursor(QtCore.Qt.PointingHandCursor)
        
        # Store service data in the widget
        card.service_data = service
        card.is_selected = is_selected
        
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)  # Reduced margins
        layout.setSpacing(5)  # Reduced spacing
        
        # Service name - no borders
        name_label = QtWidgets.QLabel(service['service_name'])
        name_label.setStyleSheet("""
            color: white; 
            font-weight: bold; 
            font-size: 13px;
            border: none;
            background: transparent;
        """)
        name_label.setWordWrap(True)
        name_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(name_label)
        
        # Category with improved styling - no borders
        category_label = QtWidgets.QLabel(f"Category: {service['category']}")
        category_label.setStyleSheet("""
            color: #B0BEC5; 
            font-size: 10px;
            border: none;
            background: transparent;
        """)
        category_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(category_label)
        
        # Price with better prominence - no borders
        price_label = QtWidgets.QLabel(f"₱{float(service['price']):.2f}")
        price_label.setStyleSheet("""
            color: #4CAF50; 
            font-weight: bold; 
            font-size: 15px;
            border: none;
            background: transparent;
        """)
        price_label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(price_label)
        
        # Selection indicator - no borders
        if is_selected:
            selected_indicator = QtWidgets.QLabel("✓ Selected")
            selected_indicator.setStyleSheet("""
                color: #4CAF50; 
                font-weight: bold; 
                font-size: 10px;
                border: none;
                background: transparent;
            """)
            selected_indicator.setAlignment(QtCore.Qt.AlignCenter)
            layout.addWidget(selected_indicator)
        else:
            # Add spacer for consistent sizing
            layout.addStretch()
        
        # Add click event
        card.mousePressEvent = lambda event: self.toggle_service_selection(service, card)
        
        return card
    
    def toggle_service_selection(self, service, card):
        """Handle service selection/deselection"""
        service_id = service['service_id']
        
        # Check if service is already selected
        existing_service = next((s for s in self.selected_services if s['service_id'] == service_id), None)
        
        if existing_service:
            # Remove from selection
            self.selected_services.remove(existing_service)
        else:
            # Check if we can add more services
            if len(self.selected_services) >= self.max_services:
                QtWidgets.QMessageBox.warning(
                    self, 
                    "Selection Limit", 
                    f"You can only select up to {self.max_services} services."
                )
                return
            
            # Add to selection
            self.selected_services.append(service)
        
        # Update UI
        self.update_selected_services_display()
        self.refresh_service_cards()
        
        # Set transaction in progress if services are selected
        if self.selected_services:
            self.parent.transaction_in_progress = True
            if hasattr(self.parent, 'parent') and self.parent.parent and hasattr(self.parent.parent, 'disable_navigation'):
                self.parent.parent.disable_navigation()
    
    def refresh_service_cards(self):
        """Refresh all service cards to show correct selection state"""
        for i in range(self.services_grid.count()):
            item = self.services_grid.itemAt(i)
            if item and item.widget():
                card = item.widget()
                if hasattr(card, 'service_data'):
                    service = card.service_data
                    is_selected = any(s['service_id'] == service['service_id'] for s in self.selected_services)
                    
                    # Update card styling
                    if is_selected:
                        card.setStyleSheet(StyleFactory.get_service_card_selected_style())
                    else:
                        card.setStyleSheet(StyleFactory.get_service_card_style())
                    
                    # Update selection indicator
                    card.is_selected = is_selected
                    # Recreate the card to update the indicator
                    row = i // 5  # Changed to 5 columns
                    col = i % 5
                    new_card = self.create_service_card(service)
                    self.services_grid.replaceWidget(card, new_card)
                    card.deleteLater()
    
    def update_selected_services_display(self):
        """Update the selected services display"""
        # Update counter
        count = len(self.selected_services)
        self.services_counter.setText(f"{count} / {self.max_services} services selected")
        
        # Update selected services list
        self.selected_services_list.clear()
        total_price = 0
        
        if count == 0:
            self.show_empty_state()
        else:
            for service in self.selected_services:
                price = float(service['price'])
                total_price += price
                
                item_text = f"{service['service_name']} - ₱{price:.2f}"
                list_item = QtWidgets.QListWidgetItem(item_text)
                
                # Add remove button functionality (double-click to remove)
                list_item.setToolTip("Double-click to remove this service")
                self.selected_services_list.addItem(list_item)
            
            # Load all required products
            self.load_all_service_products()
        
        # Update total price
        self.total_price_label.setText(f"Total: ₱{total_price:.2f}")
    
        # Enable/disable continue button based on selection
        if count == 0:
            self.continue_button.setEnabled(False)
        else:
            self.continue_button.setEnabled(True)
        
        # Update parent invoice data
        if self.parent:
            self.parent.invoice_data["services"] = self.selected_services
            self.parent.invoice_data["total_service_price"] = total_price
        
        # Connect double-click to remove service
        self.selected_services_list.itemDoubleClicked.connect(self.remove_service_from_list)
    
    def remove_service_from_list(self, item):
        """Remove service when double-clicked in the list"""
        row = self.selected_services_list.row(item)
        if 0 <= row < len(self.selected_services):
            removed_service = self.selected_services.pop(row)
            self.update_selected_services_display()
            self.refresh_service_cards()
    
    def load_all_service_products(self):
        """Load all products required for selected services"""
        if not self.selected_services:
            self.products_list.clear()
            return
            
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get all unique products needed for selected services
            service_ids = [service['service_id'] for service in self.selected_services]
            placeholders = ','.join(['%s'] * len(service_ids))
            
            query = f"""
                SELECT DISTINCT p.product_name, SUM(sp.quantity) as total_quantity
                FROM service_products sp
                JOIN products p ON sp.product_id = p.product_id
                WHERE sp.service_id IN ({placeholders})
                GROUP BY p.product_id, p.product_name
                ORDER BY p.product_name
            """
            
            cursor.execute(query, service_ids)
            products = cursor.fetchall()
            cursor.close()
            
            # Clear existing items
            self.products_list.clear()
            
            # Add products to the list
            for product in products:
                item = QtWidgets.QListWidgetItem(f"{product['product_name']} (Qty: {product['total_quantity']})")
                self.products_list.addItem(item)
            
            # If no products, add a message
            if not products:
                no_products_item = QtWidgets.QListWidgetItem("No products required")
                no_products_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.products_list.addItem(no_products_item)
                
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
        self.selected_services.clear()
        self.continue_button.setEnabled(False)
        self.products_list.clear()
        self.selected_services_list.clear()
        self.services_counter.setText("0 / 3 services selected")
        self.total_price_label.setText("Total: ₱0.00")
        self.show_empty_state()
        self.refresh_service_cards()

        # reset search & filters
        self.search_input.clear()
        self.filter_state = {
            "is_active": False,
            "category": "All Categories",
            "price_range": "All Prices"
        }
        self.filter_indicator.setVisible(False)
        self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))

        # reload all service cards
        self.load_services()
    
    def cancel_transaction(self):
        """Cancel the current transaction"""
        # Reset selections
        self.reset()
        
        # Enable navigation
        if self.parent and hasattr(self.parent, 'cancel_transaction'):
            self.parent.cancel_transaction()
        else:
            # Fallback if parent doesn't have the method
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
                # Try to find the service name in the widget
                service_name = ""
                for child in widget.findChildren(QtWidgets.QLabel):
                    if child.text() and not child.text().startswith("₱") and not child.text().startswith("Category:") and not child.text().startswith("✓"):
                        service_name = child.text().lower()
                        break
                        
                # Show/hide based on search text
                widget.setVisible(search_text == "" or search_text in service_name)
    
    def show_service_filter_dialog(self):
        """Show advanced filter dialog for services"""
        filter_dialog = ServiceFilterDialog(self, self.filter_state)
        if filter_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Get the filter state from the dialog
            new_filter_state = filter_dialog.get_filter_state()
            
            # Update our filter state
            self.filter_state = new_filter_state
            
            # Check if filters were reset or are not active
            if not self.filter_state["is_active"]:
                # Filters were reset or cleared
                self.filter_indicator.setVisible(False)
                # Update button appearance to normal state
                self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
                
                # Reload all services
                self.load_services()
            else:
                # Apply filters and update button to active state (blue)
                self.filter_button.setStyleSheet(StyleFactory.get_button_style())
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
                show_card = True
                
                # Get service data from stored attribute
                if hasattr(widget, "service_data"):
                    service_data = widget.service_data
                    
                    # Apply category filter
                    if service_category != "All Categories" and service_data.get("category") != service_category:
                        show_card = False
                    
                    # Apply price range filter
                    if price_range != "All Prices" and show_card:
                        price = float(service_data.get("price", 0))
                        
                        if price_range == "Under ₱500" and price >= 500:
                            show_card = False
                        elif price_range == "₱500 - ₱1000" and (price < 500 or price > 1000):
                            show_card = False
                        elif price_range == "₱1000 - ₱2000" and (price < 1000 or price > 2000):
                            show_card = False
                        elif price_range == "Over ₱2000" and price <= 2000:
                            show_card = False
                
                # Show/hide card based on filters
                widget.setVisible(show_card)
