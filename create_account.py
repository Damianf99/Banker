from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox
import mysql.connector as mysql
import hashlib
import socket


class CreateAccount(QDialog):
	def __init__(self):
		super(CreateAccount, self).__init__()
		loadUi("All_Windows/Create_Account.ui", self)
		self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
		self.repeatPassEdit.setEchoMode(QtWidgets.QLineEdit.Password)
		self.createAccButton.clicked.connect(self.create_account)
		self.BackButton.clicked.connect(self.go_back)

	def get_vars_from_main_file(self, widget, app):
		self.widget = widget
		self.app = app

	def create_account(self):
		try:
			connection = mysql.connect(user="uh9z6vkfosot2wi3", password=some_secrete_password,
							   host='b2vxjcddrqrhh8c7olds-mysql.services.clever-cloud.com')
			cursor = connection.cursor()
		except:
			msg = QMessageBox()
			msg.setText(f"Błąd logowania do bazy danych, spróbuj ponownie")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			cursor.close()
			connection.close()
			return
		cursor.execute('Select Login from b2vxjcddrqrhh8c7olds.Accounts')
		logins = [n[0] for n in cursor]
		if len(self.loginEdit.text()) < 4:
			msg = QMessageBox()
			msg.setText(f"Login jest zbyt krótki! Podaj inny login")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			cursor.close()
			connection.close()
			return
		if self.loginEdit.text() in logins:
			msg = QMessageBox()
			msg.setText(f"Taki login już istnieje! Podaj inny login")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			cursor.close()
			connection.close()
			return
		if self.passwordEdit.text() != self.repeatPassEdit.text():
			msg = QMessageBox()
			msg.setText(f"Hasło nie zgadza się z powtórzonym hasłem")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			cursor.close()
			connection.close()
			return
		if len(self.passwordEdit.text()) < 4:
			msg = QMessageBox()
			msg.setText(f"Podane hasło jest zbyt krótkie!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			cursor.close()
			connection.close()
			return
		license_hash = "some_secrete_code"
		#
		#
		# some secrete code
		#
		if license_hash != self.licenseEdit.text():
			msg = QMessageBox()
			msg.setText(f"Numer licencji nie jest zgodny dla zakładanego konta")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			cursor.close()
			connection.close()
			return

		password = bytes(self.passwordEdit.text(), encoding='utf-8')
		code = some_secrete_code
		code.update(password)
		password = str(code.hexdigest())

		device = bytes(socket.gethostname(), encoding='utf-8')
		code = some_secrete_code
		code.update(device)
		device = str(code.hexdigest())

		cursor.execute(
                f"INSERT INTO b2vxjcddrqrhh8c7olds.Accounts (Login, Password, Device) VALUES ('{self.loginEdit.text()}', '{password}', '{device}');")
		connection.commit()

		msg = QMessageBox()
		msg.setText(f"Twoje konto zostało założone dla loginu: {self.loginEdit.text()}.\n\nWraz z założeniem konta w ramach bezpieczeństwa powiązane zostało to konto z urządzeniem, na którym zostało utworzone ({socket.gethostname()})\n\nW przypadku zmiany urządzenia - należy wejść w ustawienia i ręcznie nadać nową nazwę urządzenia")
		x = msg.exec_()
		cursor.close()
		connection.close()

	def go_back(self):
		self.loginEdit.setText("")
		self.passwordEdit.setText("")
		self.repeatPassEdit.setText("")
		self.licenseEdit.setText("")
		self.widget.setCurrentIndex(10)


def main():
	if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
		QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
		QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	app = QApplication(sys.argv)
	widget = QtWidgets.QStackedWidget()

	create_account = CreateAccount() #11

	widget.addWidget(create_account)

	widget.setFixedWidth(800)
	widget.setFixedHeight(550)
	widget.show()

	try:
		sys.exit(app.exec_())
	except:
		print("")

if __name__ == "__main__":
	main()




