
from PyQt4 import QtGui, QtCore
import sys, os

class LCS_UI(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(LCS_UI, self).__init__(parent)
        self.setGeometry(200, 200, 1200, 800)
        mainWidget = QtGui.QWidget()
        self.setCentralWidget(mainWidget)
        mainLayout = QtGui.QVBoxLayout()
        mainWidget.setLayout(mainLayout)

        self.menu()

        self.tabWidget = QtGui.QTabWidget()
        mainLayout.addWidget(self.tabWidget)

        self.tab1 = QtGui.QWidget()
        self.tab2 = QtGui.QWidget()
        self.tab3 = QtGui.QWidget()

        self.tabWidget.addTab(self.tab1, "Tab 1")
        self.tabWidget.addTab(self.tab2, "Tab 2")
        self.tabWidget.addTab(self.tab3, "Tab 3")

        self.tab1UI()

        self.setWindowTitle("Plagarism Detector")
        self.statusBar().showMessage('Ready')

    def menu(self):
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


    def tab1UI(self):

        # Combo boxes etc
        h_layout = QtGui.QHBoxLayout()
        task_label = QtGui.QLabel("Task:")

        self.task_combo_box = QtGui.QComboBox()
        self.task_combo_box.activated[str].connect(self.tab1_task_combo_activated)
        tasklist = ["a", "b", "c", "d", "e"]
        for task in tasklist:
            self.task_combo_box.addItem(task)

        text_label = QtGui.QLabel("Text:")
        self.text_combo_box = QtGui.QComboBox()
        self.text_combo_box.activated[str].connect(self.tab1_text_combo_activated)
        # grouplist = range(0, 5)
        # member_list = ["A", "B", "C", "D", "E"]
        file_list = os.listdir('../corpus-20090418')
        for file in file_list:
            if "taska" in file and not "orig" in file:
                self.text_combo_box.addItem(file)

        # for group in grouplist:
        #     for member in member_list:
        #         self.text_combo_box.addItem("g" + str(group) + "p" + member + "_task" + "a" + ".txt")


        self.raw_btn = QtGui.QRadioButton("Raw Text")
        self.raw_btn.toggled.connect(lambda: self.tab1_radio_toggled(self.raw_btn))
        self.preproc_btn = QtGui.QRadioButton("PreProcessed Text")
        self.preproc_btn.toggled.connect(lambda: self.tab1_radio_toggled(self.preproc_btn))

        h_layout.addWidget(task_label)
        h_layout.addWidget(self.task_combo_box)
        h_layout.addWidget(text_label)
        h_layout.addWidget(self.text_combo_box)
        h_layout.addWidget(self.raw_btn)
        h_layout.addWidget(self.preproc_btn)
        h_layout.addStretch()
        h_layout.addWidget(QtGui.QLabel("Test"))

        self.corpus_text = QtGui.QTextEdit()
        self.wiki_text = QtGui.QTextEdit()
        self.substring = QtGui.QTextEdit()

        v_layout = QtGui.QVBoxLayout()
        v_layout.addLayout(h_layout)

        v1_layout = QtGui.QVBoxLayout()
        v2_layout = QtGui.QVBoxLayout()
        h1_layout = QtGui.QHBoxLayout()

        v1_layout.addWidget(self.corpus_text)
        v1_layout.addWidget(self.wiki_text)
        v2_layout.addWidget(self.substring, stretch=2)
        v2_layout.addStretch(stretch=1)

        h1_layout.addLayout(v1_layout,stretch=2)
        h1_layout.addLayout(v2_layout,stretch=1)

        v_layout.addLayout(h1_layout)

       # v_layout.addStretch()
        self.raw_btn.setChecked(True)
        self.tab1.setLayout(v_layout)

    def tab1_task_combo_activated(self,text):
        self.statusBar().showMessage("Task: "+ text+" selected.")
        index = self.text_combo_box.currentIndex()
        self.text_combo_box.clear()

        file_list = os.listdir('../corpus-20090418')
        for file in file_list:
            if "task"+str(text) in file and not "orig" in file:
                self.text_combo_box.addItem(file)

        self.text_combo_box.setCurrentIndex(index)

        self.tab1_radio_toggled(self.raw_btn)
        self.tab1_radio_toggled(self.preproc_btn)

    def tab1_text_combo_activated(self, text):
        self.statusBar().showMessage("Task: " + text + " selected.")
        self.tab1_radio_toggled(self.raw_btn)
        self.tab1_radio_toggled(self.preproc_btn)


    def tab1_radio_toggled(self, button):
        if button.text() == "Raw Text" and button.isChecked():
            self.change_text("raw")
            self.statusBar().showMessage("Displaying Raw Text")

        if button.text() == "PreProcessed Text" and button.isChecked():
            self.change_text("proc")
            self.statusBar().showMessage("Displaying PreProcessed Text")

    def change_text(self, text_type):
        if text_type == "raw":
            filename = self.text_combo_box.currentText()
            file_object = open("../corpus-20090418/" + filename)
            text = file_object.read()
            self.corpus_text.setPlainText(text)
            file_object.close()

            file_object = open("../corpus-20090418/orig_task" + self.task_combo_box.currentText() + ".txt")
            text = file_object.read()
            self.wiki_text.setPlainText(text)
            file_object.close()

        if text_type == "proc":
            filename = self.text_combo_box.currentText()
            file_object = open("../corpus-preprocessed/" + filename[:-4] + "_preprocessed.txt")
            text = file_object.read()
            self.corpus_text.setPlainText(text)
            file_object.close()

            file_object = open("../corpus-preprocessed/orig_task" + self.task_combo_box.currentText() + "_preprocessed.txt")
            text = file_object.read()
            self.wiki_text.setPlainText(text)
            file_object.close()


def main():
    app = QtGui.QApplication(sys.argv)
    lcs_ui = LCS_UI()
    lcs_ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()