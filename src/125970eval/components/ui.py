# -*- coding: utf-8 -*-

################################################################################
## UI for Propositional Logic Evaluator
## Manually written (not auto-generated from main.ui)
################################################################################

from PySide6.QtCore import (QCoreApplication, QRect, QMetaObject, QSize)
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(460, 300)
        MainWindow.setMinimumSize(QSize(460, 300))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        # Fonts
        font_bold = QFont()
        font_bold.setPointSize(12)
        font_bold.setBold(True)
        font_normal = QFont()
        font_normal.setPointSize(10)

        # Input row
        self.input_label = QLabel(self.centralwidget)
        self.input_label.setObjectName(u"input_label")
        self.input_label.setGeometry(QRect(20, 25, 50, 28))
        self.input_label.setFont(font_normal)
        self.input_text = QLineEdit(self.centralwidget)
        self.input_text.setObjectName(u"input_text")
        self.input_text.setGeometry(QRect(75, 25, 365, 28))
        self.input_text.setFont(font_normal)

        # Button row 1: t, f, ∧, ∨, (, )
        btn_w, btn_h, gap = 60, 35, 8
        y1 = 70
        x = 20
        self.button_t = QPushButton(self.centralwidget)
        self.button_t.setObjectName(u"button_t")
        self.button_t.setGeometry(QRect(x, y1, btn_w, btn_h))
        x += btn_w + gap
        self.button_f = QPushButton(self.centralwidget)
        self.button_f.setObjectName(u"button_f")
        self.button_f.setGeometry(QRect(x, y1, btn_w, btn_h))
        x += btn_w + gap
        self.button_and = QPushButton(self.centralwidget)
        self.button_and.setObjectName(u"button_and")
        self.button_and.setGeometry(QRect(x, y1, btn_w, btn_h))
        x += btn_w + gap
        self.button_or = QPushButton(self.centralwidget)
        self.button_or.setObjectName(u"button_or")
        self.button_or.setGeometry(QRect(x, y1, btn_w, btn_h))
        x += btn_w + gap
        self.button_lparen = QPushButton(self.centralwidget)
        self.button_lparen.setObjectName(u"button_lparen")
        self.button_lparen.setGeometry(QRect(x, y1, btn_w, btn_h))
        x += btn_w + gap
        self.button_rparen = QPushButton(self.centralwidget)
        self.button_rparen.setObjectName(u"button_rparen")
        self.button_rparen.setGeometry(QRect(x, y1, btn_w, btn_h))

        # Button row 2: Clear, Evaluate
        y2 = y1 + btn_h + gap
        self.button_clear = QPushButton(self.centralwidget)
        self.button_clear.setObjectName(u"button_clear")
        self.button_clear.setGeometry(QRect(20, y2, 130, btn_h))
        self.button_equal = QPushButton(self.centralwidget)
        self.button_equal.setObjectName(u"button_equal")
        self.button_equal.setGeometry(QRect(158, y2, 282, btn_h))

        # Output: Truth Value
        y3 = y2 + btn_h + 25
        self.output_value_label = QLabel(self.centralwidget)
        self.output_value_label.setObjectName(u"output_value_label")
        self.output_value_label.setGeometry(QRect(20, y3, 120, 25))
        self.output_value_label.setFont(font_normal)
        self.output_value = QLabel(self.centralwidget)
        self.output_value.setObjectName(u"output_value")
        self.output_value.setGeometry(QRect(145, y3, 295, 25))
        self.output_value.setFont(font_bold)

        # Output: Prefix Notation
        y4 = y3 + 35
        self.output_prefix_label = QLabel(self.centralwidget)
        self.output_prefix_label.setObjectName(u"output_prefix_label")
        self.output_prefix_label.setGeometry(QRect(20, y4, 120, 25))
        self.output_prefix_label.setFont(font_normal)
        self.output_prefix = QLabel(self.centralwidget)
        self.output_prefix.setObjectName(u"output_prefix")
        self.output_prefix.setGeometry(QRect(145, y4, 295, 25))
        self.output_prefix.setFont(font_bold)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 460, 30))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Propositional Logic Evaluator", None))
        self.input_label.setText(QCoreApplication.translate("MainWindow", u"Input:", None))
        self.button_t.setText(QCoreApplication.translate("MainWindow", u"t", None))
        self.button_f.setText(QCoreApplication.translate("MainWindow", u"f", None))
        self.button_and.setText(QCoreApplication.translate("MainWindow", u"\u2227", None))
        self.button_or.setText(QCoreApplication.translate("MainWindow", u"\u2228", None))
        self.button_lparen.setText(QCoreApplication.translate("MainWindow", u"(", None))
        self.button_rparen.setText(QCoreApplication.translate("MainWindow", u")", None))
        self.button_clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.button_equal.setText(QCoreApplication.translate("MainWindow", u"= Evaluate", None))
        self.output_value_label.setText(QCoreApplication.translate("MainWindow", u"Truth Value:", None))
        self.output_value.setText(u"")
        self.output_prefix_label.setText(QCoreApplication.translate("MainWindow", u"Prefix Notation:", None))
        self.output_prefix.setText(u"")
    # retranslateUi

