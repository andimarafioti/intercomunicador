from PySide.QtCore import Qt
from PySide.QtSql import QSqlQueryModel, QSqlQuery, QSqlDatabase

from gui.utils.widgetListModelCommunicator import WidgetListModelCommunicator
from helpers.emit_sentinel import pyside_none_wrap, pyside_none_deco
from helpers.observer import Subject
from helpers.worker.worker import Worker

__author__ = 'Dev6'


class WidgetListModel(QSqlQueryModel):
    EVENT_LOADING = 0
    EVENT_DONE_LOADING = 1
    ROWCOUNT_CHANGED = 2

    def __init__(self, parent):
        super(WidgetListModel, self).__init__(parent)

        self.subject = Subject(self)
        self.view = parent

        self.rowsInserted.connect(self.onRowsInserted)
        self.rowsRemoved.connect(self.onRowsRemoved)

        self.communicator = WidgetListModelCommunicator()
        self.communicator.ExecuteQueryFinish.connect(self._executeQueryFinish)

    def updateQuery(self, query_string, params):
        qt_query = QSqlQuery(QSqlDatabase.database("dbsongs"))
        qt_query.prepare(query_string)
        for index, param in enumerate(params):
            qt_query.bindValue(index, param)

        self.subject.notify(self.EVENT_LOADING)

        Worker.call(self._executeQuery).withArgs(qt_query).asDaemon.start()

    def onRowsInserted(self, first, last):
        self.subject.notify(self.ROWCOUNT_CHANGED, self.rowCount())

    def onRowsRemoved(self, first, last):
        self.subject.notify(self.ROWCOUNT_CHANGED, self.rowCount())

    def _executeQuery(self, qt_query):
        qt_query.exec_()
        self.communicator.ExecuteQueryFinish.emit(*pyside_none_wrap(qt_query))

    @pyside_none_deco
    def _executeQueryFinish(self, qt_query):
        self.setQuery(qt_query)
        while self.canFetchMore():
            self.fetchMore()

        self.subject.notify(self.EVENT_DONE_LOADING)

    def data(self, index, role=Qt.DisplayRole):
        if not self.view.indexWidget(index):
            self.view.setIndexWidget(index, self.view.getNewWidget(index))

        if role == Qt.SizeHintRole:
            return self.view.indexWidget(index).sizeHint()

        return None

    def getRealData(self, row, column):
        return super(WidgetListModel, self).data(self.createIndex(row, column), Qt.DisplayRole)

        # class MyListModel(QSqlQueryModel):
        #
        # 	EVENT_LOADING       = 0
        # 	EVENT_DONE_LOADING  = 1
        # 	ROWCOUNT_CHANGED    = 2
        #
        # 	def __init__(self, parent):
        # 		super(ItemListModel, self).__init__(parent)
        #
        # 		self.subject = Subject(self)
        # 		self.view = parent
        #
        # 		self.rowsInserted.connect(self.onRowsInserted)
        # 		self.rowsRemoved.connect(self.onRowsRemoved)
        #
        # 		#self.communicator = ItemListModelCommunicator()
        # 		#self.communicator.ExecuteQueryFinish.connect(self._executeQueryFinish)
        #
        # 	def updateQuery(self, query_string, params):
        # 		qt_query = QSqlQuery(QSqlDatabase.database("dbsongs"))
        # 		qt_query.prepare(query_string)
        # 		for index, param in enumerate(params):
        # 			qt_query.bindValue(index, param)
        #
        # 		self.subject.notify(self.EVENT_LOADING)
        #
        # 		t = threading.Thread(target=self._executeQuery, args=[qt_query])
        # 		t.daemon = True
        # 		t.start()
        #
        # 	def onRowsInserted(self, first, last):
        # 		self.subject.notify(self.ROWCOUNT_CHANGED, self.rowCount())
        #
        # 	def onRowsRemoved(self, first, last):
        # 		self.subject.notify(self.ROWCOUNT_CHANGED, self.rowCount())
        #
        # 	def _executeQuery(self, qt_query):
        # 		qt_query.exec_()
        # 		self.communicator.ExecuteQueryFinish.emit(*pyside_none_wrap(qt_query))
        #
        # 	@pyside_none_deco
        # 	def _executeQueryFinish(self, qt_query):
        # 		self.endInsertRows()
        # 		self.setQuery(qt_query)
        # 		while self.canFetchMore():
        # 			self.fetchMore()
        #
        # 		self.subject.notify(self.EVENT_DONE_LOADING)
        #
        # 	def data(self, index, role=Qt.DisplayRole):
        # 		if self.view.indexWidget(index) is None:
        # 			self.view.setIndexWidget(index, self.view.getNewWidget(index))
        #
        # 		if role == Qt.SizeHintRole:
        # 			return self.view.indexWidget(index).sizeHint()
        #
        # 		return None
        #
        # 	def getRealData(self, row, column):
        # 		return super(ItemListModel, self).data(self.createIndex(row, column), Qt.DisplayRole)