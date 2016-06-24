import gc
from helpers.worker.worker import Worker

__author__ = 'Dev6'


class GCUtils:
	def __init__(self):
		pass

	_destroyedObjects = []
	_deferredCollector = Worker.call(gc.collect)
	CAPTURED_STATES = []
	REPORT_PATH = './GCReport.txt'
	QT_DESTRUCTION_EVENTS_PATH = './GCDestructionReport.txt'

	@staticmethod
	def collectAfter(seconds):
		GCUtils._deferredCollector.after(seconds).start()

	@staticmethod
	def getInstancesOfClass(aClass):
		return filter(lambda obj: isinstance(obj, aClass), gc.get_objects())

	@staticmethod
	def getLiveObjectClassNames():
		return set(map(lambda obj: type(obj).__name__, gc.get_objects()))

	@staticmethod
	def getReferentsOf(obj):
		return gc.get_referents(obj)

	@staticmethod
	def getReferrersOf(obj):
		return gc.get_referrers(obj)

	@staticmethod
	def monitorQtDestructionEventFor(qobject):
		className = type(qobject).__name__
		qobject.destroyed.connect(lambda: GCUtils._destroyedObjects.append(className))

	@staticmethod
	def captureState(classNameFilter=None):
		liveObjectClassNames = GCUtils.getLiveObjectClassNames()

		if classNameFilter:
			liveObjectClassNames = filter(lambda className: className in classNameFilter, liveObjectClassNames)

		liveObjects = gc.get_objects()
		countByClass = {}

		for className in liveObjectClassNames:
			countByClass[className] = len(filter(lambda obj: type(obj).__name__ == className, liveObjects))

		GCUtils.CAPTURED_STATES.append(countByClass)

	@staticmethod
	def printQtDestructionEvents():
		output = open(GCUtils.QT_DESTRUCTION_EVENTS_PATH, 'w+')

		for destroyedObjectClassName in GCUtils._destroyedObjects:
			print >> output, destroyedObjectClassName

		output.close()

	@staticmethod
	def printStateComparisonBetween(state, previousState):
		output = open(GCUtils.REPORT_PATH, 'w+')

		for className in state:
			if className in previousState:
				countDiff = state[className] - previousState[className]
				if not countDiff:
					continue
				print >> output, '{}: {} instances where {}'.format(className, abs(countDiff),
																	'created' if countDiff > 0 else 'deleted')
			else:
				print >> output, '{}: {} instances where created'.format(className, state[className])

		for className in previousState:
			if className not in state:
				print >> output, '{}: {} instances where deleted'.format(className, previousState[className])

		output.close()

	@staticmethod
	def printGeneralReport(classNameFilter=None):
		liveObjectClassNames = GCUtils.getLiveObjectClassNames()

		if classNameFilter:
			liveObjectClassNames = filter(lambda className: className in classNameFilter, liveObjectClassNames)

		liveObjects = gc.get_objects()
		objCountList = list()

		for className in liveObjectClassNames:
			objCountList.append((className, len(filter(lambda obj: type(obj).__name__ == className, liveObjects))))

		objCountList.sort(key=lambda objCount: objCount[1], reverse=True)

		output = open(GCUtils.REPORT_PATH, 'w+')

		print >> output, '=== GC REPORT ===\n\n'

		for objCount in objCountList:
			print >> output, '{}: {} instance(s) alive'.format(objCount[0], objCount[1])

		output.close()

	# print 'HomeNavigationWidgets: ' + str(len(GCUtils.getInstancesOfClass(HomeNavigationWidget)))
	# print 'HomeViews: ' + str(len(GCUtils.getInstancesOfClass(HomeView)))
	# print 'CardBoards: ' + str(len(GCUtils.getInstancesOfClass(CardBoard)))
	# print 'HomeCards: ' + str(len(GCUtils.getInstancesOfClass(HomeCard)))
