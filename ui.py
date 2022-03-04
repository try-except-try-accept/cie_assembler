import sys
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication, QWidget, QTextEdit

HEIGHT = 800
WIDTH = 1000
EDITOR_WIDTH = WIDTH // 4
EDITOR_HEIGHT = HEIGHT // 2

class MyApplication(QWidget):

	def __init__(self):
		super().__init__()

		self.scene = QGraphicsScene(parent=self)
		self.scene.addText("Hello, world!")
		self.setWindowTitle("CIE Assembler")
		self.view = QGraphicsView(self.scene, parent=self)
		self.view.setGeometry(0, 0, 50, 10)
		self.view.show()
		self.code_editors = [QTextEdit(parent=self) for i in range(4)]
		self.code_editors[0].setGeometry(0, 0, EDITOR_WIDTH, EDITOR_HEIGHT)
		self.code_editors[1].setGeometry(WIDTH//2, 0, EDITOR_WIDTH, EDITOR_HEIGHT)
		self.code_editors[2].setGeometry(WIDTH//2, HEIGHT//2, EDITOR_WIDTH, EDITOR_HEIGHT)
		self.code_editors[3].setGeometry(0, HEIGHT//2, EDITOR_WIDTH, EDITOR_HEIGHT)




app = QApplication(sys.argv)
windows = MyApplication()


windows.resize(WIDTH,HEIGHT)
windows.move(100,100)
windows.show()
sys.exit(app.exec_())