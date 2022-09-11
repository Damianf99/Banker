import sys, os
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox, QStackedWidget, QInputDialog, QLineEdit
from PyQt5.QtCore import Qt


class Invoices(QDialog):
	def __init__(self):
		super(Invoices, self).__init__()
		loadUi("All_Windows/Invoices.ui", self)
		self.check_states = []
		self.check_boxes = []
		self.invoice_list = []
		self.BackButton.clicked.connect(self.go_back)
		self.checkBox.clicked.connect(self.change_all_states)
		self.goToInvoiceDataButton.clicked.connect(self.go_to_invoice_data)
		self.openInvoiceButton.clicked.connect(self.open_invoice)
		self.deleteButton.clicked.connect(self.delete_from_invoice)
		self.createInvoiceButton.clicked.connect(self.create_invoice)
		self.deleteInvoiceButton.clicked.connect(self.delete_invoice)

	def get_vars_from_main_file(self, start, invoices_data, widget, app):
		self.start = start
		self.invoices_data = invoices_data
		self.widget = widget
		self.app = app

	def change_all_states(self):
		if self.checkBox.isChecked():
			for n in range(len(self.check_states)):
				self.check_states[n].setChecked(True)
		else:
			for n in range(len(self.check_states)):
				self.check_states[n].setChecked(False)

	def delete_invoice(self):
		invoice_name = self.comboBox.currentText()
		box = QMessageBox()
		box.setIcon(QMessageBox.Question)
		box.setWindowTitle('Kalkulator Bankowy')
		box.setText(f"Czy jesteś pewien, że chcesz usunąć fakturę o nazwie: {invoice_name}?")
		box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		buttonY = box.button(QMessageBox.Yes)
		buttonY.setText('Tak')
		buttonN = box.button(QMessageBox.No)
		buttonN.setText('Nie')
		box.exec_()
		if box.clickedButton() == buttonN:
			return
		try:
			os.remove(f"MonthsBase/{self.start.current_year}/{invoice_name}")
			items = os.listdir(f"MonthsBase/{self.start.current_year}")
			counter = 0
			for i in range(len(items)):
				if ".txt" in items[i-counter]:
					items.pop(i-counter)
					counter += 1
			self.comboBox.clear()
			self.comboBox.addItem("Wybierz z listy...")
			for n in range(len(items)):
				self.comboBox.addItem(f"{items[n]}")
			msg = QMessageBox()
			msg.setText(f"Faktura o naziwe: {invoice_name} została usunięta")
			x = msg.exec_()
		except:
			msg = QMessageBox()
			msg.setText(f"Błąd usuwania faktury! Faktura o nazwie {invoice_name} nie została usunięta")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return

	def delete_from_invoice(self):
		box = QMessageBox()
		box.setIcon(QMessageBox.Question)
		box.setWindowTitle('Kalkulator Bankowy')
		box.setText("Czy napewno chcesz usunąć wybranych klientów z aktualnej faktury?")
		box.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
		buttonY = box.button(QMessageBox.Yes)
		buttonY.setText('Tak')
		buttonN = box.button(QMessageBox.No)
		buttonN.setText('Nie')
		box.exec_()
		if box.clickedButton() == buttonN:
			return
		counter = 0
		for n in range(len(self.check_states)):
			if self.check_states[n].isChecked():
				self.invoice_list.pop(n - counter)
				counter += 1
		self.start.go_to_invoices()
		msg = QMessageBox()
		msg.setText(f"Wybrani klienci zostali usunięci")
		x = msg.exec_()
		return

	def open_invoice(self):
		invoice_name = self.comboBox.currentText()
		if invoice_name != "Wybierz z listy...":
			current_location = str(os.getcwdb()).replace('\\\\','/')[2:-1]
			os.system(f"{current_location}/MonthsBase/{self.start.current_year}/{invoice_name}")

	def create_invoice(self):
		if len(self.invoice_list) == 0:
			msg = QMessageBox()
			msg.setText("Faktura nie zostanie utworzona jeżeli nie dodano żadnych klientów!")
			msg.setIcon(QMessageBox.Critical)
			x = msg.exec_()
			return
		file_name, okPressed = QInputDialog.getText(self, "Kalkulator Bankowy", "Podaj nazwę faktury", QLineEdit.Normal, "")
		if okPressed == False or file_name == '':
			return
		file_name = str(file_name).replace(" ", "_")
		self.invoices_data.set_values()
		style = """
		<style type="text/css">
			body,div,table,thead,tbody,tfoot,tr,th,td,p { font-family:"Arial"; font-size:x-small }
			a.comment-indicator:hover + comment { background:#ffd; position:absolute; display:block; border:1px solid black; padding:0.5em;  } 
			a.comment-indicator { background:red; display:inline-block; border:1px solid black; width:0.5em; height:0.5em;  } 
			comment { display:none;  } 
		</style>
		"""
		self.printhtmltopdf(
    f"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">

<html>
<head>
	
	<meta http-equiv="content-type" content="text/html; charset=utf-8"/>
	<title></title>
	
	{style}
	
</head>

<body>
<table cellspacing="0" border="0">
	<colgroup width="28"></colgroup>
	<colgroup width="207"></colgroup>
	<colgroup width="49"></colgroup>
	<colgroup width="41"></colgroup>
	<colgroup width="71"></colgroup>
	<colgroup width="73"></colgroup>
	<colgroup width="42"></colgroup>
	<colgroup width="67"></colgroup>
	<colgroup width="55"></colgroup>
	<colgroup width="76"></colgroup>
	<colgroup width="70"></colgroup>
	<tr>
		<td colspan=5 height="20" align="right" valign=bottom bgcolor="#FFFFFF"><b><font size=3>Faktura Nr</font></b></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" colspan=4 align="center" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;@"><b><font size=3>{self.invoices_data.invoiceNumberEdit.text()}<br></font></b></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td style="border-bottom: 2px solid #000000" height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td style="border-bottom: 2px solid #000000" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td style="border-bottom: 2px solid #000000" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td style="border-bottom: 2px solid #000000" colspan=3 align="center" valign=bottom bgcolor="#FFFFFF"><b>Oryginał / Kopia</b></td>
		<td style="border-bottom: 2px solid #000000" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td style="border-bottom: 2px solid #000000" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td style="border-bottom: 2px solid #000000" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td style="border-bottom: 2px solid #000000" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td style="border-top: 2px solid #000000" colspan=5 height="16" align="center" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;@">Sprzedawca:</td>
		<td style="border-top: 2px solid #000000; border-right: 1px solid #000000" colspan=5 align="center" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;@">Nabywca:</td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td colspan=5 rowspan=6 align="left" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;@" style="border: 1px solid #000000; text-align: center; vertical-align: middle;"><br>
			{self.invoices_data.seller}
		</td>
		<td colspan=5 rowspan=6 align="left" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;@" style="border: 1px solid #000000; text-align: center; vertical-align: middle;"><br>
			{self.invoices_data.buyer}
		</td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td style="border-top: 2px solid #000000" colspan=2 height="16" align="right" valign=bottom bgcolor="#FFFFFF">Data sprzedaży:  </td>
		<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" colspan=4 align="left" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;@">{self.invoices_data.sales_date}<br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td colspan=2 height="16" align="right" valign=bottom bgcolor="#FFFFFF">Data wystawienia:  </td>
		<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" colspan=4 align="left" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;@">{self.invoices_data.issuance_date}<br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td colspan=2 height="16" align="right" valign=bottom bgcolor="#FFFFFF">Termin płatności:  </td>
		<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" colspan=4 align="left" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;@">{self.invoices_data.payment_due_by}<br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td colspan=2 height="16" align="right" valign=bottom bgcolor="#FFFFFF">Forma płatności:  </td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" colspan=6 align="left" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;@"><font size=1>{self.invoices_data.paymentFormEdit.text()}</font></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="right" valign=bottom bgcolor="#FFFFFF">Uwagi:  </td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" colspan=6 align="left" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;@"><font size=1>{self.invoices_data.notesEdit.text()}</font></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td style="border-top: 1px solid #000000; border-bottom: 2px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" height="29" align="center" valign=bottom bgcolor="#FFFFFF"><font size=1>L.p.</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 2px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF"><font size=1>Nazwa towaru</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 2px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF"><font size=1>PKWiU</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 2px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF"><font size=1>J.m</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 2px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF"><font size=1>Stawka VAT</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 2px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF"><font size=1>Cena jedn. netto</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 2px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF"><font size=1>Ilość</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 2px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF"><font size=1>Wartość netto</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 2px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF"><font size=1>Podatek VAT</font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 2px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF"><font size=1>Wartość brutto</font></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	{self.invoices_data.new_services}
	<!-- <tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><font size=1><br></font></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><font size=1><br></font></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><font size=1><br></font></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" colspan=2 align="center" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;#,##0.00"><br></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">0.00</td>
		<td style="border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="left" valign=middle bgcolor="#FFFFFF" sdnum="1033;0;#,##0.00"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr> -->
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF">w tym</td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;0%"><br></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF" sdval="0.23" sdnum="1033;0;0%">23%</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.invoices_data.total_payment[0][0]}</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.invoices_data.total_payment[0][1]}</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.invoices_data.total_payment[0][2]}</td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;0%"><br></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF" sdval="0.07" sdnum="1033;0;0%">8%</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.invoices_data.total_payment[1][0]}</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.invoices_data.total_payment[1][1]}</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.invoices_data.total_payment[1][2]}</td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;0%"><br></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF" sdval="0.03" sdnum="1033;0;0%">5%</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.invoices_data.total_payment[2][0]}</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.invoices_data.total_payment[2][1]}</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.invoices_data.total_payment[2][2]}</td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;0%"><br></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;0%">0%</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">0.00</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">0.00</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">0.00</td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF">zw</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.invoices_data.total_payment[3][0]}</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.invoices_data.total_payment[3][1]}</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">{self.invoices_data.total_payment[3][2]}</td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td style="border-top: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF">np</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">0.00</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">0.00</td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" align="right" valign=bottom bgcolor="#FFFFFF" sdval="0" sdnum="1033;0;#,##0.00">0.00</td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="right" valign=bottom bgcolor="#FFFFFF">Do zapłaty: </td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000" colspan=4 align="right" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;#,##0.00"><b>{self.invoices_data.total_to_pay_for_all}</b></td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-right: 1px solid #000000" align="center" valign=bottom bgcolor="#FFFFFF"><b>PLN</b></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="right" valign=bottom bgcolor="#FFFFFF">Słownie: </td>
		<td style="border-top: 1px solid #000000; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px solid #000000" colspan=8 align="left" valign=bottom bgcolor="#FFFFFF" sdnum="1033;0;@">{self.invoices_data.price_in_words}</td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="17" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="2" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td colspan=11>
			&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>UWAGI</b>: {self.invoices_data.notesBottomEdit.text()}
		</td>
	</tr>
	<!-- <tr>
		<td height="17" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><font size=1>UWAGI: usługi posrednictwa finansowego zwolnione z podatku vat na podstawie art. 43 ust 1 ustawy o podatku od towarów i usług</font></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr> -->
	<tr>
		<td colspan=5 height="50" align="left" valign=bottom bgcolor="#FFFFFF">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...............................................................</td>
		<td colspan=3 rowspan=5 align="left" valign=bottom bgcolor="#FFFFFF"><br>
		</td>
		<td align="left" valign=bottom bgcolor="#FFFFFF">...............................................................</td>
		<td colspan=6 rowspan=5 align="left" valign=bottom bgcolor="#FFFFFF"><br>
		</td>
		</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="center" valign=bottom bgcolor="#FFFFFF">Podpis osoby upoważnionej do odbioru faktury VAT<br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="center" valign=bottom bgcolor="#FFFFFF">Podpis osoby upoważnionej do wystawienia faktury VAT<br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		</tr>
	<tr>
		<td height="31" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		</tr>
	<!-- <tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><b><font size=1>Objaśnienia: </font></b></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><font size=1>W polu &quot;Stawka VAT&quot; należy wpisać: 22, 7, 3, 0 zw (zwolniona) lub np. (niepodlegająca opodatkowaniu)</font></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="28" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td colspan=9 align="left" valign=bottom bgcolor="#FFFFFF"><font size=1>Pola &quot;wartość netto&quot;, &quot;podatek VAT&quot; oraz &quot;wartość brutto&quot; wypełaniają się automatycznie po wstawieniu wartości w polach: <br>&quot;stawka VAT&quot;, &quot;cena jednostkowa netto&quot; oraz &quot;ilość&quot;</font></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="16" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="15" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr>
	<tr>
		<td height="15" align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
		<td align="left" valign=bottom bgcolor="#FFFFFF"><br></td>
	</tr> -->
</table>
<!-- ************************************************************************** -->
</body>

</html>
""",
    f"MonthsBase/{self.start.current_year}/{file_name}.pdf",
)

	def printhtmltopdf(self, html_in, pdf_filename):
		page = QtWebEngineWidgets.QWebEnginePage()

		def handle_pdfPrintingFinished(*args):
			if args[1] == False:
				msg = QMessageBox()
				msg.setText("Faktura nie została utworzona!")
				msg.setIcon(QMessageBox.Critical)
				x = msg.exec_()
				return
			else:
				items = os.listdir(f"MonthsBase/{self.start.current_year}")
				counter = 0
				for i in range(len(items)):
					if ".txt" in items[i-counter]:
						items.pop(i-counter)
						counter += 1
				self.comboBox.clear()
				self.comboBox.addItem("Wybierz z listy...")
				for n in range(len(items)):
					self.comboBox.addItem(f"{items[n]}")
				msg = QMessageBox()
				msg.setText("Faktura została utworzona")
				x = msg.exec_()
				return

		def handle_loadFinished(finished):
			page.printToPdf(pdf_filename)

		page.pdfPrintingFinished.connect(handle_pdfPrintingFinished)
		page.loadFinished.connect(handle_loadFinished)
		page.setZoomFactor(1)
		page.setHtml(html_in)

	def go_to_invoice_data(self):
		self.widget.setCurrentIndex(9)

	def go_back(self):
		self.checkBox.setChecked(False)
		self.tableWidget.setRowCount(0)
		self.widget.setCurrentIndex(0)


def main():
	if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
		QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
	if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
		QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

	app = QApplication(sys.argv)
	widget = QtWidgets.QStackedWidget()

	invoices = Invoices() #8

	widget.addWidget(invoices)

	widget.setFixedWidth(800)
	widget.setFixedHeight(550)
	widget.show()

	try:
		sys.exit(app.exec_())
	except:
		print("")

if __name__ == "__main__":
	main()