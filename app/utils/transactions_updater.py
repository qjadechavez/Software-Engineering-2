from app.utils.db_manager import DBManager
import mysql.connector

class TransactionsUpdater:
    """Utility class for updating transaction data and related inventory"""
    
    @staticmethod
    def update_transaction_notes(transaction_id, notes):
        """Update notes for a specific transaction"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                "UPDATE transactions SET notes = %s WHERE transaction_id = %s",
                (notes, transaction_id)
            )
            
            conn.commit()
            cursor.close()
            
            return True, "Transaction notes updated successfully"
            
        except mysql.connector.Error as err:
            return False, f"Error updating transaction notes: {err}"
    
    @staticmethod
    def get_transaction_with_products(transaction_id):
        """Get transaction details along with associated products"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get transaction details
            cursor.execute("""
                SELECT t.*, s.service_name, u.username as staff_name
                FROM transactions t
                LEFT JOIN services s ON t.service_id = s.service_id
                LEFT JOIN users u ON t.created_by = u.user_id
                WHERE t.transaction_id = %s
            """, (transaction_id,))
            
            transaction = cursor.fetchone()
            
            if transaction and transaction.get('service_id'):
                # Get products used in the service
                cursor.execute("""
                    SELECT p.product_name, sp.quantity, p.price
                    FROM service_products sp
                    JOIN products p ON sp.product_id = p.product_id
                    WHERE sp.service_id = %s
                """, (transaction['service_id'],))
                
                products = cursor.fetchall()
                transaction['products'] = products
            else:
                transaction['products'] = []
            
            cursor.close()
            return transaction
            
        except mysql.connector.Error as err:
            print(f"Error fetching transaction with products: {err}")
            return None
    
    @staticmethod
    def log_inventory_transaction(product_name, transaction_type, quantity, notes=""):
        """Log an inventory transaction"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO inventory_transactions (product_name, transaction_type, quantity, notes, transaction_date)
                VALUES (%s, %s, %s, %s, NOW())
            """, (product_name, transaction_type, quantity, notes))
            
            conn.commit()
            cursor.close()
            
            return True, "Inventory transaction logged successfully"
            
        except mysql.connector.Error as err:
            return False, f"Error logging inventory transaction: {err}"