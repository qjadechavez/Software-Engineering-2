from PyQt5 import QtWidgets, QtCore, QtGui
import mysql.connector
from app.utils.db_manager import DBManager
from ..table_factory import TableFactory
from ..style_factory import StyleFactory
from ..control_panel_factory import ControlPanelFactory

class UndeliveredProductsTab(QtWidgets.QWidget):
    """Tab for displaying undelivered products report"""
    
    def __init__(self, parent=None):
        super(UndeliveredProductsTab, self).__init__()
        self.parent = parent
        self.filter_state = {
            "is_active": False,
            "supplier": "All Suppliers",
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
        
        title_label = QtWidgets.QLabel("Undelivered Products Report")
        title_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        desc_label = QtWidgets.QLabel("Track pending product deliveries from suppliers")
        desc_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        header_layout.addWidget(desc_label)
        
        self.layout.addLayout(header_layout)
        
        # Search and filter controls
        self.search_input = QtWidgets.QLineEdit()
        self.control_layout = ControlPanelFactory.create_search_control(
            self.search_input,
            self.filter_undelivered_products,
            self.show_filter_dialog
        )
        
        # Store references
        self.filter_button = self.control_layout.filter_button
        self.filter_indicator = self.control_layout.filter_indicator
        
        self.layout.addLayout(self.control_layout)
        
        # Create table
        self.undelivered_table = TableFactory.create_table()
        
        # Define column headers
        undelivered_columns = [
            ("Supplier ID", 0.08),
            ("Supplier Name", 0.20),
            ("Product Name", 0.20),
            ("Category", 0.12),
            ("Expected Quantity", 0.10),
            ("Order Date", 0.12),
            ("Expected Delivery", 0.12),
            ("Status", 0.06)
        ]
        
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.undelivered_table, undelivered_columns, screen_width)
        
        self.layout.addWidget(self.undelivered_table)
        self.load_undelivered_products()
        
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
    
    def load_undelivered_products(self):
        """Load undelivered products data"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                SELECT 
                    supplier_id,
                    supplier_name,
                    product_name,
                    category,
                    products_on_the_way,
                    created_at,
                    status
                FROM suppliers
                WHERE status = 'pending' AND products_on_the_way > 0
                ORDER BY created_at DESC
            """)
            
            undelivered = cursor.fetchall()
            self.undelivered_table.setRowCount(len(undelivered))
            
            for row, item in enumerate(undelivered):
                self.undelivered_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item.get('supplier_id', ''))))
                self.undelivered_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item.get('supplier_name', '')))
                self.undelivered_table.setItem(row, 2, QtWidgets.QTableWidgetItem(item.get('product_name', '')))
                self.undelivered_table.setItem(row, 3, QtWidgets.QTableWidgetItem(item.get('category', '')))
                self.undelivered_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(item.get('products_on_the_way', 0))))
                
                order_date = item.get('created_at')
                date_str = order_date.strftime('%Y-%m-%d') if order_date else "N/A"
                self.undelivered_table.setItem(row, 5, QtWidgets.QTableWidgetItem(date_str))
                self.undelivered_table.setItem(row, 6, QtWidgets.QTableWidgetItem("TBD"))
                
                status_item = QtWidgets.QTableWidgetItem(item.get('status', ''))
                status_item.setForeground(QtGui.QColor("#FF9800"))
                self.undelivered_table.setItem(row, 7, status_item)
            
            cursor.close()
            
            # Re-apply any active filters after loading data
            if self.filter_state["is_active"]:
                self.apply_stored_filters()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
    
    def filter_undelivered_products(self):
        """Filter undelivered products based on search input"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.undelivered_table.rowCount()):
            visible = False
            
            # Search across all columns
            for col in range(self.undelivered_table.columnCount()):
                item = self.undelivered_table.item(row, col)
                if item and search_text in item.text().lower():
                    visible = True
                    break
                    
            self.undelivered_table.setRowHidden(row, not visible)
    
    def show_filter_dialog(self):
        """Show advanced filter dialog"""
        from ..dialogs import UndeliveredProductsFilterDialog
        
        filter_dialog = UndeliveredProductsFilterDialog(self, self.filter_state)
        if filter_dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Get the filter state from the dialog
            new_filter_state = filter_dialog.get_filter_state()
            
            # Check if filters were reset
            if not new_filter_state["is_active"] and self.filter_state["is_active"]:
                # Filters were reset
                self.filter_state = new_filter_state
                self.filter_indicator.setVisible(False)
                self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
                
                # Completely reload the table
                QtCore.QTimer.singleShot(50, self.load_undelivered_products)
            else:
                # Regular filter applied
                self.filter_state = new_filter_state
                
                # Apply filters after dialog is closed
                if self.filter_state["is_active"]:
                    QtCore.QTimer.singleShot(50, self.apply_stored_filters)
                    # Update the filter indicator text
                    filter_text = []
                    if self.filter_state["supplier"] != "All Suppliers":
                        filter_text.append(f"Supplier: {self.filter_state['supplier']}")
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
        
        for row in range(self.undelivered_table.rowCount()):
            visible = True
            
            # Apply supplier filter
            if self.filter_state["supplier"] != "All Suppliers":
                supplier_item = self.undelivered_table.item(row, 1)
                if supplier_item and supplier_item.text() != self.filter_state["supplier"]:
                    visible = False
            
            # Apply category filter
            if visible and self.filter_state["category"] != "All Categories":
                category_item = self.undelivered_table.item(row, 3)
                if category_item and category_item.text() != self.filter_state["category"]:
                    visible = False
            
            # Apply status filter
            if visible and self.filter_state["status"] != "All Statuses":
                status_item = self.undelivered_table.item(row, 7)
                if status_item and status_item.text() != self.filter_state["status"]:
                    visible = False
            
            # Set row visibility
            self.undelivered_table.setRowHidden(row, not visible)
            
            # Track if at least one row is visible
            if visible:
                rows_visible = True
        
        # Show a message if no results are found
        if not rows_visible and self.undelivered_table.rowCount() > 0:
            QtWidgets.QMessageBox.information(self, "No Results", 
                "No products match the current filters. Try adjusting your filter criteria.")
    
    def refresh_data(self):
        """Refresh the tab data"""
        self.load_undelivered_products()