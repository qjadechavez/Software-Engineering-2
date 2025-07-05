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
        self.create_user_manual_tab()  # Add this first
        self.create_dashboard_tab()
        self.create_invoice_tab()
        self.create_inventory_tab()
        self.create_customer_tab()
        self.create_suppliers_tab()
        self.create_reports_tab()
        self.create_maintenance_tab()
        
        self.content_layout.addWidget(self.tabs)
    
    def create_user_manual_tab(self):
        """Create User Manual tab with complete system guide"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QtWidgets.QLabel("User Manual")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; margin-bottom: 10px; border: none;")
        layout.addWidget(title)
        
        # Description
        desc = QtWidgets.QLabel("Complete user manual for the Sales and Inventory Management System. Follow this guide for step-by-step instructions on using all system features.")
        desc.setStyleSheet("color: #cccccc; font-size: 14px; margin-bottom: 15px; border: none;")
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        # Create scroll area for the manual content
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #232323;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #232323;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #666666;
            }
        """)
        
        # Content widget for scroll area
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        
        # Getting Started Section
        getting_started_frame = self.create_feature_section("🚀 Getting Started", [
            "1. Login to the System",
            "   • Enter your username and password on the login screen",
            "   • Contact your administrator if you don't have credentials",
            "   • Click 'Login' to access the main system",
            "",
            "2. Understanding User Roles",
            "   • Admin: Full system access including user management and backups",
            "   • Staff: Access to daily operations (POS, inventory, customers)",
            "",
            "3. Navigation",
            "   • Use the sidebar menu to navigate between different sections",
            "   • Dashboard provides an overview of system status",
            "   • Click your username in the top-right to logout"
        ])
        content_layout.addWidget(getting_started_frame)
        
        # Daily Operations Section
        daily_ops_frame = self.create_feature_section("📋 Daily Operations", [
            "1. Processing a Sale (Invoice/POS)",
            "   • Navigate to Invoice/POS from the sidebar",
            "   • Step 1: Select services (up to 3 services per transaction)",
            "   • Step 2: Enter customer information (name, gender, phone, city)",
            "   • Step 3: Review transaction details and add notes if needed",
            "   • Step 4: Process payment (cash only) and apply discounts",
            "   • Step 5: Complete transaction and print/save receipt",
            "",
            "2. Managing Inventory",
            "   • Go to Inventory → Products to manage physical items",
            "   • Go to Inventory → Services to manage beauty services",
            "   • Use the search bar to find specific items quickly",
            "   • Right-click items for edit/delete options",
            "",
            "3. Customer Management",
            "   • Access Customers page to view transaction history",
            "   • Use filters to search by date, name, or phone number",
            "   • Right-click transactions to view details or print receipts"
        ])
        content_layout.addWidget(daily_ops_frame)
        
        # Advanced Features Section
        advanced_frame = self.create_feature_section("⚙️ Advanced Features", [
            "1. Reports and Analytics",
            "   • Navigate to Reports for business analytics",
            "   • Overview Report: General business performance",
            "   • Financial Report: Revenue and profit analysis",
            "   • Sales Report: Detailed transaction data",
            "   • Use date filters to analyze specific time periods",
            "",
            "2. Supplier Management",
            "   • Access Suppliers page to manage vendor information",
            "   • Add new suppliers with complete contact details",
            "   • Update supplier information as needed",
            "   • Use search and filter functions for quick access",
            "",
            "3. System Maintenance (Admin Only)",
            "   • Database Backup: Create full system backups",
            "   • User Management: Add, edit, or remove user accounts",
            "   • View system statistics and user activity"
        ])
        content_layout.addWidget(advanced_frame)
        
        # Troubleshooting Section
        troubleshooting_frame = self.create_feature_section("🔧 Troubleshooting", [
            "Common Issues and Solutions:",
            "",
            "1. Cannot login to the system",
            "   • Verify username and password are correct",
            "   • Check with administrator for account status",
            "   • Ensure database connection is working",
            "",
            "2. Transaction not completing",
            "   • Ensure all required fields are filled",
            "   • Check that services are available",
            "   • Verify customer information is complete",
            "",
            "3. Inventory items not showing",
            "   • Check if items are marked as available",
            "   • Clear search filters and try again",
            "   • Refresh the page or restart the application",
            "",
            "4. Reports not generating",
            "   • Verify date range selection",
            "   • Check that there is data for the selected period",
            "   • Try different filter combinations",
            "",
            "5. System running slowly",
            "   • Close unnecessary applications",
            "   • Contact administrator for database maintenance",
            "   • Restart the application if performance issues persist"
        ])
        content_layout.addWidget(troubleshooting_frame)
        
        # Best Practices Section
        best_practices_frame = self.create_feature_section("✅ Best Practices", [
            "1. Data Entry Guidelines",
            "   • Always enter complete customer information",
            "   • Use consistent naming conventions for products/services",
            "   • Add descriptive notes to transactions when necessary",
            "   • Double-check amounts before processing payments",
            "",
            "2. Security Recommendations",
            "   • Always logout when leaving your workstation",
            "   • Don't share login credentials with others",
            "   • Change your password regularly",
            "   • Report any suspicious activity to administrators",
            "",
            "3. Maintenance Tasks",
            "   • Regular database backups (Admin)",
            "   • Monitor inventory levels daily",
            "   • Review transaction reports weekly",
            "   • Update supplier information as needed",
            "",
            "4. Performance Tips",
            "   • Use search and filter functions for large datasets",
            "   • Close the application properly when finished",
            "   • Keep the system updated with latest versions",
            "   • Report bugs or issues to system administrators"
        ])
        content_layout.addWidget(best_practices_frame)
        
        # FAQ Section
        faq_frame = self.create_feature_section("❓ Frequently Asked Questions", [
            "Q: How do I reset a customer's transaction?",
            "A: Transactions cannot be modified after completion. Contact an administrator if changes are needed.",
            "",
            "Q: Can I process multiple payment methods?",
            "A: Currently, the system only accepts cash payments.",
            "",
            "Q: How do I add a new service?",
            "A: Go to Inventory → Services and click '+ Add Service' button.",
            "",
            "Q: What happens if I lose internet connection?",
            "A: The system works locally, so internet is not required for daily operations.",
            "",
            "Q: How do I view previous receipts?",
            "A: Go to Customers page, find the transaction, and right-click to view receipt.",
            "",
            "Q: Can I modify inventory quantities?",
            "A: Yes, go to Inventory → Products and edit the item to update quantities.",
            "",
            "Q: How do I export reports?",
            "A: In the Reports section, use the export buttons to save as Excel or PDF.",
            "",
            "Q: What should I do if the system crashes?",
            "A: Restart the application. Contact administrator if problem persists."
        ])
        content_layout.addWidget(faq_frame)
        
        # Contact Information Section
        contact_frame = self.create_feature_section("📞 Support Contact", [
            "For technical support and assistance:",
            "",
            "System Administrator:",
            "• Email: admin@mierebeauty.com",
            "• Phone: +1 (555) 123-4567",
            "• Business Hours: Monday - Friday, 9:00 AM - 5:00 PM",
            "",
            "Emergency Support:",
            "• After-hours support available for critical issues",
            "• Contact your local IT support team",
            "",
            "Training and User Support:",
            "• Schedule training sessions with your administrator",
            "• Access this help documentation anytime",
            "• Report bugs or feature requests to the development team"
        ])
        content_layout.addWidget(contact_frame)
        
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        
        self.tabs.addTab(tab, "User Manual")
    
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