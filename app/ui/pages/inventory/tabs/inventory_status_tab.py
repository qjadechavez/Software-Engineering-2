from PyQt5 import QtWidgets, QtCore, QtGui
from app.utils.db_manager import DBManager
import mysql.connector
from ..table_factory import TableFactory

class InventoryStatusTab(QtWidgets.QWidget):
    """Tab for viewing inventory status"""
    
    def __init__(self, parent=None):
        super(InventoryStatusTab, self).__init__()
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components for the inventory status tab"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 10)
        self.layout.setSpacing(15)
        
        # Add inventory analytics section - matching overview tab style
        self.create_inventory_metrics_section()
        
        # Create inventory table
        self.inventory_table = TableFactory.create_table()
        
        # Define column headers and their relative widths
        inventory_columns = [
            ("ID", 0.08),
            ("Product Name", 0.20), 
            ("Quantity", 0.12),
            ("Status", 0.18),
            ("Last Updated", 0.22),
            ("Notes", 0.20)
        ]
        
        # Configure the table columns
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.inventory_table, inventory_columns, screen_width)
        
        self.layout.addWidget(self.inventory_table)
    
    def create_metric_item(self, title, value, icon_type, color):
        """Create a smaller metric item matching overview tab style"""
        metric = QtWidgets.QFrame()
        metric.setFrameShape(QtWidgets.QFrame.StyledPanel)
        metric.setFixedHeight(80)  # Fixed smaller height
        metric.setStyleSheet(f"""
            QFrame {{
                background-color: #2a2a2a;
                border-radius: 6px;
                border-left: 3px solid {color};
                border-top: none;
                border-right: none;
                border-bottom: none;
            }}
        """)
        
        layout = QtWidgets.QHBoxLayout(metric)  # Changed to horizontal layout
        layout.setContentsMargins(12, 8, 12, 8)  # Smaller margins
        layout.setSpacing(8)
        
        # Icon
        icon_label = QtWidgets.QLabel()
        icon_map = {
            "warning": "⚠️",
            "alert": "⚠️",
            "error": "❌",
            "info": "ℹ️"
        }
        icon_label.setText(icon_map.get(icon_type, "•"))
        icon_label.setStyleSheet(f"color: {color}; font-size: 18px; background: transparent;")  # Smaller icon
        icon_label.setFixedSize(24, 24)
        
        # Text content
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(2)  # Reduced spacing
        text_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            color: #cccccc;
            font-size: 11px;
            font-weight: normal;
        """)
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet(f"""
            color: white;
            font-size: 16px;
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
    
    def create_inventory_metrics_section(self):
        """Create compact inventory metrics section"""
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
        metrics_layout.setContentsMargins(15, 12, 15, 12)  # Smaller margins
        metrics_layout.setSpacing(10)  # Reduced spacing
        
        # Metrics header
        metrics_header = QtWidgets.QLabel("Inventory Status Metrics")
        metrics_header.setStyleSheet("color: white; font-size: 14px; font-weight: bold; border: none;")  # Smaller font
        metrics_layout.addWidget(metrics_header)
        
        # Metrics row layout
        metrics_grid = QtWidgets.QHBoxLayout()
        metrics_grid.setSpacing(10)  # Reduced spacing between metrics
        
        # Create inventory metric items
        self.low_stock_metric = self.create_metric_item("Low Stock Items", "0", "warning", "#FF5252")
        self.expired_metric = self.create_metric_item("Expired Items", "0", "error", "#FF9800")
        self.total_metric = self.create_metric_item("Total Products", "0", "info", "#4CAF50")
        self.received_metric = self.create_metric_item("Recently Received", "0", "info", "#2196F3")
        
        metrics_grid.addWidget(self.low_stock_metric)
        metrics_grid.addWidget(self.expired_metric)
        metrics_grid.addWidget(self.total_metric)
        metrics_grid.addWidget(self.received_metric)
        
        metrics_layout.addLayout(metrics_grid)
        
        # Add metrics section with zero stretch factor
        self.layout.addWidget(metrics_frame, 0)
    
    def load_inventory(self):
        """Load inventory data from the new inventory_status table"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.inventory_table.setRowCount(0)
            
            # Query for inventory status items
            cursor.execute("""
                SELECT 
                    inventory_id,
                    product_name,
                    quantity,
                    status,
                    last_updated
                FROM inventory_status
                ORDER BY last_updated DESC
            """)
            
            inventory_items = cursor.fetchall()
            
            # Populate the table
            self.inventory_table.setRowCount(len(inventory_items))
            
            for row, item in enumerate(inventory_items):
                # ID
                id_item = QtWidgets.QTableWidgetItem(str(item['inventory_id']))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.inventory_table.setItem(row, 0, id_item)
                
                # Product Name
                self.inventory_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item['product_name']))
                
                # Quantity
                qty_item = QtWidgets.QTableWidgetItem(str(item['quantity']))
                qty_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.inventory_table.setItem(row, 2, qty_item)
                
                # Status with color coding
                status = item['status'] or "Unknown"
                status_item = QtWidgets.QTableWidgetItem(status)
                status_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                # Set color based on status
                if status == 'In Stock':
                    status_item.setForeground(QtGui.QColor("#4CAF50"))  # Green
                elif status == 'Low Stock':
                    status_item.setForeground(QtGui.QColor("#FF9800"))  # Orange
                elif status == 'Out of Stock':
                    status_item.setForeground(QtGui.QColor("#FF5252"))  # Red
                elif status == 'Received':
                    status_item.setForeground(QtGui.QColor("#2196F3"))  # Blue
                elif status == 'Updated':
                    status_item.setForeground(QtGui.QColor("#9C27B0"))  # Purple
                    
                self.inventory_table.setItem(row, 3, status_item)
                
                # Last Updated
                last_updated = item.get('last_updated')
                last_updated_str = last_updated.strftime('%Y-%m-%d %I:%M %p') if last_updated else "N/A"
                self.inventory_table.setItem(row, 4, QtWidgets.QTableWidgetItem(last_updated_str))
                
                # Notes (based on status)
                notes = ""
                if status == 'Received':
                    notes = "Recently received from supplier"
                elif status == 'Low Stock':
                    notes = "Needs restocking"
                elif status == 'Out of Stock':
                    notes = "Urgent: Out of stock"
                    
                self.inventory_table.setItem(row, 5, QtWidgets.QTableWidgetItem(notes))
            
            cursor.close()
            print(f"✓ Loaded {len(inventory_items)} inventory status records")
            
        except mysql.connector.Error as err:
            print(f"Error loading inventory status: {err}")
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def update_analytics(self):
        """Update inventory analytics metrics"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get total products count
            cursor.execute("SELECT COUNT(*) as count FROM inventory_status")
            total_count = cursor.fetchone()['count']
            
            # Get low stock items count
            cursor.execute("""
                SELECT COUNT(*) as count FROM inventory_status 
                WHERE status = 'Low Stock'
            """)
            low_stock_count = cursor.fetchone()['count']
            
            # Get expired items count (from products table)
            cursor.execute("""
                SELECT COUNT(*) as count FROM products 
                WHERE expiry_date IS NOT NULL AND expiry_date < CURDATE()
            """)
            expired_count = cursor.fetchone()['count']
            
            # Get recently received items count
            cursor.execute("""
                SELECT COUNT(*) as count FROM inventory_status 
                WHERE status = 'Received' AND last_updated >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            """)
            received_count = cursor.fetchone()['count']
            
            # Update the metrics
            self.low_stock_metric.value_label.setText(str(low_stock_count))
            self.expired_metric.value_label.setText(str(expired_count))
            self.total_metric.value_label.setText(str(total_count))
            self.received_metric.value_label.setText(str(received_count))
            
            cursor.close()
            print(f"✓ Updated analytics: Total={total_count}, Low Stock={low_stock_count}, Expired={expired_count}, Recently Received={received_count}")
            
        except mysql.connector.Error as err:
            print(f"Error updating analytics: {err}")
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")