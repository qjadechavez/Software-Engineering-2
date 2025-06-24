from PyQt5 import QtWidgets, QtCore, QtGui
from app.utils.db_manager import DBManager
import mysql.connector
from ..style_factory import StyleFactory
from ..table_factory import TableFactory
from ..control_panel_factory import ControlPanelFactory
from ..dialogs import ServiceDialog

class ServicesTab(QtWidgets.QWidget):
    """Tab for managing services in inventory"""
    
    def __init__(self, parent=None):
        super(ServicesTab, self).__init__()
        self.parent = parent
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
        control_layout = ControlPanelFactory.create_search_control(
            self.search_input,
            "+ Add Service",
            self.show_add_service_dialog,
            self.filter_services,
            self.show_service_filter_dialog  # Add filter callback
        )
        self.layout.addLayout(control_layout)
        
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
    
    def load_services(self):
        """Load services from the database and populate the table"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Clear existing items
            self.services_table.setRowCount(0)
            
            # Reset search filter
            self.search_input.clear()
            
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
    
    def show_context_menu(self, position):
        """Show context menu for service actions"""
        context_menu = QtWidgets.QMenu()
        
        # Get the current row
        current_row = self.services_table.currentRow()
        
        if current_row >= 0:
            edit_action = context_menu.addAction("Edit")
            delete_action = context_menu.addAction("Delete")
            
            # Show the context menu
            action = context_menu.exec_(self.services_table.mapToGlobal(position))
            
            if action == edit_action:
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
    
    def show_service_filter_dialog(self):
        """Show advanced filter dialog for services"""
        # Create a dialog
        filter_dialog = QtWidgets.QDialog(self)
        filter_dialog.setWindowTitle("Filter Services")
        filter_dialog.setMinimumWidth(400)
        filter_dialog.setStyleSheet(StyleFactory.get_dialog_style())
        
        # Create layout
        layout = QtWidgets.QVBoxLayout(filter_dialog)
        form_layout = QtWidgets.QFormLayout()
        
        # Category filter
        category_label = QtWidgets.QLabel("Category:")
        category_combo = QtWidgets.QComboBox()
        category_combo.addItem("All Categories")
        
        # Get unique categories
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT category FROM services WHERE category IS NOT NULL AND category != ''")
            categories = cursor.fetchall()
            for category in categories:
                category_combo.addItem(category['category'])
            cursor.close()
        except mysql.connector.Error:
            pass
        
        form_layout.addRow(category_label, category_combo)
        
        # Availability filter
        availability_label = QtWidgets.QLabel("Availability:")
        availability_combo = QtWidgets.QComboBox()
        availability_combo.addItem("All")
        availability_combo.addItem("Available")
        availability_combo.addItem("Unavailable")
        form_layout.addRow(availability_label, availability_combo)
        
        # Price range filter
        price_range_label = QtWidgets.QLabel("Price Range:")
        price_range_layout = QtWidgets.QHBoxLayout()
        min_price = QtWidgets.QDoubleSpinBox()
        min_price.setPrefix("₱ ")
        min_price.setMaximum(1000000)
        max_price = QtWidgets.QDoubleSpinBox()
        max_price.setPrefix("₱ ")
        max_price.setMaximum(1000000)
        max_price.setValue(1000000)
        price_range_layout.addWidget(min_price)
        price_range_layout.addWidget(QtWidgets.QLabel(" to "))
        price_range_layout.addWidget(max_price)
        form_layout.addRow(price_range_label, price_range_layout)
        
        # Buttons
        buttons_layout = QtWidgets.QHBoxLayout()
        apply_button = QtWidgets.QPushButton("Apply Filter")
        reset_button = QtWidgets.QPushButton("Reset")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #666;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #777;
            }
        """)
        
        buttons_layout.addWidget(reset_button)
        buttons_layout.addWidget(apply_button)
        
        layout.addLayout(form_layout)
        layout.addLayout(buttons_layout)
        
        # Connect signals
        def apply_filters():
            category = category_combo.currentText()
            availability = availability_combo.currentText()
            min_price_val = min_price.value()
            max_price_val = max_price.value()
            
            for row in range(self.services_table.rowCount()):
                show_row = True
        
                # Apply category filter
                if category != "All Categories":
                    category_cell = self.services_table.item(row, 2).text()
                    if category_cell != category:
                        show_row = False
        
                # Apply availability filter
                if availability != "All" and show_row:
                    availability_cell = self.services_table.item(row, 4).text()
                    if (availability == "Available" and availability_cell != "Available") or \
                        (availability == "Unavailable" and availability_cell != "Unavailable"):
                        show_row = False
        
                # Apply price filter
                if show_row:
                    price_text = self.services_table.item(row, 3).text().replace("₱", "")
                    try:
                        price = float(price_text)
                        if price < min_price_val or price > max_price_val:
                            show_row = False
                    except ValueError:
                        pass
        
                self.services_table.setRowHidden(row, not show_row)
            
            filter_dialog.accept()
        
        def reset_filters():
            # Show all rows
            for row in range(self.services_table.rowCount()):
                self.services_table.setRowHidden(row, False)
            filter_dialog.accept()
        
        apply_button.clicked.connect(apply_filters)
        reset_button.clicked.connect(reset_filters)
        
        filter_dialog.exec_()