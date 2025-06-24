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
        
        # Add inventory analytics section
        analytics_layout = QtWidgets.QHBoxLayout()
        analytics_layout.setSpacing(15)
        
        # Create info cards
        self.low_stock_card = self.create_info_card("Low Stock Items", "0", "#FF5252", "warning")
        self.expired_card = self.create_info_card("Expired Items", "0", "#FF9800", "expired")
        self.total_card = self.create_info_card("Total Products", "0", "#4CAF50", "products")
        self.received_card = self.create_info_card("Recently Received", "0", "#2196F3", "received")
        
        analytics_layout.addWidget(self.low_stock_card)
        analytics_layout.addWidget(self.expired_card)
        analytics_layout.addWidget(self.total_card)
        analytics_layout.addWidget(self.received_card)
        
        self.layout.addLayout(analytics_layout)
        
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
    
    def create_info_card(self, title, value, color, icon_type=None, subtitle=None):
        """Create an info card for the inventory dashboard"""
        card = QtWidgets.QFrame()
        card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #232323;
                border-radius: 10px;
                border-left: 5px solid {color};
                padding: 10px;
                min-height: 80px;
            }}
        """)
        
        card_layout = QtWidgets.QHBoxLayout(card)
        card_layout.setContentsMargins(15, 10, 15, 10)
        
        # Add icon based on card type
        icon_label = QtWidgets.QLabel()
        icon_label.setFixedSize(60, 60)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        icon_label.setText("●")
        icon_label.setStyleSheet(f"""
            color: {color};
            font-size: 40px;
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
            font-size: 24px;
            font-weight: bold;
        """)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        
        # Add icon and text to card layout
        card_layout.addWidget(icon_label)
        card_layout.addLayout(text_layout, 1)
        
        card.value_label = value_label
        card.title = title
        
        return card
    
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
        """Update inventory analytics cards"""
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
            
            # Update the info cards
            self.low_stock_card.value_label.setText(str(low_stock_count))
            self.expired_card.value_label.setText(str(expired_count))
            self.total_card.value_label.setText(str(total_count))
            self.received_card.value_label.setText(str(received_count))
            
            cursor.close()
            print(f"✓ Updated analytics: Total={total_count}, Low Stock={low_stock_count}, Expired={expired_count}, Recently Received={received_count}")
            
        except mysql.connector.Error as err:
            print(f"Error updating analytics: {err}")
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")