from PyQt5 import QtWidgets, QtCore, QtGui
import mysql.connector
from app.utils.db_manager import DBManager
from ..table_factory import TableFactory
from ..style_factory import StyleFactory
from ..control_panel_factory import ControlPanelFactory
from ..dialogs import SupplierDialog

class SuppliersTab(QtWidgets.QWidget):
    """Tab for managing suppliers"""
    
    def __init__(self, parent=None):
        super(SuppliersTab, self).__init__()
        self.parent = parent
        # Initialize filter state storage
        self.filter_state = {
            "is_active": False,
            "category": "All Categories",
            "accepts_returns": "All",
            "products_on_the_way": "All"
        }
        self.setup_ui()
        self.load_suppliers()
        
    def setup_ui(self):
        """Set up the UI components for the suppliers tab"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 10)
        self.layout.setSpacing(10)
        
        # Create search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search suppliers...")
        
        # Create control panel using factory
        self.control_layout = ControlPanelFactory.create_search_control(
            self.search_input, 
            "+ Add Supplier", 
            self.show_add_supplier_dialog,
            self.filter_suppliers,
            self.show_supplier_filter_dialog
        )
        
        # Store reference to filter button and indicator
        self.filter_button = self.control_layout.filter_button
        self.filter_indicator = self.control_layout.filter_indicator
        
        self.layout.addLayout(self.control_layout)
        
        # Create suppliers table
        self.suppliers_table = TableFactory.create_table()
        
        # Define column headers and their relative widths
        supplier_columns = [
            ("ID", 0.05), 
            ("Supplier Name", 0.15),
            ("Product Name", 0.15),
            ("Category", 0.10),
            ("Contact Number", 0.12),
            ("Email", 0.10),
            ("Accepts Returns", 0.10),
            ("Products on the Way", 0.23)
        ]
        
        # Configure the table columns to fit horizontally
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.suppliers_table, supplier_columns, screen_width)
        
        # Add context menu to the table
        self.suppliers_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.suppliers_table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.layout.addWidget(self.suppliers_table)
        
        # Add filter indicator label
        self.filter_indicator = QtWidgets.QLabel()
        self.filter_indicator.setStyleSheet("color: #4FC3F7; font-style: italic;")
        self.filter_indicator.setVisible(False)
        self.layout.addWidget(self.filter_indicator)
    
    def load_suppliers(self):
        """Load suppliers from the database and populate the table"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.suppliers_table.clearContents()
            self.suppliers_table.setRowCount(0)
            
            # Reset search filter (but preserve filter state)
            self.search_input.blockSignals(True)
            self.search_input.clear()
            self.search_input.blockSignals(False)
            
            # Query for all suppliers
            cursor.execute("SELECT * FROM suppliers ORDER BY supplier_name")
            suppliers = cursor.fetchall()
            
            # Populate the table
            self.suppliers_table.setRowCount(len(suppliers))
            
            for row, supplier in enumerate(suppliers):
                # Set item with proper alignment
                id_item = QtWidgets.QTableWidgetItem(str(supplier['supplier_id']))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.suppliers_table.setItem(row, 0, id_item)
                
                # Supplier name
                self.suppliers_table.setItem(row, 1, QtWidgets.QTableWidgetItem(supplier['supplier_name']))
                
                # Product name
                self.suppliers_table.setItem(row, 2, QtWidgets.QTableWidgetItem(supplier['product_name']))
                
                # Category
                self.suppliers_table.setItem(row, 3, QtWidgets.QTableWidgetItem(supplier.get('category', '')))
                
                # Contact number - center aligned
                contact_item = QtWidgets.QTableWidgetItem(supplier.get('contact_number', ''))
                contact_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.suppliers_table.setItem(row, 4, contact_item)
                
                # Email
                self.suppliers_table.setItem(row, 5, QtWidgets.QTableWidgetItem(supplier.get('email', '')))
                
                # Accepts Returns with color indicators
                accepts_returns = "Yes" if supplier.get('accepts_returns', False) else "No"
                returns_item = QtWidgets.QTableWidgetItem(accepts_returns)
                returns_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                # Set color based on accepts_returns
                if supplier.get('accepts_returns', False):
                    returns_item.setForeground(QtGui.QColor("#4CAF50"))  # Green for yes
                else:
                    returns_item.setForeground(QtGui.QColor("#FF5252"))  # Red for no
                    
                self.suppliers_table.setItem(row, 6, returns_item)
                
                # Products on the way
                on_the_way = supplier.get('products_on_the_way', 0)
                on_the_way_text = str(on_the_way) if on_the_way > 0 else "None"
                on_the_way_item = QtWidgets.QTableWidgetItem(on_the_way_text)
                on_the_way_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                if on_the_way > 0:
                    on_the_way_item.setForeground(QtGui.QColor("#2196F3"))  # Blue for in transit
                
                self.suppliers_table.setItem(row, 7, on_the_way_item)
            
            cursor.close()
            
            # Re-apply any active filters after loading data
            if self.filter_state["is_active"]:
                self.apply_stored_filters()
                
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def filter_suppliers(self):
        """Filter suppliers based on search input"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.suppliers_table.rowCount()):
            match_found = False
            
            for col in range(self.suppliers_table.columnCount()):
                item = self.suppliers_table.item(row, col)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
            
            # Show/hide row based on match
            self.suppliers_table.setRowHidden(row, not match_found)
            
    def show_supplier_filter_dialog(self):
        """Show advanced filter dialog for suppliers"""
        from ..dialogs import SupplierFilterDialog  # Import here to avoid circular imports
        
        filter_dialog = SupplierFilterDialog(self, self.filter_state)
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
                    # Show filter indicator
                    self.filter_indicator.setVisible(True)
                    # Use the same blue button style as the products tab
                    self.filter_button.setStyleSheet(StyleFactory.get_active_filter_button_style())
                else:
                    self.filter_indicator.setVisible(False)
                    self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))

    def apply_stored_filters(self):
        """Apply the filters stored in filter_state"""
        # Get current filter settings
        category = self.filter_state["category"]
        accepts_returns = self.filter_state["accepts_returns"]
        products_on_the_way = self.filter_state["products_on_the_way"]
        
        # Update the filter indicator text
        filter_text = []
        if category != "All Categories":
            filter_text.append(f"Category: {category}")
        if accepts_returns != "All":
            filter_text.append(f"Returns: {accepts_returns}")
        if products_on_the_way != "All":
            filter_text.append(f"Status: {products_on_the_way}")
            
        if filter_text:
            self.filter_indicator.setText(f"Active filters: {', '.join(filter_text)}")
            self.filter_indicator.setVisible(True)
            # Use active filter button style
            self.filter_button.setStyleSheet(StyleFactory.get_active_filter_button_style())
        else:
            self.filter_indicator.setVisible(False)
            self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
        
        # Track if any row is visible
        rows_visible = False
        
        # Go through all rows
        for row in range(self.suppliers_table.rowCount()):
            # Get row data
            row_category = self.suppliers_table.item(row, 3).text() if self.suppliers_table.item(row, 3) else ""
            
            # Get accepts returns value (column 6 - "Yes" or "No")
            row_returns_text = self.suppliers_table.item(row, 6).text() if self.suppliers_table.item(row, 6) else "No"
            row_returns = (row_returns_text == "Yes")
            
            # Get products on the way value (column 7)
            row_on_the_way_text = self.suppliers_table.item(row, 7).text() if self.suppliers_table.item(row, 7) else "None"
            row_has_products_on_way = (row_on_the_way_text != "None")
            
            # By default, show the row
            show_row = True
            
            # Apply category filter
            if category != "All Categories" and row_category != category:
                show_row = False
            
            # Apply accepts returns filter
            if show_row and accepts_returns != "All":
                if accepts_returns == "Accepts Returns" and not row_returns:
                    show_row = False
                elif accepts_returns == "No Returns" and row_returns:
                    show_row = False
            
            # Apply products on the way filter
            if show_row and products_on_the_way != "All":
                if products_on_the_way == "Has Products on the Way" and not row_has_products_on_way:
                    show_row = False
                elif products_on_the_way == "No Products on the Way" and row_has_products_on_way:
                    show_row = False
            
            # Set row visibility
            self.suppliers_table.setRowHidden(row, not show_row)
            
            # Track if at least one row is visible
            if show_row:
                rows_visible = True
        
        # Show a message if no results are found
        if not rows_visible and self.suppliers_table.rowCount() > 0:
            QtWidgets.QMessageBox.information(self, "No Results", 
                "No suppliers match the current filters. Try adjusting your filter criteria.")
    
    def show_context_menu(self, position):
        """Show context menu for supplier actions"""
        context_menu = QtWidgets.QMenu()
        
        # Get the current row
        current_row = self.suppliers_table.currentRow()
        
        if current_row >= 0:
            edit_action = context_menu.addAction("Edit")
            delete_action = context_menu.addAction("Delete")
            
            # Show the context menu
            action = context_menu.exec_(self.suppliers_table.mapToGlobal(position))
            
            if action == edit_action:
                self.edit_supplier(current_row)
            elif action == delete_action:
                self.delete_supplier(current_row)
    
    def show_add_supplier_dialog(self):
        """Show dialog to add a new supplier"""
        dialog = SupplierDialog(self.parent or self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_suppliers()
            # Reset row visibility
            for row in range(self.suppliers_table.rowCount()):
                self.suppliers_table.setRowHidden(row, False)
    
    def edit_supplier(self, row):
        """Edit the selected supplier"""
        supplier_id = int(self.suppliers_table.item(row, 0).text())
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM suppliers WHERE supplier_id = %s", (supplier_id,))
            supplier = cursor.fetchone()
            
            if supplier:
                dialog = SupplierDialog(self.parent or self, supplier)
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    self.load_suppliers()
                    
            # Reset row visibility
            for row in range(self.suppliers_table.rowCount()):
                self.suppliers_table.setRowHidden(row, False)
            
            cursor.close()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def delete_supplier(self, row):
        """Delete the selected supplier"""
        supplier_id = int(self.suppliers_table.item(row, 0).text())
        supplier_name = self.suppliers_table.item(row, 1).text()
        
        # Confirm deletion
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete supplier: {supplier_name}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if confirm == QtWidgets.QMessageBox.Yes:
            try:
                conn = DBManager.get_connection()
                cursor = conn.cursor()
                
                # Delete the supplier
                cursor.execute("DELETE FROM suppliers WHERE supplier_id = %s", (supplier_id,))
                
                conn.commit()
                cursor.close()
                
                # Refresh the supplier list
                self.load_suppliers()
                
                # Show success message
                QtWidgets.QMessageBox.information(
                    self,
                    "Success",
                    f"Supplier '{supplier_name}' has been deleted successfully."
                )
                
            except mysql.connector.Error as err:
                if self.parent:
                    self.parent.show_error_message(f"Database error: {err}")
                else:
                    QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def rebuild_table(self):
        """Completely rebuild the table with fresh data"""
        # Store current filter state
        was_filtered = self.filter_state["is_active"]
        filter_state_copy = self.filter_state.copy()
        
        # Reset filter state temporarily
        self.filter_state = {
            "is_active": False,
            "category": "All Categories", 
            "accepts_returns": "All",
            "products_on_the_way": "All"
        }
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Query for all suppliers
            cursor.execute("SELECT * FROM suppliers ORDER BY supplier_name")
            suppliers = cursor.fetchall()
            
            # Create and configure a new table from scratch
            new_table = TableFactory.create_table()
            supplier_columns = [
                ("ID", 0.05), 
                ("Supplier Name", 0.15),
                ("Product Name", 0.15),
                ("Category", 0.10),
                ("Contact Number", 0.12),
                ("Email", 0.10),
                ("Accepts Returns", 0.10),
                ("Products on the Way", 0.23)
            ]
            screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
            TableFactory.configure_table_columns(new_table, supplier_columns, screen_width)
            
            # Set up context menu for the new table
            new_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            new_table.customContextMenuRequested.connect(self.show_context_menu)
            
            # Populate the new table
            new_table.setRowCount(len(suppliers))
            
            for row, supplier in enumerate(suppliers):
                # Set item with proper alignment
                id_item = QtWidgets.QTableWidgetItem(str(supplier['supplier_id']))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                new_table.setItem(row, 0, id_item)
                
                # Supplier name
                new_table.setItem(row, 1, QtWidgets.QTableWidgetItem(supplier['supplier_name']))
                
                # Product name
                new_table.setItem(row, 2, QtWidgets.QTableWidgetItem(supplier['product_name']))
                
                # Category
                new_table.setItem(row, 3, QtWidgets.QTableWidgetItem(supplier.get('category', '')))
                
                # Contact number - center aligned
                contact_item = QtWidgets.QTableWidgetItem(supplier.get('contact_number', ''))
                contact_item.setTextAlignment(QtCore.Qt.AlignCenter)
                new_table.setItem(row, 4, contact_item)
                
                # Email
                new_table.setItem(row, 5, QtWidgets.QTableWidgetItem(supplier.get('email', '')))
                
                # Accepts Returns with color indicators
                accepts_returns = "Yes" if supplier.get('accepts_returns', False) else "No"
                returns_item = QtWidgets.QTableWidgetItem(accepts_returns)
                returns_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                # Set color based on accepts_returns
                if supplier.get('accepts_returns', False):
                    returns_item.setForeground(QtGui.QColor("#4CAF50"))  # Green for yes
                else:
                    returns_item.setForeground(QtGui.QColor("#FF5252"))  # Red for no
                    
                new_table.setItem(row, 6, returns_item)
                
                # Products on the way
                on_the_way = supplier.get('products_on_the_way', 0)
                on_the_way_text = str(on_the_way) if on_the_way > 0 else "None"
                on_the_way_item = QtWidgets.QTableWidgetItem(on_the_way_text)
                on_the_way_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                if on_the_way > 0:
                    on_the_way_item.setForeground(QtGui.QColor("#2196F3"))  # Blue for in transit
                
                new_table.setItem(row, 7, on_the_way_item)
            
            # Replace the old table with the new one
            old_table = self.suppliers_table
            self.layout.replaceWidget(old_table, new_table)
            self.suppliers_table = new_table
            old_table.deleteLater()
            
            cursor.close()
            
            # Restore filter state if necessary
            if was_filtered:
                self.filter_state = filter_state_copy
                # Add a short delay before applying filters to ensure table is fully rendered
                QtCore.QTimer.singleShot(50, self.apply_stored_filters)
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")