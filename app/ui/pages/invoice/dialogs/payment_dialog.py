from PyQt5 import QtWidgets, QtCore, QtGui
from ...inventory.dialogs.base_dialog import BaseDialog

class PaymentDialog(BaseDialog):
    """Dialog for processing payment and calculating change"""
    
    def __init__(self, parent=None, total_amount=0):
        self.total_amount = total_amount
        super(PaymentDialog, self).__init__(parent, title="Payment Processing")
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the payment dialog UI"""
        # scale dialog to a portion of the available screen
        screen_geom = QtWidgets.QApplication.desktop().availableGeometry(self)
        dlg_width  = int(screen_geom.width()  * 0.5)
        dlg_height = int(screen_geom.height() * 0.9)
        # initialize base UI at computed height and lock size
        self.setup_base_ui(dlg_height)
        # disable scrolling – force content to resize into the dialog
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy  (QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        # set a base fixed size, disable scroll bars
        self.setFixedSize(dlg_width, dlg_height)
        # now expand to fit content, capped at 90% of screen
        self.adjustSize()
        cap_w = int(screen_geom.width() * 0.9)
        cap_h = int(screen_geom.height() * 0.9)
        new_w = min(self.width(), cap_w)
        new_h = min(self.height(), cap_h)
        self.setFixedSize(new_w, new_h)

         # Update header
        self.header_label.setText("Payment Processing")
        
        # Total amount display
        total_frame = QtWidgets.QFrame()
        total_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a2a;
                border: 2px solid #4CAF50;
                border-radius: 8px;
                padding: 15px;
                margin: 5px 0px;
            }
        """)
        total_layout = QtWidgets.QVBoxLayout(total_frame)
        
        total_label = QtWidgets.QLabel("Total Amount to Pay:")
        total_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; border: none;")
        total_layout.addWidget(total_label)
        
        self.total_display = QtWidgets.QLabel(f"₱{self.total_amount:.2f}")
        self.total_display.setStyleSheet("color: #4CAF50; font-size: 24px; font-weight: bold;")
        self.total_display.setAlignment(QtCore.Qt.AlignCenter)
        total_layout.addWidget(self.total_display)
        
        self.form_layout.addRow("", total_frame)
        
        # Amount received input
        amount_label = QtWidgets.QLabel("Amount Received:")
        amount_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        
        self.amount_input = QtWidgets.QDoubleSpinBox()
        self.amount_input.setRange(0, 999999)
        self.amount_input.setDecimals(2)
        self.amount_input.setPrefix("₱")
        self.amount_input.setValue(self.total_amount)
        self.amount_input.setStyleSheet("""
            QDoubleSpinBox {
                padding: 10px;
                background-color: #2a2a2a;
                color: white;
                border: 2px solid #444444;
                border-radius: 6px;
                font-size: 16px;
                font-weight: bold;
            }
            QDoubleSpinBox:focus {
                border: 2px solid #2196F3;
            }
            QDoubleSpinBox::up-button, QDoubleSpinBox::down-button {
                background-color: #3a3a3a;
                width: 25px;
                border-radius: 3px;
            }
            QDoubleSpinBox::up-button:hover, QDoubleSpinBox::down-button:hover {
                background-color: #4a4a4a;
            }
        """)
        self.amount_input.valueChanged.connect(self.calculate_change)
        
        self.form_layout.addRow(amount_label, self.amount_input)
        
        # Change calculation display
        change_frame = QtWidgets.QFrame()
        change_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a1a;
                border: 2px solid #FF9800;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0px;
            }
        """)
        change_layout = QtWidgets.QVBoxLayout(change_frame)
        
        change_label = QtWidgets.QLabel("Change to Give:")
        change_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold; border: none;")
        change_layout.addWidget(change_label)
        
        self.change_display = QtWidgets.QLabel("₱0.00")
        self.change_display.setStyleSheet("color: #FF9800; font-size: 28px; font-weight: bold;")
        self.change_display.setAlignment(QtCore.Qt.AlignCenter)
        change_layout.addWidget(self.change_display)
        
        # Payment status
        self.payment_status = QtWidgets.QLabel("")
        self.payment_status.setAlignment(QtCore.Qt.AlignCenter)
        self.payment_status.setStyleSheet("font-size: 14px; font-weight: bold; margin: 5px;")
        change_layout.addWidget(self.payment_status)
        
        self.form_layout.addRow("", change_frame)
        
        # Quick amount buttons
        quick_amounts_label = QtWidgets.QLabel("Quick Amounts:")
        quick_amounts_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        
        quick_buttons_widget = QtWidgets.QWidget()
        quick_buttons_layout = QtWidgets.QHBoxLayout(quick_buttons_widget)
        quick_buttons_layout.setSpacing(10)
        
        # Common bill denominations
        amounts = [20, 50, 100, 200, 500, 1000]
        for amount in amounts:
            btn = QtWidgets.QPushButton(f"₱{amount}")
            btn.setStyleSheet("""
                QPushButton {
                    padding: 8px 12px;
                    background-color: #444444;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #555555;
                }
                QPushButton:pressed {
                    background-color: #333333;
                }
            """)
            btn.clicked.connect(lambda checked, amt=amount: self.set_quick_amount(amt))
            quick_buttons_layout.addWidget(btn)
        
        self.form_layout.addRow(quick_amounts_label, quick_buttons_widget)
        
        # Exact amount button
        exact_button = QtWidgets.QPushButton("Exact Amount")
        exact_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        exact_button.clicked.connect(self.set_exact_amount)
        
        self.form_layout.addRow("", exact_button)
        
        # Configure save button
        self.save_button.setText("Complete Payment")
        self.save_button.setStyleSheet("""
            QPushButton {
                padding: 12px 25px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }
        """)
        self.save_button.clicked.connect(self.complete_payment)
        
        # Initially calculate change
        self.calculate_change()
        
        # Set focus to amount input
        self.amount_input.setFocus()
        self.amount_input.selectAll()
    
    def calculate_change(self):
        """Calculate and display the change"""
        amount_received = self.amount_input.value()
        change = amount_received - self.total_amount
        
        self.change_display.setText(f"₱{change:.2f}")
        
        if change < 0:
            self.change_display.setStyleSheet("color: #F44336; font-size: 28px; font-weight: bold;")
            self.payment_status.setText("⚠️ Insufficient Payment")
            self.payment_status.setStyleSheet("color: #F44336; font-size: 14px; font-weight: bold; margin: 5px;")
            self.save_button.setEnabled(False)
        elif change == 0:
            self.change_display.setStyleSheet("color: #4CAF50; font-size: 28px; font-weight: bold;")
            self.payment_status.setText("✓ Exact Payment")
            self.payment_status.setStyleSheet("color: #4CAF50; font-size: 14px; font-weight: bold; margin: 5px;")
            self.save_button.setEnabled(True)
        else:
            self.change_display.setStyleSheet("color: #FF9800; font-size: 28px; font-weight: bold;")
            self.payment_status.setText("💰 Change Required")
            self.payment_status.setStyleSheet("color: #FF9800; font-size: 14px; font-weight: bold; margin: 5px;")
            self.save_button.setEnabled(True)
    
    def set_quick_amount(self, amount):
        """Set a quick amount from the buttons"""
        # Calculate how many bills needed to cover the total
        bills_needed = int((self.total_amount + amount - 1) // amount)  # Ceiling division
        total_amount = bills_needed * amount
        self.amount_input.setValue(total_amount)
    
    def set_exact_amount(self):
        """Set the exact amount needed"""
        self.amount_input.setValue(self.total_amount)
    
    def complete_payment(self):
        """Complete the payment process"""
        amount_received = self.amount_input.value()
        change = amount_received - self.total_amount
        
        if change < 0:
            QtWidgets.QMessageBox.warning(self, "Insufficient Payment", 
                                        f"The amount received (₱{amount_received:.2f}) is less than the total amount (₱{self.total_amount:.2f}).")
            return
        
        # Show change confirmation if there's change to give
        if change > 0:
            reply = QtWidgets.QMessageBox.question(self, "Confirm Change", 
                                                f"Please give ₱{change:.2f} change to the customer.\n\nHave you given the change?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)
            
            if reply == QtWidgets.QMessageBox.No:
                return
        
        # Payment completed successfully
        self.accept()
    
    def get_payment_data(self):
        """Get the payment data"""
        return {
            "amount_received": self.amount_input.value(),
            "change_given": self.amount_input.value() - self.total_amount
        }