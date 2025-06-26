from PyQt5 import QtWidgets, QtCore, QtGui
import mysql.connector
from app.utils.db_manager import DBManager
from ..table_factory import TableFactory
from ..style_factory import StyleFactory
from ..control_panel_factory import ControlPanelFactory

class MissingProductsTab(QtWidgets.QWidget):
    """Tab for displaying missing products report"""
    
    def __init__(self, parent=None):
        super(MissingProductsTab, self).__init__()
        self.parent = parent
        self.filter_state = {
            "is_active": False,
            "status": "All",
            "severity": "All",
            "category": "All Categories"
        }
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(15)
        
        # Header section
        header_layout = QtWidgets.QVBoxLayout()
        
        title_label = QtWidgets.QLabel("Missing Products Report")
        title_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        desc_label = QtWidgets.QLabel("Track missing or unaccounted inventory items")
        desc_label.setStyleSheet("color: #cccccc; font-size: 12px;")
        header_layout.addWidget(desc_label)
        
        self.layout.addLayout(header_layout)
        
        # Search and filter controls
        self.search_input = QtWidgets.QLineEdit()
        self.control_layout = ControlPanelFactory.create_search_control(
            self.search_input,
            self.filter_missing_products,
            self.show_filter_dialog
        )
        
        # Store references
        self.filter_button = self.control_layout.filter_button
        self.filter_indicator = self.control_layout.filter_indicator
        
        self.layout.addLayout(self.control_layout)
        
        # Create table
        self.missing_table = TableFactory.create_table()
        
        # Define column headers
        missing_columns = [
            ("Product ID", 0.10),
            ("Product Name", 0.25),
            ("Category", 0.12),
            ("Expected Quantity", 0.12),
            ("Actual Quantity", 0.12),
            ("Difference", 0.10),
            ("Last Counted", 0.11),
            ("Action Required", 0.08)
        ]
        
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.missing_table, missing_columns, screen_width)
        
        self.layout.addWidget(self.missing_table)
        self.load_missing_products()
        
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
    
    def load_missing_products(self):
        """Load missing products data"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Query for products with discrepancies
            cursor.execute("""
                SELECT 
                    p.product_id,
                    p.product_name,
                    p.category,
                    p.quantity as expected_quantity,
                    COALESCE(it.total_in, 0) - COALESCE(it.total_out, 0) as calculated_quantity,
                    p.quantity - (COALESCE(it.total_in, 0) - COALESCE(it.total_out, 0)) as difference,
                    NOW() as last_checked
                FROM products p
                LEFT JOIN (
                    SELECT 
                        product_name,
                        SUM(CASE WHEN transaction_type = 'Stock In' THEN quantity ELSE 0 END) as total_in,
                        SUM(CASE WHEN transaction_type = 'Stock Out' THEN quantity ELSE 0 END) as total_out
                    FROM inventory_transactions
                    GROUP BY product_name
                ) it ON p.product_name = it.product_name
                WHERE ABS(p.quantity - (COALESCE(it.total_in, 0) - COALESCE(it.total_out, 0))) > 0
                ORDER BY ABS(p.quantity - (COALESCE(it.total_in, 0) - COALESCE(it.total_out, 0))) DESC
            """)
            
            missing = cursor.fetchall()
            self.missing_table.setRowCount(len(missing))
            
            for row, item in enumerate(missing):
                difference = item.get('difference', 0)
                
                self.missing_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(item.get('product_id', ''))))
                self.missing_table.setItem(row, 1, QtWidgets.QTableWidgetItem(item.get('product_name', '')))
                self.missing_table.setItem(row, 2, QtWidgets.QTableWidgetItem(item.get('category', '')))
                
                expected_item = QtWidgets.QTableWidgetItem(str(item.get('expected_quantity', 0)))
                expected_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.missing_table.setItem(row, 3, expected_item)
                
                actual_item = QtWidgets.QTableWidgetItem(str(item.get('calculated_quantity', 0)))
                actual_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.missing_table.setItem(row, 4, actual_item)
                
                diff_item = QtWidgets.QTableWidgetItem(str(difference))
                diff_item.setTextAlignment(QtCore.Qt.AlignCenter)
                if difference > 0:
                    diff_item.setForeground(QtGui.QColor("#4CAF50"))  # Green for excess
                else:
                    diff_item.setForeground(QtGui.QColor("#F44336"))  # Red for missing
                self.missing_table.setItem(row, 5, diff_item)

                # Last counted
                last_checked = item.get('last_checked')
                date_str = last_checked.strftime('%Y-%m-%d') if last_checked else "N/A"
                self.missing_table.setItem(row, 6, QtWidgets.QTableWidgetItem(date_str))
                
                # Action required
                abs_diff = abs(difference)
                if abs_diff > 10:
                    action = "Critical"
                elif abs_diff > 5:
                    action = "Moderate"
                else:
                    action = "Minor"
                
                action_item = QtWidgets.QTableWidgetItem(action)
                action_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.missing_table.setItem(row, 7, action_item)
            
            cursor.close()
            
            # Re-apply any active filters after loading data
            if self.filter_state["is_active"]:
                self.apply_stored_filters()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
    
    def filter_missing_products(self):
        """Filter missing products based on search input"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.missing_table.rowCount()):
            visible = False
            
            # Search across all columns
            for col in range(self.missing_table.columnCount()):
                item = self.missing_table.item(row, col)
                if item and search_text in item.text().lower():
                    visible = True
                    break
                    
            self.missing_table.setRowHidden(row, not visible)
    
    def show_filter_dialog(self):
        """Show advanced filter dialog"""
        from ..dialogs import MissingProductsFilterDialog
        
        filter_dialog = MissingProductsFilterDialog(self, self.filter_state)
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
                QtCore.QTimer.singleShot(50, self.load_missing_products)
            else:
                # Regular filter applied
                self.filter_state = new_filter_state
                
                # Apply filters after dialog is closed
                if self.filter_state["is_active"]:
                    QtCore.QTimer.singleShot(50, self.apply_stored_filters)
                    # Update the filter indicator text
                    filter_text = []
                    if self.filter_state["status"] != "All":
                        filter_text.append(f"Status: {self.filter_state['status']}")
                    if self.filter_state["severity"] != "All":
                        filter_text.append(f"Severity: {self.filter_state['severity']}")
                    if self.filter_state["category"] != "All Categories":
                        filter_text.append(f"Category: {self.filter_state['category']}")
                        
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
        
        for row in range(self.missing_table.rowCount()):
            visible = True
            
            # Apply status filter (based on difference value)
            if self.filter_state["status"] != "All":
                diff_item = self.missing_table.item(row, 5)
                if diff_item:
                    try:
                        difference = int(diff_item.text())
                        status = "Excess" if difference > 0 else "Missing"
                        
                        if self.filter_state["status"] != status:
                            visible = False
                    except ValueError:
                        pass
            
            # Apply severity filter
            if visible and self.filter_state["severity"] != "All":
                action_item = self.missing_table.item(row, 7)
                if action_item:
                    action_text = action_item.text()
                    severity_filter = self.filter_state["severity"]
                    
                    if severity_filter == "Critical (>10)" and action_text != "Critical":
                        visible = False
                    elif severity_filter == "Moderate (5-10)" and action_text != "Moderate":
                        visible = False
                    elif severity_filter == "Minor (<5)" and action_text != "Minor":
                        visible = False
            
            # Apply category filter
            if visible and self.filter_state["category"] != "All Categories":
                category_item = self.missing_table.item(row, 2)
                if category_item and category_item.text() != self.filter_state["category"]:
                    visible = False
            
            # Set row visibility
            self.missing_table.setRowHidden(row, not visible)
            
            # Track if at least one row is visible
            if visible:
                rows_visible = True
        
        # Show a message if no results are found
        if not rows_visible and self.missing_table.rowCount() > 0:
            QtWidgets.QMessageBox.information(self, "No Results", 
                "No products match the current filters. Try adjusting your filter criteria.")
    
    def refresh_data(self):
        """Refresh the tab data"""
        self.load_missing_products()