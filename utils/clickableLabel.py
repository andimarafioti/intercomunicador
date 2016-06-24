# -*- coding: utf-8 -*-
from PySide.QtCore import Signal, Qt
from PySide.QtGui import QLabel, QFontMetrics

from helpers.emit_sentinel import pyside_none_wrap


class ClickableLabel(QLabel):

    labelClicked = Signal(str)
    labelEntered = Signal()
    labelLeft = Signal()

    def __init__(self,  parent=None, text=None, image=None, enabled=True):
        super(ClickableLabel, self).__init__(parent)

        if image:
            self.setPixmap(image)

        self.enabled = enabled

    def setText(self, text):
        super(ClickableLabel,self).setText(text)
        # self.setToolTip(text)

    def mousePressEvent(self, event):
        if self.enabled:
            super(ClickableLabel, self).mousePressEvent(event)
            if event.button() == Qt.LeftButton:
                self.labelClicked.emit(*pyside_none_wrap(self.text()))

    def enterEvent(self, event):
        if self.enabled:
            self.setCursor(Qt.PointingHandCursor)
        self.labelEntered.emit()

    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        self.labelLeft.emit()

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value

class ElidedClickableLabel(ClickableLabel):

    def __init__(self,  parent=None, text=None, image=None):
        super(ElidedClickableLabel, self).__init__(parent, text, image)

        # self.setText('')
        self.texto = text
        self.show_tooltip = True

    def setText(self, text):
        metrics = QFontMetrics(self.font())
        elided  = metrics.elidedText(text, Qt.ElideRight, self.maximumWidth())
        super(ElidedClickableLabel,self).setText(elided)
        self.texto = text
        if self.show_tooltip:
            self.setToolTip(self.texto)

    def showTooltip(self, value):
        self.show_tooltip = value