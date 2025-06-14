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
    HelpPage,
    AboutPage
)
from app.utils.auth_manager import AuthManager

# This class is maintained for backward compatibility
class Ui_MainWindow:
    def setupUi(self, MainWindow):
        # Just a stub to maintain compatibility
        pass


class MainWindow(QtWidgets.QMainWindow):
    """Main application window with sidebar navigation"""
    
    # Define page classes and their icons for easier maintenance
    PAGE_CONFIG = [
        {"name": "Dashboard", "icon": "app/resources/images/main-window/Home.png", "class": DashboardPage},
        {"name": "Inventory", "icon": "app/resources/images/main-window/Inventory.png", "class": InventoryPage},
        {"name": "Reports", "icon": "app/resources/images/main-window/Group 11.png", "class": ReportsPage},
        {"name": "Customers", "icon": "app/resources/images/main-window/Suppliers.png", "class": CustomersPage},
        {"name": "Suppliers", "icon": "app/resources/images/main-window/Suppliers.png", "class": SuppliersPage},
        {"name": "Sales", "icon": "app/resources/images/main-window/Order.png", "class": SalesPage},
        {"name": "Maintenance", "icon": "app/resources/images/main-window/Group 15.png", "class": MaintenancePage},
    ]
    
    # Bottom navigation items
    BOTTOM_NAV_CONFIG = [
        {"name": "Help", "icon": "app/resources/images/main-window/Settings.png", "class": HelpPage},
        {"name": "About", "icon": "app/resources/images/main-window/Suppliers.png", "class": AboutPage},
        {"name": "Logout", "icon": "app/resources/images/main-window/Vector.png", "action": "handle_logout"},
    ]
    
    def __init__(self, parent=None, user_info=None):
        super(MainWindow, self).__init__(parent)
        self.user_info = user_info
        self.pages = {}  # Store pages by name
        self.page_indices = {}  # Store page indices by name
        self.setupUi()
        
    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setupCentralWidget()
        self.setupWindow()
        self.apply_page_styling()
        
    def setupCentralWidget(self):
        # Create the central widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        
        # Set up the main layout
        self.main_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create the sidebar
        self.create_sidebar()
        
        # Create the stacked widget for pages
        self.stackedWidgetMain = QtWidgets.QStackedWidget()
        self.main_layout.addWidget(self.stackedWidgetMain)
        
        # Add pages with user info
        self.setup_pages_with_user_info()
        
        # Set initial page
        self.stackedWidgetMain.setCurrentIndex(0)
        
    def setupWindow(self):
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
        
    def create_sidebar(self):
        # Create sidebar widget and layout
        self.sidebar = QtWidgets.QWidget()
        self.sidebar.setFixedWidth(240) 
        self.sidebar.setStyleSheet("background-color: #232323;")
        
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(20, 20, 20, 20)
        self.sidebar_layout.setSpacing(0)
        
        # Add components to sidebar
        self.setupLogo()
        self.setupNavigationButtons()
        self.sidebar_layout.addStretch(1)  # Push bottom buttons to the bottom
        self.setupBottomButtons()
        
        # Add sidebar to main layout
        self.main_layout.addWidget(self.sidebar)
        
    def setupLogo(self):
        # Logo
        self.logo_label = QtWidgets.QLabel()
        self.logo_label.setPixmap(QtGui.QPixmap("app/resources/images/logo/Miere1.png"))
        self.logo_label.setFixedHeight(100)
        self.sidebar_layout.addWidget(self.logo_label)
        self.sidebar_layout.addSpacing(10)
        
    def setupNavigationButtons(self):
        # Navigation container
        self.nav_container = QtWidgets.QWidget()
        self.nav_layout = QtWidgets.QVBoxLayout(self.nav_container)
        self.nav_layout.setContentsMargins(0, 0, 0, 0)
        self.nav_layout.setSpacing(5)
        
        # Create navigation buttons from configuration
        for item in self.PAGE_CONFIG:
            self.create_nav_button(item["name"], item["icon"])
        
        # Add navigation container to sidebar
        self.sidebar_layout.addWidget(self.nav_container)
        
    def setupBottomButtons(self):
        # Bottom buttons container
        self.bottom_container = QtWidgets.QWidget()
        self.bottom_layout = QtWidgets.QVBoxLayout(self.bottom_container)
        self.bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.bottom_layout.setSpacing(5)
        
        # Create bottom buttons from configuration
        for item in self.BOTTOM_NAV_CONFIG:
            self.create_bottom_button(item["name"], item["icon"])
        
        # Add to sidebar
        self.sidebar_layout.addWidget(self.bottom_container)
        
    def create_nav_button(self, text, icon_path):
        button = self._create_sidebar_button(text, icon_path, 20)
        self.nav_layout.addWidget(button)
        setattr(self, f"pushButton{text}", button)
        
    def create_bottom_button(self, text, icon_path):
        button = self._create_sidebar_button(text, icon_path, 18)
        self.bottom_layout.addWidget(button)
        setattr(self, f"pushButton{text}", button)
    
    def _create_sidebar_button(self, text, icon_path, icon_size):
        """Helper method to create sidebar buttons with consistent styling"""
        button = QtWidgets.QPushButton(f" {text}")
        button.setMinimumHeight(50)
        button.setFont(QtGui.QFont("Segoe UI", 10))
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
        # Apply styling
        button.setStyleSheet("""
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
        
        # Set icon
        icon = QtGui.QIcon(icon_path)
        button.setIcon(icon)
        button.setIconSize(QtCore.QSize(icon_size, icon_size))
        
        return button
        
    def setup_pages_with_user_info(self):
        page_index = 0
        
        # Add main navigation pages
        for item in self.PAGE_CONFIG:
            page = item["class"](self, user_info=self.user_info)
            self.stackedWidgetMain.addWidget(page)
            
            # Store references to the page and its index
            self.pages[item["name"]] = page
            self.page_indices[item["name"]] = page_index
            page_index += 1
            
        # Add bottom navigation pages (except Logout which is an action)
        for item in self.BOTTOM_NAV_CONFIG:
            if "class" in item:  # Skip items without a page class (like Logout)
                page = item["class"](self, user_info=self.user_info)
                self.stackedWidgetMain.addWidget(page)
                
                # Store references
                self.pages[item["name"]] = page
                self.page_indices[item["name"]] = page_index
                page_index += 1
        
        # Connect buttons to their actions
        self.connect_buttons()
        
    def connect_buttons(self):
        # Connect main navigation buttons
        for item in self.PAGE_CONFIG:
            name = item["name"]
            button = getattr(self, f"pushButton{name}")
            index = self.page_indices[name]
            button.clicked.connect(lambda checked=False, idx=index: self.stackedWidgetMain.setCurrentIndex(idx))
        
        # Connect bottom buttons
        for item in self.BOTTOM_NAV_CONFIG:
            name = item["name"]
            button = getattr(self, f"pushButton{name}")
            
            if "action" in item:
                # Connect to a method if it's an action
                method = getattr(self, item["action"])
                button.clicked.connect(method)
            else:
                # Connect to page navigation
                index = self.page_indices[name]
                button.clicked.connect(lambda checked=False, idx=index: self.stackedWidgetMain.setCurrentIndex(idx))
    
    def apply_page_styling(self):
        """Apply consistent styling to all pages"""
        header_style = "background-color: rgba(35, 35, 35, 0.95);"
        
        for i in range(self.stackedWidgetMain.count()):
            page = self.stackedWidgetMain.widget(i)
            
            # Find header widget in each page
            for child in page.children():
                if isinstance(child, QtWidgets.QWidget) and hasattr(child, 'objectName'):
                    if 'header' in child.objectName().lower() or hasattr(child, 'isHeader'):
                        # Apply consistent style
                        child.setStyleSheet(header_style)
                        
                        # Style header labels
                        for header_child in child.children():
                            if isinstance(header_child, QtWidgets.QLabel):
                                if 'title' in header_child.objectName().lower():
                                    header_child.setStyleSheet("color: white; font-size: 24px;")
                                elif 'date' in header_child.objectName().lower():
                                    header_child.setStyleSheet("color: #E2F163; font-size: 14px;")
        
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
