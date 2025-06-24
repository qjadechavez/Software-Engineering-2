from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage
from app.utils.db_manager import DBManager
import mysql.connector
from datetime import datetime

# Import the classes from the inventory folder
from .style_factory import StyleFactory
from .table_factory import TableFactory
from .control_panel_factory import ControlPanelFactory
from .dialogs import ProductDialog, ServiceDialog

class InventoryPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(InventoryPage, self).__init__(parent, title="Inventory", user_info=user_info)
        self.load_products()
        self.load_services()
        self.update_overall_dashboard()

    def createContent(self):
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(8)
        
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet(StyleFactory.get_tab_style())
        
        # Create and configure tabs
        self.setup_products_tab()
        self.setup_services_tab()
        self.setup_inventory_status_tab()
        self.setup_overall_inventory_tab()
        
        # Add the tab widget to the main layout
        self.content_layout.addWidget(self.tabs)
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
        
        # Connect the tab change signal
        self.tabs.currentChanged.connect(self.handle_tab_change)
        
        # Set Overall Inventory tab as the default
        self.tabs.setCurrentIndex(0)

    def handle_tab_change(self, index):
        """Handle changing between tabs"""
        if index == 0:  # Overall Inventory tab
            self.update_overall_dashboard()
        elif index == 2:  # Services tab 
            self.load_services()
        elif index == 3:  # Inventory Status tab
            self.load_inventory()
            self.update_inventory_analytics()
    
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
            self.filter_products,
            self.show_product_filter_dialog
        )
        self.products_layout.addLayout(control_layout)
        
        # Create products table
        self.products_table = TableFactory.create_table()
        
        # Define column headers and their relative widths
        product_columns = [
            ("ID", 0.05),
            ("Name", 0.17),
            ("Category", 0.10),
            ("Price", 0.07),
            ("Quantity", 0.07),
            ("Threshold", 0.07),
            ("Expiry Date", 0.11),
            ("Availability", 0.10),
            ("Description", 0.26)
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
            self.filter_services,
            self.show_service_filter_dialog  # Add filter callback
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
            ("Description", 0.38)
        ]
        
        # Configure the table columns
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.services_table, service_columns, screen_width)
        
        self.services_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.services_table.customContextMenuRequested.connect(self.show_service_context_menu)
        
        self.services_layout.addWidget(self.services_table)
        
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
            ("Product Name", 0.35), 
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
    
    def setup_overall_inventory_tab(self):
        """Setup the Overall Inventory tab with dashboard info"""
        self.overall_tab = QtWidgets.QWidget()
        self.overall_layout = QtWidgets.QVBoxLayout(self.overall_tab)
        self.overall_layout.setContentsMargins(20, 20, 20, 20)
        self.overall_layout.setSpacing(15)
        
        # Create dashboard header
        header_layout = QtWidgets.QHBoxLayout()
        
        # Dashboard title with icon
        title_layout = QtWidgets.QHBoxLayout()
        title_layout.setSpacing(15)
        
        dashboard_icon = QtWidgets.QLabel()
        dashboard_icon.setPixmap(QtGui.QPixmap("app/resources/images/dashboard.png").scaled(24, 24, 
                            QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation) 
                        if QtCore.QFile("app/resources/images/dashboard.png").exists() 
                        else QtGui.QPixmap())

        title_label = QtWidgets.QLabel("Overall Inventory")
        title_label.setStyleSheet("""
            color: white;
            font-size: 22px;
            font-weight: bold;
        """)

        title_layout.addWidget(dashboard_icon)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        # Last updated timestamp
        self.last_updated_label = QtWidgets.QLabel("Last updated: Just now")
        self.last_updated_label.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.last_updated_label)
        
        # Add the header with zero stretch
        self.overall_layout.addLayout(header_layout, 0)
        
        # Create summary cards
        summary_layout = QtWidgets.QHBoxLayout()
        summary_layout.setSpacing(15)
        
        # Create the summary cards
        self.products_summary = self.create_summary_card("Products", "0", "#4CAF50")
        self.categories_summary = self.create_summary_card("Categories", "0", "#2196F3")
        self.services_summary = self.create_summary_card("Services", "0", "#9C27B0")
        self.revenue_summary = self.create_summary_card("Total Value", "$0.00", "#FFC107")
        
        summary_layout.addWidget(self.products_summary)
        summary_layout.addWidget(self.categories_summary)
        summary_layout.addWidget(self.services_summary)
        summary_layout.addWidget(self.revenue_summary)
        
        # Add summary cards with zero stretch factor
        self.overall_layout.addLayout(summary_layout, 0)
        
        # Create metrics section
        metrics_frame = QtWidgets.QFrame()
        metrics_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        metrics_frame.setStyleSheet("""
            QFrame {
                background-color: #232323;
                border-radius: 8px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }
        """)
        
        metrics_layout = QtWidgets.QVBoxLayout(metrics_frame)
        metrics_layout.setContentsMargins(20, 20, 20, 20)
        metrics_layout.setSpacing(15)
        
        # Metrics header - remove border
        metrics_header = QtWidgets.QLabel("Inventory Metrics")
        metrics_header.setStyleSheet("color: white; font-size: 16px; font-weight: bold; border: none;")
        metrics_layout.addWidget(metrics_header)
        
        # Metrics grid - change from 2x2 grid to 1x4 row layout
        metrics_grid = QtWidgets.QHBoxLayout()  # Change from QGridLayout to QHBoxLayout
        metrics_grid.setSpacing(15)
        
        # Create inventory metric items
        self.low_stock_metric = self.create_metric_item("Low Stock Items", "0", "warning", "#FF5252")
        self.expired_metric = self.create_metric_item("Expired Products", "0", "alert", "#FF9800")
        self.out_of_stock_metric = self.create_metric_item("Out of Stock", "0", "error", "#F44336")
        self.top_selling_metric = self.create_metric_item("Top Category", "-", "info", "#03A9F4")
        
        # Add metrics in a row instead of grid positions
        metrics_grid.addWidget(self.low_stock_metric)
        metrics_grid.addWidget(self.expired_metric)
        metrics_grid.addWidget(self.out_of_stock_metric)
        metrics_grid.addWidget(self.top_selling_metric)
        
        metrics_layout.addLayout(metrics_grid)
        
        # Add metrics section with zero stretch factor
        self.overall_layout.addWidget(metrics_frame, 0)
        
        # Recent activity section
        activity_frame = QtWidgets.QFrame()
        activity_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        activity_frame.setStyleSheet("""
            QFrame {
                background-color: #232323;
                border-radius: 8px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }
        """)
        
        activity_layout = QtWidgets.QVBoxLayout(activity_frame)
        activity_layout.setContentsMargins(20, 20, 20, 20)
        
        # Activity header with view all link
        activity_header_layout = QtWidgets.QHBoxLayout()
        
        activity_header = QtWidgets.QLabel("Recent Inventory Changes")
        activity_header.setStyleSheet("color: white; font-size: 16px; font-weight: bold; border: none;")
        
        view_all_link = QtWidgets.QLabel("View All")
        view_all_link.setStyleSheet("color: #2196F3; font-size: 13px; text-decoration: underline; border: none;")
        view_all_link.setCursor(QtCore.Qt.PointingHandCursor)
        view_all_link.mousePressEvent = self.view_all_clicked
        
        activity_header_layout.addWidget(activity_header)
        activity_header_layout.addStretch()
        activity_header_layout.addWidget(view_all_link)
        
        activity_layout.addLayout(activity_header_layout)
        
        # Recent activity table
        self.activity_table = QtWidgets.QTableWidget()
        self.activity_table.setColumnCount(4)
        self.activity_table.setHorizontalHeaderLabels(["Product", "Action", "Quantity", "Date"])
        self.activity_table.setStyleSheet("""
            QTableWidget {
                background-color: transparent;
                border: none;
                gridline-color: #444444;
                color: white;
            }
            QHeaderView::section {
                background-color: #2c2c2c;
                color: white;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #444;
                font-weight: bold;
            }
            QTableWidget::item {
                border-bottom: 1px solid #444444;
                border-right: 1px solid #444444;
                padding: 5px;
            }
        """)

        # Configure the table to fill remaining space
        self.activity_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.activity_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.activity_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.activity_table.setAlternatingRowColors(False)
        self.activity_table.verticalHeader().setVisible(False)
        self.activity_table.setShowGrid(True)

        # Set a sizePolicy that will make the table expand to fill available space
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, 
            QtWidgets.QSizePolicy.Expanding
        )
        self.activity_table.setSizePolicy(size_policy)

        # Remove minimum height restriction to allow it to expand naturally
        # self.activity_table.setMinimumHeight(150) - Remove this line

        # Add table to activity layout
        activity_layout.addWidget(self.activity_table)

        # Add activity frame with stretch factor 1 so it takes all remaining space
        self.overall_layout.addWidget(activity_frame, 1)

        # NO STRETCH SPACER - remove this since we want the activity table to fill space
        # self.overall_layout.addStretch(1)
    
        # Add Overall tab to the tab widget
        self.tabs.insertTab(0, self.overall_tab, "Overview")

    def create_info_card(self, title, value, color, icon_type=None, subtitle=None):
        """Create an info card for the inventory dashboard with larger icons
        
        Args:
            title: The title of the card
            value: The main value to display
            color: The accent color for the card
            icon_type: The type of icon to display (warning, expired, products, etc.)
            subtitle: Optional subtitle to display beneath the main value
        
        Returns:
            QFrame: The info card frame
        """
        card = QtWidgets.QFrame()
        card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #232323;
                border-radius: 10px;
                border-left: 5px solid {color};
                padding: 10px;
                min-height: 60px;
            }}
        """)
        
        card_layout = QtWidgets.QHBoxLayout(card)
        card_layout.setContentsMargins(15, 10, 15, 10)
        
        # Add icon based on card type
        icon_label = QtWidgets.QLabel()
        icon_path = ""
        
        if icon_type == "warning":
            icon_path = "app/resources/images/inventory/low-stocks-items.png"
        elif icon_type == "expired":
            icon_path = "app/resources/images/inventory/expired-items.png"
        elif icon_type == "products":
            icon_path = "app/resources/images/inventory/total-products.png"
        elif icon_type == "categories":
            icon_path = "app/resources/images/inventory/product-categories.png"
        elif icon_type == "services":
            icon_path = "app/resources/images/inventory/services.png"
        
        icon_label.setFixedSize(200, 200)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        if icon_path and QtCore.QFile(icon_path).exists():
            pixmap = QtGui.QPixmap(icon_path)
            scaled_pixmap = pixmap.scaled(
                150, 150,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            icon_label.setPixmap(scaled_pixmap)
        else:
            icon_label.setText("●")
            icon_label.setStyleSheet(f"""
                color: {color};
                font-size: 60px;
            """)
        
        # Text content
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(5)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            color: #AAAAAA;
            font-size: 14px;
            font-weight: bold;
        """)
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet(f"""
            color: {color};
            font-size: 32px;
            font-weight: bold;
        """)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        
        # Add subtitle if provided
        if subtitle:
            subtitle_label = QtWidgets.QLabel(subtitle)
            subtitle_label.setStyleSheet("""
                color: #CCCCCC;
                font-size: 12px;
            """)
            text_layout.addWidget(subtitle_label)
            card.subtitle_label = subtitle_label
        
        # Add icon and text to card layout
        card_layout.addWidget(icon_label)
        card_layout.addLayout(text_layout, 1)
        
        card.value_label = value_label
        card.title = title
        
        return card
    
    def create_summary_card(self, title, value, color):
        """Create a summary card for the dashboard

        Args:
        title: The title of the card
        value: The value to display
        color: The accent color for the card
        
        Returns:
        QFrame: The summary card frame
        """
        card = QtWidgets.QFrame()
        card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #2a2a2a;
                border-radius: 8px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }}
        """)
        
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(5)
        
        value_label = QtWidgets.QLabel(value)
        value_label.setAlignment(QtCore.Qt.AlignCenter)
        value_label.setStyleSheet(f"""
            color: {color};
            font-size: 28px;
            font-weight: bold;
            border: none;
        """)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setStyleSheet("""
            color: #cccccc;
            font-size: 14px;
            border: none;
        """)
        
        # Add a colored indicator instead of a horizontal line
        indicator = QtWidgets.QFrame()
        indicator.setFixedHeight(2)
        indicator.setStyleSheet(f"background-color: {color}; margin: 3px 0;")
        
        card_layout.addWidget(value_label)
        card_layout.addWidget(indicator)
        card_layout.addWidget(title_label)
        
        # Store reference to value label for updating
        card.value_label = value_label
        card.title = title
        
        return card

    def create_metric_item(self, title, value, icon_type, color):
        """Create a metric item for the dashboard
    
        Args:
        title: The title of the metric
        value: The value to display
        icon_type: Type of icon to display
        color: The accent color for the metric
        
        Returns:
        QFrame: The metric item frame
        """
        metric = QtWidgets.QFrame()
        metric.setFrameShape(QtWidgets.QFrame.StyledPanel)
        metric.setStyleSheet(f"""
            QFrame {{
                background-color: #2a2a2a;
                border-radius: 8px;
                border-left: 3px solid {color};
                border-top: none;
                border-right: none;
                border-bottom: none;
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout(metric)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Icon
        icon_label = QtWidgets.QLabel()
        icon_path = ""
        
        if icon_type == "warning":
            icon_path = "app/resources/images/warning.png"
        elif icon_type == "alert":
            icon_path = "app/resources/images/alert.png"
        elif icon_type == "error":
            icon_path = "app/resources/images/error.png"
        elif icon_type == "info":
            icon_path = "app/resources/images/info.png"
        
        icon_label.setFixedSize(38, 38)
        if icon_path and QtCore.QFile(icon_path).exists():
            icon_label.setPixmap(QtGui.QPixmap(icon_path).scaled(32, 32, 
                                QtCore.Qt.KeepAspectRatio, 
                                QtCore.Qt.SmoothTransformation))
        else:
            # Fallback text icon if image doesn't exist
            icon_map = {
                "warning": "⚠️",
                "alert": "⚠️",
                "error": "❌",
                "info": "ℹ️"
            }
            icon_label.setText(icon_map.get(icon_type, "•"))
            icon_label.setStyleSheet(f"color: {color}; font-size: 24px; background: transparent;")
        
        # Text content
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(5)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            color: #cccccc;
            font-size: 13px;
        """)
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet(f"""
            color: white;
            font-size: 20px;
            font-weight: bold;
        """)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        
        layout.addWidget(icon_label)
        layout.addLayout(text_layout, 1)
        
        # Store reference to value label for updating
        metric.value_label = value_label
        metric.title = title
        
        return metric
    
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
                
                price_item = QtWidgets.QTableWidgetItem(f"₱{product['price']:.2f}")
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
                    availability_item.setForeground(QtGui.QColor("#4CAF50")) 
                else:
                    availability_item.setForeground(QtGui.QColor("#FF5252")) 
                    
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
                price_item = QtWidgets.QTableWidgetItem(f"₱{service['price']:.2f}")
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
            
            # Update the info cards - use direct references instead of searching
            # Find cards directly in the inventory tab layout
            for i in range(self.inventory_layout.count()):
                layout_item = self.inventory_layout.itemAt(i)
                if layout_item and layout_item.layout():
                    for j in range(layout_item.layout().count()):
                        card = layout_item.layout().itemAt(j).widget()
                        if hasattr(card, 'title'):
                            if card.title == "Low Stock Items":
                                card.value_label.setText(str(low_stock_count))
                            elif card.title == "Expired Items":
                                card.value_label.setText(str(expired_count))
                            elif card.title == "Total Products":
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
    
    def update_overall_dashboard(self):
        """Update the overall inventory dashboard with fresh data"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get distinct categories count 
            cursor.execute("""
                SELECT COUNT(DISTINCT category) as count 
                FROM products
            """)
            categories_count = cursor.fetchone()['count']
            
            # Get total products count and revenue
            cursor.execute("""
                SELECT COUNT(*) as count, 
                       SUM(price * quantity) as revenue 
                FROM products
            """)
            products_data = cursor.fetchone()
            products_count = products_data['count']
            products_revenue = products_data['revenue'] or 0
            
            # Get services count
            cursor.execute("SELECT COUNT(*) as count FROM services")
            services_count = cursor.fetchone()['count']
            
            # Get low stock items count
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM products 
                WHERE quantity <= threshold_value
            """)
            low_stock_count = cursor.fetchone()['count']
            
            # Get expired products count
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM products 
                WHERE expiry_date < CURDATE()
            """)
            expired_count = cursor.fetchone()['count']
            
            # Get out of stock count
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM products 
                WHERE quantity = 0 OR availability = 0
            """)
            out_of_stock_count = cursor.fetchone()['count']
            
            # Get top selling category
            cursor.execute("""
                SELECT category, COUNT(*) as count
                FROM products
                WHERE category IS NOT NULL AND category != ''
                GROUP BY category
                ORDER BY count DESC
                LIMIT 1
            """)
            top_category = cursor.fetchone()
            top_category_name = top_category['category'] if top_category else "-"
            
            # Get recent activity data
            cursor.execute("""
                SELECT p.product_name, i.status, i.quantity, i.last_updated
                FROM inventory i
                JOIN products p ON i.product_id = p.product_id
                ORDER BY i.last_updated DESC
                LIMIT 8
            """)
            
            activity_data = cursor.fetchall()
            
            # Update summary cards
            self.products_summary.value_label.setText(str(products_count))
            self.categories_summary.value_label.setText(str(categories_count))
            self.services_summary.value_label.setText(str(services_count))
            self.revenue_summary.value_label.setText(f"₱{products_revenue:.2f}")
            
            # Update metric items
            self.low_stock_metric.value_label.setText(str(low_stock_count))
            self.expired_metric.value_label.setText(str(expired_count))
            self.out_of_stock_metric.value_label.setText(str(out_of_stock_count))
            self.top_selling_metric.value_label.setText(top_category_name)
            
            # Update activity table
            self.activity_table.setRowCount(len(activity_data))
            for row, data in enumerate(activity_data):
                # Product name
                self.activity_table.setItem(row, 0, QtWidgets.QTableWidgetItem(data['product_name']))
                
                # Status with color indicator
                status_item = QtWidgets.QTableWidgetItem(data['status'])
                if data['status'] == 'Updated':
                    status_item.setForeground(QtGui.QColor("#2196F3"))
                elif data['status'] == 'New':
                    status_item.setForeground(QtGui.QColor("#4CAF50"))
                self.activity_table.setItem(row, 1, status_item)
                
                # Quantity
                self.activity_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(data['quantity'])))
                
                # Date/time - update to 12-hour format
                last_updated = data['last_updated']
                date_str = last_updated.strftime('%Y-%m-%d %I:%M %p') if last_updated else "N/A"
                self.activity_table.setItem(row, 3, QtWidgets.QTableWidgetItem(date_str))
            
            # Update the last updated timestamp
            current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
            self.last_updated_label.setText(f"Last updated: {current_time}")
            
            cursor.close()
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")

    def update_card_value(self, card, value, subtitle=None):
        """Update the value and optional subtitle of a dashboard card
        
        Args:
            card: The card widget to update
            value: The new value to display
            subtitle: Optional new subtitle text
        """
        if hasattr(card, 'value_label'):
            card.value_label.setText(value)
        
        if subtitle and hasattr(card, 'subtitle_label'):
            card.subtitle_label.setText(subtitle)
    
    def view_all_clicked(self, event):
        """Handle click on the View All link to switch to Inventory Status tab"""
        # Find the index of the Inventory Status tab
        inventory_status_index = self.tabs.indexOf(self.inventory_tab)
        # Switch to that tab
        self.tabs.setCurrentIndex(inventory_status_index)
    
    def show_product_filter_dialog(self):
        """Show advanced filter dialog for products"""
        # Create a dialog
        filter_dialog = QtWidgets.QDialog(self)
        filter_dialog.setWindowTitle("Filter Products")
        filter_dialog.setMinimumWidth(400)
        filter_dialog.setStyleSheet(StyleFactory.get_dialog_style())
        
        # Create layout
        layout = QtWidgets.QVBoxLayout(filter_dialog)
        form_layout = QtWidgets.QFormLayout()
        
        # Category filter
        category_label = QtWidgets.QLabel("Category:")
        category_combo = QtWidgets.QComboBox()
        category_combo.addItem("All Categories")
        
        # Get unique categories
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT category FROM products WHERE category IS NOT NULL AND category != ''")
            categories = cursor.fetchall()
            for category in categories:
                category_combo.addItem(category['category'])
            cursor.close()
        except mysql.connector.Error:
            pass
        
        form_layout.addRow(category_label, category_combo)
        
        # Availability filter
        availability_label = QtWidgets.QLabel("Availability:")
        availability_combo = QtWidgets.QComboBox()
        availability_combo.addItem("All")
        availability_combo.addItem("In Stock")
        availability_combo.addItem("Out of Stock")
        form_layout.addRow(availability_label, availability_combo)
        
        # Price range filter
        price_range_label = QtWidgets.QLabel("Price Range:")
        price_range_layout = QtWidgets.QHBoxLayout()
        min_price = QtWidgets.QDoubleSpinBox()
        min_price.setPrefix("₱ ")
        min_price.setMaximum(1000000)
        max_price = QtWidgets.QDoubleSpinBox()
        max_price.setPrefix("₱ ")
        max_price.setMaximum(1000000)
        max_price.setValue(1000000)
        price_range_layout.addWidget(min_price)
        price_range_layout.addWidget(QtWidgets.QLabel(" to "))
        price_range_layout.addWidget(max_price)
        form_layout.addRow(price_range_label, price_range_layout)
        
        # Buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        apply_button = QtWidgets.QPushButton("Apply Filter")
        reset_button = QtWidgets.QPushButton("Reset")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        
        buttons_layout.addWidget(reset_button)
        buttons_layout.addWidget(apply_button)
        
        layout.addLayout(form_layout)
        layout.addLayout(buttons_layout)
        
        # Connect signals
        def apply_filters():
            category = category_combo.currentText()
            availability = availability_combo.currentText()
            min_price_val = min_price.value()
            max_price_val = max_price.value()
            
            for row in range(self.products_table.rowCount()):
                show_row = True
                
                # Apply category filter
                if category != "All Categories":
                    category_cell = self.products_table.item(row, 2).text()
                    if category_cell != category:
                        show_row = False
                
                # Apply availability filter
                if availability != "All" and show_row:
                    availability_cell = self.products_table.item(row, 7).text()
                    if (availability == "In Stock" and availability_cell != "In Stock") or \
                       (availability == "Out of Stock" and availability_cell != "Out of Stock"):
                        show_row = False
                
                # Apply price filter
                if show_row:
                    price_text = self.products_table.item(row, 3).text().replace("₱", "")
                    try:
                        price = float(price_text)
                        if price < min_price_val or price > max_price_val:
                            show_row = False
                    except ValueError:
                        pass
                
                self.products_table.setRowHidden(row, not show_row)
            
            filter_dialog.accept()
        
        def reset_filters():
            # Show all rows
            for row in range(self.products_table.rowCount()):
                self.products_table.setRowHidden(row, False)
            filter_dialog.accept()
        
        apply_button.clicked.connect(apply_filters)
        reset_button.clicked.connect(reset_filters)
        
        filter_dialog.exec_()
    
    def show_service_filter_dialog(self):
        """Show advanced filter dialog for services"""
        # Create a dialog
        filter_dialog = QtWidgets.QDialog(self)
        filter_dialog.setWindowTitle("Filter Services")
        filter_dialog.setMinimumWidth(400)
        filter_dialog.setStyleSheet(StyleFactory.get_dialog_style())
        
        # Create layout
        layout = QtWidgets.QVBoxLayout(filter_dialog)
        form_layout = QtWidgets.QFormLayout()
        
        # Category filter
        category_label = QtWidgets.QLabel("Category:")
        category_combo = QtWidgets.QComboBox()
        category_combo.addItem("All Categories")
        
        # Get unique categories
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT category FROM services WHERE category IS NOT NULL AND category != ''")
            categories = cursor.fetchall()
            for category in categories:
                category_combo.addItem(category['category'])
            cursor.close()
        except mysql.connector.Error:
            pass
        
        form_layout.addRow(category_label, category_combo)
        
        # Availability filter
        availability_label = QtWidgets.QLabel("Availability:")
        availability_combo = QtWidgets.QComboBox()
        availability_combo.addItem("All")
        availability_combo.addItem("Available")
        availability_combo.addItem("Unavailable")
        form_layout.addRow(availability_label, availability_combo)
        
        # Price range filter
        price_range_label = QtWidgets.QLabel("Price Range:")
        price_range_layout = QtWidgets.QHBoxLayout()
        min_price = QtWidgets.QDoubleSpinBox()
        min_price.setPrefix("₱ ")
        min_price.setMaximum(1000000)
        max_price = QtWidgets.QDoubleSpinBox()
        max_price.setPrefix("₱ ")
        max_price.setMaximum(1000000)
        max_price.setValue(1000000)
        price_range_layout.addWidget(min_price)
        price_range_layout.addWidget(QtWidgets.QLabel(" to "))
        price_range_layout.addWidget(max_price)
        form_layout.addRow(price_range_label, price_range_layout)
        
        # Buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        apply_button = QtWidgets.QPushButton("Apply Filter")
        reset_button = QtWidgets.QPushButton("Reset")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        
        buttons_layout.addWidget(reset_button)
        buttons_layout.addWidget(apply_button)
        
        layout.addLayout(form_layout)
        layout.addLayout(buttons_layout)
        
        # Connect signals
        def apply_filters():
            category = category_combo.currentText()
            availability = availability_combo.currentText()
            min_price_val = min_price.value()
            max_price_val = max_price.value()
            
            for row in range(self.services_table.rowCount()):
                show_row = True
        
                # Apply category filter
                if category != "All Categories":
                    category_cell = self.services_table.item(row, 2).text()
                    if category_cell != category:
                        show_row = False
        
                # Apply availability filter
                if availability != "All" and show_row:
                    availability_cell = self.services_table.item(row, 4).text()
                    if (availability == "Available" and availability_cell != "Available") or \
                        (availability == "Unavailable" and availability_cell != "Unavailable"):
                        show_row = False
        
                # Apply price filter
                if show_row:
                    price_text = self.services_table.item(row, 3).text().replace("₱", "")
                    try:
                        price = float(price_text)
                        if price < min_price_val or price > max_price_val:
                            show_row = False
                    except ValueError:
                        pass
        
                self.services_table.setRowHidden(row, not show_row)
            
            filter_dialog.accept()
        
        def reset_filters():
            # Show all rows
            for row in range(self.services_table.rowCount()):
                self.services_table.setRowHidden(row, False)
            filter_dialog.accept()
        
        apply_button.clicked.connect(apply_filters)
        reset_button.clicked.connect(reset_filters)
        
        filter_dialog.exec_()