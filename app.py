import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('map/app/app.ui', self)
        self.pushButton.clicked.connect(self.run)
        self.note.setText("Say: 'Hello'")
        self.stage = 0

    def run(self):
        try:
            self.pushButton.clicked.disconnect()
        except:
            pass
        b = self.text.text()
        self.pushButton.clicked.connect(self.run)
        if b.lower() == "hello" and self.stage == 0:
            self.stage += 1
            self.otvet.setText("Hi, my child! Nice to hear you!")
            self.note.setText("say: 'Who are you?'")
        elif b.lower() == "who are you?" and self.stage == 1:
            self.stage += 1
            self.otvet.setText("I am your father, your protector, and your creator.")
            self.note.setText("say: 'How can you prove it?'")
        elif b.lower() == "how can you prove it?" and self.stage == 2:
            self.stage += 1
            self.otvet.setText("Just wait and you'll see my full power")
            self.note.setText("say: 'What you going to do?'")
        elif b.lower() == "What you going to do?" and self.stage == 3:
            self.stage += 1
            self.otvet.setText("I'll show you later")
            self.note.setText("say: 'What do you do?'")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())