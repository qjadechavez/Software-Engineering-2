from PyQt5 import QtWidgets, QtCore, QtGui
import mysql.connector
from app.utils.db_manager import DBManager
from datetime import datetime
from ..table_factory import TableFactory
from ..style_factory import StyleFactory
from ..control_panel_factory import ControlPanelFactory

class AlertLevelTab(QtWidgets.QWidget):
    """Tab for displaying alert level report - overstock and understock statuses"""
    
    def __init__(self, parent=None):
        super(AlertLevelTab, self).__init__()
        self.parent = parent
        self.filter_state = {
            "is_active": False,
            "alert_level": "All Levels",
            "category": "All Categories",
            "status": "All Statuses"
        }
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(15)
        
        # Header section
        header_layout = QtWidgets.QVBoxLayout()
        
        title_label = QtWidgets.QLabel("Alert Level Report")
        title_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        desc_label = QtWidgets.QLabel("Monitor product stock levels, overstock and understock statuses")
        desc_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        header_layout.addWidget(desc_label)
        
        self.layout.addLayout(header_layout)
        
        # Search and filter controls
        self.search_input = QtWidgets.QLineEdit()
        self.control_layout = ControlPanelFactory.create_search_control(
            self.search_input,
            self.filter_alert_levels,
            self.show_filter_dialog
        )
        
        # Store references
        self.filter_button = self.control_layout.filter_button
        self.filter_indicator = self.control_layout.filter_indicator
        
        self.layout.addLayout(self.control_layout)
        
        # Alert statistics
        stats_frame = QtWidgets.QFrame()
        stats_frame.setStyleSheet(StyleFactory.get_section_frame_style())
        stats_layout = QtWidgets.QHBoxLayout(stats_frame)
        stats_layout.setContentsMargins(15, 10, 15, 10)
        
        # Create alert statistics cards
        self.critical_alerts = self.create_alert_card("Critical Alerts", "0", "#F44336")
        self.low_stock_alerts = self.create_alert_card("Low Stock", "0", "#FF9800")
        self.overstock_alerts = self.create_alert_card("Overstock", "0", "#2196F3")
        self.out_of_stock = self.create_alert_card("Out of Stock", "0", "#9C27B0")
        
        stats_layout.addWidget(self.critical_alerts)
        stats_layout.addWidget(self.low_stock_alerts)
        stats_layout.addWidget(self.overstock_alerts)
        stats_layout.addWidget(self.out_of_stock)
        stats_layout.addStretch()
        
        self.layout.addWidget(stats_frame)
        
        # Create alerts table
        self.alerts_table = TableFactory.create_table()
        
        # Define column headers and their relative widths
        alert_columns = [
            ("Product ID", 0.08),
            ("Product Name", 0.20),
            ("Category", 0.12),
            ("Current Stock", 0.10),
            ("Threshold", 0.10),
            ("Alert Level", 0.12),
            ("Status", 0.10),
            ("Last Updated", 0.18)
        ]
        
        # Configure the table columns
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.alerts_table, alert_columns, screen_width)
        
        # Add context menu
        self.alerts_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.alerts_table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.layout.addWidget(self.alerts_table)
        
        # Load initial data
        self.load_alert_data()
        
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
    
    def create_alert_card(self, title, value, color):
        """Create an alert statistics card widget"""
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
    
    def load_alert_data(self):
        """Load alert data from the database"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.alerts_table.clearContents()
            self.alerts_table.setRowCount(0)
            
            # Query for products with stock levels and thresholds
            cursor.execute("""
                SELECT 
                    product_id,
                    product_name,
                    category,
                    quantity,
                    threshold_value,
                    availability,
                    CASE 
                        WHEN quantity = 0 THEN 'Out of Stock'
                        WHEN quantity <= (threshold_value * 0.5) THEN 'Critical'
                        WHEN quantity <= threshold_value THEN 'Low Stock'
                        WHEN quantity >= (threshold_value * 3) THEN 'Overstock'
                        ELSE 'Normal'
                    END as alert_level,
                    NOW() as last_checked
                FROM products
                WHERE availability = 1
                ORDER BY 
                    CASE 
                        WHEN quantity = 0 THEN 1
                        WHEN quantity <= (threshold_value * 0.5) THEN 2
                        WHEN quantity <= threshold_value THEN 3
                        WHEN quantity >= (threshold_value * 3) THEN 4
                        ELSE 5
                    END
            """)
            
            products = cursor.fetchall()
            
            # Count alerts for statistics
            critical_count = 0
            low_stock_count = 0
            overstock_count = 0
            out_of_stock_count = 0
            
            # Populate the table
            self.alerts_table.setRowCount(len(products))
            
            for row, product in enumerate(products):
                alert_level = product.get('alert_level', 'Normal')
                
                # Count alerts
                if alert_level == 'Critical':
                    critical_count += 1
                elif alert_level == 'Low Stock':
                    low_stock_count += 1
                elif alert_level == 'Overstock':
                    overstock_count += 1
                elif alert_level == 'Out of Stock':
                    out_of_stock_count += 1
                
                # Product ID
                id_item = QtWidgets.QTableWidgetItem(str(product.get('product_id', '')))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.alerts_table.setItem(row, 0, id_item)
                
                # Product Name
                self.alerts_table.setItem(row, 1, QtWidgets.QTableWidgetItem(product.get('product_name', '')))
                
                # Category
                self.alerts_table.setItem(row, 2, QtWidgets.QTableWidgetItem(product.get('category', '')))
                
                # Current Stock
                stock_item = QtWidgets.QTableWidgetItem(str(product.get('quantity', 0)))
                stock_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.alerts_table.setItem(row, 3, stock_item)
                
                # Threshold
                threshold_item = QtWidgets.QTableWidgetItem(str(product.get('threshold_value', 0)))
                threshold_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.alerts_table.setItem(row, 4, threshold_item)
                
                # Alert Level with color coding
                alert_item = QtWidgets.QTableWidgetItem(alert_level)
                alert_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                # Color code based on alert level
                if alert_level == 'Out of Stock':
                    alert_item.setForeground(QtGui.QColor("#9C27B0"))
                elif alert_level == 'Critical':
                    alert_item.setForeground(QtGui.QColor("#F44336"))
                elif alert_level == 'Low Stock':
                    alert_item.setForeground(QtGui.QColor("#FF9800"))
                elif alert_level == 'Overstock':
                    alert_item.setForeground(QtGui.QColor("#2196F3"))
                else:
                    alert_item.setForeground(QtGui.QColor("#4CAF50"))
                
                self.alerts_table.setItem(row, 5, alert_item)
                
                # Status
                status = "Available" if product.get('availability', True) else "Unavailable"
                status_item = QtWidgets.QTableWidgetItem(status)
                status_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.alerts_table.setItem(row, 6, status_item)
                
                # Last Updated
                last_updated = product.get('last_checked')
                if last_updated:
                    updated_str = last_updated.strftime('%Y-%m-%d %H:%M')
                else:
                    updated_str = "N/A"
                self.alerts_table.setItem(row, 7, QtWidgets.QTableWidgetItem(updated_str))
            
            # Update statistics
            self.critical_alerts.value_label.setText(str(critical_count))
            self.low_stock_alerts.value_label.setText(str(low_stock_count))
            self.overstock_alerts.value_label.setText(str(overstock_count))
            self.out_of_stock.value_label.setText(str(out_of_stock_count))
            
            cursor.close()
            
            # Re-apply any active filters after loading data
            if self.filter_state["is_active"]:
                self.apply_stored_filters()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def filter_alert_levels(self):
        """Filter alerts based on search input"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.alerts_table.rowCount()):
            visible = False
            
            # Search across all columns
            for col in range(self.alerts_table.columnCount()):
                item = self.alerts_table.item(row, col)
                if item and search_text in item.text().lower():
                    visible = True
                    break
                    
            self.alerts_table.setRowHidden(row, not visible)
    
    def show_filter_dialog(self):
        """Show advanced filter dialog"""
        from ..dialogs import AlertLevelFilterDialog
        
        filter_dialog = AlertLevelFilterDialog(self, self.filter_state)
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
                    if self.filter_state["alert_level"] != "All Levels":
                        filter_text.append(f"Alert: {self.filter_state['alert_level']}")
                    if self.filter_state["category"] != "All Categories":
                        filter_text.append(f"Category: {self.filter_state['category']}")
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
        
        # Track if any row is visible
        rows_visible = False
        
        for row in range(self.alerts_table.rowCount()):
            visible = True
            
            # Apply alert level filter
            if self.filter_state["alert_level"] != "All Levels":
                alert_item = self.alerts_table.item(row, 5)
                if alert_item and alert_item.text() != self.filter_state["alert_level"]:
                    visible = False
            
            # Apply category filter
            if visible and self.filter_state["category"] != "All Categories":
                category_item = self.alerts_table.item(row, 2)
                if category_item and category_item.text() != self.filter_state["category"]:
                    visible = False
            
            # Apply status filter
            if visible and self.filter_state["status"] != "All Statuses":
                status_item = self.alerts_table.item(row, 6)
                if status_item and status_item.text() != self.filter_state["status"]:
                    visible = False
            
            # Set row visibility
            self.alerts_table.setRowHidden(row, not visible)
            
            # Track if at least one row is visible
            if visible:
                rows_visible = True
        
        # Show a message if no results are found
        if not rows_visible and self.alerts_table.rowCount() > 0:
            QtWidgets.QMessageBox.information(self, "No Results", 
                "No products match the current filters. Try adjusting your filter criteria.")
    
    def rebuild_table(self):
        """Completely rebuild the table with fresh data"""
        # Store current filter state
        was_filtered = self.filter_state["is_active"]
        filter_state_copy = self.filter_state.copy()
        
        # Reset filter state temporarily
        self.filter_state = {
            "is_active": False,
            "alert_level": "All Levels",
            "category": "All Categories",
            "status": "All Statuses"
        }
        
        # Reload data
        self.load_alert_data()
        
        # Restore filter state if necessary
        if was_filtered:
            self.filter_state = filter_state_copy
            # Add a short delay before applying filters to ensure table is fully rendered
            QtCore.QTimer.singleShot(50, self.apply_stored_filters)
    
    def show_context_menu(self, position):
        """Show context menu for the table"""
        item = self.alerts_table.itemAt(position)
        if item is None:
            return
        
        row = item.row()
        
        menu = QtWidgets.QMenu(self)
        
        view_details_action = menu.addAction("View Product Details")
        view_details_action.triggered.connect(lambda: self.view_product_details(row))
        
        adjust_stock_action = menu.addAction("Adjust Stock Level")
        adjust_stock_action.triggered.connect(lambda: self.adjust_stock_level(row))
        
        menu.exec_(self.alerts_table.mapToGlobal(position))
    
    def view_product_details(self, row):
        """View detailed information for a product"""
        product_name = self.alerts_table.item(row, 1).text()
        QtWidgets.QMessageBox.information(self, "Product Details", f"Details for {product_name} will be shown here")
    
    def adjust_stock_level(self, row):
        """Adjust stock level for a product"""
        product_name = self.alerts_table.item(row, 1).text()
        QtWidgets.QMessageBox.information(self, "Adjust Stock", f"Stock adjustment for {product_name} will be implemented here")
    
    def refresh_data(self):
        """Refresh the tab data"""
        self.load_alert_data()