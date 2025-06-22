# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from app.ui.pages import (
    DashboardPage,
    InventoryPage,
    ReportsPage,
    CustomersPage,
    SuppliersPage,
    SalesPage,
    MaintenancePage,
    InvoicePage,
    HelpPage,
    AboutPage
)
from app.utils.auth_manager import AuthManager


class NavigationItem:
    """Class representing a navigation item in the sidebar"""
    
    def __init__(self, name, icon_path, page_class=None, action_method=None):
        """Initialize navigation item
        
        Args:
            name (str): Display name for the navigation item
            icon_path (str): Path to the icon image
            page_class (class, optional): Page class to instantiate
            action_method (str, optional): Method name to call instead of page navigation
        """
        self.name = name
        self.icon_path = icon_path
        self.page_class = page_class
        self.action_method = action_method
        self.button = None
        self.page = None
        self.page_index = None
    
    def create_button(self, parent, icon_size=20):
        """Create a navigation button
        
        Args:
            parent: Parent widget for the button
            icon_size (int): Size of the icon in pixels
            
        Returns:
            QPushButton: The created button
        """
        self.button = QtWidgets.QPushButton(f" {self.name}")
        self.button.setMinimumHeight(50)
        self.button.setFont(QtGui.QFont("Segoe UI", 10))
        self.button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        # Apply styling
        self.button.setStyleSheet("""
            QPushButton {
                color: white;
                text-align: left;
                padding-left: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2d2d2d;
            }
        """)
        
        # Set icon if path exists
        if self.icon_path:
            icon = QtGui.QIcon(self.icon_path)
            self.button.setIcon(icon)
            self.button.setIconSize(QtCore.QSize(icon_size, icon_size))
        
        return self.button
    
    def create_page(self, parent, user_info):
        """Create the page for this navigation item
        
        Args:
            parent: Parent for the page
            user_info (dict): User information to pass to the page
            
        Returns:
            QWidget: The created page or None if no page_class
        """
        if self.page_class:
            self.page = self.page_class(parent, user_info=user_info)
            return self.page
        return None


class SidebarSection:
    """Class representing a section in the sidebar"""
    
    def __init__(self, items=None):
        """Initialize sidebar section
        
        Args:
            items (list): List of NavigationItem objects
        """
        self.items = items or []
        self.container = None
        self.layout = None
    
    def create_container(self, parent):
        """Create container widget for this section
        
        Args:
            parent: Parent widget
            
        Returns:
            QWidget: The container widget
        """
        self.container = QtWidgets.QWidget(parent)
        self.layout = QtWidgets.QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        
        # Create buttons for each item
        for item in self.items:
            if item.name == "Logout":
                button = item.create_button(parent, 18) 
            else:
                button = item.create_button(parent)
                
            self.layout.addWidget(button)
        
        return self.container


class Sidebar:
    """Class representing the sidebar"""
    
    def __init__(self, main_window, navigation_items, bottom_items):
        """Initialize sidebar
        
        Args:
            main_window: Parent MainWindow
            navigation_items (list): Main navigation items
            bottom_items (list): Bottom navigation items
        """
        self.main_window = main_window
        self.navigation_section = SidebarSection(navigation_items)
        self.bottom_section = SidebarSection(bottom_items)
        self.widget = None
        self.layout = None
        self.logo_label = None
    
    def create(self):
        """Create the sidebar
        
        Returns:
            QWidget: The sidebar widget
        """
        # Create sidebar widget and layout
        self.widget = QtWidgets.QWidget()
        self.widget.setFixedWidth(240) 
        self.widget.setStyleSheet("background-color: #232323;")
        
        self.layout = QtWidgets.QVBoxLayout(self.widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(0)
        
        # Add logo
        self.setup_logo()
        
        # Add main navigation section
        nav_container = self.navigation_section.create_container(self.widget)
        self.layout.addWidget(nav_container)
        
        # Add stretch to push bottom buttons down
        self.layout.addStretch(1)
        
        # Add bottom navigation section
        bottom_container = self.bottom_section.create_container(self.widget)
        self.layout.addWidget(bottom_container)
        
        return self.widget
    
    def setup_logo(self):
        """Add logo to the sidebar"""
        self.logo_label = QtWidgets.QLabel()
        self.logo_label.setPixmap(QtGui.QPixmap("app/resources/images/logo/Miere1.png"))
        self.logo_label.setFixedHeight(100)
        self.layout.addWidget(self.logo_label)
        self.layout.addSpacing(10)


class PageManager:
    """Manager for handling application pages"""
    
    def __init__(self, stacked_widget):
        """Initialize page manager
        
        Args:
            stacked_widget (QStackedWidget): Widget that holds the pages
        """
        self.stacked_widget = stacked_widget
        self.pages = {}  # Store pages by name
        self.page_indices = {}  # Store page indices by name
    
    def add_page(self, nav_item, user_info):
        """Add a page to the stacked widget
        
        Args:
            nav_item (NavigationItem): Navigation item containing page info
            user_info (dict): User information to pass to the page
            
        Returns:
            int: Index of the added page or None if no page
        """
        if not nav_item.page_class:
            return None
            
        # Create page
        page = nav_item.create_page(self.stacked_widget, user_info)
        
        # Add to stacked widget
        index = self.stacked_widget.addWidget(page)
        
        # Store references
        self.pages[nav_item.name] = page
        self.page_indices[nav_item.name] = index
        nav_item.page_index = index
        
        return index
    
    def get_page(self, name):
        """Get a page by name
        
        Args:
            name (str): Page name
            
        Returns:
            QWidget: The page
        """
        return self.pages.get(name)
    
    def get_index(self, name):
        """Get page index by name
        
        Args:
            name (str): Page name
            
        Returns:
            int: Page index
        """
        return self.page_indices.get(name)
    
    def set_current_page(self, index):
        """Set the current page
        
        Args:
            index (int): Page index
        """
        self.stacked_widget.setCurrentIndex(index)
    
    def apply_styling(self):
        """Apply consistent styling to all pages"""
        header_style = "background-color: rgba(35, 35, 35, 0.95);"
        
        for i in range(self.stacked_widget.count()):
            page = self.stacked_widget.widget(i)
            
            # Find header widget in each page
            for child in page.children():
                if isinstance(child, QtWidgets.QWidget) and hasattr(child, 'objectName'):
                    if 'header' in child.objectName().lower() or hasattr(child, 'isHeader'):
                        child.setStyleSheet(header_style)
                        
                        # Style header labels
                        for header_child in child.children():
                            if isinstance(header_child, QtWidgets.QLabel):
                                if 'title' in header_child.objectName().lower():
                                    header_child.setStyleSheet("color: white; font-size: 24px;")
                                elif 'date' in header_child.objectName().lower():
                                    header_child.setStyleSheet("color: #E2F163; font-size: 14px;")


class MainWindow(QtWidgets.QMainWindow):
    """Main application window with sidebar navigation"""
    
    def __init__(self, parent=None, user_info=None):
        super(MainWindow, self).__init__(parent)
        self.user_info = user_info
        self.navigation_items = []
        self.bottom_items = []
        self.initialize_navigation_items()
        self.setupUi()
        
    def initialize_navigation_items(self):
        """Initialize navigation items from configuration"""
        # Main navigation items
        nav_config = [
            {"name": "Dashboard", "icon": "app/resources/images/main-window/Home.png", "class": DashboardPage},
            {"name": "Inventory", "icon": "app/resources/images/main-window/Inventory.png", "class": InventoryPage},
            {"name": "Reports", "icon": "app/resources/images/main-window/Report.png", "class": ReportsPage},
            {"name": "Customers", "icon": "app/resources/images/main-window/Suppliers.png", "class": CustomersPage},
            {"name": "Suppliers", "icon": "app/resources/images/main-window/Suppliers.png", "class": SuppliersPage},
            {"name": "Sales", "icon": "app/resources/images/main-window/Order.png", "class": SalesPage},
            {"name": "Maintenance", "icon": "app/resources/images/main-window/Group 15.png", "class": MaintenancePage},
            {"name": "Invoice", "icon": "app/resources/images/main-window/Invoice.png", "class": InvoicePage},
        ]
        
        # Bottom navigation items
        bottom_config = [
            {"name": "Help", "icon": "app/resources/images/main-window/Settings.png", "class": HelpPage},
            {"name": "About", "icon": "app/resources/images/main-window/Suppliers.png", "class": AboutPage},
            {"name": "Logout", "icon": "app/resources/images/main-window/Vector.png", "action": "handle_logout"},
        ]
        
        # Create NavigationItem objects
        for item in nav_config:
            nav_item = NavigationItem(
                name=item["name"],
                icon_path=item["icon"],
                page_class=item["class"]
            )
            self.navigation_items.append(nav_item)
            
        for item in bottom_config:
            nav_item = NavigationItem(
                name=item["name"],
                icon_path=item["icon"],
                page_class=item.get("class"),
                action_method=item.get("action")
            )
            self.bottom_items.append(nav_item)
        
    def setupUi(self):
        """Set up the user interface"""
        self.setObjectName("MainWindow")
        self.setupCentralWidget()
        self.setupWindow()
        
    def setupCentralWidget(self):
        """Set up the central widget and layout"""
        # Create the central widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        
        # Set up the main layout
        self.main_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create the sidebar
        self.sidebar = Sidebar(self, self.navigation_items, self.bottom_items)
        self.sidebar_widget = self.sidebar.create()
        self.main_layout.addWidget(self.sidebar_widget)
        
        # Create the stacked widget for pages
        self.stackedWidgetMain = QtWidgets.QStackedWidget()
        self.main_layout.addWidget(self.stackedWidgetMain)
        
        # Create page manager
        self.page_manager = PageManager(self.stackedWidgetMain)
        
        # Add pages
        self.setup_pages()
        
        # Connect buttons
        self.connect_buttons()
        
        # Apply styling to pages
        self.page_manager.apply_styling()
        
        # Set initial page
        self.stackedWidgetMain.setCurrentIndex(0)
        
    def setupWindow(self):
        """Set up window properties"""
        self.setWindowTitle("Miere Beauty Lounge - Sales and Inventory Management System")
        
        # Set window properties
        self.setWindowFlags(
            QtCore.Qt.Window |
            QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint |
            QtCore.Qt.WindowCloseButtonHint
        )
        
        self.showMaximized()
        self.setFixedSize(self.size())
        
    def setup_pages(self):
        """Set up all pages"""
        # Add main navigation pages
        for item in self.navigation_items:
            self.page_manager.add_page(item, self.user_info)
            
        # Add bottom navigation pages
        for item in self.bottom_items:
            if item.page_class: 
                self.page_manager.add_page(item, self.user_info)
        
    def connect_buttons(self):
        """Connect buttons to their actions"""
        # Connect main navigation buttons
        for item in self.navigation_items:
            if item.button and item.page_index is not None:
                item.button.clicked.connect(
                    lambda checked=False, idx=item.page_index: 
                    self.stackedWidgetMain.setCurrentIndex(idx)
                )
        
        # Connect bottom buttons
        for item in self.bottom_items:
            if item.button:
                if item.action_method:
                    # Connect to a method if it's an action
                    method = getattr(self, item.action_method)
                    item.button.clicked.connect(method)
                elif item.page_index is not None:
                    # Connect to page navigation
                    item.button.clicked.connect(
                        lambda checked=False, idx=item.page_index: 
                        self.stackedWidgetMain.setCurrentIndex(idx)
                    )
    
    def handle_logout(self):
        """Handle user logout"""
        username = self.user_info.get("username")
        if not username:
            print("Error: No username found for logout")
            return
            
        # Record logout in database
        auth_manager = AuthManager()
        auth_manager.logout(username)
        
        # Return to login screen
        from app.ui.pages.login_page import LoginPage
        self.login_window = LoginPage()
        self.login_window.show()
        self.close()
    
    def disable_navigation(self):
        """Disable navigation during an active invoice transaction"""
        # Disable all navigation buttons/menu items except the current one
        for action in self.navigation_actions:
            if action != self.sender():
                action.setEnabled(False)
        
        # You may also want to add a visual indication that navigation is disabled
        self.statusBar().showMessage("Transaction in progress - Navigation disabled")

    def enable_navigation(self):
        """Enable navigation after a transaction is completed or cancelled"""
        # Re-enable all navigation actions
        for action in self.navigation_actions:
            action.setEnabled(True)
        
        self.statusBar().clearMessage()
