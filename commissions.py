import sys, os
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QWidget, QMessageBox, QStackedWidget, QHeaderView, QInputDialog, QLineEdit, QCheckBox, QHBoxLayout, QDoubleSpinBox
from PyQt5.QtCore import Qt
from encrypting import decryption, encryption

class Commissions(QDialog):
	def __init__(self):
		super(Commissions, self).__init__()
		loadUi("All_Windows/New_Commissions.ui", self)
		self.current_bank = ""
		self.check_states = []
		self.check_boxes = []
		self.spin_boxes = []
		self.spin_boxes_widgets = []
		self.made_changes = False
		self.checkBox.clicked.connect(self.change_all_states)
		self.deleteButton.clicked.connect(self.delete_from_commissions)
		self.addBankButton.clicked.connect(self.add_bank)
		self.addNewOfferButton.clicked.connect(self.add_new_offer)
		self.saveButton.clicked.connect(self.save_to_file)
		self.loadButton.clicked.connect(self.load_from_file)
		self.BackButton.clicked.connect(self.go_back)
		self.deleteBankButton.clicked.connect(self.delete_bank)
		self.setData()

	def get_vars_from_main_file(self, widget, app):
		self.widget = widget
		self.app = app

	def change_all_states(self):
		if self.checkBox.isChecked():
			for n in range(len(self.check_states)):
				self.check_states[n].setChecked(True)
		else:
			for n in range(len(self.check_states)):
				self.check_states[n].setChecked(False)

	def delete_bank(self):
		banks_name = self.comboBox.currentText()
		box = QMessageBox()
		box.setIcon(QMessageBox.Question)
		box.setWindowTitle('Kalkulator Bankowy')
		box.setText(f"Czy napewno chcesz usunąć bank {banks_name}? Po usunięciu banku dane zostaną nieodwracalnie usunięte")
		box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		buttonY = box.button(QMessageBox.Yes)
		buttonY.setText('Tak')
		buttonN = box.button(QMessageBox.No)
		buttonN.setText('Nie')
		box.exec_()
		if box.clickedButton() == buttonN:
			return
		os.remove(f"MonthsBase/Banks/{banks_name}.txt")
		msg = QMessageBox()
		msg.setText(f"Bank {banks_name} został usunięty")
		x = msg.exec_()
		if self.current_bank == banks_name:
			self.current_bank = ""
			self.tableWidget.setRowCount(0)
		self.setData()

	def get_current_data(self, banks_name):
		try:
			decryption(f'MonthsBase/Banks/{banks_name}.txt')
			with open(f'MonthsBase/Banks/{banks_name}.txt', 'r',encoding='utf-8') as f:
				line = f.readline()
				data = []
				while line != '':
					data.append((line.replace('\n', '')).split("~`"))
					line = f.readline()
			encryption(f'MonthsBase/Banks/{banks_name}.txt')
		except:
			self.current_bank = ""
			return
		return data

	def save_to_file(self):
		box = QMessageBox()
		box.setIcon(QMessageBox.Question)
		box.setWindowTitle('Kalkulator Bankowy')
		box.setText(f"Czy napewno chcesz zapisać wszystkie oferty banku {self.current_bank} wraz z prowizjami do systemu?")
		box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		buttonY = box.button(QMessageBox.Yes)
		buttonY.setText('Tak')
		buttonN = box.button(QMessageBox.No)
		buttonN.setText('Nie')
		box.exec_()
		if box.clickedButton() == buttonN:
			return
		data_to_save = []
		for i in range(self.tableWidget.rowCount()):
			data_to_save.append(self.tableWidget.item(i, 1).text() + "~`" + str(self.spin_boxes[i].value()) + "\n")
		try:
			decryption(f'MonthsBase/Banks/{self.current_bank}.txt')
			with open(f'MonthsBase/Banks/{self.current_bank}.txt', 'w',encoding='utf-8') as f:
				for i in range(len(data_to_save)):
					f.write(data_to_save[i])
			encryption(f'MonthsBase/Banks/{self.current_bank}.txt')
			msg = QMessageBox()
			msg.setText(f"Dane zostały zapisane dla banku: {self.current_bank}")
			x = msg.exec_()
			self.made_changes = False
		except:
			self.current_bank = ""
			return

	def add_data_to_table_widget(self, data):
		self.tableWidget.setRowCount(len(data))
		header = self.tableWidget.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

		self.check_states.clear()
		self.check_boxes.clear()
		self.spin_boxes.clear()
		self.spin_boxes_widgets.clear()

		for n in range(len(data)):
			Widget = QWidget()
			self.CheckBox = QCheckBox()
			self.check_states.append(self.CheckBox)
			Layout = QHBoxLayout(Widget)
			Layout.addWidget(self.CheckBox)
			Layout.setAlignment(Qt.AlignCenter)
			Layout.setContentsMargins(0,0,0,0)
			Widget.setLayout(Layout)
			self.check_boxes.append(Widget)

			New_Widget = QWidget()
			self.DoubleSpinBox = QDoubleSpinBox()
			self.DoubleSpinBox.setValue(float(data[n][1]))
			self.spin_boxes.append(self.DoubleSpinBox)
			Layout = QHBoxLayout(New_Widget)
			Layout.addWidget(self.DoubleSpinBox)
			Layout.setAlignment(Qt.AlignCenter)
			Layout.setContentsMargins(0,0,0,0)
			New_Widget.setLayout(Layout)
			self.spin_boxes_widgets.append(New_Widget)

	def load_from_file(self):
		if self.made_changes:
			box = QMessageBox()
			box.setIcon(QMessageBox.Question)
			box.setWindowTitle('Kalkulator Bankowy')
			box.setText("Pamiętaj, wszystkie niezapisane dane zostaną usunięte po opuszczeniu obecnego widoku. Czy napewno chcesz przejść dalej?")
			box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
			buttonY = box.button(QMessageBox.Yes)
			buttonY.setText('Tak')
			buttonN = box.button(QMessageBox.No)
			buttonN.setText('Nie')
			box.exec_()
			if box.clickedButton() == buttonN:
				return
			else:
				self.made_changes = False
		self.current_bank = self.comboBox.currentText()
		data = self.get_current_data(self.current_bank)
		if self.current_bank == "":
			self.tableWidget.setRowCount(0)
			return
		self.add_data_to_table_widget(data)

		for n in range(len(data)):
			self.tableWidget.setCellWidget(n, 0, self.check_boxes[n])
			self.tableWidget.setItem(n, 1, QTableWidgetItem(data[n][0]))
			self.tableWidget.setCellWidget(n, 2, self.spin_boxes_widgets[n])

	def add_new_offer(self):
		self.made_changes = True
		if self.current_bank == "":
			return
		Widget = QWidget()
		self.CheckBox = QCheckBox()
		self.check_states.append(self.CheckBox)
		Layout = QHBoxLayout(Widget)
		Layout.addWidget(self.CheckBox)
		Layout.setAlignment(Qt.AlignCenter)
		Layout.setContentsMargins(0,0,0,0)
		Widget.setLayout(Layout)
		self.check_boxes.append(Widget)

		New_Widget = QWidget()
		self.DoubleSpinBox = QDoubleSpinBox()
		self.spin_boxes.append(self.DoubleSpinBox)
		Layout = QHBoxLayout(New_Widget)
		Layout.addWidget(self.DoubleSpinBox)
		Layout.setAlignment(Qt.AlignCenter)
		Layout.setContentsMargins(0,0,0,0)
		New_Widget.setLayout(Layout)
		self.spin_boxes_widgets.append(New_Widget)

		self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)

		self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 0, self.check_boxes[-1])
		self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(""))
		self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 2, self.spin_boxes_widgets[-1])

	def add_bank(self):
		items = os.listdir(f"MonthsBase/Banks")
		bank_name, okPressed = QInputDialog.getText(self, "Kalkulator Bankowy", f"Podaj nazwę nowego banku:", QLineEdit.Normal, "")
		if okPressed and bank_name != '' and bank_name not in items:
			try:
				f = open(f'MonthsBase/Banks/{bank_name}.txt','w',encoding='utf-8')
				f.close
				encryption(f'MonthsBase/Banks/{bank_name}.txt')
				self.setData()
				msg = QMessageBox()
				msg.setText(f"Bank o nazwie {bank_name} został utworzony")
				x = msg.exec_()
			except Exception as e:
				msg = QMessageBox()
				msg.setText(f"Bład zapisu banku! Wystąpił błąd:\n{e}")
				msg.setIcon(QMessageBox.Critical)
				x = msg.exec_()
				return
		elif bank_name in items:
			msg = QMessageBox()
			msg.setText("Taki bank już istnieje!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return
		else:
			return

	def delete_from_commissions(self):
		self.made_changes = True
		if self.current_bank == "":
			return
		box = QMessageBox()
		box.setIcon(QMessageBox.Question)
		box.setWindowTitle('Kalkulator Bankowy')
		box.setText("Czy napewno chcesz usunąć zaznaczone oferty banku?")
		box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		buttonY = box.button(QMessageBox.Yes)
		buttonY.setText('Tak')
		buttonN = box.button(QMessageBox.No)
		buttonN.setText('Nie')
		box.exec_()
		if box.clickedButton() == buttonN:
			return
		counter = 0
		current_table_data = [self.tableWidget.item(i,1).text() for i in range(self.tableWidget.rowCount())]
		for n in range(len(self.check_states)):
			if self.check_states[n - counter].isChecked():
				current_table_data.pop(n - counter)
				self.check_states.pop(n - counter)
				self.check_boxes.pop(n - counter)
				self.spin_boxes.pop(n - counter)
				self.spin_boxes_widgets.pop(n - counter)
				self.tableWidget.removeRow(n - counter)
				counter += 1

	def setData(self):
		items = os.listdir(f"MonthsBase/Banks")
		items = [item[:-4] for item in items]
		self.comboBox.clear()
		self.comboBox.addItem("Wybierz z listy...")
		for n in range(len(items)):
			self.comboBox.addItem(f"{items[n]}")

	def go_back(self):
		if self.made_changes:
			box = QMessageBox()
			box.setIcon(QMessageBox.Question)
			box.setWindowTitle('Kalkulator Bankowy')
			box.setText("Pamiętaj, wszystkie niezapisane dane zostaną usunięte po opuszczeniu obecnego widoku. Czy napewno chcesz przejść dalej?")
			box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
			buttonY = box.button(QMessageBox.Yes)
			buttonY.setText('Tak')
			buttonN = box.button(QMessageBox.No)
			buttonN.setText('Nie')
			box.exec_()
			if box.clickedButton() == buttonN:
				return
			else:
				self.made_changes = False
		self.current_bank = ""
		self.tableWidget.setRowCount(0)
		self.setData()
		self.widget.setCurrentIndex(0)


def main():
	if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
		QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
		QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	app = QApplication(sys.argv)
	widget = QtWidgets.QStackedWidget()

	commissions = Commissions() #6

	widget.addWidget(commissions)

	widget.setFixedWidth(800)
	widget.setFixedHeight(550)
	widget.show()

	try:
		sys.exit(app.exec_())
	except:
		print("")

if __name__ == "__main__":
	main()