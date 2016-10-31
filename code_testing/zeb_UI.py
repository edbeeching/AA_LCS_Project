#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Plagarism detector UI example
"""

import sys
from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):

        # Window Geometry, Title etc
        # Note show() has to be last in order for other components (combo box etc) to be visible
        self.setGeometry(200, 200, 1200, 800)
        # self.setFixedSize(1200,800)
        self.setWindowTitle('Plagarism Detector')

        # File Menu
        # Exit Function in menu bar
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu = menubar.addMenu('&Options')
        # Layout
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        self.setLayout(vbox)
        # Tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.adjustSize()
        vbox.addWidget(self.tab_widget)
        self.tab1 = QWidget()
        self.tab_widget.addTab(self.tab1,"Tab 1")

        # Tab 1

        layout = QFormLayout()
        layout.addRow("Name", QLineEdit())
        layout.addRow("Address", QLineEdit())
        self.tab_widget.setTabText(0, "Contact Details")
        self.tab1.setLayout(layout)

        # Other



        # Status Bar
        self.statusBar().showMessage('Ready')



        self.show()

    def tab0(self):
        # Combo Boxes
        self.task_label = QtGui.QLabel("Task:", self)
        tasklist = ["a", "b", "c", "d", "e"]
        self.task_combo_box = QtGui.QComboBox(self)
        for task in tasklist:
            self.task_combo_box.addItem(task)

        self.task_label.move(20, 32)
        self.task_label.adjustSize()
        self.task_combo_box.move(50, 30)
        self.task_combo_box.adjustSize()

        self.task_combo_box.activated[str].connect(self.combo_activated)

        self.text_label = QtGui.QLabel("Text:", self)
        self.text_combo_box = QtGui.QComboBox(self)
        # text_combo_box.addItem("g0pA_taska.txt")

        grouplist = range(0, 5)
        member_list = ["A", "B", "C", "D", "E"]

        for g in grouplist:
            for m in member_list:
                self.text_combo_box.addItem("g" + str(g) + "p" + m + "_task" + "a" + ".txt")

        self.text_combo_box.move(120, 30)
        self.text_combo_box.adjustSize()
        self.text_label.move(90, 32)
        self.text_label.adjustSize()

        # Text Boxes


        self.corpus_text = QtGui.QTextEdit(self)
        self.wiki_text = QtGui.QTextEdit(self)
        self.substring = QtGui.QTextEdit(self)

        self.corpus_text.setGeometry(30, 70, 800, 320)

        self.wiki_text.setGeometry(30, 410, 800, 320)
        self.substring.setGeometry(860, 70, 300, 500)
    def tab1(self):
        # Combo Boxes
        self.task_label = QtGui.QLabel("Task:", self)
        tasklist = ["a", "b", "c", "d", "e"]
        self.task_combo_box = QtGui.QComboBox(self)
        for task in tasklist:
            self.task_combo_box.addItem(task)

        self.task_label.move(20, 32)
        self.task_label.adjustSize()
        self.task_combo_box.move(50, 30)
        self.task_combo_box.adjustSize()

        self.task_combo_box.activated[str].connect(self.combo_activated)

        self.text_label = QtGui.QLabel("Text:", self)
        self.text_combo_box = QtGui.QComboBox(self)
        # text_combo_box.addItem("g0pA_taska.txt")

        grouplist = range(0, 5)
        member_list = ["A", "B", "C", "D", "E"]

        for g in grouplist:
            for m in member_list:
                self.text_combo_box.addItem("g" + str(g) + "p" + m + "_task" + "a" + ".txt")

        self.text_combo_box.move(120, 30)
        self.text_combo_box.adjustSize()
        self.text_label.move(90, 32)
        self.text_label.adjustSize()

        # Text Boxes


        self.corpus_text = QtGui.QTextEdit(self)
        self.wiki_text = QtGui.QTextEdit(self)
        self.substring = QtGui.QTextEdit(self)

        self.corpus_text.setGeometry(30, 70, 800, 320)

        self.wiki_text.setGeometry(30, 410, 800, 320)
        self.substring.setGeometry(860, 70, 300, 500)

    def combo_activated(self,text):
        self.statusBar().showMessage("Task: "+ text+" selected.")
        index = self.text_combo_box.currentIndex()
        self.text_combo_box.clear()
        grouplist = range(0,5)
        member_list = ["A","B","C","D","E"]

        for g in grouplist:
            for m in member_list:
                self.text_combo_box.addItem("g"+str(g)+"p"+m+"_task"+text+".txt")
        self.text_combo_box.setCurrentIndex(index)


def main():
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()