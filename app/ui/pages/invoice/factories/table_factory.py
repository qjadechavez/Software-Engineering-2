from PyQt5 import QtWidgets, QtCore

class TableFactory:
    """Factory class for creating and configuring tables for the invoice module"""
    
    @staticmethod
    def create_table():
        """Create a styled table widget"""
        table = QtWidgets.QTableWidget()
        table.setStyleSheet("""
            QTableWidget {
                background-color: #232323;
                color: white;
                gridline-color: #444444;
                border: 1px solid #444444;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #2c2c2c;
                color: white;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #444;
                font-weight: bold;
            }
            QTableWidget::item {
                border-bottom: 1px solid #444444;
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #3a3a3a;
                color: #ffffff;
            }
        """)
        
        table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        table.setSelectionMode(QtWidgets.QTableWidget.SingleSelection)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.setShowGrid(True)
        
        return table
    
    @staticmethod
    def configure_table_columns(table, columns, screen_width):
        """Configure table columns with specified widths"""
        table.setColumnCount(len(columns))
        header_labels = [col[0] for col in columns]
        table.setHorizontalHeaderLabels(header_labels)
        
        for i, (_, width) in enumerate(columns):
            table.setColumnWidth(i, int(screen_width * width))