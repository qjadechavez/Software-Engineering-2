from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage

class HelpPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(HelpPage, self).__init__(parent, title="Help & Documentation", user_info=user_info)
    
    def createContent(self):
        # Content area
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(15)
        
        # Create tabs for different functionalities
        self.create_tabs()
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
    
    def create_tabs(self):
        """Create tabs for different system functionalities"""
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { 
                border: 1px solid #444; 
                background-color: #232323;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #343434;
                color: #ffffff;
                padding: 10px 20px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                min-width: 100px;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background-color: #1a1a1a;
                border-bottom-color: #1a1a1a;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3a3a3a;
            }
        """)
        
        # Create tabs for each navigation page
        self.create_dashboard_tab()
        self.create_invoice_tab()
        self.create_inventory_tab()
        self.create_customer_tab()
        self.create_suppliers_tab()
        self.create_reports_tab()
        self.create_maintenance_tab()
        
        self.content_layout.addWidget(self.tabs)
    
    def create_dashboard_tab(self):
        """Create Dashboard help tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QtWidgets.QLabel("Dashboard Overview")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px; border: none;")
        layout.addWidget(title)
        
        # Description
        desc = QtWidgets.QLabel("The Dashboard provides a real-time overview of your business performance with key metrics and analytics.")
        desc.setStyleSheet("color: #cccccc; font-size: 14px; margin-bottom: 15px; border: none;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Features section
        features_frame = self.create_feature_section("Key Features:", [
            "📊 Sales Analytics - Track daily revenue and transaction volume over the last 7 days",
            "📦 Inventory Status - Monitor stock levels across product categories with color-coded status",
            "💰 Revenue Metrics - View total revenue and today's earnings at a glance",
            "🔄 Transaction Counter - Track today's transaction count",
            "🛠️ Services Overview - Monitor total available services",
            "🎯 Quick Navigation - Click 'View All' buttons to jump to detailed pages"
        ])
        layout.addWidget(features_frame)
        
        # How to use section
        usage_frame = self.create_feature_section("How to Use:", [
            "1. View real-time metrics in the colored cards at the top",
            "2. Analyze sales trends in the Sales Analytics chart",
            "3. Monitor inventory status with the color-coded stock levels",
            "4. Click 'View All →' buttons to navigate to detailed pages",
            "5. Dashboard auto-refreshes after completing transactions"
        ])
        layout.addWidget(usage_frame)
        
        layout.addStretch()
        self.tabs.addTab(tab, "Dashboard")
    
    def create_invoice_tab(self):
        """Create Invoice/POS help tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QtWidgets.QLabel("Invoice & Point of Sale")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px; border: none;")
        layout.addWidget(title)
        
        desc = QtWidgets.QLabel("Complete transaction processing system for creating invoices, managing customers, and processing payments.")
        desc.setStyleSheet("color: #cccccc; font-size: 14px; margin-bottom: 15px; border: none;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        features_frame = self.create_feature_section("Features:", [
            "🛍️ Service Selection - Choose up to 3 services with filtering options",
            "👥 Customer Management - Add new customers or select existing ones",
            "💳 Payment Processing - Only Accept Cash",
            "🎫 Coupon System - Apply discount coupons and percentage discounts",
            "📄 Invoice Generation - Create detailed invoices with customer information",
            "🖨️ Receipt Printing - Print or save receipts as PDF",
            "📝 Service Notes - Add special notes or instructions for services"
        ])
        layout.addWidget(features_frame)
        
        workflow_frame = self.create_feature_section("Transaction Workflow:", [
            "1. Select Service → Choose your services and review selection",
            "2. Customer Info → Enter or select customer details",
            "3. Overview → Review transaction details and add notes",
            "4. Payment → Process payment and apply discounts",
            "5. Complete → Generate receipt and finalize transaction"
        ])
        layout.addWidget(workflow_frame)
        
        layout.addStretch()
        self.tabs.addTab(tab, "Invoice/POS")
    
    def create_inventory_tab(self):
        """Create Inventory help tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QtWidgets.QLabel("Inventory Management")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px; border: none;")
        layout.addWidget(title)
        
        desc = QtWidgets.QLabel("Comprehensive inventory system for managing products, services, and tracking stock levels.")
        desc.setStyleSheet("color: #cccccc; font-size: 14px; margin-bottom: 15px; border: none;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        features_frame = self.create_feature_section("Inventory Tabs:", [
            "📋 Overview - Dashboard view of inventory statistics and alerts",
            "📦 Products - Manage physical products, quantities, and suppliers",
            "🛠️ Services - Manage beauty services, pricing, and availability",
            "📊 Inventory Status - Monitor stock levels and reorder points"
        ])
        layout.addWidget(features_frame)
        
        actions_frame = self.create_feature_section("Available Actions:", [
            "➕ Add new products and services",
            "✏️ Edit existing items and update information",
            "🗑️ Delete outdated or discontinued items",
            "🔍 Search and filter by category, price, or availability",
            "📈 Track quantity changes and stock movements",
            "⚠️ Set low stock alerts and threshold values"
        ])
        layout.addWidget(actions_frame)
        
        layout.addStretch()
        self.tabs.addTab(tab, "Inventory")
    
    def create_customer_tab(self):
        """Create Customer help tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QtWidgets.QLabel("Customer Management")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px; border: none;")
        layout.addWidget(title)
        
        desc = QtWidgets.QLabel("View and manage customer transaction history with detailed filtering and receipt management.")
        desc.setStyleSheet("color: #cccccc; font-size: 14px; margin-bottom: 15px; border: none;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        features_frame = self.create_feature_section("Customer Features:", [
            "📊 Transaction History - Complete record of all customer transactions",
            "🔍 Advanced Search - Search by name, phone, service, or transaction ID",
            "🗓️ Date Filtering - Filter by date ranges (Today, Week, Month, Year)",
            "💳 Payment Filters - Filter by payment method (Cash, GCash, Card)",
            "👤 Gender Filtering - Filter transactions by customer gender",
            "📄 Receipt Management - View, print, or save transaction receipts"
        ])
        layout.addWidget(features_frame)
        
        actions_frame = self.create_feature_section("Available Actions:", [
            "👀 View Transaction Details - Right-click any transaction",
            "🖨️ Print Receipts - Generate physical receipt copies",
            "💾 Save as PDF - Export receipts for digital storage",
            "🔍 Quick Search - Use the search bar for instant filtering",
            "📊 Sort Data - Click column headers to sort information"
        ])
        layout.addWidget(actions_frame)
        
        layout.addStretch()
        self.tabs.addTab(tab, "Customers")
    
    def create_suppliers_tab(self):
        """Create Suppliers help tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QtWidgets.QLabel("Supplier Management")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px; border: none;")
        layout.addWidget(title)
        
        desc = QtWidgets.QLabel("Manage supplier relationships, contact information, and product sourcing.")
        desc.setStyleSheet("color: #cccccc; font-size: 14px; margin-bottom: 15px; border: none;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        features_frame = self.create_feature_section("Supplier Features:", [
            "🏢 Supplier Database - Complete supplier contact information",
            "📱 Contact Management - Phone numbers, emails, and addresses",
            "🔍 Search & Filter - Find suppliers by name, category, or location",
            "📊 Supplier Statistics - Track number of suppliers and categories",
            "✏️ Edit Information - Update supplier details as needed",
            "🗑️ Remove Suppliers - Delete inactive or outdated suppliers"
        ])
        layout.addWidget(features_frame)
        
        management_frame = self.create_feature_section("Supplier Management:", [
            "1. Add New Suppliers - Click '+ Add Supplier' button",
            "2. Enter Complete Information - Name, contact details, category",
            "3. Search Existing Suppliers - Use search bar for quick access",
            "4. Update Information - Right-click to edit supplier details",
            "5. Filter by Category - Use filter button for specific categories",
            "6. Remove Inactive Suppliers - Right-click to delete"
        ])
        layout.addWidget(management_frame)
        
        layout.addStretch()
        self.tabs.addTab(tab, "Suppliers")
    
    def create_reports_tab(self):
        """Create Reports help tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QtWidgets.QLabel("Reports & Analytics")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px; border: none;")
        layout.addWidget(title)
        
        desc = QtWidgets.QLabel("Comprehensive reporting system for business analytics, financial tracking, and performance monitoring.")
        desc.setStyleSheet("color: #cccccc; font-size: 14px; margin-bottom: 15px; border: none;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        reports_frame = self.create_feature_section("Available Reports:", [
            "📊 Overview Report - General business performance summary",
            "📈 Financial Report - Revenue, profit, and financial analytics",
            "🛍️ Sales Report - Detailed sales data and transaction analysis",
            "📦 Inventory Report - Stock levels, product performance, and alerts",
            "👥 Customer Report - Customer analytics and transaction patterns"
        ])
        layout.addWidget(reports_frame)
        
        features_frame = self.create_feature_section("Report Features:", [
            "🗓️ Date Range Selection - Custom date filtering for all reports",
            "📊 Visual Charts - Graphs and charts for easy data interpretation",
            "📄 Export Options - Export reports to Excel or PDF formats",
            "🔍 Advanced Filtering - Filter by categories, payment methods, etc.",
            "📈 Trend Analysis - Identify business trends and patterns",
            "🎯 Key Metrics - Focus on important business indicators"
        ])
        layout.addWidget(features_frame)
        
        layout.addStretch()
        self.tabs.addTab(tab, "Reports")
    
    def create_maintenance_tab(self):
        """Create Maintenance help tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QtWidgets.QLabel("System Maintenance")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px; border: none;")
        layout.addWidget(title)
        
        desc = QtWidgets.QLabel("System administration tools for database management, user control, and system maintenance.")
        desc.setStyleSheet("color: #cccccc; font-size: 14px; margin-bottom: 15px; border: none;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        database_frame = self.create_feature_section("Database Backup:", [
            "💾 Full Database Backup - Create complete system backups",
            "📊 Table Information - View database table sizes and row counts",
            "📁 Backup Location - Choose custom backup save locations",
            "🔄 Restore Options - Restore from previous backup files",
            "⚡ Quick Backup - One-click backup creation"
        ])
        layout.addWidget(database_frame)
        
        user_frame = self.create_feature_section("User Management:", [
            "👥 User Accounts - Manage staff and admin accounts",
            "🔐 Role Assignment - Set user permissions (Admin/Staff)",
            "✏️ Edit Users - Update user information and passwords",
            "📊 User Statistics - View user distribution and activity",
            "🗑️ Remove Users - Delete inactive user accounts"
        ])
        layout.addWidget(user_frame)
        
        layout.addStretch()
        self.tabs.addTab(tab, "Maintenance")
    
    def create_feature_section(self, title, features):
        """Create a feature section with title and bullet points"""
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border-radius: 8px;
                border: none;
            }
        """)
        layout = QtWidgets.QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        # Section title
        section_title = QtWidgets.QLabel(title)
        section_title.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-bottom: 5px; border: none;")
        layout.addWidget(section_title)
        
        # Feature list
        for feature in features:
            feature_label = QtWidgets.QLabel(feature)
            feature_label.setStyleSheet("color: #cccccc; font-size: 13px; margin-left: 10px; border: none;")
            feature_label.setWordWrap(True)
            layout.addWidget(feature_label)
        
        return frame
    
    def create_faq_item(self, question, answer):
        """Create a collapsible FAQ item"""
        faq_item = QtWidgets.QFrame()
        faq_item.setStyleSheet("""
            QFrame {
                background-color: #323232;
                border-radius: 5px;
                border: none;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(faq_item)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Question header with toggle
        question_layout = QtWidgets.QHBoxLayout()
        
        question_label = QtWidgets.QLabel(f"Q: {question}")
        question_label.setStyleSheet("color: white; font-size: 13px; font-weight: bold; border: none;")
        question_label.setWordWrap(True)
        
        toggle_btn = QtWidgets.QPushButton("▼")
        toggle_btn.setFixedSize(20, 20)
        toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0099FF;
            }
        """)
        
        question_layout.addWidget(question_label)
        question_layout.addWidget(toggle_btn)
        
        layout.addLayout(question_layout)
        
        # Answer (initially hidden)
        answer_label = QtWidgets.QLabel(f"A: {answer}")
        answer_label.setStyleSheet("color: #cccccc; font-size: 12px; margin-left: 15px; border: none;")
        answer_label.setWordWrap(True)
        answer_label.setVisible(False)
        
        layout.addWidget(answer_label)
        
        # Connect toggle functionality
        def toggle_answer():
            is_visible = answer_label.isVisible()
            answer_label.setVisible(not is_visible)
            toggle_btn.setText("▲" if not is_visible else "▼")
        
        toggle_btn.clicked.connect(toggle_answer)
        
        return faq_item
    
    def toggle_faq(self):
        """Toggle FAQ section visibility"""
        is_visible = self.faq_content.isVisible()
        self.faq_content.setVisible(not is_visible)
        self.faq_toggle_btn.setText("▲ Hide FAQ" if not is_visible else "▼ Show FAQ")
    
    def search_help_content(self):
        """Search through help content"""
        search_text = self.search_input.text().lower()
        
        if not search_text:
            # Show all content when search is empty
            for i in range(self.tabs.count()):
                tab_widget = self.tabs.widget(i)
                self.show_all_content(tab_widget)
            return
        
        # Search through tab content
        for i in range(self.tabs.count()):
            tab_widget = self.tabs.widget(i)
            self.filter_tab_content(tab_widget, search_text)
    
    def show_all_content(self, widget):
        """Show all content in a widget"""
        if isinstance(widget, QtWidgets.QLabel):
            widget.setVisible(True)
        elif isinstance(widget, QtWidgets.QFrame):
            widget.setVisible(True)
        
        # Recursively show all child widgets
        for child in widget.findChildren(QtWidgets.QWidget):
            if isinstance(child, (QtWidgets.QLabel, QtWidgets.QFrame)):
                child.setVisible(True)
    
    def filter_tab_content(self, widget, search_text):
        """Filter tab content based on search text"""
        if isinstance(widget, QtWidgets.QLabel):
            text = widget.text().lower()
            widget.setVisible(search_text in text)
        elif isinstance(widget, QtWidgets.QFrame):
            # Check if any child label contains the search text
            has_match = False
            for child in widget.findChildren(QtWidgets.QLabel):
                if search_text in child.text().lower():
                    has_match = True
                    break
            widget.setVisible(has_match)
        
        # Recursively filter child widgets
        for child in widget.findChildren(QtWidgets.QWidget):
            if isinstance(child, (QtWidgets.QLabel, QtWidgets.QFrame)):
                self.filter_tab_content(child, search_text)