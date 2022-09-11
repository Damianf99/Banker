import sys, os, shutil
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QWidget, QMessageBox, QStackedWidget, QHeaderView, QInputDialog, QCheckBox, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve
from datetime import date, datetime
from encrypting import encryption
import mysql.connector as mysql
import hashlib

class Start(QDialog):
	def __init__(self):
		super(Start, self).__init__()
		loadUi("All_Windows/Start.ui", self)
		self.current_year = "Aktualny"
		self.addButton.clicked.connect(self.add)
		self.nextButton.clicked.connect(self.next)
		self.quitButton.clicked.connect(self.quit)
		self.provButton.clicked.connect(self.comms)
		self.provButton_2.clicked.connect(self.comms_compar)
		self.archiveButton.clicked.connect(self.archive)
		self.loadArchivedButton.clicked.connect(self.load_archived)
		self.invoicesButton.clicked.connect(self.go_to_invoices)
		self.settingsButton.clicked.connect(self.open_settings)
		self.changeDeviceButton.clicked.connect(self.change_device_name)

	def get_vars_from_main_file(self, mainwindow, new_client, commissions, commission_calculator, invoices, login, widget, app):
		self.mainwindow = mainwindow
		self.new_client = new_client
		self.commissions = commissions
		self.commission_calculator = commission_calculator
		self.invoices = invoices
		self.login = login
		self.widget = widget
		self.app = app

	def go_to_calc(self):
		self.widget.setCurrentIndex(11)

	def open_settings(self):
		width = self.frame.width()
		buttonX = self.settingsButton.pos().x()

		# If minimized
		if width == 0:
			# Expand menu
			newWidth = 211
			newButtonX = 210
		# If maximized
		else:
			# Restore menu
			newWidth = 0
			newButtonX = 0

		# Animate the transition
		self.animation = QPropertyAnimation(self.frame, b"geometry")#Animate minimumWidht
		self.animation.setDuration(250)
		self.animation.setStartValue(QRect(0, 0, width, 551))#Start value is the current menu width
		self.animation.setEndValue(QRect(0, 0, newWidth, 551))#end value is the new menu width
		self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)

		self.buttonAnimation = QPropertyAnimation(self.settingsButton, b"geometry")
		self.buttonAnimation.setDuration(250)
		self.buttonAnimation.setStartValue(QRect(buttonX, 0, 51, 41))
		self.buttonAnimation.setEndValue(QRect(newButtonX, 0, 51, 41))
		self.buttonAnimation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)

		self.animation.start()
		self.buttonAnimation.start()

	def change_device_name(self):
		box = QMessageBox()
		box.setIcon(QMessageBox.Question)
		box.setWindowTitle('Kalkulator Bankowy')
		box.setText(f'Czy napewno chcesz zmienić nazwę urządzenia na {self.deviceEdit.text()}? W przypadku zmiany nazwy urządzenia - po wylogowaniu opcja zalogowania się z tego urządzenia będzie niemożliwa')
		box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		buttonY = box.button(QMessageBox.Yes)
		buttonY.setText('Tak')
		buttonN = box.button(QMessageBox.No)
		buttonN.setText('Nie')
		box.exec_()
		if box.clickedButton() == buttonN:
			return

		device = "some secrete operation"
		#
		#some secrete code
		#

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
		cursor.execute(
                f"UPDATE b2vxjcddrqrhh8c7olds.Accounts SET Device = '{device}' WHERE Login = '{self.login.login}'")
		connection.commit()
		msg = QMessageBox()
		msg.setText(f"Nazwa urządzenia została zmieniona na {self.deviceEdit.text()}")
		x = msg.exec_()
		cursor.close()
		connection.close()

	def add(self):
		self.widget.setCurrentIndex(4)

	def go_to_invoices(self):
		self.invoices.tableWidget.setRowCount(len(self.invoices.invoice_list))
		self.invoices.tableWidget.setColumnCount(8)
		self.invoices.tableWidget.setHorizontalHeaderLabels(['','Nazwisko i Imie','Data wprowadzenia', 'Data sfinalizowania','Kwota Kredytu','Wynagrodzenie','Bank','Prowizje'])
		header = self.invoices.tableWidget.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

		self.invoices.check_states.clear()
		self.invoices.check_boxes.clear()

		items = os.listdir(f"MonthsBase/{self.current_year}")
		counter = 0
		for i in range(len(items)):
			if ".txt" in items[i-counter]:
				items.pop(i-counter)
				counter += 1
		self.invoices.comboBox.clear()
		self.invoices.comboBox.addItem("Wybierz z listy...")
		for n in range(len(items)):
			self.invoices.comboBox.addItem(f"{items[n]}")

		for n in range(len(self.invoices.invoice_list)):
			Widget = QWidget()
			self.CheckBox = QCheckBox()
			self.invoices.check_states.append(self.CheckBox)
			Layout = QHBoxLayout(Widget)
			Layout.addWidget(self.CheckBox)
			Layout.setAlignment(Qt.AlignCenter)
			Layout.setContentsMargins(0,0,0,0)
			Widget.setLayout(Layout)
			self.invoices.check_boxes.append(Widget)

		total_to_pay = 0
		for i in range(len(self.invoices.invoice_list)):
			total_to_pay += float(self.invoices.invoice_list[i][4])
			self.invoices.tableWidget.setCellWidget(i, 0, self.invoices.check_boxes[i])
			self.invoices.tableWidget.setItem(i, 0, QTableWidgetItem(""))
			self.invoices.tableWidget.setItem(i, 1, QTableWidgetItem(str(self.invoices.invoice_list[i][0])))
			self.invoices.tableWidget.setItem(i, 2, QTableWidgetItem(str(self.invoices.invoice_list[i][1])))
			self.invoices.tableWidget.setItem(i, 3, QTableWidgetItem(str(self.invoices.invoice_list[i][2])))
			self.invoices.tableWidget.setItem(i, 4, QTableWidgetItem(str(self.invoices.invoice_list[i][3])))
			self.invoices.tableWidget.setItem(i, 5, QTableWidgetItem(str(self.invoices.invoice_list[i][4])))
			self.invoices.tableWidget.setItem(i, 6, QTableWidgetItem(str(self.invoices.invoice_list[i][5])))
			self.invoices.tableWidget.setItem(i, 7, QTableWidgetItem(str(self.invoices.invoice_list[i][6])))

		if total_to_pay != 0:
			total_to_pay = str(total_to_pay).split(".")
			if len(total_to_pay[1]) < 2:
				total_to_pay[1] += "0"
			if len(total_to_pay[0]) > 3:
				total_to_pay[0] = list(total_to_pay[0])
				total_to_pay[0][-4] += " "
				total_to_pay[0] = "".join(total_to_pay[0])
			if len(total_to_pay[0]) > 7:
				total_to_pay[0] = list(total_to_pay[0])
				total_to_pay[0][-8] += " "
				total_to_pay[0] = "".join(total_to_pay[0])
			total_to_pay = ".".join(total_to_pay)
		self.invoices.label_4.setText(str(total_to_pay))
		self.widget.setCurrentIndex(8)

	def next(self):
		self.widget.setCurrentIndex(1)

	def comms(self):
		box = QMessageBox()
		box.setIcon(QMessageBox.Question)
		box.setWindowTitle('Kalkulator Bankowy')
		box.setText(f'Czy napewno chcesz dokonać zmian w prowizjach?')
		box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		buttonY = box.button(QMessageBox.Yes)
		buttonY.setText('Tak')
		buttonN = box.button(QMessageBox.No)
		buttonN.setText('Nie')
		box.exec_()
		if box.clickedButton() == buttonN:
			return
		self.commissions.setData()
		self.widget.setCurrentIndex(6)

	def comms_compar(self):
		self.commission_calculator.setData()
		self.widget.setCurrentIndex(7)

	def load_archived(self):
		items = list(os.walk("MonthsBase"))[0][1]
		items.remove("Banks")
		item, ok = QInputDialog.getItem(self, "Kalkulator Bankowy", 
		   "Wybierz rok", items, 0, False)
		if ok and item:
			self.current_year = str(item)
			self.yearLabel.setText(f"Rok: {self.current_year}")
			self.mainwindow.yearLabel.setText(f"Rok: {self.current_year}")
			self.new_client.yearLabel.setText(f"Rok: {self.current_year}")
			self.invoices.yearLabel.setText(f"Rok: {self.current_year}")

	def archive(self):
		year = str(int(datetime.today().year) - 1)
		box = QMessageBox()
		box.setIcon(QMessageBox.Question)
		box.setWindowTitle('Kalkulator Bankowy')
		box.setText(f"Czy napewno chcesz zarchiwizować rok {year}? Pamiętaj, archiwizację możesz przeprowadzić tylko raz")
		box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		buttonY = box.button(QMessageBox.Yes)
		buttonY.setText('Tak')
		buttonN = box.button(QMessageBox.No)
		buttonN.setText('Nie')
		box.exec_()
		if box.clickedButton() == buttonN:
			return
		try:
			os.mkdir(f"MonthsBase/{year}")
			source_folder = "MonthsBase/Aktualny"
			destination_folder = f"MonthsBase/{year}"
			for file_name in os.listdir(source_folder):
				source = f"{source_folder}/{file_name}"
				destination = f"{destination_folder}/{file_name}"
				# copy only files
				if os.path.isfile(source):
					shutil.copy(source, destination)
			for file_name in os.listdir(source_folder):
				os.remove(f"{source_folder}/{file_name}")
			for i in range(1,13):
				fp = open(f"{source_folder}/{i}.txt", 'x')
				encryption(f"{source_folder}/{i}.txt")
				fp.close()
			msg = QMessageBox()
			msg.setText(f"Rok {year} został poprawnie zarchiwizowany")
			x = msg.exec_()
			return
		except FileExistsError:
			msg = QMessageBox()
			msg.setText(f"Rok {year} został już wcześniej zarchiwizowany! Aby dokonać w nim zmian - wczytaj ten rok")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return

	def quit(self):
		box = QMessageBox()
		box.setIcon(QMessageBox.Question)
		box.setWindowTitle('Kalkulator Bankowy')
		box.setText(f"Czy napewno chcesz się wylogować?")
		box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		buttonY = box.button(QMessageBox.Yes)
		buttonY.setText('Tak')
		buttonN = box.button(QMessageBox.No)
		buttonN.setText('Nie')
		box.exec_()
		if box.clickedButton() == buttonN:
			return
		self.widget.setCurrentIndex(10)

def main():
	if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
		QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
		QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	app = QApplication(sys.argv)
	widget = QtWidgets.QStackedWidget()

	start = Start() #0

	widget.addWidget(start)

	widget.setFixedWidth(800)
	widget.setFixedHeight(550)
	widget.show()

	try:
		sys.exit(app.exec_())
	except:
		print("")

if __name__ == "__main__":
	main()

