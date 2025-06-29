from PyQt5 import QtWidgets, QtCore, QtGui
import mysql.connector
from app.utils.db_manager import DBManager
from datetime import datetime
import os
from ..style_factory import StyleFactory
from ..table_factory import TableFactory
from ..control_panel_factory import ControlPanelFactory

class DatabaseBackupTab(QtWidgets.QWidget):
    """Tab for database backup management"""
    
    def __init__(self, parent=None):
        super(DatabaseBackupTab, self).__init__()
        self.parent = parent
        
        # Check if parent has user info and validate access
        if self.parent and hasattr(self.parent, 'user_info'):
            user_role = self.parent.user_info.get("role", "").lower()
            if user_role != "admin":
                self.show_access_denied()
                return
        
        self.setup_ui()
        self.load_table_info()
    
    def show_access_denied(self):
        """Show access denied message in the tab"""
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        message = QtWidgets.QLabel("Access denied. Admin privileges required.")
        message.setStyleSheet("color: #f44336; font-size: 16px; font-weight: bold;")
        message.setAlignment(QtCore.Qt.AlignCenter)
        
        layout.addWidget(message)
    
    def setup_ui(self):
        """Set up the UI components"""
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        
        # Header section with database info
        header_layout = QtWidgets.QHBoxLayout()
        
        # Database info
        db_info_layout = QtWidgets.QVBoxLayout()
        
        self.db_name_label = QtWidgets.QLabel("Database: testdb")
        self.db_name_label.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
        """)
        
        self.table_count_label = QtWidgets.QLabel("Total Tables: 0")
        self.table_count_label.setStyleSheet("""
            color: #B0B0B0;
            font-size: 14px;
            margin-bottom: 10px;
            border: none;
            background: transparent;
        """)
        
        db_info_layout.addWidget(self.db_name_label)
        db_info_layout.addWidget(self.table_count_label)
        
        header_layout.addLayout(db_info_layout)
        header_layout.addStretch()
        
        # Action buttons
        self.backup_button = QtWidgets.QPushButton("Create Full Backup")
        self.backup_button.setStyleSheet(StyleFactory.get_button_style())
        self.backup_button.clicked.connect(self.create_backup)
        
        self.restore_button = QtWidgets.QPushButton("Restore from Backup")
        self.restore_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
        self.restore_button.clicked.connect(self.restore_backup)
        
        header_layout.addWidget(self.backup_button)
        header_layout.addWidget(self.restore_button)
        
        self.layout.addLayout(header_layout)
        
        # Database info cards
        info_layout = QtWidgets.QHBoxLayout()
        info_layout.setSpacing(15)
        
        self.tables_card = self.create_info_card("Total Tables", "0", "#4CAF50", "tables")
        self.size_card = self.create_info_card("Database Size", "N/A", "#2196F3", "size")
        self.backup_card = self.create_info_card("Last Backup", "Never", "#FF9800", "backup")
        
        info_layout.addWidget(self.tables_card)
        info_layout.addWidget(self.size_card)
        info_layout.addWidget(self.backup_card)
        
        self.layout.addLayout(info_layout)
        
        # Backup controls
        controls_frame = QtWidgets.QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: #232323;
                border-radius: 8px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }
        """)
        controls_layout = QtWidgets.QVBoxLayout(controls_frame)
        controls_layout.setContentsMargins(20, 20, 20, 20)
        controls_layout.setSpacing(15)
        
        # Backup options
        backup_title = QtWidgets.QLabel("Full Database Backup")
        backup_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold; border: none; background: transparent;")
        controls_layout.addWidget(backup_title)
        
        # Backup description
        desc_label = QtWidgets.QLabel("Create a complete backup of all database tables and data")
        desc_label.setStyleSheet("color: #cccccc; font-size: 14px; margin-bottom: 10px; border: none; background: transparent;")
        controls_layout.addWidget(desc_label)
        
        # Backup location
        location_layout = QtWidgets.QHBoxLayout()
        
        location_label = QtWidgets.QLabel("Backup Location:")
        location_label.setStyleSheet("color: #cccccc; font-size: 14px; border: none; background: transparent;")
        
        self.location_input = QtWidgets.QLineEdit()
        self.location_input.setText(os.path.expanduser("~/Desktop"))
        self.location_input.setStyleSheet(StyleFactory.get_search_input_style())
        
        browse_button = QtWidgets.QPushButton("Browse")
        browse_button.setStyleSheet(StyleFactory.get_button_style(secondary=True))
        browse_button.clicked.connect(self.browse_location)
        
        location_layout.addWidget(location_label)
        location_layout.addWidget(self.location_input, 1)
        location_layout.addWidget(browse_button)
        
        controls_layout.addLayout(location_layout)
        
        # Backup buttons
        button_layout = QtWidgets.QHBoxLayout()
        
        create_backup_btn = QtWidgets.QPushButton("Create Backup")
        create_backup_btn.setStyleSheet(StyleFactory.get_button_style())
        create_backup_btn.clicked.connect(self.create_backup)
        
        restore_backup_btn = QtWidgets.QPushButton("Restore from Backup")
        restore_backup_btn.setStyleSheet(StyleFactory.get_button_style(secondary=True))
        restore_backup_btn.clicked.connect(self.restore_backup)
        
        button_layout.addStretch()
        button_layout.addWidget(create_backup_btn)
        button_layout.addWidget(restore_backup_btn)
        
        controls_layout.addLayout(button_layout)
        
        self.layout.addWidget(controls_frame)
        
        # Tables information
        tables_frame = QtWidgets.QFrame()
        tables_frame.setStyleSheet("""
            QFrame {
                background-color: #232323;
                border-radius: 8px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }
        """)
        tables_layout = QtWidgets.QVBoxLayout(tables_frame)
        tables_layout.setContentsMargins(20, 20, 20, 20)
        
        tables_title = QtWidgets.QLabel("Database Tables")
        tables_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold; border: none;")
        tables_layout.addWidget(tables_title)
        
        # Create tables table
        self.tables_table = TableFactory.create_table()
        
        # Define column headers
        table_columns = [
            ("Table Name", 0.30),
            ("Rows", 0.20),
            ("Size (KB)", 0.20),
            ("Engine", 0.15),
            ("Collation", 0.15)
        ]
        
        screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
        TableFactory.configure_table_columns(self.tables_table, table_columns, screen_width)
        
        tables_layout.addWidget(self.tables_table)
        
        self.layout.addWidget(tables_frame, 1)
        
        # Progress bar (initially hidden)
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555;
                border-radius: 5px;
                text-align: center;
                background-color: #2a2a2a;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 5px;
            }
        """)
        self.progress_bar.setVisible(False)
        self.layout.addWidget(self.progress_bar)
    
    def create_info_card(self, title, value, color, icon_type):
        """Create an information card widget"""
        card = QtWidgets.QFrame()
        card.setFixedHeight(80)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #232323;
                border-radius: 8px;
                border: 1px solid rgba(100, 100, 100, 0.3);
            }}
        """)
        
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        # Icon
        icon_label = QtWidgets.QLabel()
        icon_label.setFixedSize(32, 32)
        icon_label.setStyleSheet(f"color: {color}; font-size: 24px; font-weight: bold;")
        
        # Set icon based on type
        icon_map = {
            "tables": "📋",
            "size": "💾",
            "backup": "🔄"
        }
        icon_label.setText(icon_map.get(icon_type, "📋"))
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Text content
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(2)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("color: #cccccc; font-size: 12px; border: none; background: transparent;")
        
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet(f"color: {color}; font-size: 18px; font-weight: bold; border: none; background: transparent;")
        
        text_layout.addWidget(title_label)
        text_layout.addWidget(value_label)
        
        layout.addWidget(icon_label)
        layout.addLayout(text_layout)
        layout.addStretch()
        
        # Store reference to value label for updates
        card.value_label = value_label
        
        return card
    
    def load_table_info(self):
        """Load database table information"""
        try:
            conn = DBManager.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Get database name first
            cursor.execute("SELECT DATABASE() as db_name")
            db_result = cursor.fetchone()
            current_db = db_result['db_name'] if db_result else 'testdb'
            
            # Query to get table information with correct column names
            cursor.execute("""
                SELECT 
                    TABLE_NAME as table_name,
                    TABLE_ROWS as table_rows,
                    ROUND(((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024), 2) as size_mb,
                    CREATE_TIME as created_date,
                    UPDATE_TIME as updated_date
                FROM information_schema.TABLES 
                WHERE TABLE_SCHEMA = %s
                AND TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """, (current_db,))
            
            tables = cursor.fetchall()
            
            # Clear existing items
            self.tables_table.setRowCount(0)
            
            # Populate the table
            self.tables_table.setRowCount(len(tables))
            
            for row, table in enumerate(tables):
                # Table Name
                self.tables_table.setItem(row, 0, QtWidgets.QTableWidgetItem(table['table_name']))
                
                # Row Count
                row_count = table.get('table_rows', 0) or 0
                row_item = QtWidgets.QTableWidgetItem(str(row_count))
                row_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tables_table.setItem(row, 1, row_item)
                
                # Size
                size_mb = table.get('size_mb', 0) or 0
                size_item = QtWidgets.QTableWidgetItem(f"{size_mb:.2f} MB")
                size_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tables_table.setItem(row, 2, size_item)
                
                # Created Date
                created = table.get('created_date')
                created_str = created.strftime('%Y-%m-%d') if created else "N/A"
                created_item = QtWidgets.QTableWidgetItem(created_str)
                created_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tables_table.setItem(row, 3, created_item)
                
                # Updated Date
                updated = table.get('updated_date')
                updated_str = updated.strftime('%Y-%m-%d') if updated else "N/A"
                updated_item = QtWidgets.QTableWidgetItem(updated_str)
                updated_item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tables_table.setItem(row, 4, updated_item)
            
            cursor.close()
            
            # Update table count
            self.update_table_count(len(tables))
            
        except mysql.connector.Error as err:
            print(f"Database error loading table info: {err}")
            if self.parent:
                self.parent.show_error_message(f"Database error: {err}")
        except Exception as e:
            print(f"Error loading table info: {e}")
            if self.parent:
                self.parent.show_error_message(f"Error loading table information: {e}")
    
    def browse_location(self):
        """Browse for backup location"""
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self, 
            "Select Backup Location",
            self.location_input.text()
        )
        if folder:
            self.location_input.setText(folder)
    
    def create_backup(self):
        """Create database backup"""
        try:
            backup_location = self.location_input.text()
            if not os.path.exists(backup_location):
                QtWidgets.QMessageBox.warning(self, "Warning", "Backup location does not exist!")
                return
            
            # Generate backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"database_backup_{timestamp}.sql"
            backup_path = os.path.join(backup_location, backup_filename)
            
            # Show progress bar
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            conn = DBManager.get_connection()
            cursor = conn.cursor()
            
            # Get database name
            cursor.execute("SELECT DATABASE()")
            db_name = cursor.fetchone()[0]
            
            self.progress_bar.setValue(20)
            
            # Create mysqldump command (simplified version)
            # In a real implementation, you would use subprocess to call mysqldump
            # For now, we'll create a basic SQL export
            
            with open(backup_path, 'w', encoding='utf-8') as backup_file:
                backup_file.write(f"-- Database backup created on {datetime.now()}\n")
                backup_file.write(f"-- Database: {db_name}\n\n")
                
                # Get all tables
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                progress_step = 60 / len(tables) if tables else 0
                current_progress = 20
                
                for table_tuple in tables:
                    table_name = table_tuple[0]
                    
                    # Get table structure
                    cursor.execute(f"SHOW CREATE TABLE `{table_name}`")
                    create_table = cursor.fetchone()[1]
                    
                    backup_file.write(f"-- Table structure for {table_name}\n")
                    backup_file.write(f"DROP TABLE IF EXISTS `{table_name}`;\n")
                    backup_file.write(f"{create_table};\n\n")
                    
                    # Get table data
                    cursor.execute(f"SELECT * FROM `{table_name}`")
                    rows = cursor.fetchall()
                    
                    if rows:
                        backup_file.write(f"-- Dumping data for table {table_name}\n")
                        backup_file.write(f"LOCK TABLES `{table_name}` WRITE;\n")
                        
                        # Insert data (simplified)
                        cursor.execute(f"DESCRIBE `{table_name}`")
                        columns = [col[0] for col in cursor.fetchall()]
                        
                        backup_file.write(f"INSERT INTO `{table_name}` ({', '.join([f'`{col}`' for col in columns])}) VALUES\n")
                        
                        for i, row in enumerate(rows):
                            # Convert row to string representation
                            values = []
                            for value in row:
                                if value is None:
                                    values.append("NULL")
                                elif isinstance(value, str):
                                    values.append(f"'{value.replace('\'', '\\\'')}'" )
                                else:
                                    values.append(str(value))
                            
                            backup_file.write(f"({', '.join(values)})")
                            if i < len(rows) - 1:
                                backup_file.write(",\n")
                            else:
                                backup_file.write(";\n")
                        
                        backup_file.write(f"UNLOCK TABLES;\n\n")
                    
                    current_progress += progress_step
                    self.progress_bar.setValue(int(current_progress))
            
            self.progress_bar.setValue(100)
            
            # Update last backup time
            self.backup_card.value_label.setText(datetime.now().strftime("%Y-%m-%d %H:%M"))
            
            QtWidgets.QMessageBox.information(
                self, 
                "Backup Complete", 
                f"Database backup created successfully!\nLocation: {backup_path}"
            )
            
            cursor.close()
            
        except Exception as err:
            QtWidgets.QMessageBox.critical(self, "Error", f"Backup failed: {str(err)}")
        finally:
            self.progress_bar.setVisible(False)
    
    def restore_backup(self):
        """Restore database from backup"""
        backup_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select Backup File",
            self.location_input.text(),
            "SQL Files (*.sql);;All Files (*)"
        )
        
        if backup_file:
            reply = QtWidgets.QMessageBox.question(
                self,
                "Confirm Restore",
                "This will replace all current data with the backup data. Are you sure?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            
            if reply == QtWidgets.QMessageBox.Yes:
                try:
                    # Show progress bar
                    self.progress_bar.setVisible(True)
                    self.progress_bar.setValue(0)
                    
                    # Read and execute SQL file
                    with open(backup_file, 'r', encoding='utf-8') as f:
                        sql_content = f.read()
                    
                    conn = DBManager.get_connection()
                    cursor = conn.cursor()
                    
                    # Split SQL content into statements
                    statements = sql_content.split(';')
                    total_statements = len(statements)
                    
                    for i, statement in enumerate(statements):
                        statement = statement.strip()
                        if statement and not statement.startswith('--'):
                            try:
                                cursor.execute(statement)
                            except mysql.connector.Error:
                                pass  # Skip errors for individual statements
                        
                        progress = int((i / total_statements) * 100)
                        self.progress_bar.setValue(progress)
                    
                    conn.commit()
                    cursor.close()
                    
                    self.progress_bar.setValue(100)
                    
                    QtWidgets.QMessageBox.information(
                        self,
                        "Restore Complete",
                        "Database restored successfully!"
                    )
                    
                    # Reload table information
                    self.load_table_info()
                    
                except Exception as err:
                    QtWidgets.QMessageBox.critical(self, "Error", f"Restore failed: {str(err)}")
                finally:
                    self.progress_bar.setVisible(False)
    
    def update_table_count(self, count):
        """Update the table count display"""
        try:
            # Update any table count labels or info displays
            if hasattr(self, 'table_count_label'):
                self.table_count_label.setText(f"Total Tables: {count}")
            
            # Update any info cards that might display table counts
            if hasattr(self, 'tables_card'):
                self.tables_card.value_label.setText(str(count))
                
            print(f"✓ Updated table count: {count} tables")
            
        except Exception as e:
            print(f"Error updating table count: {e}")