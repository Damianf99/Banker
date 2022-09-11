import sys
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QMessageBox, QStackedWidget, QHeaderView, QCheckBox, QHBoxLayout, QDoubleSpinBox
from encrypting import decryption, encryption

class MainWindow(QDialog):
	def __init__(self):
		super(MainWindow, self).__init__()
		loadUi("All_Windows/Main.ui", self)
		self.month = 0
		self.pushButton.clicked.connect(self.January)
		self.pushButton_2.clicked.connect(self.February)
		self.pushButton_3.clicked.connect(self.March)
		self.pushButton_4.clicked.connect(self.April)
		self.pushButton_5.clicked.connect(self.May)
		self.pushButton_6.clicked.connect(self.June)
		self.pushButton_7.clicked.connect(self.July)
		self.pushButton_8.clicked.connect(self.August)
		self.pushButton_9.clicked.connect(self.September)
		self.pushButton_10.clicked.connect(self.October)
		self.pushButton_11.clicked.connect(self.November)
		self.pushButton_12.clicked.connect(self.December)
		self.BackButton.clicked.connect(self.back)
		self.pushButton_14.clicked.connect(self.all_data)
		self.pushButton_15.clicked.connect(self.to_customers)

	def get_vars_from_main_file(self, calculator, customers, widget, app):
		self.customers = customers
		self.calculator = calculator
		self.widget = widget
		self.app = app

	def January(self, finalization = False):
		self.calculator.full_base = 0
		self.calculator.label_4.setText("Styczeń")
		self.month = 1
		if finalization:
			self.widget.setCurrentIndex(2)
			self.calculator.setData()
			return
		self.calculator.next()

	def February(self, finalization = False):
		self.calculator.full_base = 0
		self.calculator.label_4.setText("Luty")
		self.month = 2
		if finalization:
			self.widget.setCurrentIndex(2)
			self.calculator.setData()
			return
		self.calculator.next()

	def March(self, finalization = False):
		self.calculator.full_base = 0
		self.calculator.label_4.setText("Marzec")
		self.month = 3
		if finalization:
			self.widget.setCurrentIndex(2)
			self.calculator.setData()
			return
		self.calculator.next()

	def April(self, finalization = False):
		self.calculator.full_base = 0
		self.calculator.label_4.setText("Kwiecień")
		self.month = 4
		if finalization:
			self.widget.setCurrentIndex(2)
			self.calculator.setData()
			return
		self.calculator.next()

	def May(self, finalization = False):
		self.calculator.full_base = 0
		self.calculator.label_4.setText("Maj")
		self.month = 5
		if finalization:
			self.widget.setCurrentIndex(2)
			self.calculator.setData()
			return
		self.calculator.next()

	def June(self, finalization = False):
		self.calculator.full_base = 0
		self.calculator.label_4.setText("Czerwiec")
		self.month = 6
		if finalization:
			self.widget.setCurrentIndex(2)
			self.calculator.setData()
			return
		self.calculator.next()

	def July(self, finalization = False):
		self.calculator.full_base = 0
		self.calculator.label_4.setText("Lipiec")
		self.month = 7
		if finalization:
			self.widget.setCurrentIndex(2)
			self.calculator.setData()
			return
		self.calculator.next()

	def August(self, finalization = False):
		self.calculator.full_base = 0
		self.calculator.label_4.setText("Sierpień")
		self.month = 8
		if finalization:
			self.widget.setCurrentIndex(2)
			self.calculator.setData()
			return
		self.calculator.next()

	def September(self, finalization = False):
		self.calculator.full_base = 0
		self.calculator.label_4.setText("Wrzesień")
		self.month = 9
		if finalization:
			self.widget.setCurrentIndex(2)
			self.calculator.setData()
			return
		self.calculator.next()

	def October(self, finalization = False):
		self.calculator.full_base = 0
		self.calculator.label_4.setText("Październik")
		self.month = 10
		if finalization:
			self.widget.setCurrentIndex(2)
			self.calculator.setData()
			return
		self.calculator.next()

	def November(self, finalization = False):
		self.calculator.full_base = 0
		self.calculator.label_4.setText("Listopad")
		self.month = 11
		if finalization:
			self.widget.setCurrentIndex(2)
			self.calculator.setData()
			return
		self.calculator.next()

	def December(self, finalization = False):
		self.calculator.full_base = 0
		self.calculator.label_4.setText("Grudzień")
		self.month = 12
		if finalization:
			self.widget.setCurrentIndex(2)
			self.calculator.setData()
			return
		self.calculator.next()

	def all_data(self):
		self.calculator.full_base = 1
		self.calculator.next()

	def back(self):
		self.widget.setCurrentIndex(0)

	def to_customers(self, month_data = None, indexes = None):
		self.customers.tableWidget.setRowCount(0)

		if month_data == None or month_data == False:
			decryption('MonthsBase/Customers.txt')
			f = open('MonthsBase/Customers.txt','r',encoding='utf-8')
			line = f.readline()
			month_data = []
			while line != '':
				month_data.append((line.replace('\n', '')).split(","))
				line = f.readline()
			f.close()
			encryption('MonthsBase/Customers.txt')
			self.customers.searched = False
		else:
			for n in range(len(month_data)):
				month_data[n] = month_data[n].split(",")

		if len(month_data) == 0:
			msg = QMessageBox()
			msg.setText("Baza danych jest pusta!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return

		self.customers.comboBox.clear()
		self.customers.comboBox.addItem("Wybierz z listy...")
		self.customers.comboBox_2.clear()
		self.customers.comboBox_2.addItem("Wybierz z listy...")
		self.customers.comboBox_3.clear()
		self.customers.comboBox_3.addItem("Wybierz z listy...")
		for n in range(len(month_data)):
			self.customers.comboBox.addItem(f"{month_data[n][0]} ({month_data[n][1]})")
			self.customers.comboBox_2.addItem(f"{month_data[n][0]} ({month_data[n][1]})")
			self.customers.comboBox_3.addItem(f"{month_data[n][0]} ({month_data[n][1]})")
		
		self.customers.tableWidget.setRowCount(len(month_data))
		self.customers.tableWidget.setColumnCount(len(month_data[0]))
		header = self.customers.tableWidget.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

		for i in range(len(month_data)):
				self.customers.tableWidget.setItem(i, 0, QTableWidgetItem(str(month_data[i][0])))
				self.customers.tableWidget.setItem(i, 1, QTableWidgetItem(str(month_data[i][1])))
				self.customers.tableWidget.setItem(i, 2, QTableWidgetItem(str(month_data[i][2])))

		self.widget.setCurrentIndex(5)

def main():
	if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
		QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
		QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	app = QApplication(sys.argv)
	widget = QtWidgets.QStackedWidget()

	mainwindow = MainWindow() #1

	widget.addWidget(mainwindow)

	widget.setFixedWidth(800)
	widget.setFixedHeight(550)
	widget.show()

	try:
		sys.exit(app.exec_())
	except:
		print("")

if __name__ == "__main__":
	main()



