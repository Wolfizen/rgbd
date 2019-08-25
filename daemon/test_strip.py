import math
import sys
from PyQt5.QtGui import QBrush, QColor, QPainter, QPalette, QPen, QPolygonF
from PyQt5.QtCore import pyqtSignal, QObject, QPointF, QRectF, Qt, QThread, QTimer
from PyQt5.QtWidgets import QApplication, QWidget

import strip


class TestingStrip(strip.Strip):
	"""Uses a graphical window to simulate the light strip"""

	qt_app = None
	qt_widget = None
	rgbd_thread = None

	def setup_strip(self):
		"""Return a mock strip that displays to a graphical window instead of connecting to hardware."""
		strip_backend = TestingStripBackend(self, self.strip_conf.get("count"), self.strip_conf.get("brightness"))
		if TestingStrip.qt_widget is not None:
			TestingStrip.qt_widget.connect_show_strip_signal()
		return strip_backend

	@classmethod
	def setup_window(cls, continuance_function):
		"""Start the Qt window, run `continuance_function` in a separate thread (generally is rgbd.run)."""

		if cls.qt_app is not None:
			cls.qt_app.quit()

		cls.qt_app = QApplication(sys.argv)
		cls.qt_widget = TestingStripWidget()

		# We have to hack the FUCK out of this. I'd rather call qt_app.exec() in a sub thread, but NOOOOO PyQt won't let
		# us do it anywhere but the main thread. So we have to pull this bullshit of spinning up a sub thread to
		# continue the primary control flow.

		cls.rgbd_thread = RgbdThread(continuance_function)
		cls.rgbd_thread.start()

		cls.qt_widget.show()
		cls.qt_app.exec()


class RgbdThread(QThread):
	strip_show_signal = pyqtSignal(list)
	"""Qt signal for sending updates to the widget. Must be connected to a QObject, that's why this class exists."""

	def __init__(self, run):
		super().__init__()
		self.run = run


# noinspection PyPep8Naming
class TestingStripBackend:
	"""Mock class for the neopixel strip interface. Writes data to the TestingStrip window instead."""

	def __init__(self, testing_strip, pixel_count: int, initial_brightness: float):
		self.testing_strip = testing_strip
		self.pixel_count = pixel_count
		self.brightness = initial_brightness

		# Memory buffer for the current pixel values. Calling show() writes this buffer to the window.
		self.data = [0] * self.pixel_count

	def setPixelColor(self, index: int, color: int):
		self.data[index] = color

	def setBrightness(self, brightness: float):
		self.brightness = brightness
		pass

	def numPixels(self) -> int:
		return self.pixel_count

	def show(self):
		# Send the data to the UI for repainting
		TestingStrip.rgbd_thread.strip_show_signal.emit(self.data)


class TestingStripWidget(QWidget):
	def __init__(self):
		super().__init__()
		self.data = None

		# set black background
		pal = self.palette()
		pal.setColor(QPalette.Background, Qt.black)
		self.setAutoFillBackground(True)
		self.setPalette(pal)

		self.setWindowTitle("rgbd Testing Simulation")

	def connect_show_strip_signal(self):
		"""Called by TestingStrip to update the currently running backend. The backend stores the pixel buffer."""
		TestingStrip.rgbd_thread.strip_show_signal.connect(self.show_strip)

	def show_strip(self, data: [int]):
		"""Called by TestingStripBackend when the rgbd thread calls `strip_backend.show()`."""
		self.data = data
		self.repaint()

	def paintEvent(self, event):
		painter = QPainter(self)

		if self.data is not None:
			strip_start_x = 10
			strip_start_y = 10
			strip_pixel_size = 4
			for i, color in enumerate(self.data):
				painter.fillRect(
					QRectF(
						strip_start_x + strip_pixel_size * i,
						strip_start_y,
						strip_pixel_size,
						strip_pixel_size),
					QColor.fromRgb(color))
			painter.setPen(QPen(Qt.GlobalColor.white))
			painter.drawText(
				QRectF(
					strip_start_x, strip_start_y + strip_pixel_size + 2,
					strip_pixel_size * len(self.data), 20),
				Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
				"0")
			painter.drawText(
				QRectF(
					strip_start_x, strip_start_y + strip_pixel_size + 2,
					strip_pixel_size * len(self.data), 20),
				Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop,
				str(len(self.data)))
		else:
			painter.setPen(QPen(Qt.GlobalColor.red))
			painter.drawText(QPointF(10, 10), "No strip loaded")
