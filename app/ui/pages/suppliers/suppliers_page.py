from PyQt5 import QtWidgets, QtCore, QtGui
from app.ui.pages.base_page import BasePage
from app.utils.db_manager import DBManager
import mysql.connector
from datetime import datetime

# Import the classes from the suppliers folder
from .style_factory import StyleFactory
from .table_factory import TableFactory
from .control_panel_factory import ControlPanelFactory
from .dialogs import SupplierDialog

class SuppliersPage(BasePage):
    def __init__(self, parent=None, user_info=None):
        super(SuppliersPage, self).__init__(parent, title="Suppliers", user_info=user_info)
        self.load_suppliers()
    
    def createContent(self):
        self.content_area = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(8)
        
        # Create the tabs widget similar to inventory page
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.setStyleSheet(StyleFactory.get_tab_style())
        
        # Create the suppliers tab
        self.setup_suppliers_tab()
        
        # Add the tab widget to the main layout
        self.content_layout.addWidget(self.tabs)
        
        # Add the content area to the page layout
        self.layout.addWidget(self.content_area)
    
    def setup_suppliers_tab(self):
        """Setup the Suppliers tab"""
        self.suppliers_tab = QtWidgets.QWidget()
        self.suppliers_layout = QtWidgets.QVBoxLayout(self.suppliers_tab)
        self.suppliers_layout.setContentsMargins(10, 15, 10, 10)
        self.suppliers_layout.setSpacing(10)
        
        # Create search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search suppliers...")
        
        # Create control panel using factory - same as inventory products tab
        control_layout = ControlPanelFactory.create_search_control(
            self.search_input, 
            "+ Add Supplier", 
            self.show_add_supplier_dialog,
            self.filter_suppliers
        )
        self.suppliers_layout.addLayout(control_layout)
        
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
            ("Accepts Returns", 0.10),  # Changed from 0.5 to 0.10
            ("Products on the Way", 0.23)
        ]
        
        # Configure the table columns to fit horizontally
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.suppliers_table, supplier_columns, screen_width)
        
        # Add context menu to the table
        self.suppliers_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.suppliers_table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.suppliers_layout.addWidget(self.suppliers_table)
        
        # Add Suppliers tab to the tab widget
        self.tabs.addTab(self.suppliers_tab, "Suppliers")
    
    def load_suppliers(self):
        """Load suppliers from the database and populate the table"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.suppliers_table.setRowCount(0)
            
            # Reset search filter
            self.search_input.clear()
            
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
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
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
        dialog = SupplierDialog(self)
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
                dialog = SupplierDialog(self, supplier)
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    self.load_suppliers()
                    
            # Reset row visibility
            for row in range(self.suppliers_table.rowCount()):
                self.suppliers_table.setRowHidden(row, False)
            
            cursor.close()
            
        except mysql.connector.Error as err:
            self.show_error_message(f"Database error: {err}")
    
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
                self.show_error_message(f"Database error: {err}")
    
    def show_error_message(self, message):
        """Show error message dialog"""
        QtWidgets.QMessageBox.critical(self, "Error", message)