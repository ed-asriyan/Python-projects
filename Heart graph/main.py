class LoveDrawer (object):
	_drawingStep = 1e-3

	def _f1(self, x):
		return 5 * (abs(x) ** 0.5 - (1 - x ** 2) ** 0.5) / 6

	def _f2(self, x):
		return 5 * (abs(x) ** 0.5 + (1 - x ** 2) ** 0.5) / 6

	def SetDrawingStep(self, value):
		fVal = float(value)
		if fVal > 0:
			self._drawingStep = fVal
	
	def DrawPlot(self):
		from matplotlib import pyplot as plt
		from matplotlib.mlab import frange
		import numpy

		xBegin = -1
		xEnd   = 1

		xRange = frange(xBegin, xEnd, self._drawingStep)

		y1Points = [ self._f1(x) for x in xRange ]
		y2Points = [ self._f2(x) for x in xRange ]

		top,    = plt.plot(xRange, y1Points, color="red", linewidth=2.5)
		bottom, = plt.plot(xRange, y2Points, color="red", linewidth=2.5)

		plt.fill_between(xRange, y1Points, y2Points, color="red", alpha=0.25)

		plt.xlim(-2, 2)

		plt.title("♥")
		plt.show()


ld = LoveDrawer()
ld.DrawPlot()