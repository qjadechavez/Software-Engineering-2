from PyQt5 import QtWidgets, QtCore, QtGui
from app.utils.db_manager import DBManager
import mysql.connector
from datetime import datetime

class CustomerUpdater:
    """Utility class for updating customer tables with fresh data"""
    
    @staticmethod
    def refresh_customers_table(customers_tab):
        """Refresh the customers table with fresh data"""
        print("Refreshing customers table...")
        
        try:
            # Store current filter state to reapply later if needed
            was_filtered = False
            filter_state_copy = None
            
            if hasattr(customers_tab, 'filter_state'):
                was_filtered = customers_tab.filter_state.get("is_active", False)
                filter_state_copy = customers_tab.filter_state.copy() if was_filtered else None
                
                # Temporarily reset filter state
                customers_tab.filter_state = {
                    "is_active": False,
                    "date_range": "All Time",
                    "payment_method": "All Methods",
                    "gender": "All"
                }
            
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Query for all transactions with joined data
            cursor.execute("""
                SELECT t.*, u.username as staff_name, s.service_name 
                FROM transactions t
                LEFT JOIN users u ON t.created_by = u.user_id
                LEFT JOIN services s ON t.service_id = s.service_id
                ORDER BY t.transaction_date DESC
            """)
            transactions = cursor.fetchall()
            
            # Check if the customers table exists
            if not hasattr(customers_tab, 'customers_table') or not customers_tab.customers_table:
                print("Customers table not found")
                cursor.close()
                return False
                
            # Clear existing data
            customers_tab.customers_table.setRowCount(0)
            
            # Populate the table with fresh data
            customers_tab.customers_table.setRowCount(len(transactions))
            
            for row, transaction in enumerate(transactions):
                # Transaction ID
                id_item = QtWidgets.QTableWidgetItem(str(transaction.get('transaction_id', '')))
                id_item.setTextAlignment(QtCore.Qt.AlignCenter)
                customers_tab.customers_table.setItem(row, 0, id_item)
                
                # OR Number
                or_item = QtWidgets.QTableWidgetItem(str(transaction.get('or_number', '')))
                or_item.setTextAlignment(QtCore.Qt.AlignCenter)
                customers_tab.customers_table.setItem(row, 1, or_item)
                
                # Customer name
                customers_tab.customers_table.setItem(row, 2, QtWidgets.QTableWidgetItem(transaction.get('customer_name', '')))
                
                # Phone
                phone_item = QtWidgets.QTableWidgetItem(transaction.get('customer_phone', ''))
                phone_item.setTextAlignment(QtCore.Qt.AlignCenter)
                customers_tab.customers_table.setItem(row, 3, phone_item)
                
                # Gender
                gender_item = QtWidgets.QTableWidgetItem(transaction.get('customer_gender', ''))
                gender_item.setTextAlignment(QtCore.Qt.AlignCenter)
                customers_tab.customers_table.setItem(row, 4, gender_item)
                
                # City
                customers_tab.customers_table.setItem(row, 5, QtWidgets.QTableWidgetItem(transaction.get('customer_city', '')))
                
                # Service
                customers_tab.customers_table.setItem(row, 6, QtWidgets.QTableWidgetItem(transaction.get('service_name', '')))
                
                # Amount with proper formatting
                total = float(transaction.get('total_amount', 0))
                amount_item = QtWidgets.QTableWidgetItem(f"₱{total:.2f}")
                amount_item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                
                # Color code based on amount
                if total > 1000:
                    amount_item.setForeground(QtGui.QColor("#4CAF50"))  # Green for high value
                
                customers_tab.customers_table.setItem(row, 7, amount_item)
                
                # Payment Method
                payment_item = QtWidgets.QTableWidgetItem(transaction.get('payment_method', ''))
                payment_item.setTextAlignment(QtCore.Qt.AlignCenter)
                customers_tab.customers_table.setItem(row, 8, payment_item)
                
                # Discount
                discount = float(transaction.get('discount_percentage', 0))
                discount_item = QtWidgets.QTableWidgetItem(f"{discount:.0f}%")
                discount_item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                if discount > 0:
                    discount_item.setForeground(QtGui.QColor("#FF9800"))  # Orange for discount
                
                customers_tab.customers_table.setItem(row, 9, discount_item)
                
                # Date
                date = transaction.get('transaction_date')
                date_str = date.strftime('%Y-%m-%d %H:%M') if date else ""
                date_item = QtWidgets.QTableWidgetItem(date_str)
                date_item.setTextAlignment(QtCore.Qt.AlignCenter)
                customers_tab.customers_table.setItem(row, 10, date_item)
                
                # Staff
                customers_tab.customers_table.setItem(row, 11, QtWidgets.QTableWidgetItem(transaction.get('staff_name', '')))
            
            cursor.close()
            
            # Restore filter state if necessary
            if was_filtered and filter_state_copy:
                customers_tab.filter_state = filter_state_copy
                # Add a short delay before applying filters
                QtCore.QTimer.singleShot(50, customers_tab.apply_stored_filters)
            
            print("✓ Customers table refreshed successfully")
            return True
            
        except mysql.connector.Error as err:
            print(f"Database error refreshing customers table: {err}")
            return False
        except Exception as e:
            print(f"Error refreshing customers table: {e}")
            return False