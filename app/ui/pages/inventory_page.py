from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage

class InventoryPage(BasePage):
    def __init__(self, parent=None):
        super(InventoryPage, self).__init__(parent)
        
    def setupUi(self):
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Header widget with buttons
        self.header_widget = QtWidgets.QWidget()
        self.header_widget.setFixedHeight(99)
        self.header_widget.setStyleSheet("background-color: rgba(35, 35, 35, 0.95);")
        
        # Create Products and Services buttons
        self.create_header_buttons()
        
        self.layout.addWidget(self.header_widget)
        
        # Stacked widget to switch between Products and Services pages
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.create_products_page()
        self.create_services_page()
        
        self.layout.addWidget(self.stacked_widget)
        
        # Connect buttons to switch pages
        self.btn_products.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_services.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        
    def create_header_buttons(self):
        # Products button
        self.btn_products = QtWidgets.QPushButton(self.header_widget)
        self.btn_products.setGeometry(QtCore.QRect(20, 20, 121, 50))
        self.btn_products.setText("Products")
        self.btn_products.setStyleSheet(
            "background-color: white; "
            "color: #232323; "
            "border-radius: 5px;"
        )
        self.btn_products.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        font = QtGui.QFont("Segoe UI", 10)
        self.btn_products.setFont(font)
        self.btn_products.setCheckable(True)
        self.btn_products.setChecked(True)
        
        # Services button
        self.btn_services = QtWidgets.QPushButton(self.header_widget)
        self.btn_services.setGeometry(QtCore.QRect(160, 20, 131, 50))
        self.btn_services.setText("Services")
        self.btn_services.setStyleSheet(
            "background-color: white; "
            "color: #232323; "
            "border-radius: 5px;"
        )
        self.btn_services.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_services.setFont(font)
        self.btn_services.setCheckable(True)
        
    def create_products_page(self):
        products_page = QtWidgets.QWidget()
        
        # Create a scroll area
        scroll_area = QtWidgets.QScrollArea(products_page)
        scroll_area.setGeometry(QtCore.QRect(0, 0, 1041, 621))
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_area.setWidgetResizable(True)
        
        # Create scroll content
        scroll_content = QtWidgets.QWidget()
        scroll_area.setWidget(scroll_content)
        
        # Create layout for content
        v_layout = QtWidgets.QVBoxLayout(scroll_content)
        
        # Create widgets like in the original UI
        # Overall Inventory section
        self.create_overall_inventory_section(v_layout)
        
        # Products table
        self.create_products_table(v_layout)
        
        self.stacked_widget.addWidget(products_page)
        
    def create_services_page(self):
        services_page = QtWidgets.QWidget()
        
        # Create content for services page
        label = QtWidgets.QLabel(services_page)
        label.setGeometry(QtCore.QRect(490, 280, 55, 16))
        label.setText("services")
        
        self.stacked_widget.addWidget(services_page)
        
    def create_overall_inventory_section(self, parent_layout):
        # Create a widget for the overall inventory section
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background-color: #232323; border-radius: 10px;")
        
        # Add title and other elements
        title_label = QtWidgets.QLabel(widget)
        title_label.setGeometry(QtCore.QRect(20, 10, 171, 31))
        title_label.setStyleSheet("color: #E2F163;")
        font = QtGui.QFont("Segoe UI", 12)
        font.setBold(True)
        font.setWeight(75)
        title_label.setFont(font)
        title_label.setText("Overall Inventory")
        
        # Add other labels and stats like in the original UI
        # ...
        
        parent_layout.addWidget(widget)
        
    def create_products_table(self, parent_layout):
        # Create a widget for the products table
        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background-color: #232323; border-radius: 10px;")
        
        # Create table widget
        table = QtWidgets.QTableWidget(widget)
        table.setGeometry(QtCore.QRect(10, 10, 951, 371))
        table.setColumnCount(7)
        
        # Set headers
        headers = ["New Column", "New Column", "New Column", "New Column", 
                  "New Column", "New Column", "New Column"]
        
        for i, header in enumerate(headers):
            item = QtWidgets.QTableWidgetItem(header)
            table.setHorizontalHeaderItem(i, item)
        
        parent_layout.addWidget(widget)