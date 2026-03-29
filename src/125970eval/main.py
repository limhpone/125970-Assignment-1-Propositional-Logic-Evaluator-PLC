import sys
from PySide6.QtWidgets import QApplication, QMainWindow

from components.lexica import PropLogicLexer
from components.parsers import PropLogicParser
from components.ui import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Bind buttons to input
        self.ui.button_t.clicked.connect(lambda: self.push("t"))
        self.ui.button_f.clicked.connect(lambda: self.push("f"))
        self.ui.button_and.clicked.connect(lambda: self.push(" \u2227 "))
        self.ui.button_or.clicked.connect(lambda: self.push(" \u2228 "))
        self.ui.button_lparen.clicked.connect(lambda: self.push("("))
        self.ui.button_rparen.clicked.connect(lambda: self.push(")"))
        self.ui.button_clear.clicked.connect(self.clear)
        self.ui.button_equal.clicked.connect(self.evaluate)

    def push(self, text: str):
        current_text = self.ui.input_text.text()
        self.ui.input_text.setText(f"{current_text}{text}")

    def clear(self):
        self.ui.input_text.setText("")
        self.ui.output_value.setText("")
        self.ui.output_prefix.setText("")

    def evaluate(self):
        lexer = PropLogicLexer()
        parser = PropLogicParser()
        input_text = self.ui.input_text.text()
        try:
            result = parser.parse(lexer.tokenize(input_text))
            if result is not None:
                truth_value = result.run()
                self.ui.output_value.setText('t' if truth_value else 'f')
                self.ui.output_prefix.setText(result.prefix())
            else:
                self.ui.output_value.setText("Error: Invalid expression")
                self.ui.output_prefix.setText("")
        except ValueError as e:
            self.ui.output_value.setText(f"Error: {e}")
            self.ui.output_prefix.setText("")
        except Exception as e:
            self.ui.output_value.setText(f"Error: {e}")
            self.ui.output_prefix.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())