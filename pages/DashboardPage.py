from PyQt5 import QtWidgets, QtCore, QtGui
from pages.BasePage import BasePage

class DashboardPage(BasePage):
    def __init__(self, parent=None):
        super(DashboardPage, self).__init__(parent)
        
    def setupUi(self):
        # Main layout
        self.layout = QtWidgets.QVBoxLayout(self)
        
        # Header
        self.widget_header = QtWidgets.QWidget()
        self.widget_header.setFixedHeight(99)
        self.widget_header.setStyleSheet("background-color: rgba(35, 35, 35, 0.95);")
        self.layout.addWidget(self.widget_header)
        
        # Scroll area
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        # Scroll content widget
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content)
        
        # Create dashboard content
        self.create_dashboard_content()
        
        self.layout.addWidget(self.scroll_area)
        
    def create_dashboard_content(self):
        # Sales Overview widget
        self.create_sales_overview_widget()
        
        # Inventory Summary widget
        self.create_inventory_summary_widget()
        
        # Purchase Overview widget
        self.create_purchase_overview_widget()
        
        # Top Selling Products widget
        self.create_top_selling_products_widget()
        
        # Product Summary widget
        self.create_product_summary_widget()
        
        # Service Summary widget
        self.create_service_summary_widget()
        
        # Top Selling Products table
        self.create_top_selling_products_table()
        
        # Low Quantity Stock widget
        self.create_low_quantity_stock_widget()
    
    def create_sales_overview_widget(self):
        sales_widget = QtWidgets.QWidget()
        sales_widget.setStyleSheet("background-color: #232323; border-radius: 10px;")
        sales_widget.setFixedHeight(201)
        
        # Title
        title_label = QtWidgets.QLabel(sales_widget)
        title_label.setGeometry(QtCore.QRect(20, 10, 171, 31))
        title_label.setStyleSheet("color: #E2F163;")
        font = QtGui.QFont("Segoe UI", 12)
        font.setBold(True)
        font.setWeight(75)
        title_label.setFont(font)
        title_label.setText("Sales Overview")
        
        # Additional widgets similar to the original UI
        # ...
        
        self.scroll_layout.addWidget(sales_widget)
    
    def create_inventory_summary_widget(self):
        # Similar to sales_overview_widget but with inventory summary content
        pass
    
    def create_purchase_overview_widget(self):
        # Similar structure with purchase overview content
        pass
    
    def create_top_selling_products_widget(self):
        # Top selling products widget
        pass
    
    def create_product_summary_widget(self):
        # Product summary widget
        pass
    
    def create_service_summary_widget(self):
        # Service summary widget
        pass
    
    def create_top_selling_products_table(self):
        # Table widget for top selling products
        pass
    
    def create_low_quantity_stock_widget(self):
        # Low quantity stock widget
        pass