from PyQt5 import QtWidgets
from .style_factory import StyleFactory

class TableFactory:
    """Factory class for creating consistent tables"""
    
    @staticmethod
    def create_table():
        """Create a base table with common configuration"""
        table = QtWidgets.QTableWidget()
        table.setStyleSheet("""
            QTableWidget {
                background-color: #1e1e1e;
                gridline-color: #444;
                color: white;
                border-radius: 5px;
                border: 1px solid #555;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #2c2c2c;
                color: white;
                padding: 8px;
                border: 1px solid #444;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
                background-color: #1e1e1e;
            }
            QTableWidget::item:selected {
                background-color: #0078d7;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 12px;
            }
            QScrollBar::handle:vertical {
                background: #666;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar:horizontal {
                background: #2a2a2a;
                height: 12px;
            }
            QScrollBar::handle:horizontal {
                background: #666;
                border-radius: 5px;
                min-width: 20px;
            }
        """)
        table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.setAlternatingRowColors(False)
        table.verticalHeader().setVisible(False)
        table.setSortingEnabled(True)
        table.setShowGrid(True)
        
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        table.horizontalHeader().setStretchLastSection(False)
        
        return table
    
    @staticmethod
    def configure_table_columns(table, column_data, screen_width):
        """Configure table columns with headers and widths"""
        table_width = screen_width - 300
        
        table.setColumnCount(len(column_data))
        
        headers = [col[0] for col in column_data]
        table.setHorizontalHeaderLabels(headers)
        
        table.horizontalHeader().setStretchLastSection(True)
        
        for idx, (_, width_pct) in enumerate(column_data[:-1]):
            table.setColumnWidth(idx, int(table_width * width_pct))