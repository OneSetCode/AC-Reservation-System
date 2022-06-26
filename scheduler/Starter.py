import sys
import Scheduler
from PyQt5.QtWidgets import (QMainWindow, QPushButton, QApplication, QInputDialog,
    QMessageBox, QLabel, QLineEdit, QDialog, QDialogButtonBox, QFormLayout)
from PyQt5.QtGui import QFont

# The GUI window
class GUIWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):      
        font1 = QFont("Roman times", 15, QFont.Bold)
        font2 = QFont("Roman times", 12)
        
        lbl1 = QLabel('Welcome! What service do you require?', self)
        lbl1.setFont(font1)
        lbl1.move(50, 35)
        lbl1.adjustSize()

        # Define the buttons
        btn1 = QPushButton("Create Customer", self)
        btn1.setFont(font2)
        btn1.setGeometry(50, 100, 220, 50)
 
        btn2 = QPushButton("Create Technician", self)
        btn2.setFont(font2)
        btn2.setGeometry(50, 175, 220, 50)

        btn3 = QPushButton("Login Customer", self)
        btn3.setFont(font2)
        btn3.setGeometry(50, 250, 220, 50)

        btn4 = QPushButton("Login Technician", self)
        btn4.setFont(font2)
        btn4.setGeometry(50, 325, 220, 50)

        btn5 = QPushButton("Search Availability", self)
        btn5.setFont(font2)
        btn5.setGeometry(50, 400, 220, 50)

        btn6 = QPushButton("Reserve", self)
        btn6.setFont(font2)
        btn6.setGeometry(50, 475, 220, 50)

        btn7 = QPushButton("Upload Availability", self)
        btn7.setFont(font2)
        btn7.setGeometry(350, 100, 220, 50)

        btn8 = QPushButton("Cancel Appointments", self)
        btn8.setFont(font2)
        btn8.setGeometry(350, 175, 220, 50)

        btn9 = QPushButton("Add Quantity", self)
        btn9.setFont(font2)
        btn9.setGeometry(350, 250, 220, 50)

        btn10 = QPushButton("Show Appointments", self)
        btn10.setFont(font2)
        btn10.setGeometry(350, 325, 220, 50)

        btn11 = QPushButton("Logout", self)
        btn11.setFont(font2)
        btn11.setGeometry(350, 400, 220, 50)

        btn12 = QPushButton("Quit", self)
        btn12.setFont(font2)
        btn12.setGeometry(350, 475, 220, 50)
      
        btn1.clicked.connect(self.showDialog_CreateCustomer)            
        btn2.clicked.connect(self.showDialog_CreateTechnician)
        btn3.clicked.connect(self.showDialog_LoginCustomer)
        btn4.clicked.connect(self.showDialog_LoginTechnician)
        btn5.clicked.connect(self.showDialog_SearchAvailability)
        btn6.clicked.connect(self.showDialog_Reserve)
        btn7.clicked.connect(self.showDialog_UploadAvailability)
        btn8.clicked.connect(self.showDialog_Cancel)
        btn9.clicked.connect(self.showDialog_AddQuantity)
        btn10.clicked.connect(self.showDialog_ShowAppointments)
        btn11.clicked.connect(self.showDialog_Logout)
        btn12.clicked.connect(self.showDialog_Quit)
        
        self.setGeometry(550, 200, 650, 600)
        self.setWindowTitle('AC Installation Scheduler')
        self.show()

    # The dialogs for implementing the services
    def showDialog_CreateCustomer(self):
        dialog = InputDialog_CreateAndLogin()
        if dialog.exec():
            username, password = dialog.getInputs()
            result = Scheduler.create_customer([username, password])
            QMessageBox.information(self, 'Message', result)

    def showDialog_CreateTechnician(self):
        dialog = InputDialog_CreateAndLogin()
        if dialog.exec():
            username, password = dialog.getInputs()
            result = Scheduler.create_technician([username, password])
            QMessageBox.information(self, 'Message', result)

    def showDialog_LoginCustomer(self):
        dialog = InputDialog_CreateAndLogin()
        if dialog.exec():
            username, password = dialog.getInputs()
            result = Scheduler.login_customer([username, password])
            QMessageBox.information(self, 'Message', result)

    def showDialog_LoginTechnician(self):
        dialog = InputDialog_CreateAndLogin()
        if dialog.exec():
            username, password = dialog.getInputs()
            result = Scheduler.login_technician([username, password])
            QMessageBox.information(self, 'Message', result)

    def showDialog_SearchAvailability(self):
        if Scheduler.current_customer is None and Scheduler.current_technician is None:
            QMessageBox.information(self, 'Message', "Please login first!")
            return
        date, ok = QInputDialog.getText(self, 'Search Availability', 'Enter date (mm-dd-yyyy)')
        if ok:
            result = Scheduler.search_technician_schedule(date)
            QMessageBox.information(self, 'Message', result)
    
    def showDialog_Reserve(self):
        if Scheduler.current_customer is None:
            QMessageBox.information(self, 'Message', "Please login as a customer!")
            return
        dialog = InputDialog_Reserve()
        if dialog.exec():
            date, ac = dialog.getInputs()
            result = Scheduler.reserve([date, ac])
            QMessageBox.information(self, 'Message', result)

    def showDialog_UploadAvailability(self):
        if Scheduler.current_technician is None:
            QMessageBox.information(self, 'Message', "Please login as a technician!")
            return
        date, ok = QInputDialog.getText(self, 'Upload Availability', 'Enter date (mm-dd-yyyy)')
        if ok:
            result = Scheduler.upload_availability(date)
            QMessageBox.information(self, 'Message', result)

    def showDialog_Cancel(self):
        if Scheduler.current_customer is None and Scheduler.current_technician is None:
            QMessageBox.information(self, 'Message', "Please login first!")
            return
        appid, ok = QInputDialog.getText(self, 'Cancel Appointment', 'Enter ID')
        if ok:
            result = Scheduler.cancel(appid)
            QMessageBox.information(self, 'Message', result)

    def showDialog_AddQuantity(self):
        if Scheduler.current_technician is None:
            QMessageBox.information(self, 'Message', "Please login as a technician!")
            return
        dialog = InputDialog_AddQuantity()
        if dialog.exec():
            ac, num = dialog.getInputs()
            result = Scheduler.add_quantity([ac, num])
            QMessageBox.information(self, 'Message', result)

    def showDialog_ShowAppointments(self):
        if Scheduler.current_customer is None and Scheduler.current_technician is None:
            QMessageBox.information(self, 'Message', "Please login first!")
            return
        result = Scheduler.show_appointments()
        QMessageBox.information(self, 'Message', result)

    def showDialog_Logout(self):
        result = Scheduler.logout()
        QMessageBox.information(self, 'Message', result)

    # Quit the application with the quit button
    def showDialog_Quit(self):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            quit()

    # Close the application with the x button
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()   
        
# The input dialog class for creating users and user login 
class InputDialog_CreateAndLogin(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("User Name", self.first)
        layout.addRow("Password", self.second)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.second.text())

# The input dialog class for reserving appointments
class InputDialog_Reserve(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("Date (mm-dd-yyyy)", self.first)
        layout.addRow("AC Brand", self.second)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.second.text())

# The input dialog class for adding AC quantity
class InputDialog_AddQuantity(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.first = QLineEdit(self)
        self.second = QLineEdit(self)
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)

        layout = QFormLayout(self)
        layout.addRow("AC Brand", self.first)
        layout.addRow("Number", self.second)
        layout.addWidget(buttonBox)

        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    def getInputs(self):
        return (self.first.text(), self.second.text())


if __name__ == "__main__":
    # start the application
    app = QApplication(sys.argv)
    ex = GUIWindow()
    sys.exit(app.exec_())