from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage
from app.utils.db_manager import DBManager
from app.utils.dashboard_updater import DashboardUpdater
import mysql.connector
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')

class DashboardPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(DashboardPage, self).__init__(parent, title="Dashboard", user_info=user_info)
        self.user_info = user_info
    
    def createContent(self):
        # Content area - matching other pages style
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(15)
        
        # Dashboard header
        self.create_header()
        
        # Key metrics cards
        self.create_metrics_cards()
        
        # Charts section
        charts_layout = QtWidgets.QHBoxLayout()
        charts_layout.setSpacing(20)
        
        # Sales analytics chart
        self.sales_chart_widget = self.create_chart_widget(
            "Sales Analytics", 
            "Track daily revenue and transaction volume",
            self.create_sales_chart,
            "SalesReports"
        )
        
        # Inventory status chart
        self.inventory_chart_widget = self.create_chart_widget(
            "Inventory Status", 
            "Monitor stock levels and product availability",
            self.create_inventory_chart,
            "Inventory"
        )
        
        charts_layout.addWidget(self.sales_chart_widget)
        charts_layout.addWidget(self.inventory_chart_widget)
        
        # Add charts layout with stretch factor to maximize space
        self.content_layout.addLayout(charts_layout, 1)
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
        
        # Load initial data
        self.load_dashboard_data()
    
    def create_header(self):
        """Create dashboard header with welcome message and timestamp"""
        header_frame = QtWidgets.QFrame()
        header_frame.setFixedHeight(80)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #232323;
                border-radius: 12px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }
        """)
        header_layout = QtWidgets.QHBoxLayout(header_frame)
        header_layout.setContentsMargins(25, 15, 25, 15)
        
        # Welcome section
        welcome_layout = QtWidgets.QVBoxLayout()
        
        user_name = self.user_info.get('full_name', 'User') if self.user_info else 'User'
        welcome_label = QtWidgets.QLabel(f"Welcome back, {user_name}!")
        welcome_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold; border: none;")
        
        current_time = datetime.now().strftime("%A, %B %d, %Y")
        time_label = QtWidgets.QLabel(current_time)
        time_label.setStyleSheet("color: #cccccc; font-size: 12px; border: none;")
        
        welcome_layout.addWidget(welcome_label)
        welcome_layout.addWidget(time_label)
        
        # System status
        status_layout = QtWidgets.QVBoxLayout()
        status_layout.setAlignment(QtCore.Qt.AlignRight)
        
        status_label = QtWidgets.QLabel("System Status")
        status_label.setStyleSheet("color: #cccccc; font-size: 10px; border: none;")
        status_label.setAlignment(QtCore.Qt.AlignRight)
        
        online_label = QtWidgets.QLabel("● Online")
        online_label.setStyleSheet("color: #4CAF50; font-size: 12px; font-weight: bold; border: none;")
        online_label.setAlignment(QtCore.Qt.AlignRight)
        
        status_layout.addWidget(status_label)
        status_layout.addWidget(online_label)
        
        header_layout.addLayout(welcome_layout)
        header_layout.addStretch()
        header_layout.addLayout(status_layout)
        
        self.content_layout.addWidget(header_frame)
    
    def create_metrics_cards(self):
        """Create key metrics cards"""
        metrics_layout = QtWidgets.QHBoxLayout()
        metrics_layout.setSpacing(15)
        
        # Total Revenue card
        self.total_revenue_card = self.create_metric_card("Total Revenue", "₱0.00", "#4CAF50", "")
        
        # Today's Revenue card
        self.today_revenue_card = self.create_metric_card("Today's Revenue", "₱0.00", "#2196F3", "")
        
        # Services card
        self.services_card = self.create_metric_card("Total Services", "0", "#9C27B0", "")
        
        # Today's Transactions card
        self.transactions_card = self.create_metric_card("Today's Transactions", "0", "#FF9800", "")
        
        metrics_layout.addWidget(self.total_revenue_card)
        metrics_layout.addWidget(self.today_revenue_card)
        metrics_layout.addWidget(self.services_card)
        metrics_layout.addWidget(self.transactions_card)
        
        self.content_layout.addLayout(metrics_layout)
    
    def create_metric_card(self, title, value, color, icon):
        """Create a metric card widget"""
        card = QtWidgets.QFrame()
        card.setFixedHeight(100)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #2a2a2a;
                border-radius: 10px;
                border-left: 4px solid {color};
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)
        
        # Icon and title row
        top_layout = QtWidgets.QHBoxLayout()
        
        icon_label = QtWidgets.QLabel(icon)
        icon_label.setStyleSheet(f"color: {color}; font-size: 20px; border: none;")
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("color: #cccccc; font-size: 10px; font-weight: bold; border: none;")
        
        top_layout.addWidget(icon_label)
        top_layout.addStretch()
        top_layout.addWidget(title_label)
        
        # Value
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet(f"color: white; font-size: 24px; font-weight: bold; border: none;")
        value_label.setAlignment(QtCore.Qt.AlignCenter)
        
        layout.addLayout(top_layout)
        layout.addWidget(value_label)
        layout.addStretch()
        
        # Store reference for updates
        card.value_label = value_label
        
        return card
    
    def create_chart_widget(self, title, description, chart_function, page_name):
        """Create a chart widget with view all functionality"""
        widget = QtWidgets.QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: #232323;
                border-radius: 12px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(widget)
        layout.setContentsMargins(15, 10, 15, 10) 
        layout.setSpacing(8)  # Reduced spacing
        
        # Header with title and view all button
        header_layout = QtWidgets.QHBoxLayout()
        
        title_layout = QtWidgets.QVBoxLayout()
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; border: none;")  # Smaller font
        
        desc_label = QtWidgets.QLabel(description)
        desc_label.setStyleSheet("color: #cccccc; font-size: 10px; border: none;") 
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(desc_label)
        

        
        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        
        layout.addLayout(header_layout)
        
        # Chart area 
        chart_frame = chart_function()
        layout.addWidget(chart_frame, 1)
        
        return widget
    
    def create_sales_chart(self):
        """Create sales analytics chart with zoomed out view"""
        # Smaller figure size for zoomed out effect
        figure = Figure(figsize=(6, 3.5), facecolor='#232323', dpi=80)  # Reduced DPI and size
        canvas = FigureCanvas(figure)
        canvas.setStyleSheet("background-color: #232323;")
        
        ax = figure.add_subplot(111)
        ax.set_facecolor('#232323')
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get daily transaction data for the last 7 days
            cursor.execute("""
                SELECT 
                    DATE(transaction_date) as date,
                    COUNT(*) as transactions,
                    SUM(total_amount) as revenue
                FROM transactions 
                WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                GROUP BY DATE(transaction_date)
                ORDER BY date
            """)
            
            data = cursor.fetchall()
            cursor.close()
            
            if data:
                dates = [item['date'].strftime('%m/%d') for item in data]
                revenue = [float(item['revenue']) for item in data]
                transactions = [item['transactions'] for item in data]
            else:
                dates = ['No Data']
                revenue = [0]
                transactions = [0]
            
        except Exception as e:
            print(f"Error loading sales data: {e}")
            dates = ['No Data']
            revenue = [0]
            transactions = [0]
        
        # Create bar chart for revenue
        bars = ax.bar(dates, revenue, color='#4CAF50', alpha=0.7, label='Revenue (₱)', width=0.5)
        
        # Create line chart for transactions on secondary y-axis
        ax2 = ax.twinx()
        line = ax2.plot(dates, transactions, color='#FF9800', marker='o', linewidth=2, markersize=4, label='Transactions')
        
        # Styling with smaller fonts for zoomed out view
        ax.set_ylabel('Revenue (₱)', color='white', fontsize=9)
        ax2.set_ylabel('Transactions', color='white', fontsize=9)
        ax.set_xlabel('Date', color='white', fontsize=9)
        
        ax.tick_params(colors='white', labelsize=8)
        ax2.tick_params(colors='white', labelsize=8)
        ax.grid(True, alpha=0.2)
        
        # Compact legend
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', 
                 facecolor='#333', edgecolor='white', labelcolor='white', fontsize=8)
        
        # Tighter layout
        figure.subplots_adjust(left=0.1, right=0.9, top=0.95, bottom=0.15)
        
        return canvas
    
    def create_inventory_chart(self):
        """Create inventory status chart with zoomed out view"""
        figure = Figure(figsize=(6, 3.5), facecolor='#232323', dpi=80)  # Reduced DPI and size
        canvas = FigureCanvas(figure)
        canvas.setStyleSheet("background-color: #232323;")
        
        ax = figure.add_subplot(111)
        ax.set_facecolor('#232323')
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get product categories and their stock levels
            cursor.execute("""
                SELECT 
                    category,
                    COUNT(*) as total_products,
                    SUM(CASE WHEN quantity > threshold_value THEN 1 ELSE 0 END) as in_stock,
                    SUM(CASE WHEN quantity <= threshold_value AND quantity > 0 THEN 1 ELSE 0 END) as low_stock,
                    SUM(CASE WHEN quantity = 0 THEN 1 ELSE 0 END) as out_of_stock
                FROM products 
                WHERE category IS NOT NULL AND category != ''
                GROUP BY category
                ORDER BY total_products DESC
                LIMIT 5
            """)
            
            data = cursor.fetchall()
            cursor.close()
            
            if data:
                categories = [item['category'][:8] + '...' if len(item['category']) > 8 else item['category'] for item in data] 
                in_stock = [item['in_stock'] for item in data]
                low_stock = [item['low_stock'] for item in data]
                out_of_stock = [item['out_of_stock'] for item in data]
                
                # Create stacked bar chart with narrower bars
                x_pos = range(len(categories))
                bar_width = 0.4  # Narrower bars
                
                bars1 = ax.bar(x_pos, in_stock, bar_width, color='#4CAF50', alpha=0.8, label='In Stock')
                bars2 = ax.bar(x_pos, low_stock, bar_width, bottom=in_stock, color='#FF9800', alpha=0.8, label='Low Stock')
                bars3 = ax.bar(x_pos, out_of_stock, bar_width,
                             bottom=[i+j for i,j in zip(in_stock, low_stock)], 
                             color='#F44336', alpha=0.8, label='Out of Stock')
                
                ax.set_xticks(x_pos)
                ax.set_xticklabels(categories, rotation=45, ha='right')
                
                # Add smaller value labels on bars
                for i, (category, total) in enumerate(zip(categories, [i+j+k for i,j,k in zip(in_stock, low_stock, out_of_stock)])):
                    if total > 0:  # Only show label if there's data
                        ax.text(i, total + 0.1, str(total), ha='center', va='bottom', color='white', fontweight='bold', fontsize=8)
                
            else:
                ax.text(0.5, 0.5, 'No Product Data Available', ha='center', va='center', 
                       transform=ax.transAxes, color='white', fontsize=12)
                
        except Exception as e:
            print(f"Error loading inventory data: {e}")
            ax.text(0.5, 0.5, ' ', ha='center', va='center', 
                   transform=ax.transAxes, color='white', fontsize=12)
        
        # Styling with smaller fonts for zoomed out view
        ax.set_ylabel('Products', color='white', fontsize=9)
        ax.set_xlabel('Categories', color='white', fontsize=9)
        
        ax.tick_params(colors='white', labelsize=8)
        ax.grid(True, alpha=0.2, axis='y')
        
        # Compact legend
        ax.legend(loc='upper right', facecolor='#333', edgecolor='white', labelcolor='white', fontsize=8)
        
        # Tighter layout
        figure.subplots_adjust(left=0.12, right=0.95, top=0.95, bottom=0.25)
        
        return canvas
    
    def navigate_to_page(self, page_name):
        """Navigate to specified page"""
        main_window = self.parent()
        while main_window and not hasattr(main_window, 'stackedWidgetMain'):
            main_window = main_window.parent()
        
        if main_window and hasattr(main_window, 'page_manager'):
            if page_name == "SalesReports":
                # Navigate to Reports page and switch to Sales Report tab
                for nav_item in main_window.page_manager.nav_items:
                    if nav_item.text == "Reports & Analytics":
                        page_index = main_window.page_manager.nav_items.index(nav_item)
                        main_window.stackedWidgetMain.setCurrentIndex(page_index)
                        
                        # Switch to Sales Report tab
                        reports_page = main_window.stackedWidgetMain.currentWidget()
                        if hasattr(reports_page, 'tabs'):
                            reports_page.tabs.setCurrentIndex(2) 
                        break
                        
            elif page_name == "Inventory":
                # Navigate to Inventory page
                for nav_item in main_window.page_manager.nav_items:
                    if nav_item.text == "Inventory":
                        page_index = main_window.page_manager.nav_items.index(nav_item)
                        main_window.stackedWidgetMain.setCurrentIndex(page_index)
                        break
    
    def refresh_dashboard(self):
        """Refresh dashboard data - called after transactions"""
        DashboardUpdater.refresh_metrics_and_charts(self)

    def showEvent(self, event):
        """Called when the page is shown"""
        super().showEvent(event)
        # Use QTimer to ensure the refresh happens after the page is fully displayed
        QtCore.QTimer.singleShot(100, lambda: DashboardUpdater.refresh_metrics_and_charts(self))
    
    def load_dashboard_data(self):
        """Load dashboard data from database"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Load total revenue (all time)
            cursor.execute("""
                SELECT COALESCE(SUM(total_amount), 0) as total_revenue 
                FROM transactions
            """)
            total_revenue_data = cursor.fetchone()
            total_revenue = total_revenue_data['total_revenue'] if total_revenue_data else 0
            
            # Load today's revenue
            cursor.execute("""
                SELECT COALESCE(SUM(total_amount), 0) as daily_revenue 
                FROM transactions 
                WHERE DATE(transaction_date) = CURDATE()
            """)
            daily_revenue_data = cursor.fetchone()
            daily_revenue = daily_revenue_data['daily_revenue'] if daily_revenue_data else 0
            
            # Load total services count
            cursor.execute("SELECT COUNT(*) as count FROM services")
            services_count = cursor.fetchone()['count']
            
            # Load today's transactions count
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM transactions 
                WHERE DATE(transaction_date) = CURDATE()
            """)
            transactions_count = cursor.fetchone()['count']
            
            # Update metric cards
            self.total_revenue_card.value_label.setText(f"₱{total_revenue:,.2f}")
            self.today_revenue_card.value_label.setText(f"₱{daily_revenue:,.2f}")
            self.services_card.value_label.setText(str(services_count))
            self.transactions_card.value_label.setText(str(transactions_count))
            
            cursor.close()
            
        except mysql.connector.Error as err:
            print(f"Database error loading dashboard: {err}")
        except Exception as e:
            print(f"Error loading dashboard data: {e}")