import mysql.connector
from .db_manager import DBManager
from PyQt5 import QtWidgets

class InventoryUpdater:
    """Utility class for updating inventory when supplier deliveries are received"""
    
    @staticmethod
    def update_inventory_on_delivery(supplier_id, product_name, category, quantity, supplier_name):
        """Update inventory when a supplier delivery is marked as received"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            # Check if product already exists in inventory
            cursor.execute(
                "SELECT product_id, quantity FROM products WHERE product_name = %s",
                (product_name,)
            )
            existing_product = cursor.fetchone()
            
            if existing_product:
                # Update existing product quantity
                new_quantity = existing_product[1] + quantity
                cursor.execute(
                    "UPDATE products SET quantity = %s WHERE product_id = %s",
                    (new_quantity, existing_product[0])
                )
                product_id = existing_product[0]
            else:
                # Create new product entry
                cursor.execute(
                    """INSERT INTO products (product_name, category, quantity, price, threshold_value, availability) 
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (product_name, category, quantity, 0.00, 10, True)
                )
                product_id = cursor.lastrowid
            
            # Update inventory status with "Received" status and supplier info
            cursor.execute("""
                INSERT INTO inventory_status (product_id, product_name, quantity, status, last_updated, supplier_name)
                VALUES (%s, %s, %s, %s, NOW(), %s)
                ON DUPLICATE KEY UPDATE
                    quantity = %s,
                    status = 'Received',
                    last_updated = NOW(),
                    supplier_name = %s
            """, (product_id, product_name, quantity, 'Received', supplier_name, quantity, supplier_name))
            
            # Log the inventory transaction
            cursor.execute(
                """INSERT INTO inventory_transactions (product_name, transaction_type, quantity, notes, transaction_date) 
                   VALUES (%s, %s, %s, %s, NOW())""",
                (product_name, 'Stock In', quantity, f'Received from supplier: {supplier_name}')
            )
            
            # Reset products_on_the_way to 0 since they've been received
            cursor.execute(
                "UPDATE suppliers SET products_on_the_way = 0 WHERE supplier_id = %s",
                (supplier_id,)
            )
            
            conn.commit()
            cursor.close()
            
            return True, f"Successfully added {quantity} units of '{product_name}' to inventory"
            
        except mysql.connector.Error as err:
            return False, f"Error updating inventory: {err}"
    
    @staticmethod
    def refresh_all_inventory_displays(main_window):
        """Refresh all inventory-related displays in the application"""
        try:
            print("Starting comprehensive inventory refresh...")
            
            # Find the inventory page through the application
            app = QtWidgets.QApplication.instance()
            inventory_page = None
            
            # Search through all widgets in the application
            for widget in app.allWidgets():
                # Look for InventoryPage class specifically
                if hasattr(widget, '__class__') and 'InventoryPage' in str(widget.__class__):
                    inventory_page = widget
                    print(f"Found InventoryPage: {widget}")
                    break
                    
                # Alternative: Look for widgets with inventory tab structure
                if (hasattr(widget, 'overview_tab') and 
                    hasattr(widget, 'products_tab') and 
                    hasattr(widget, 'inventory_status_tab')):
                    inventory_page = widget
                    print(f"Found inventory page by tab structure: {widget}")
                    break
            
            if inventory_page:
                print("Refreshing all inventory components...")
                
                try:
                    # Refresh overview tab
                    if hasattr(inventory_page, 'overview_tab') and hasattr(inventory_page.overview_tab, 'update_dashboard'):
                        inventory_page.overview_tab.update_dashboard()
                        print("✓ Refreshed overview tab dashboard")
                    
                    # Refresh products tab
                    if hasattr(inventory_page, 'products_tab'):
                        if hasattr(inventory_page.products_tab, 'rebuild_table'):
                            inventory_page.products_tab.rebuild_table()
                            print("✓ Refreshed products tab table")
                        elif hasattr(inventory_page.products_tab, 'load_products'):
                            inventory_page.products_tab.load_products()
                            print("✓ Refreshed products tab (load_products)")
                    
                    # Refresh inventory status tab - MOST IMPORTANT
                    if hasattr(inventory_page, 'inventory_status_tab'):
                        if hasattr(inventory_page.inventory_status_tab, 'load_inventory'):
                            inventory_page.inventory_status_tab.load_inventory()
                            print("✓ Refreshed inventory status tab data")
                        if hasattr(inventory_page.inventory_status_tab, 'update_analytics'):
                            inventory_page.inventory_status_tab.update_analytics()
                            print("✓ Refreshed inventory analytics")
                    
                    print("Successfully refreshed all inventory displays")
                    
                except Exception as e:
                    print(f"Error refreshing specific inventory tabs: {e}")
                    
            else:
                print("Could not find inventory page to refresh")
                
        except Exception as e:
            print(f"Error in refresh_all_inventory_displays: {e}")
    
    @staticmethod
    def _find_inventory_page_recursive(widget):
        """Recursively search for inventory page in widget hierarchy"""
        # Check current widget
        if (hasattr(widget, 'overview_tab') and 
            hasattr(widget, 'products_tab') and 
            hasattr(widget, 'inventory_status_tab')):
            return widget
        
        # Check children
        for child in widget.findChildren(QtWidgets.QWidget):
            if (hasattr(child, 'overview_tab') and 
                hasattr(child, 'products_tab') and 
                hasattr(child, 'inventory_status_tab')):
                return child
        
        return None