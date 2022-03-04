import sys
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QWidget, QTextEdit, QGridLayout, QLabel
from PyQt5.QtCore import QRect, QEvent
from PyQt5.QtGui import QTextFormat

HEIGHT = 800
WIDTH = 1000
EDITOR_WIDTH = WIDTH // 4
EDITOR_HEIGHT = HEIGHT // 2
RAM_WIDTH = WIDTH // 2
RAM_HEIGHT = RAM_WIDTH
RAM_CELL_WIDTH = RAM_WIDTH // 10
RAM_CELL_HEIGHT = RAM_HEIGHT // 40

class ErrorDisplay(QLabel):

	def __init__(self):
		super().__init__()
		self.setStyleSheet("color: red")

	def show(self, msg):
		self.setText(msg)

class MemoryLocation(QTextEdit):
	def __init__(self, x, y, error_display):
		super().__init__()
		self.setText("000")
		self.setGeometry(x, y, RAM_CELL_WIDTH, RAM_CELL_HEIGHT)
		self.last_text = "000"
		self.error = error_display

		super().textChanged.connect(self.validate)

	def validate(self) -> None:
		print("Leaving")
		new_value = self.toPlainText()

		print(type(new_value))
		if not new_value.isdigit():
			print("error")
			# 	self.error.display("Illegal value")
			self.setText(self.last_text)
		elif len(new_value) > 3:
			self.setText(new_value[:3])
		else:
			self.last_text = new_value





class MyApplication(QWidget):

	def __init__(self):
		super().__init__()


		# self.scene = QGraphicsScene(parent=self)
		# self.scene.addText("Hello, world!")
		# self.setWindowTitle("CIE Assembler")
		# self.view = QGraphicsView(self.scene, parent=self)
		# self.view.setGeometry(0, 0, 50, 10)
		# self.view.show()
		# self.code_editors = [QTextEdit(parent=self) for i in range(4)]
		# self.code_editors[0].setGeometry(0, 0, EDITOR_WIDTH, EDITOR_HEIGHT)
		# self.code_editors[1].setGeometry(WIDTH//2, 0, EDITOR_WIDTH, EDITOR_HEIGHT)
		# self.code_editors[2].setGeometry(WIDTH//2, HEIGHT//2, EDITOR_WIDTH, EDITOR_HEIGHT)
		# self.code_editors[3].setGeometry(0, HEIGHT//2, EDITOR_WIDTH, EDITOR_HEIGHT)
		self.error_display = ErrorDisplay()
		self.ram_container = QWidget(parent=self)
		grid = QGridLayout()
		self.ram_container.setLayout(grid)
		self.ram_container.setGeometry(0, HEIGHT//4, RAM_WIDTH, RAM_HEIGHT)

		self.ram = []



		address = 0
		for row in range(10):
			address += 10
			# for column in range(10):
			# 	x, y = column*RAM_CELL_WIDTH, row*RAM_CELL_HEIGHT
			# 	label = QLabel()
			# 	label.setText(str(address + column))
			# 	grid.addWidget(label, x, y)
			# 	label.setGeometry(x, y, RAM_CELL_WIDTH, RAM_CELL_HEIGHT)

			for column in range(10):
				x, y = column*RAM_CELL_WIDTH, (row*RAM_CELL_HEIGHT)+RAM_CELL_HEIGHT
				memory_location = MemoryLocation(x, y, self.error_display)
				self.ram.append(memory_location)
				grid.addWidget(memory_location, x, y)


		self.ram_container.show()










app = QApplication(sys.argv)
windows = MyApplication()


windows.resize(WIDTH,HEIGHT)
windows.move(100,100)
windows.show()
sys.exit(app.exec_())