from PyQt5 import QtWidgets, QtCore, QtGui
from app.utils.db_manager import DBManager
import mysql.connector
from datetime import datetime

class OverviewTab(QtWidgets.QWidget):
    """Tab for displaying overall inventory dashboard"""
    
    def __init__(self, parent=None):
        super(OverviewTab, self).__init__()
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components for the overview tab"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 10)
        self.layout.setSpacing(10)
        
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
        self.layout.addLayout(header_layout, 0)
        
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
        self.layout.addLayout(summary_layout, 0)
        
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
        self.layout.addWidget(metrics_frame, 0)
        
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

        # Add table to activity layout
        activity_layout.addWidget(self.activity_table)

        # Add activity frame with stretch factor 1 so it takes all remaining space
        self.layout.addWidget(activity_frame, 1)
    
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
        
    def update_dashboard(self):
        """Update the overview dashboard with fresh data"""
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
            
            # Get recent activity data - FIXED QUERY
            cursor.execute("""
                SELECT 
                    it.product_name,
                    it.transaction_type as status,
                    it.quantity,
                    it.transaction_date as last_updated
                FROM inventory_transactions it
                ORDER BY it.transaction_date DESC
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
                if data['status'] == 'Stock In':
                    status_item.setForeground(QtGui.QColor("#4CAF50"))  # Green for stock in
                elif data['status'] == 'Stock Out':
                    status_item.setForeground(QtGui.QColor("#FF5252"))  # Red for stock out
                elif data['status'] == 'Adjustment':
                    status_item.setForeground(QtGui.QColor("#2196F3"))  # Blue for adjustment
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
            
            print("✓ Overview dashboard updated successfully")
            
        except mysql.connector.Error as err:
            print(f"Error updating dashboard: {err}")
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def view_all_clicked(self, event):
        """Handle click on the View All link to switch to Inventory Status tab"""
        # Signal to parent to switch to inventory status tab
        if self.parent and hasattr(self.parent, "switch_to_inventory_status"):
            self.parent.switch_to_inventory_status()