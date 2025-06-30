from PyQt5 import QtWidgets, QtCore
from app.utils.db_manager import DBManager
import mysql.connector
from datetime import datetime
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DashboardUpdater:
    """Utility class for updating dashboard metrics and charts with fresh data"""
    
    @staticmethod
    def refresh_metrics_and_charts(dashboard_page):
        """Refresh all dashboard metrics and charts with fresh data"""
        print("Refreshing dashboard metrics and charts...")
        
        try:
            # First refresh metrics
            DashboardUpdater._update_metrics(dashboard_page)
            
            # Then refresh charts
            DashboardUpdater._update_charts(dashboard_page)
            
            print("✓ Dashboard refresh complete")
            return True
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")
            return False
    
    @staticmethod
    def _update_metrics(dashboard_page):
        """Update the dashboard metric cards with fresh data"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Load total revenue (all time)
            cursor.execute("""
                SELECT COALESCE(SUM(total_amount), 0) as total_revenue 
                FROM transactions
            """)
            total_revenue_data = cursor.fetchone()
            total_revenue = total_revenue_data['total_revenue'] if total_revenue_data else 0
            
            # Load today's revenue
            cursor.execute("""
                SELECT COALESCE(SUM(total_amount), 0) as daily_revenue 
                FROM transactions 
                WHERE DATE(transaction_date) = CURDATE()
            """)
            daily_revenue_data = cursor.fetchone()
            daily_revenue = daily_revenue_data['daily_revenue'] if daily_revenue_data else 0
            
            # Load total services count
            cursor.execute("SELECT COUNT(*) as count FROM services")
            services_count = cursor.fetchone()['count']
            
            # Load today's transactions count
            cursor.execute("""
                SELECT COUNT(*) as count 
                FROM transactions 
                WHERE DATE(transaction_date) = CURDATE()
            """)
            transactions_count = cursor.fetchone()['count']
            
            cursor.close()
            
            # Update metric cards if they exist
            if hasattr(dashboard_page, 'total_revenue_card') and dashboard_page.total_revenue_card:
                dashboard_page.total_revenue_card.value_label.setText(f"₱{total_revenue:,.2f}")
                
            if hasattr(dashboard_page, 'today_revenue_card') and dashboard_page.today_revenue_card:
                dashboard_page.today_revenue_card.value_label.setText(f"₱{daily_revenue:,.2f}")
                
            if hasattr(dashboard_page, 'services_card') and dashboard_page.services_card:
                dashboard_page.services_card.value_label.setText(str(services_count))
                
            if hasattr(dashboard_page, 'transactions_card') and dashboard_page.transactions_card:
                dashboard_page.transactions_card.value_label.setText(str(transactions_count))
            
            print("✓ Dashboard metrics updated successfully")
            
        except mysql.connector.Error as err:
            print(f"Database error updating metrics: {err}")
        except Exception as e:
            print(f"Error updating metrics: {e}")
    
    @staticmethod
    def _update_charts(dashboard_page):
        """Update the dashboard charts with fresh data"""
        try:
            # Check if the chart widgets exist
            if not (hasattr(dashboard_page, 'sales_chart_widget') and dashboard_page.sales_chart_widget):
                print("Sales chart widget not found")
                return
                
            if not (hasattr(dashboard_page, 'inventory_chart_widget') and dashboard_page.inventory_chart_widget):
                print("Inventory chart widget not found")
                return
                
            # First replace the sales chart
            try:
                new_sales_chart = dashboard_page.create_sales_chart()
                
                # Safely remove the old chart
                for i in reversed(range(dashboard_page.sales_chart_widget.layout().count())):
                    item = dashboard_page.sales_chart_widget.layout().itemAt(i)
                    if item and item.widget() and isinstance(item.widget(), FigureCanvas):
                        widget = item.widget()
                        dashboard_page.sales_chart_widget.layout().removeWidget(widget)
                        widget.setParent(None)
                        widget.deleteLater()
                
                # Add the new chart and force a layout update
                dashboard_page.sales_chart_widget.layout().addWidget(new_sales_chart, 1)
                dashboard_page.sales_chart_widget.layout().update()
                print("✓ Sales chart updated successfully")
            except Exception as e:
                print(f"Error updating sales chart: {e}")
                
            # Then replace the inventory chart
            try:
                new_inventory_chart = dashboard_page.create_inventory_chart()
                
                # Safely remove the old chart
                for i in reversed(range(dashboard_page.inventory_chart_widget.layout().count())):
                    item = dashboard_page.inventory_chart_widget.layout().itemAt(i)
                    if item and item.widget() and isinstance(item.widget(), FigureCanvas):
                        widget = item.widget()
                        dashboard_page.inventory_chart_widget.layout().removeWidget(widget)
                        widget.setParent(None)
                        widget.deleteLater()
                
                # Add the new chart and force a layout update
                dashboard_page.inventory_chart_widget.layout().addWidget(new_inventory_chart, 1)
                dashboard_page.inventory_chart_widget.layout().update()
                print("✓ Inventory chart updated successfully")
            except Exception as e:
                print(f"Error updating inventory chart: {e}")
            
            # Force update of the dashboard page
            dashboard_page.update()
            
        except Exception as e:
            print(f"Error updating charts: {e}")