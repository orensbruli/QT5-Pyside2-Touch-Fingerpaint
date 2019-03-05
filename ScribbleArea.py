from PySide2.QtCore import Qt, QSize, QPoint, QEvent, QSizeF
from PySide2.QtGui import qRgb, QColor, QImage, QPainter
from PySide2.QtWidgets import QWidget


class ScribbleArea(QWidget):
	def __init__(self, parent=None):
		super(ScribbleArea, self).__init__(parent)
		self.myPenColors = [QColor("green"),
							QColor("purple"),
							QColor("red"),
							QColor("blue"),
							QColor("yellow"),
							QColor("pink"),
							QColor("orange"),
							QColor("brown"),
							QColor("grey"),
							QColor("black")]
		self.setAttribute(Qt.WA_AcceptTouchEvents)
		self.setAttribute(Qt.WA_StaticContents)
		self.image = QImage()

		self.modified = False

	def s_print(self):
		pass

	def clearImage(self):
		self.image.fill(qRgb(255, 255, 255))
		self.modified = True
		self.update()

	def openImage(self, fileName):
		loadedImage = QImage()
		if not loadedImage.load(fileName):
			return False

		newSize = loadedImage.size().expandedTo(self.size())
		self.resizeImage(loadedImage, newSize)
		self.image = loadedImage
		self.modified = False
		self.update()
		return True

	def saveImage(self, fileName, fileFormat):

		visibleImage = self.image.copy()
		self.resizeImage(visibleImage, self.size())

		if visibleImage.save(fileName, fileFormat):
			self.modified = False
			return True
		else:
			return False

	def paintEvent(self, event):
		painter = QPainter(self)
		rect = event.rect()
		painter.drawImage(rect.topLeft(), self.image, rect)

	def resizeEvent(self, event):
		if self.width() > self.image.width() or self.height() > self.image.height():
			newWidth = max(self.width() + 128, self.image.width())
			newHeight = max(self.height() + 128, self.image.height())
			self.resizeImage(self.image, QSize(newWidth, newHeight))
			self.update()
		super(ScribbleArea, self).resizeEvent(event)

	def resizeImage(self, image, newSize):
		if self.image.size() == newSize:
			return

		newImage = QImage(newSize, QImage.Format_RGB32)
		newImage.fill(qRgb(255, 255, 255))
		painter = QPainter(newImage)
		painter.drawImage(QPoint(0, 0), self.image)
		self.image = newImage

	#
	# def print(self, )
	# {
	# #ifndef QT_NO_PRINTER:
	#     QPrinter printer(QPrinter.HighResolution)
	#
	#     QPrintDialog *printDialog = new QPrintDialog(&printer, this)
	#     if (printDialog.exec() == QDialog.Accepted) {
	#         QPainter painter(&printer)
	#         QRect rect = painter.viewport()
	#         QSize size = self.image.size()
	#         size.scale(rect.size(), Qt.KeepAspectRatio)
	#         painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
	#         painter.setWindow(self.image.rect())
	#         painter.drawImage(0, 0, image)
	#     }
	# #endif // QT_NO_PRINTER
	# }
	#
	def event(self, event):
		if event.type() == QEvent.TouchBegin or event.type() == QEvent.TouchUpdate or event.type() == QEvent.TouchEnd:
			touchPoints = event.touchPoints()
			for touchPoint in touchPoints:
				if touchPoint.state() == Qt.TouchPointStationary:
					continue
				else:
					rect = touchPoint.rect()
					if rect.isEmpty():
						diameter = 50 * touchPoint.pressure()
						rect.setSize(QSizeF(diameter, diameter))

					painter = QPainter(self.image)
					painter.setPen(Qt.NoPen)
					painter.setBrush(self.myPenColors[touchPoint.id() % len(self.myPenColors)])
					painter.drawEllipse(rect)
					painter.end()

					self.modified = True
					rad = 2
					self.update(rect.toRect().adjusted(-rad, -rad, +rad, +rad))

		else:
			return super(ScribbleArea, self).event(event)
		return True