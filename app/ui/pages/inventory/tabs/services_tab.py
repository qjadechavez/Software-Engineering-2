from PyQt5 import QtWidgets, QtCore, QtGui
from app.utils.db_manager import DBManager
import mysql.connector
from ..style_factory import StyleFactory
from ..table_factory import TableFactory
from ..control_panel_factory import ControlPanelFactory
from ..dialogs import ServiceDialog
from ..dialogs.service_products_dialog import ServiceProductsDialog

class ServicesTab(QtWidgets.QWidget):
    """Tab for managing services in inventory"""
    
    def __init__(self, parent=None):
        super(ServicesTab, self).__init__()
        self.parent = parent
        # Initialize filter state storage
        self.filter_state = {
            "is_active": False,
            "category": "All Categories",
            "availability": "All",
            "price_sort": "No Sorting"
        }
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components for the services tab"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 15, 10, 10)
        self.layout.setSpacing(10)
        
        # Create search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search services...")
        
        # Create control panel using factory
        self.control_layout = ControlPanelFactory.create_search_control(
            self.search_input,
            "+ Add Service",
            self.show_add_service_dialog,
            self.filter_services,
            self.show_service_filter_dialog
        )
        self.layout.addLayout(self.control_layout)
        
        # Store reference to filter button
        self.filter_button = self.control_layout.filter_button
        
        # Create services table
        self.services_table = TableFactory.create_table()
        
        # Define column headers and their relative widths
        service_columns = [
            ("ID", 0.05),
            ("Name", 0.20),
            ("Category", 0.15),
            ("Price", 0.10),
            ("Availability", 0.12),
            ("Description", 0.38)
        ]
        
        # Configure the table columns
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.services_table, service_columns, screen_width)
        
        self.services_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.services_table.customContextMenuRequested.connect(self.show_context_menu)
        
        self.layout.addWidget(self.services_table)
        
        # Add filter indicator label
        self.filter_indicator = QtWidgets.QLabel()
        self.filter_indicator.setStyleSheet("color: #4FC3F7; font-style: italic;")
        self.filter_indicator.setVisible(False)
        self.layout.addWidget(self.filter_indicator)
    
    def load_services(self):
        """Load services from the database and populate the table"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items and reset table state completely
            self.services_table.clearContents()
            self.services_table.setRowCount(0)
            
            # Reset search filter (but preserve filter state)
            self.search_input.blockSignals(True)
            self.search_input.clear()
            self.search_input.blockSignals(False)
            
            # Query for all services
            cursor.execute("SELECT * FROM services ORDER BY service_name")
            services = cursor.fetchall()
            
            # Populate the table
            self.services_table.setRowCount(len(services))
            
            for row, service in enumerate(services):
                # Set item with proper alignment
                id_item = QtWidgets.QTableWidgetItem(str(service['service_id']))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.services_table.setItem(row, 0, id_item)
                
                self.services_table.setItem(row, 1, QtWidgets.QTableWidgetItem(service['service_name']))
                self.services_table.setItem(row, 2, QtWidgets.QTableWidgetItem(service.get('category', '')))
                
                # Price with better formatting and alignment
                price_item = QtWidgets.QTableWidgetItem(f"₱{service['price']:.2f}")
                price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                self.services_table.setItem(row, 3, price_item)
                
                # Availability
                availability_status = "Available" if service.get('availability', 0) else "Unavailable"
                availability_item = QtWidgets.QTableWidgetItem(availability_status)
                availability_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                # Set color based on availability
                if service.get('availability', 0):
                    availability_item.setForeground(QtGui.QColor(0, 170, 0))  # Green for available
                else:
                    availability_item.setForeground(QtGui.QColor(200, 0, 0))  # Red for unavailable
                
                self.services_table.setItem(row, 4, availability_item)
                
                # Description
                self.services_table.setItem(row, 5, QtWidgets.QTableWidgetItem(service.get('description', '')))
    
            cursor.close()
            
            # Re-apply any active filters after loading data
            if self.filter_state["is_active"]:
                self.apply_stored_filters()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def filter_services(self):
        """Filter services based on search input"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.services_table.rowCount()):
            match_found = False
            
            for col in range(self.services_table.columnCount()):
                item = self.services_table.item(row, col)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
            
            # Show/hide row based on match
            self.services_table.setRowHidden(row, not match_found)

    def apply_stored_filters(self):
        """Apply the filters stored in filter_state"""
        # Get current filter settings
        service_category = self.filter_state["category"]
        availability = self.filter_state["availability"]
        price_sort = self.filter_state["price_sort"]
        
        # Update the filter indicator text
        filter_text = []
        if service_category != "All Categories":
            filter_text.append(f"Category: {service_category}")
        if availability != "All":
            filter_text.append(f"Status: {availability}")
        if price_sort != "No Sorting":
            filter_text.append(f"Price: {price_sort}")
            
        if filter_text:
            self.filter_indicator.setText(f"Active filters: {', '.join(filter_text)}")
            self.filter_indicator.setVisible(True)
        else:
            self.filter_indicator.setVisible(False)
        
        # Track if any row is visible
        rows_visible = False
        
        # First apply the filters
        for row in range(self.services_table.rowCount()):
            show_row = True
            
            # Apply category filter
            if service_category != "All Categories":
                category_cell = self.services_table.item(row, 2)
                if category_cell is None or category_cell.text() != service_category:
                    show_row = False
            
            # Apply availability filter
            if availability != "All" and show_row:
                availability_cell = self.services_table.item(row, 6)
                if availability_cell is None:
                    show_row = False
                else:
                    availability_text = availability_cell.text()
                    if (availability == "Available" and availability_text != "Available") or \
                       (availability == "Unavailable" and availability_text != "Unavailable"):
                        show_row = False
            
            # Show/hide row based on filters
            self.services_table.setRowHidden(row, not show_row)
            
            # Track if at least one row is visible
            if show_row:
                rows_visible = True
        
        # Show a message if no results are found
        if not rows_visible and self.services_table.rowCount() > 0:
            QtWidgets.QMessageBox.information(self, "No Results", 
                "No services match the current filters. Try adjusting your filter criteria.")
        
        # Then apply sorting if selected
        if price_sort != "No Sorting":
            # Use the built-in sort functionality with the correct column and order
            order = QtCore.Qt.AscendingOrder if price_sort == "Lowest - Highest" else QtCore.Qt.DescendingOrder
            self.services_table.sortItems(3, order)
            
        # Update button appearance
        if self.filter_state["is_active"]:
            self.filter_button.setStyleSheet(StyleFactory.get_active_filter_button_style())
        else:
            self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
    
    def show_context_menu(self, position):
        """Show context menu for service actions"""
        context_menu = QtWidgets.QMenu()
        
        # Get the current row
        current_row = self.services_table.currentRow()
        
        if current_row >= 0:
            view_products_action = context_menu.addAction("View Products")
            edit_action = context_menu.addAction("Edit")
            delete_action = context_menu.addAction("Delete")
            
            # Show the context menu
            action = context_menu.exec_(self.services_table.mapToGlobal(position))
            
            if action == view_products_action:
                self.view_service_products(current_row)
            elif action == edit_action:
                self.edit_service(current_row)
            elif action == delete_action:
                self.delete_service(current_row)
    
    def show_add_service_dialog(self):
        """Show dialog to add a new service"""
        dialog = ServiceDialog(self.parent or self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_services()
            # Reset row visibility
            for row in range(self.services_table.rowCount()):
                self.services_table.setRowHidden(row, False)
            
            # Notify parent to update overview tab if it exists
            if self.parent and hasattr(self.parent, "update_overview_tab"):
                self.parent.update_overview_tab()
    
    def edit_service(self, row):
        """Edit the selected service"""
        service_id = int(self.services_table.item(row, 0).text())
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM services WHERE service_id = %s", (service_id,))
            service = cursor.fetchone()
            
            if service:
                dialog = ServiceDialog(self.parent or self, service)
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    self.load_services()
                
            # Reset row visibility
            for row in range(self.services_table.rowCount()):
                self.services_table.setRowHidden(row, False)
        
            cursor.close()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")
    
    def delete_service(self, row):
        """Delete the selected service"""
        service_id = int(self.services_table.item(row, 0).text())
        service_name = self.services_table.item(row, 1).text()
        
        # Confirm deletion
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete service: {service_name}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if confirm == QtWidgets.QMessageBox.Yes:
            try:
                conn = DBManager.get_connection()
                cursor = conn.cursor()
                
                # Delete the service
                cursor.execute("DELETE FROM services WHERE service_id = %s", (service_id,))
                
                conn.commit()
                cursor.close()
                
                # Refresh the service list
                self.load_services()
                
                # Show success message
                QtWidgets.QMessageBox.information(
                    self,
                    "Success",
                    f"Service '{service_name}' has been deleted successfully."
                )
                
                # Notify parent to update overview tab if it exists
                if self.parent and hasattr(self.parent, "update_overview_tab"):
                    self.parent.update_overview_tab()
                
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
            "availability": "All",
            "price_sort": "No Sorting"
        }
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Query for all services
            cursor.execute("SELECT * FROM services ORDER BY service_name")
            services = cursor.fetchall()
            
            # Create and configure a new table from scratch
            new_table = TableFactory.create_table()
            service_columns = [
                ("ID", 0.05),
                ("Name", 0.20),
                ("Category", 0.15),
                ("Price", 0.10),
                ("Availability", 0.12),
                ("Description", 0.38)
            ]
            screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
            TableFactory.configure_table_columns(new_table, service_columns, screen_width)
            
            # Set up context menu for the new table
            new_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            new_table.customContextMenuRequested.connect(self.show_context_menu)
            
            # Populate the new table
            new_table.setRowCount(len(services))
            
            for row, service in enumerate(services):
                id_item = QtWidgets.QTableWidgetItem(str(service['service_id']))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                new_table.setItem(row, 0, id_item)
                
                new_table.setItem(row, 1, QtWidgets.QTableWidgetItem(service['service_name']))
                new_table.setItem(row, 2, QtWidgets.QTableWidgetItem(service.get('category', '')))
                
                price_item = QtWidgets.QTableWidgetItem(f"₱{service['price']:.2f}")
                price_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                new_table.setItem(row, 3, price_item)
                
                # Availability
                availability_status = "Available" if service.get('availability', 0) else "Unavailable"
                availability_item = QtWidgets.QTableWidgetItem(availability_status)
                availability_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                # Set color based on availability
                if service.get('availability', 0):
                    availability_item.setForeground(QtGui.QColor(0, 170, 0))  # Green for available
                else:
                    availability_item.setForeground(QtGui.QColor(200, 0, 0))  # Red for unavailable
                
                new_table.setItem(row, 4, availability_item)
                
                # Description
                new_table.setItem(row, 5, QtWidgets.QTableWidgetItem(service.get('description', '')))
        
            # Replace the old table with the new one
            old_table = self.services_table
            self.layout.replaceWidget(old_table, new_table)
            self.services_table = new_table
            old_table.deleteLater()
            
            cursor.close()
            
            # Restore filter state if necessary
            if was_filtered:
                self.filter_state = filter_state_copy
                # Add a short delay before applying filters to ensure table is fully rendered
                QtCore.QTimer.singleShot(5, self.apply_stored_filters)
        
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")

    def show_service_filter_dialog(self):
        """Show advanced filter dialog for services"""
        from ..dialogs import ServiceFilterDialog  # Import here to avoid circular imports
        
        filter_dialog = ServiceFilterDialog(self, self.filter_state)
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
                else:
                    self.filter_indicator.setVisible(False)
                    self.filter_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))

    def view_service_products(self, row):
        """View products associated with a service"""
        service_id = int(self.services_table.item(row, 0).text())
        service_name = self.services_table.item(row, 1).text()
        
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get products used in this service
            query = """
                SELECT p.product_id, p.product_name, p.category, p.price, sp.quantity
                FROM service_products sp
                JOIN products p ON sp.product_id = p.product_id
                WHERE sp.service_id = %s
                ORDER BY p.product_name
            """
            cursor.execute(query, (service_id,))
            products = cursor.fetchall()
            cursor.close()
            
            if not products:
                QtWidgets.QMessageBox.information(
                    self,
                    "No Products",
                    f"Service '{service_name}' does not use any products."
                )
                return
                
            # Create and show dialog with products
            dialog = ServiceProductsDialog(self, service_name, products)
            dialog.exec_()
            
        except mysql.connector.Error as err:
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", f"Database error: {err}")