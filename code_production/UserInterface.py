
from PyQt4 import QtGui, QtCore

import sys, os
import prototype
import PrintingNeatly
import PandasModel
import pandas as pd

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import Plotting


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
        self.tab4 = QtGui.QWidget()
        self.tab5 = QtGui.QWidget()

        self.tabWidget.addTab(self.tab1, "LCS Unit")
        self.tabWidget.addTab(self.tab2, "Table")
        self.tabWidget.addTab(self.tab3, "General graph")
        self.tabWidget.addTab(self.tab4, "Graph by task")
        self.tabWidget.addTab(self.tab5, "Repartition by Category")

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()
        self.tab5UI()

        self.setWindowTitle("Plagiarism Detector")
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
        h1_layout = QtGui.QHBoxLayout()
        h2_layout = QtGui.QHBoxLayout()
        task_label = QtGui.QLabel("Task:")

        self.task_combo_box = QtGui.QComboBox()
        self.task_combo_box.activated[str].connect(self.tab1_task_combo_activated)
        tasklist = ["a", "b", "c", "d", "e"]
        for task in tasklist:
            self.task_combo_box.addItem(task)

        text_label = QtGui.QLabel("Text:")
        self.text_combo_box = QtGui.QComboBox()
        self.text_combo_box.activated[str].connect(self.tab1_text_combo_activated)

        file_list = os.listdir('../corpus-20090418')
        for file in file_list:
            if "taska" in file and not "orig" in file:
                self.text_combo_box.addItem(file)

        self.raw_btn = QtGui.QRadioButton("Raw")
        self.raw_btn.toggled.connect(lambda: self.tab1_radio_toggled(self.raw_btn))
        self.preproc_btn = QtGui.QRadioButton("PreProc")
        self.preproc_btn.toggled.connect(lambda: self.tab1_radio_toggled(self.preproc_btn))
        self.adv_preproc_btn = QtGui.QRadioButton("Adv PreProc")
        self.adv_preproc_btn.toggled.connect(lambda: self.tab1_radio_toggled(self.adv_preproc_btn))
        self.adv_preproc_sentence_btn = QtGui.QRadioButton("Adv PreProc And Sentence")
        self.adv_preproc_sentence_btn.toggled.connect(lambda: self.tab1_radio_toggled(self.adv_preproc_sentence_btn))

        h1_layout.addWidget(task_label)
        h1_layout.addWidget(self.task_combo_box)
        h1_layout.addWidget(text_label)
        h1_layout.addWidget(self.text_combo_box)
        h1_layout.addWidget(self.raw_btn)
        h1_layout.addWidget(self.preproc_btn)
        h1_layout.addWidget(self.adv_preproc_btn)
        h1_layout.addWidget(self.adv_preproc_sentence_btn)
        h1_layout.addStretch()


        self.neatly_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.neatly_slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.neatly_slider.setGeometry(30, 40, 100, 30)
        self.neatly_slider.setMinimum(20)
        self.neatly_slider.setMaximum(60)
        self.neatly_slider.setValue(20)
        self.neatly_slider.valueChanged[int].connect(self.tab1_neatly_slider_change_value)
        self.neatly_text = QtGui.QLabel(str(self.neatly_slider.value()))

        h2_layout.addWidget(QtGui.QLabel("Printing neatly"))
        h2_layout.addWidget(self.neatly_slider)
        h2_layout.addWidget(self.neatly_text)
        h2_layout.addStretch()

        self.corpus_text = QtGui.QTextEdit()
        self.wiki_text = QtGui.QTextEdit()
        self.substring = QtGui.QTextEdit()

        v1_layout = QtGui.QVBoxLayout()
        v2_layout = QtGui.QVBoxLayout()

        v1_layout.addLayout(h1_layout)
        v1_layout.addWidget(self.corpus_text)
        v1_layout.addWidget(self.wiki_text)

        v2_layout.addLayout(h2_layout)
        v2_layout.addWidget(self.substring, stretch=2)

        self.corpus_length_label = QtGui.QLabel("Corpus length")
        self.substring_length_label  = QtGui.QLabel("LCS Length")
        self.pieChart = Plotting.init_pieChart()
        self.pieChartCanvas = FigureCanvas(self.pieChart)
        self.pieChartCanvas.draw()

        v2_layout.addWidget(self.corpus_length_label)
        v2_layout.addWidget(self.substring_length_label)
        v2_layout.addWidget(self.pieChartCanvas)
        v2_layout.addStretch(stretch=1)

        h_layout.addLayout(v1_layout, stretch=2)
        h_layout.addLayout(v2_layout, stretch=1)

        # v_layout.addLayout(h1_layout)

         # v_layout.addStretch()
        self.raw_btn.setChecked(True)
        self.tab1.setLayout(h_layout)

    def tab1_task_combo_activated(self, text):
        self.statusBar().showMessage("Task: " + text + " selected.")
        index = self.text_combo_box.currentIndex()
        self.text_combo_box.clear()

        file_list = os.listdir('../corpus-20090418')
        for file in file_list:
            if "task"+str(text) in file and not "orig" in file:
                self.text_combo_box.addItem(file)

        self.text_combo_box.setCurrentIndex(index)

        self.tab1_radio_toggled(self.raw_btn)
        self.tab1_radio_toggled(self.preproc_btn)
        self.tab1_radio_toggled(self.adv_preproc_btn)
        self.tab1_radio_toggled(self.adv_preproc_sentence_btn)

    def tab1_text_combo_activated(self, text):
        self.statusBar().showMessage("Task: " + text + " selected.")
        self.tab1_radio_toggled(self.raw_btn)
        self.tab1_radio_toggled(self.preproc_btn)
        self.tab1_radio_toggled(self.adv_preproc_btn)
        self.tab1_radio_toggled(self.adv_preproc_sentence_btn)

    def tab1_radio_toggled(self, button):
        if button.text() == "Raw" and button.isChecked():
            self.change_text("raw")
            self.statusBar().showMessage("Displaying Raw Text")

        if button.text() == "PreProc" and button.isChecked():
            self.change_text("proc")
            self.statusBar().showMessage("Displaying PreProcessed Text")
        if button.text() == "Adv PreProc" and button.isChecked():
            self.change_text("adv proc")
            self.statusBar().showMessage("Displaying Advanced Preprocessed Text")
        if button.text() == "Adv PreProc And Sentence" and button.isChecked():
            self.change_text("adv proc sentence")
            self.statusBar().showMessage("Displaying Advanced Preprocessed Text with LCS sentence algorithm")

    def change_text(self, text_type):
        if text_type == "raw":
            filename = self.text_combo_box.currentText()
            file_object = open("../corpus-20090418/" + filename)
            text = file_object.read()
            self.corpus_text.setPlainText(text)
            cor_length = len(text.split(" "))
            file_object.close()

            file_object = open("../corpus-20090418/orig_task" + self.task_combo_box.currentText() + ".txt")
            text = file_object.read()
            self.wiki_text.setPlainText(text)
            file_object.close()
            length, lengthLCS, LCSLIST  = prototype.LCS("../corpus-preprocessed/" + filename[:-4] + "_preprocessed.txt",
                                                         "../corpus-20090418/orig_task" + self.task_combo_box.currentText()+ ".txt", "classic")
            self.corpus_length_label.setText("Corpus Length: "+ str(cor_length))
            self.substring_length_label.setText("LCS Length: "+ str(len(LCSLIST)))
            Plotting.update_pieChart(self.pieChart,length,lengthLCS)
            self.pieChartCanvas.draw()

            neatly = PrintingNeatly.print_neatly_greedy(LCSLIST, self.neatly_slider.value())

            self.substring.setPlainText("\n".join(neatly))
            return

        if text_type == "proc":
            filename = self.text_combo_box.currentText()
            file_object = open("../corpus-preprocessed/" + filename[:-4] + "_preprocessed.txt")
            text = file_object.read()
            self.corpus_text.setPlainText(text)
            cor_length = len(text.split(" "))
            file_object.close()

            file_object = open("../corpus-preprocessed/orig_task" + self.task_combo_box.currentText() + "_preprocessed.txt")
            text = file_object.read()
            self.wiki_text.setPlainText(text)
            file_object.close()
            length, lengthLCS, LCSLIST  = prototype.LCS("../corpus-preprocessed/" + filename[:-4] + "_preprocessed.txt",
                                                         "../corpus-preprocessed/orig_task" + self.task_combo_box.currentText() + "_preprocessed.txt", "classic")

            self.corpus_length_label.setText("Corpus Length: "+ str(cor_length))
            self.substring_length_label.setText("LCS Length: "+ str(len(LCSLIST)))
            Plotting.update_pieChart(self.pieChart,length,lengthLCS)

            neatly = PrintingNeatly.print_neatly_greedy(LCSLIST, self.neatly_slider.value())

            self.substring.setPlainText("\n".join(neatly))
            return

        if text_type == "adv proc":
            filename = self.text_combo_box.currentText()
            file_object = open("../corpus-adv_preprocessed/" + filename[:-4] + "_adv_preprocessed.txt")
            text = file_object.read()
            self.corpus_text.setPlainText(text)
            cor_length = len(text.split(" "))
            file_object.close()

            file_object = open("../corpus-adv_preprocessed/orig_task" + self.task_combo_box.currentText() + "_adv_preprocessed.txt")
            text = file_object.read()
            self.wiki_text.setPlainText(text)
            file_object.close()
            length, lengthLCS, LCSLIST  = prototype.LCS("../corpus-adv_preprocessed/" + filename[:-4] + "_adv_preprocessed.txt",
                                                         "../corpus-adv_preprocessed/orig_task" + self.task_combo_box.currentText() + "_adv_preprocessed.txt", "classic")
            

            self.corpus_length_label.setText("Corpus Length: "+ str(cor_length))
            self.substring_length_label.setText("LCS Length: "+ str(len(LCSLIST)))
            Plotting.update_pieChart(self.pieChart,length,lengthLCS)

            neatly = PrintingNeatly.print_neatly_greedy(LCSLIST, self.neatly_slider.value())

            self.substring.setPlainText("\n".join(neatly))
            return
        if text_type == "adv proc sentence":
            filename = self.text_combo_box.currentText()
            file_object = open("../corpus-adv_preprocessed/" + filename[:-4] + "_adv_preprocessed.txt")
            text = file_object.read()
            self.corpus_text.setPlainText(text)
            cor_length = len(text.split(" "))
            file_object.close()

            file_object = open("../corpus-adv_preprocessed/orig_task" + self.task_combo_box.currentText() + "_adv_preprocessed.txt")
            text = file_object.read()
            self.wiki_text.setPlainText(text)
            file_object.close()
            length, lengthLCS, LCSLIST  = prototype.LCS_Sentence("../corpus-adv_preprocessed/" + filename[:-4] + "_adv_preprocessed.txt",
                                                         "../corpus-adv_preprocessed/orig_task" + self.task_combo_box.currentText() + "_adv_preprocessed.txt", "classic")

            self.corpus_length_label.setText("Corpus Length: "+ str(cor_length))
            self.substring_length_label.setText("LCS Length: "+ str(len(LCSLIST)))
            Plotting.update_pieChart(self.pieChart,length,lengthLCS)

            neatly = PrintingNeatly.print_neatly_greedy(LCSLIST, self.neatly_slider.value())

            self.substring.setPlainText("\n".join(neatly))
            return

    def tab1_neatly_slider_change_value(self, value):
        self.neatly_text.setText(str(value))
        self.tab1_radio_toggled(self.raw_btn)
        self.tab1_radio_toggled(self.preproc_btn)
        self.tab1_radio_toggled(self.adv_preproc_btn)
        self.tab1_radio_toggled(self.adv_preproc_sentence_btn)


    def tab2UI(self):
        view = QtGui.QTableView()
        xl = pd.ExcelFile("../corpus-final09.xls")
        df = xl.parse("File list")
        model = PandasModel.PandasModel2(df, self)
        view.setModel(model)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(view)

        self.tab2.setLayout(layout)

    def tab3UI(self):
        PlotAllLCS = Plotting.plotAllLCS(self)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(PlotAllLCS)

        self.tab3.setLayout(layout)

    def tab4UI(self):
        layout = QtGui.QGridLayout()

        PlotByCat = Plotting.plotByCategory(self)
        layout.addWidget(PlotByCat)

        self.tab4.setLayout(layout)

    def tab5UI(self):
        layout = QtGui.QGridLayout()

        PlotByCat = Plotting.plotByCategory2(self)
        layout.addWidget(PlotByCat)

        self.tab5.setLayout(layout)

def main():
    app = QtGui.QApplication(sys.argv)
    lcs_ui = LCS_UI()
    lcs_ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
