from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
import mysql.connector
from app.utils.db_manager import DBManager
from datetime import datetime, timedelta
from ..table_factory import TableFactory
from ..style_factory import StyleFactory
from ..control_panel_factory import ControlPanelFactory

class DeliveredProductsTab(QtWidgets.QWidget):
    """Tab for displaying delivered/received products report"""
    
    def __init__(self, parent=None):
        super(DeliveredProductsTab, self).__init__()
        self.parent = parent
        self.filter_state = {
            "is_active": False,
            "date_range": "All Time",
            "supplier": "All Suppliers",
            "status": "All Statuses"
        }
        self.setup_ui()
        self.load_delivered_products()
    
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(15)
        
        # Header section
        header_layout = QtWidgets.QVBoxLayout()
        
        title_label = QtWidgets.QLabel("Delivered Products Report")
        title_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        desc_label = QtWidgets.QLabel("Track all products that have been delivered and received into inventory")
        desc_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        header_layout.addWidget(desc_label)
        
        self.layout.addLayout(header_layout)
        
        # Search and filter controls
        self.search_input = QtWidgets.QLineEdit()
        self.control_layout = ControlPanelFactory.create_search_control(
            self.search_input,
            self.filter_delivered_products,
            self.show_filter_dialog
        )
        
        # Store references
        self.filter_button = self.control_layout.filter_button
        self.filter_indicator = self.control_layout.filter_indicator
        
        self.layout.addLayout(self.control_layout)
        
        # Statistics summary
        stats_frame = QtWidgets.QFrame()
        stats_frame.setStyleSheet(StyleFactory.get_section_frame_style())
        stats_layout = QtWidgets.QHBoxLayout(stats_frame)
        stats_layout.setContentsMargins(15, 10, 15, 10)
        
        # Create statistics cards
        self.total_deliveries_label = self.create_stat_card("Total Deliveries", "0", "#4CAF50")
        self.total_quantity_label = self.create_stat_card("Total Quantity", "0", "#2196F3")
        self.unique_products_label = self.create_stat_card("Unique Products", "0", "#FF9800")
        self.recent_deliveries_label = self.create_stat_card("Recent (7 days)", "0", "#9C27B0")
        
        stats_layout.addWidget(self.total_deliveries_label)
        stats_layout.addWidget(self.total_quantity_label)
        stats_layout.addWidget(self.unique_products_label)
        stats_layout.addWidget(self.recent_deliveries_label)
        stats_layout.addStretch()
        
        self.layout.addWidget(stats_frame)
        
        # Create delivered products table
        self.delivered_table = TableFactory.create_table()
        
        # Define column headers and their relative widths
        delivered_columns = [
            ("ID", 0.06),
            ("Product Name", 0.20),
            ("Supplier", 0.15),
            ("Quantity Delivered", 0.11),
            ("Delivery Date", 0.12),
            ("Status", 0.10),
            ("Notes", 0.18),
            ("Updated", 0.08)
        ]
        
        # Configure the table columns
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.delivered_table, delivered_columns, screen_width)
        
        # Add context menu
        self.delivered_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.delivered_table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.layout.addWidget(self.delivered_table)
        
        # Add filter indicator label
        self.filter_indicator = QtWidgets.QLabel()
        self.filter_indicator.setVisible(False)
        self.filter_indicator.setStyleSheet("""
            QLabel {
                color: #4FC3F7;
                font-style: italic;
                padding-top: 5px;
            }
        """)
        self.layout.addWidget(self.filter_indicator)
    
    def create_stat_card(self, title, value, color):
        """Create a statistics card widget"""
        card = QtWidgets.QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #333333;
                border: 2px solid {color};
                border-radius: 8px;
                padding: 10px;
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout(card)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("color: #cccccc; font-size: 11px; font-weight: bold;")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: bold;")
        value_label.setAlignment(QtCore.Qt.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        
        # Store reference to value label for updates
        card.value_label = value_label
        
        return card
    
    def load_delivered_products(self):
        """Load delivered products from the database"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.delivered_table.clearContents()
            self.delivered_table.setRowCount(0)
            
            # Query for delivered products from inventory_status table
            cursor.execute("""
                SELECT 
                    inventory_id,
                    product_name,
                    supplier_name,
                    quantity,
                    status,
                    last_updated,
                    created_at
                FROM inventory_status 
                WHERE status = 'Received'
                ORDER BY last_updated DESC
            """)
            
            delivered_products = cursor.fetchall()
            
            # Populate the table
            self.delivered_table.setRowCount(len(delivered_products))
            
            for row, product in enumerate(delivered_products):
                # ID
                id_item = QtWidgets.QTableWidgetItem(str(product.get('inventory_id', '')))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.delivered_table.setItem(row, 0, id_item)
                
                # Product Name
                self.delivered_table.setItem(row, 1, QtWidgets.QTableWidgetItem(product.get('product_name', '')))
                
                # Supplier
                supplier_name = product.get('supplier_name', 'N/A')
                self.delivered_table.setItem(row, 2, QtWidgets.QTableWidgetItem(supplier_name))
                
                # Quantity
                quantity_item = QtWidgets.QTableWidgetItem(str(product.get('quantity', 0)))
                quantity_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.delivered_table.setItem(row, 3, quantity_item)
                
                # Delivery Date (using last_updated)
                delivery_date = product.get('last_updated')
                date_str = delivery_date.strftime('%Y-%m-%d %H:%M') if delivery_date else "N/A"
                date_item = QtWidgets.QTableWidgetItem(date_str)
                date_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.delivered_table.setItem(row, 4, date_item)
                
                # Status
                status_item = QtWidgets.QTableWidgetItem(product.get('status', ''))
                status_item.setTextAlignment(QtCore.Qt.AlignCenter)
                status_item.setForeground(QtGui.QColor("#4CAF50"))  # Green for received
                self.delivered_table.setItem(row, 5, status_item)
                
                # Notes
                notes = f"Delivered by {supplier_name}" if supplier_name != 'N/A' else "Product delivered"
                self.delivered_table.setItem(row, 6, QtWidgets.QTableWidgetItem(notes))
                
                # Updated timestamp
                updated_date = product.get('created_at')
                updated_str = updated_date.strftime('%Y-%m-%d') if updated_date else "N/A"
                self.delivered_table.setItem(row, 7, QtWidgets.QTableWidgetItem(updated_str))
            
            # Update statistics
            self.update_statistics(delivered_products)
            
            cursor.close()
            
            # Re-apply any active filters after loading data
            if self.filter_state["is_active"]:
                self.apply_stored_filters()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def update_statistics(self, delivered_products):
        """Update the statistics cards"""
        total_deliveries = len(delivered_products)
        total_quantity = sum(product.get('quantity', 0) for product in delivered_products)
        unique_products = len(set(product.get('product_name', '') for product in delivered_products))
        
        # Count recent deliveries (last 7 days)
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_deliveries = sum(1 for product in delivered_products 
                              if product.get('last_updated') and product['last_updated'] >= seven_days_ago)
        
        # Update the statistics cards
        self.total_deliveries_label.value_label.setText(str(total_deliveries))
        self.total_quantity_label.value_label.setText(str(total_quantity))
        self.unique_products_label.value_label.setText(str(unique_products))
        self.recent_deliveries_label.value_label.setText(str(recent_deliveries))
    
    def filter_delivered_products(self):
        """Filter delivered products based on search input"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.delivered_table.rowCount()):
            visible = False
            
            # Search across all columns
            for col in range(self.delivered_table.columnCount()):
                item = self.delivered_table.item(row, col)
                if item and search_text in item.text().lower():
                    visible = True
                    break
                    
            self.delivered_table.setRowHidden(row, not visible)
    
    def show_filter_dialog(self):
        """Show advanced filter dialog"""
        from ..dialogs import DeliveredProductsFilterDialog
        
        filter_dialog = DeliveredProductsFilterDialog(self, self.filter_state)
        if filter_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Get the filter state from the dialog
            new_filter_state = filter_dialog.get_filter_state()
            
            # Check if filters were reset
            if not new_filter_state["is_active"] and self.filter_state["is_active"]:
                # Filters were reset
                self.filter_state = new_filter_state
                self.filter_indicator.setVisible(False)
                self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
                
                # Completely rebuild the table
                QtCore.QTimer.singleShot(50, self.rebuild_table)
            else:
                # Regular filter applied
                self.filter_state = new_filter_state
                
                # Apply filters after dialog is closed
                if self.filter_state["is_active"]:
                    QtCore.QTimer.singleShot(50, self.apply_stored_filters)
                    # Update the filter indicator text
                    filter_text = []
                    if self.filter_state["date_range"] != "All Time":
                        filter_text.append(f"Date: {self.filter_state['date_range']}")
                    if self.filter_state["supplier"] != "All Suppliers":
                        filter_text.append(f"Supplier: {self.filter_state['supplier']}")
                    if self.filter_state["status"] != "All Statuses":
                        filter_text.append(f"Status: {self.filter_state['status']}")
                        
                    if filter_text:
                        self.filter_indicator.setText(f"Active filters: {', '.join(filter_text)}")
                        self.filter_indicator.setVisible(True)
                        self.filter_button.setStyleSheet(StyleFactory.get_active_filter_button_style())
                else:
                    self.filter_indicator.setVisible(False)
                    self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
    
    def apply_stored_filters(self):
        """Apply the filters stored in filter_state"""
        if not self.filter_state["is_active"]:
            return
            
        current_date = datetime.now()
        
        # Track if any row is visible
        rows_visible = False
        
        for row in range(self.delivered_table.rowCount()):
            visible = True
            
            # Apply date range filter
            if self.filter_state["date_range"] != "All Time":
                date_item = self.delivered_table.item(row, 4)
                if date_item and date_item.text() and date_item.text() != "N/A":
                    try:
                        delivery_date = datetime.strptime(date_item.text(), '%Y-%m-%d %H:%M')
                        
                        if self.filter_state["date_range"] == "Today":
                            if delivery_date.date() != current_date.date():
                                visible = False
                        elif self.filter_state["date_range"] == "This Week":
                            days_since = (current_date.date() - delivery_date.date()).days
                            if days_since < 0 or days_since >= 7:
                                visible = False
                        elif self.filter_state["date_range"] == "This Month":
                            if (delivery_date.year != current_date.year or 
                                delivery_date.month != current_date.month):
                                visible = False
                        elif self.filter_state["date_range"] == "Last 30 Days":
                            days_since = (current_date.date() - delivery_date.date()).days
                            if days_since < 0 or days_since > 30:
                                visible = False
                        elif self.filter_state["date_range"] == "Last 90 Days":
                            days_since = (current_date.date() - delivery_date.date()).days
                            if days_since < 0 or days_since > 90:
                                visible = False
                    except ValueError:
                        pass
            
            # Apply supplier filter
            if visible and self.filter_state["supplier"] != "All Suppliers":
                supplier_item = self.delivered_table.item(row, 2)
                if supplier_item and supplier_item.text() != self.filter_state["supplier"]:
                    visible = False
            
            # Apply status filter
            if visible and self.filter_state["status"] != "All Statuses":
                status_item = self.delivered_table.item(row, 5)
                if status_item and status_item.text() != self.filter_state["status"]:
                    visible = False
            
            # Set row visibility
            self.delivered_table.setRowHidden(row, not visible)
            
            # Track if at least one row is visible
            if visible:
                rows_visible = True
        
        # Show a message if no results are found
        if not rows_visible and self.delivered_table.rowCount() > 0:
            QtWidgets.QMessageBox.information(self, "No Results", 
                "No deliveries match the current filters. Try adjusting your filter criteria.")
    
    def rebuild_table(self):
        """Completely rebuild the table with fresh data"""
        # Store current filter state
        was_filtered = self.filter_state["is_active"]
        filter_state_copy = self.filter_state.copy()
        
        # Reset filter state temporarily
        self.filter_state = {
            "is_active": False,
            "date_range": "All Time",
            "supplier": "All Suppliers",
            "status": "All Statuses"
        }
        
        # Reload data
        self.load_delivered_products()
        
        # Restore filter state if necessary
        if was_filtered:
            self.filter_state = filter_state_copy
            # Add a short delay before applying filters to ensure table is fully rendered
            QtCore.QTimer.singleShot(50, self.apply_stored_filters)
    
    def show_context_menu(self, position):
        """Show context menu for the table"""
        item = self.delivered_table.itemAt(position)
        if item is None:
            return
        
        row = item.row()
        
        menu = QtWidgets.QMenu(self)
        
        view_details_action = menu.addAction("View Details")
        view_details_action.triggered.connect(lambda: self.view_delivery_details(row))
        
        menu.exec_(self.delivered_table.mapToGlobal(position))
    
    def view_delivery_details(self, row):
        """View detailed information for a delivery"""
        product_name = self.delivered_table.item(row, 1).text()
        QtWidgets.QMessageBox.information(self, "Delivery Details", f"Details for {product_name} will be shown here")
    
    def refresh_data(self):
        """Refresh the tab data"""
        self.load_delivered_products()