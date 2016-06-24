# -*- coding: utf-8 -*-
from PySide.QtCore import Signal
from PySide.QtGui import QLineEdit, QPalette, QColor, QFont, QWidget


class LineEditWithDefaultCommunicator(QWidget):
	FocusIn = Signal(object)
	FocusOut = Signal(object)

class lineEditWithDefault(QLineEdit):

	first_time = True
	original_text = None
	original_stylesheet = None
	edition_stylesheet = None

	def __init__(self, parent=None):
		super(lineEditWithDefault, self).__init__(parent)
		self.comm = LineEditWithDefaultCommunicator()

	def focusInEvent(self, event):
		if self.first_time:
			self.original_text = super(lineEditWithDefault, self).text()
			self.clear()
			self.original_stylesheet = self.styleSheet()
			self.setStyleSheet(self.edition_stylesheet)
			self.first_time = False
		self.comm.FocusIn.emit(self)
		super(lineEditWithDefault, self).focusInEvent(event)

	def focusOutEvent (self, event):
		if len(super(lineEditWithDefault, self).text()) == 0:
			self.first_time = True
			self.setStyleSheet(self.original_stylesheet)
			self.setText(self.original_text)
		self.comm.FocusOut.emit(self)
		super(lineEditWithDefault, self).focusOutEvent(event)

	def text(self):
		if self.first_time:
			return ''
		else:
			return super(lineEditWithDefault, self).text()

	def setEditionStyleSheet(self, stylesheet):
		self.edition_stylesheet = stylesheet

	def setDefaultText(self, text):
		self.original_text = text
		if self.first_time:
			super(lineEditWithDefault, self).setText(text)

	def isEmpty(self):
		return self.first_time

class QLineEditPassword(QLineEdit):

	primera_vez = True
	paleta_original = None
	texto_original = None

	def focusInEvent(self, event):
		if self.primera_vez:
			self.texto_original = super(QLineEditPassword, self).text()
			self.setEchoMode(QLineEdit.Password)
			self.clear()
			self.paleta_original = QPalette(self.palette())
			paleta = self.palette()
			paleta.setColor(QPalette.Text, QColor(0, 0, 0))
			self.setPalette(paleta)
			font = QFont("Arial", 14)
			font.setItalic(False)
			font.setPixelSize(14)
			self.setFont(font)
			self.primera_vez = False
		super(QLineEditPassword, self).focusInEvent(event)

	def focusOutEvent(self, event):
		if len(super(QLineEditPassword, self).text()) == 0:
			self.setEchoMode(QLineEdit.Normal)
			self.setPalette(self.paleta_original)
			font = QFont("Arial", 14)
			font.setItalic(True)
			font.setPixelSize(14)
			self.setFont(font)
			self.setText(self.texto_original)
			self.primera_vez = True
		super(QLineEditPassword, self).focusOutEvent(event)

	def text(self):
		if self.primera_vez:
			return ''
		return super(QLineEditPassword, self).text()

class QLineEditUsername(lineEditWithDefault):

	def __init__(self, parent):
		super(QLineEditUsername, self).__init__(parent)

		edition_stylesheet = \
			'font: 14px "Arial"; \
			color: rgb(0, 0, 0);'
		self.setEditionStyleSheet(edition_stylesheet)

class lineEditBuscador(lineEditWithDefault):

	click = Signal()

	def __init__(self, *args):
		super(lineEditBuscador, self).__init__(*args)

	def mousePressEvent(self, event):
		self.click.emit()
		super(lineEditBuscador, self).mousePressEvent(event)
