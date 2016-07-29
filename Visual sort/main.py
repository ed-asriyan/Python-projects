from random import *
from math import ceil
from tkinter import *
from time import sleep
from threading import Thread, Lock
from sortMethods import SORT_METHODS

def beep(item, duration, minValue, maxValue):
	return None
	MIN_FREQ = 37
	MAX_FREQ = 20000
	freq = ((item - minValue) / (maxValue - minValue)) * (MAX_FREQ - MIN_FREQ) + MIN_FREQ
	freq = 20000
	print(int(freq))
	beep_(int(freq), 100, int(duration * 1000))

# --- Classes ------------------------------------------------------

class MyList(list):
	# --- "Private" Members ----------------------------------------

	_setHistory    = [ ]
	_getHistory    = [ ]
	_accessHistory = [ ]

	_setCount      = 0
	_setEqualCount = 0
	_getCount      = 0
	_accessCount   = 0

	_onGet    = [ ]
	_onSet    = [ ]
	_onAccess = [ ]

	def _subscribeOnEvent(self, event, method):
		event.append(method)

	def _unsubscribeFromEvent(self, event, method):
		event.remove(method)

	def _invokeEvent(self, event, **kwargs):
		for method in event:
			method(**kwargs)

	def _getMethodBase(self, index):
		return super(MyList, self).__getitem__(index)

	def _setMethodBase(self, index, value):
		return super(MyList, self).__setitem__(index, value)

	# --- Public Members --------------------------------------------

	def SilentGet(self, index):
		return self._getMethodBase(index)

	def GetHistory(self):
		return self._getHistory

	def SetHistory(self):
		return self._setHistory

	def AccessHistory(self):
		return self._accessHistory

	def GetCount(self):
		return self._getCount

	def SetCount(self):
		return self._setCount

	def SetEqualCount(self):
		return self._setEqualCount

	def AccessCount(self):
		return self._accessCount


	def ResetCounters(self):
		self._accessCount = 0
		self._getCount    = 0
		self._setCount    = 0

		self._accessHistory = [ ]
		self._getHistory	= [ ]
		self._setHistory	= [ ]

	def OnAccessSubscribe(self, method):
		self._subscribeOnEvent(self._onAccess, method)

	def OnSetSubscribe(self, method):
		self._subscribeOnEvent(self._onSet, method)

	def OnGetSubscribe(self, method):
		self._subscribeOnEvent(self._onGet, method)

	def __getitem__(self, itemIndex):
		if type(itemIndex) is slice:
			result = MyList(self._getMethodBase(itemIndex))

			return result

		resValue = self._getMethodBase(itemIndex)

		self._getHistory.append([ itemIndex, resValue ])
		self._accessHistory.append(itemIndex)

		self._getCount	+= 1
		self._accessCount += 1

		self._invokeEvent(self._onGet, index=itemIndex, value=resValue)
		self._invokeEvent(self._onAccess, index=itemIndex)

		return resValue

	def __setitem__(self, itemIndex, newValue):
		if type(itemIndex) is slice:
			result = MyList(self._setMethodBase(itemIndex), newValue)

			return result

		oldVal = self._getMethodBase(itemIndex)

		self._setHistory.append([ itemIndex, newValue, oldVal ])
		self._accessHistory.append(itemIndex)

		self._setCount	  += 1
		self._accessCount   += 1
		self._setEqualCount += newValue == oldVal

		self._invokeEvent(self._onSet, index=itemIndex, value=newValue, oldValue=oldVal)
		self._invokeEvent (self._onAccess, index=itemIndex)

		resValue = self._setMethodBase(itemIndex, newValue)

		return resValue

class ListViewerCanvas(Canvas):
	# --- "Private" Members ----------------------------------------

	_title = None

	_lock = None

	_height = None
	_width  = None

	_itemWidth  = None
	_itemHeight = None

	_delay		= 0.1

	_drawOnSet = True
	_drawOnGet = True

	# canvas items
	_blocks = [ ]

	_getBlockIndex = None
	_setBlockIndex = None

	_textTitle     = None
	_textAccesses  = None
	_textGets      = None
	_textSets      = None
	_textSetsEqual = None
	_textDelay     = None
	_textSize      = None

	def _safelyInvoke(self, method, **kwargs):
		with self._lock:
			method(**kwargs)


	# Drawing Text Fields

	def _drawText(self, textIndex, **kwargs):
		return self.create_text(10, textIndex * 20, anchor="w", fill="red", font="bold", **kwargs)


	def _drawTitleText(self, value):
		if not self._textTitle is None:
			self.delete(self._textTitle)

		self._textTitle = self._drawText(1, text="Name: " + str(self._title))

	def _drawAccessesText(self):
		if not self._textAccesses is None:
			self.delete(self._textAccesses)

		self._textAccesses = self._drawText(3, text="Accesses: " + str(self._list.AccessCount()))

	def _drawGetsText(self):
		if not self._textGets is None:
			self.delete(self._textGets)

		if self._drawOnGet:
			self._textGets = self._drawText(4, text="Gets: " + str(self._list.GetCount()))


	def _drawSetsText(self):
		if not self._textSets is None:
			self.delete(self._textSets)

		if self._drawOnSet:
			self._textSets = self._drawText(5, text="Sets: " + str(self._list.SetCount()))

	def _drawSetsEqualText(self):
		if not self._textSets is None:
			self.delete(self._textSetsEqual)

		if self._drawOnSet:
			self._textSetsEqual = self._drawText(6, text="Equal sets: " + str(self._list.SetEqualCount()))

	def _drawDelayText(self):
		if not self._textDelay is None:
			self.delete(self._textDelay)

		self._textDelay = self._drawText(8, text="Delay: " + str(self._delay))

	def _drawSizeText(self):
		if not self._textSize is None:
			self.delete(self._textSize)

		self._textSize = self._drawText(9, text="Size: " + str(len(self._list)))


	# Drawing blocks
	def _drawBlock(self, index, color="gray"):
		leftX,  leftY  = index * self._itemWidth, self._height
		rightX, rightY = (index + 1) * (self._itemWidth), self._height - (self._list.SilentGet(index) - self._minValue) * self._itemHeight

		if not self._blocks[index] is None:
			self.delete(self._blocks[index][0])
			self.delete(self._blocks[index][1])


		blockBody = self.create_rectangle(leftX, leftY,\
													rightX, rightY + self._itemWidth,\
											 		fill=color, outline=color)
		blockHead = self.create_rectangle(leftX, rightY+self._itemWidth,\
													rightX, rightY,\
											 		fill="black")

		self._blocks[index] = [ blockBody, blockHead ]

	def _drawGet(self):
		gets = self._list.GetHistory()
		getsLen = len(gets)

		getIndex = gets[getsLen - 1][0] if getsLen > 1 else -1

		if not self._getBlockIndex is None:
			self._drawBlock(self._getBlockIndex)

		if getIndex >= 0:
			self._drawBlock(getIndex, "green")
			self._getBlockIndex = getIndex

	def _drawSet(self):
		sets = self._list.SetHistory()
		setsLen = len(sets)

		setIndex = sets[setsLen - 1][0] if setsLen > 1 else -1

		if not self._setBlockIndex is None:
			self._drawBlock(self._setBlockIndex)

		if setIndex >= 0:
			self._drawBlock(setIndex, "red")
			self._setBlockIndex = setIndex

	def _drawAll(self):
		self.delete("all")

		self._textSets      = None
		self._textGets      = None
		self._textAccesse   = None
		self._textTitle     = None
		self._setBlockIndex = None
		self._getBlockIndex = None
		self._blocks        = [ ]

		self._drawTitleText(self._title)
		self._drawAccessesText()
		self._drawSetsText()
		self._drawGetsText()
		self._drawDelayText()
		self._drawSizeText()

		for i in range(len(self._list)):
			self._blocks.append(None)
			self._drawBlock(i)

	def _updateWidgetInfo(self):
		h = self.winfo_height()
		w = self.winfo_width()

		reDraw = ((len(self._blocks) != len(self._list))   or
				 (h != self._height) or (w != self._width))

		self._height = h
		self._width  = w

		self._itemWidth  = self._width / len(self._list)
		self._itemHeight = self._height / (self._maxValue - self._minValue)

		if reDraw:
			self._drawAll()

	def _onSet(self, value=0, **kwargs):
		if not self._drawOnSet:
			return

		if value < self._minValue:
			self._minValue = value
		if value > self._maxValue:
			self._maxValue = value

		self._updateWidgetInfo()

		self._drawAccessesText()
		self._drawSetsText()
		self._drawSetsEqualText()

		self._drawSet()

		self.update()
		sleep(self._delay)

	def _onGet(self, index=-1, **kwargs):
		if not self._drawOnGet:
			return

		self._updateWidgetInfo()

		self._drawAccessesText()
		self._drawGetsText()

		self._drawGet()
		self._drawSet()

		self.update()
		sleep(self._delay)

	# --- Public Members -------------------------------------------

	def Delay(self, value=None):
		if not value is None and value >= 0:
			self._delay = value
		return self._delay

	def DrawOnSet(self, value):
		self._drawOnSet = bool(value)

	def DrawOnGet(self, value):
		self._drawOnGet = bool(value)


	def ReDraw(self):
		self._safelyInvoke(self._drawAll)

	def __init__(self, l, root, title=None, lockObj=None, **kwargs):
		self._root = root
		Canvas.__init__(self, root, **kwargs)

		self._maxValue = max(l)
		self._minValue = min(l)

		self._title = title
		self._lock = lockObj if lockObj else Lock()

		self._list = l
		self._list.ResetCounters()

		self._updateWidgetInfo()
		self._drawAll()

		self._list.OnGetSubscribe(lambda **kwargs: self._safelyInvoke(self._onGet, **kwargs))
		self._list.OnSetSubscribe(lambda **kwargs: self._safelyInvoke(self._onSet, **kwargs))

# --- Generate functions -------------------------------------------

def generateRandomList(size, minValue=None, maxValue=None):
	if size is None or size < 0:
		return None

	if minValue == None == maxValue:
		minValue = 0
		maxValue = size

	if minValue is None:
		minValue = maxValue - size
	if maxValue is None:
		maxValue = minValue + size

	if minValue > maxValue:
		minValue, maxValue = maxValue, minValue

	return [ randint(minValue, maxValue) for i in range(size) ]


def generateSortedList(size, minValue=None, maxValue=None, increase=True):
	if size is None or size < 0:
		return None
	if not size:
		return [ ]

	if minValue == None == maxValue:
		minValue = 0
		maxValue = size

	if minValue is None:
		minValue = maxValue - size
	if maxValue is None:
		maxValue = minValue + size

	if (minValue > maxValue and increase) or (minValue < maxValue and not increase):
		minValue, maxValue = maxValue, minValue

	return [ i for i in range(minValue, maxValue, (maxValue - minValue) // size) ]


# --- Main ---------------------------------------------------------


selectedMethods = [ ]
selectedMethodsCount = 0
listSize    = 100
drawGets    = True
drawSets    = True
generateFunc = generateRandomList

def printMethods():
	print("Sort method list:")
	for i in range(len(SORT_METHODS)):
		SORT_METHODS[i].__name__ = SORT_METHODS[i].__name__.replace("Sort", "").title()
		print("%2d - " % i, SORT_METHODS[i].__name__, sep='')

	print("\nCommand: <METHOD,METHOD,...> <COUNT> [ parameters ]")
	print("Available parameters:")
	print("\tr   - random list")
	print("\ts   - sorted list")
	print("\tbs  - back sorted list")
	print("\tset - draw on sets only")

def parseInput(s):
	global selectedMethods, listSize, drawSets, drawGets, generateFunc, selectedMethodsCount, isSimultaneously

	l = s.split()

	if len(l) < 2:
		return False

	selectedMethods = [ SORT_METHODS[int(i)] for i in l[0].split(',') ]
	selectedMethodsCount = len(selectedMethods)
	listSize    = int(l[1])

	inc = "s" in l
	if ("s" in l) or ("bs" in l):
		generateFunc = lambda s: generateSortedList(s, increase=inc)
	if "set" in l:
		drawGets = False

	isSimultaneously = "sm" in l

	return True

printMethods()
while True:
	if parseInput(input("Enter command: ")):
		break
	else:
		print("\t\tInvalid command.")



locker = Lock()
root = Tk()
frame = Frame(root)

testList = generateFunc(listSize)

listToSort = [ ]
viewers    = [ ]

gridWidth = ceil(selectedMethodsCount ** 0.5)

for i in range(selectedMethodsCount):
	l = MyList(testList.copy())
	c = ListViewerCanvas(l, frame, selectedMethods[i].__name__, locker,  borderwidth=2, relief='sunken')
	c.Delay(listSize ** -3)
	c.DrawOnGet(drawGets)
	# c.pack(fill=BOTH, expand=1)

	columnNum = i % gridWidth
	rowNum    = i // gridWidth

	c.grid(row=rowNum, column=columnNum,\
		   sticky="nsew", columnspan=(1 if i != selectedMethodsCount - 1 else gridWidth - columnNum))

	listToSort.append([ l, selectedMethods[i] ])

	viewers.append(c)

frame.pack(fill=BOTH, expand=1)

for i in range(gridWidth):
	frame.columnconfigure(i, weight=1)
	frame.rowconfigure(i, weight=1)

for l in listToSort:
	t = Thread(target=l[1], args=(l[0], ))
	t.start()

root.mainloop()
