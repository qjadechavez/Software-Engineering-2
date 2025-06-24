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
        
        analytics_layout.addWidget(self.low_stock_card)
        analytics_layout.addWidget(self.expired_card)
        analytics_layout.addWidget(self.total_card)
        
        self.layout.addLayout(analytics_layout)
        
        # Create inventory table
        self.inventory_table = TableFactory.create_table()
        
        # Define column headers and their relative widths
        inventory_columns = [
            ("ID", 0.05),
            ("Product Name", 0.35), 
            ("Quantity", 0.15),
            ("Status", 0.20),
            ("Last Updated", 0.25)
        ]
        
        # Configure the table columns
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.inventory_table, inventory_columns, screen_width)
        
        self.layout.addWidget(self.inventory_table)
    
    def create_info_card(self, title, value, color, icon_type=None, subtitle=None):
        """Create an info card for the inventory dashboard with larger icons
        
        Args:
            title: The title of the card
            value: The main value to display
            color: The accent color for the card
            icon_type: The type of icon to display (warning, expired, products, etc.)
            subtitle: Optional subtitle to display beneath the main value
        
        Returns:
            QFrame: The info card frame
        """
        card = QtWidgets.QFrame()
        card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #232323;
                border-radius: 10px;
                border-left: 5px solid {color};
                padding: 10px;
                min-height: 60px;
            }}
        """)
        
        card_layout = QtWidgets.QHBoxLayout(card)
        card_layout.setContentsMargins(15, 10, 15, 10)
        
        # Add icon based on card type
        icon_label = QtWidgets.QLabel()
        icon_path = ""
        
        if icon_type == "warning":
            icon_path = "app/resources/images/inventory/low-stocks-items.png"
        elif icon_type == "expired":
            icon_path = "app/resources/images/inventory/expired-items.png"
        elif icon_type == "products":
            icon_path = "app/resources/images/inventory/total-products.png"
        elif icon_type == "categories":
            icon_path = "app/resources/images/inventory/product-categories.png"
        elif icon_type == "services":
            icon_path = "app/resources/images/inventory/services.png"
        
        icon_label.setFixedSize(200, 200)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        if icon_path and QtCore.QFile(icon_path).exists():
            pixmap = QtGui.QPixmap(icon_path)
            scaled_pixmap = pixmap.scaled(
                150, 150,
                QtCore.Qt.KeepAspectRatio,
                QtCore.Qt.SmoothTransformation
            )
            icon_label.setPixmap(scaled_pixmap)
        else:
            icon_label.setText("●")
            icon_label.setStyleSheet(f"""
                color: {color};
                font-size: 60px;
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
            font-size: 32px;
            font-weight: bold;
        """)
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        
        # Add subtitle if provided
        if subtitle:
            subtitle_label = QtWidgets.QLabel(subtitle)
            subtitle_label.setStyleSheet("""
                color: #CCCCCC;
                font-size: 12px;
            """)
            text_layout.addWidget(subtitle_label)
            card.subtitle_label = subtitle_label
        
        # Add icon and text to card layout
        card_layout.addWidget(icon_label)
        card_layout.addLayout(text_layout, 1)
        
        card.value_label = value_label
        card.title = title
        
        return card
    
    def load_inventory(self):
        """Load inventory data from the database"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.inventory_table.setRowCount(0)
            
            # Query for inventory items with product names
            cursor.execute("""
                SELECT i.inventory_id, p.product_name, i.quantity, i.status, i.last_updated
                FROM inventory i
                JOIN products p ON i.product_id = p.product_id
                ORDER BY i.last_updated DESC
            """)
            
            inventory_items = cursor.fetchall()
            
            # Populate the table
            self.inventory_table.setRowCount(len(inventory_items))
            
            for row, item in enumerate(inventory_items):
                self.inventory_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item['inventory_id'])))
                self.inventory_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item['product_name']))
                self.inventory_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(item['quantity'])))
                self.inventory_table.setItem(row, 3, QtWidgets.QTableWidgetItem(item['status'] or "N/A"))
                
                # Format last updated date
                last_updated = item.get('last_updated')
                last_updated_str = last_updated.strftime('%Y-%m-%d %H:%M') if last_updated else "N/A"
                self.inventory_table.setItem(row, 4, QtWidgets.QTableWidgetItem(last_updated_str))
            
            cursor.close()
            
        except mysql.connector.Error as err:
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
            cursor.execute("SELECT COUNT(*) as count FROM products")
            total_count = cursor.fetchone()['count']
            
            # Get low stock items count
            cursor.execute("""
                SELECT COUNT(*) as count FROM products 
                WHERE quantity <= threshold_value
            """)
            low_stock_count = cursor.fetchone()['count']
            
            # Get expired items count
            cursor.execute("""
                SELECT COUNT(*) as count FROM products 
                WHERE expiry_date IS NOT NULL AND expiry_date < CURDATE()
            """)
            expired_count = cursor.fetchone()['count']
            
            # Update the info cards
            self.low_stock_card.value_label.setText(str(low_stock_count))
            self.expired_card.value_label.setText(str(expired_count))
            self.total_card.value_label.setText(str(total_count))
            
            cursor.close()
        
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")