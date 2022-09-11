from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
import mysql.connector as mysql
import hashlib
import socket

class Login(QDialog):
	def __init__(self):
		super(Login, self).__init__()
		loadUi("All_Windows/Login.ui", self)
		self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
		self.loginButton.clicked.connect(self.log_in)
		self.quitButton.clicked.connect(self.quit)
		self.createAccButton.clicked.connect(self.create_account)

	def get_vars_from_main_file(self, start, widget, app):
		self.start = start
		self.widget = widget
		self.app = app

	def quit(self):
		box = QMessageBox()
		box.setIcon(QMessageBox.Question)
		box.setWindowTitle('Kalkulator Bankowy')
		box.setText('Czy napewno zamknąć system?')
		box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		buttonY = box.button(QMessageBox.Yes)
		buttonY.setText('Tak')
		buttonN = box.button(QMessageBox.No)
		buttonN.setText('Nie')
		box.exec_()
		if box.clickedButton() == buttonY:
			self.app.quit()
		elif box.clickedButton() == buttonN:
			return

	def log_in(self):
		try:
			connection = mysql.connect(user="uh9z6vkfosot2wi3", password=some_secrete_password,
							   host='b2vxjcddrqrhh8c7olds-mysql.services.clever-cloud.com')
			cursor = connection.cursor()
		except:
			msg = QMessageBox()
			msg.setText(f"Błąd łączenia z bazą danych, spróbuj ponownie")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return
		login = self.loginEdit.text()
		password = self.passwordEdit.text()

		password = some_secrete_operation
		#
		#some secrete code
		#

		device = some_secete_operation
		#
		#some secrete code
		#

		cursor.execute(f'Select Password, Device from b2vxjcddrqrhh8c7olds.Accounts where login = "{login}"')
		login_data = [n for n in cursor]
		if len(login_data) == 0 or login_data[0][0] != password:
			msg = QMessageBox()
			msg.setText(f"Błędne dane logowania")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			cursor.close()
			connection.close()
			return
		if login_data[0][1] != device:
			msg = QMessageBox()
			msg.setText(f"To urządzenie nie ma zezwolenia na logowanie na to konto!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			cursor.close()
			connection.close()
			return
		msg = QMessageBox()
		msg.setText("     Zalogowano     ")
		x = msg.exec_()
		cursor.close()
		connection.close()
		self.widget.setCurrentIndex(0)
		self.loginEdit.setText("")
		self.passwordEdit.setText("")
		self.start.deviceEdit.setText(socket.gethostname())
		self.login = login

	def create_account(self):
		self.loginEdit.setText("")
		self.passwordEdit.setText("")
		self.widget.setCurrentIndex(11)


def main():
	if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
		QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
		QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	app = QApplication(sys.argv)
	widget = QtWidgets.QStackedWidget()

	login = Login() #10

	widget.addWidget(login)

	widget.setFixedWidth(800)
	widget.setFixedHeight(550)
	widget.show()

	try:
		sys.exit(app.exec_())
	except:
		print("")

if __name__ == "__main__":
	main()

