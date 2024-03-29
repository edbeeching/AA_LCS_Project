"""
    The User Interfact for the plagiarism detector
    There are 5 Tabs containing:
        1. Options to compare the different texts from the corpus and their associated LCS
           LCS words are highlight in bold, the LCS text is shown of the right with options
           to change the length of the "printing neatly" and the choise to use dynamic or greedy
        2. A table with the corpus data and the scores generated from different methods
        3. A graph displaying the various scores obtains from the analysis
        4. Plots of the individual tasks and their scores
        5. Plots of the different types of plagiarism (cut, light, heavy & non) vs. their scores
"""

import os
import sys
import time
import math
import pandas as pd
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import pandas_model
import plagiarism_detector
import plotting
import printing_neatly
import prototype


#memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

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

        process_label = QtGui.QLabel("Processing:")
        self.process_combo_box = QtGui.QComboBox()
        self.process_combo_box.activated[str].connect(self.tab1_process_combo_activated)

        Corpus_list = os.listdir('../')

        self.process_combo_box.addItem("Raw")
        for folder in Corpus_list:
            if folder.find("corpus") !=-1 and folder.find('20090418') ==-1:
                process_name = folder.replace("corpus-",'')
                process_name = process_name.replace("_",' ')
                process_name = process_name.replace("preprocessed",'preprocessing')
                if os.path.isdir("../"+folder):
                    self.process_combo_box.addItem(process_name)


        algo_label = QtGui.QLabel("Algorithm:")
        self.algo_combo_box = QtGui.QComboBox()
        self.algo_combo_box.activated[str].connect(self.tab1_algo_combo_activated)
        self.algo_combo_box.addItem("LCS")
        self.algo_combo_box.addItem("LCS-Sentence")

        h1_layout.addWidget(task_label)
        h1_layout.addWidget(self.task_combo_box)
        h1_layout.addWidget(text_label)
        h1_layout.addWidget(self.text_combo_box)
        h1_layout.addWidget(self.process_combo_box)
        h1_layout.addWidget(self.algo_combo_box)
        h1_layout.addStretch()


        self.neatly_slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.neatly_slider.setFocusPolicy(QtCore.Qt.NoFocus)
        self.neatly_slider.setGeometry(30, 40, 100, 30)
        self.neatly_slider.setMinimum(20)
        self.neatly_slider.setMaximum(60)
        self.neatly_slider.setValue(20)
        self.neatly_slider.valueChanged[int].connect(self.tab1_neatly_slider_change_value)
        self.neatly_text = QtGui.QLabel(str(self.neatly_slider.value()))
        # Create an empty sting which hold the LCS text, so it can be changed dynamically with printing neatly
        self.neatly_string_list = []

        self.neatly_algo_combo_box = QtGui.QComboBox()
        self.neatly_algo_combo_box.activated[str].connect(self.tab1_neatly_algo_change)
        self.neatly_algo_combo_box.addItem("Dynamic")
        self.neatly_algo_combo_box.addItem("Greedy")

        h2_layout.addWidget(QtGui.QLabel("Printing neatly"), stretch=0)
        h2_layout.addWidget(self.neatly_slider, stretch=0)
        h2_layout.addWidget(self.neatly_algo_combo_box)
        h2_layout.addWidget(self.neatly_text, stretch=1)
        h2_layout.addStretch()

        self.corpus_text = QtGui.QTextEdit()
        self.wiki_text = QtGui.QTextEdit()
        self.substring = QtGui.QTextEdit()
        # set text to read only
        self.corpus_text.setReadOnly(True)
        self.wiki_text.setReadOnly(True)
        self.substring.setReadOnly(True)


        v1_layout = QtGui.QVBoxLayout()
        v2_layout = QtGui.QVBoxLayout()
        v2h_layout = QtGui.QHBoxLayout()
        synth_layout = QtGui.QVBoxLayout()

        v1_layout.addLayout(h1_layout)
        v1_layout.addWidget(self.corpus_text)
        v1_layout.addWidget(self.wiki_text)

        v2_layout.addLayout(h2_layout)
        v2_layout.addWidget(self.substring, stretch=3)

        self.is_plagiarised_label = QtGui.QLabel("Plagiarised: YES")
        self.corpus_length_label = QtGui.QLabel("Corpus length")
        self.substring_length_label  = QtGui.QLabel("LCS Length")
        self.plagiarised_sentences = QtGui.QLabel("9/11 Sentences plagiarised")
        self.plagiarism_score_label  = QtGui.QLabel("Running Time")
        self.running_time_label  = QtGui.QLabel("Running Time")

        self.pieChart = plotting.init_pieChart()
        self.pieChartCanvas = FigureCanvas(self.pieChart)
        self.pieChartCanvas.draw()

        self.pieChart2 = plotting.init_pieChart()
        self.pieChartCanvas2 = FigureCanvas(self.pieChart2)
        self.pieChartCanvas2.draw()

        synth_layout.addWidget(self.is_plagiarised_label)
        synth_layout.addWidget(self.corpus_length_label)
        synth_layout.addWidget(self.substring_length_label)
        synth_layout.addWidget(self.plagiarised_sentences)
        synth_layout.addWidget(self.plagiarism_score_label)
        synth_layout.addWidget(self.running_time_label)
        # synth_layout.addWidget(self.pieChartCanvas)
        # v2_layout.addStretch(stretch=1)

        v2h_layout.addLayout(synth_layout)
        v2h_layout.addWidget(self.pieChartCanvas)
        v2h_layout.addWidget(self.pieChartCanvas2)

        v2_layout.addLayout(v2h_layout, stretch=1)

        h_layout.addLayout(v1_layout,stretch=2)
        h_layout.addLayout(v2_layout,stretch=2)

        # v_layout.addLayout(h1_layout)

         # v_layout.addStretch()
        self.update_text()
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

        self.update_text()

    def tab1_text_combo_activated(self, text):
        self.statusBar().showMessage("Task: " + text + " selected.")
        self.update_text()

    def tab1_process_combo_activated(self, text):
        self.update_text()

    def tab1_algo_combo_activated(self, text):
        self.update_text()

    def get_process_folder(self,text):
        if text=='Raw' :
            return "corpus-20090418"
        path = text.replace('preprocessing', 'preprocessed')
        path = path.replace(' ', '_')
        path = 'corpus-'+path
        return path

    def get_current_process_suffix(self):
        path = self.get_process_folder(self.process_combo_box.currentText())
        file_suffix = path.replace("corpus-", "_") + ".txt"
        if path == "corpus-20090418":
            file_suffix = ".txt"
        return file_suffix

    def get_bold_text(self, lcs_text, corpus_text):
        def same_as(word1, word2):
            word1 = word1.replace(".", "")
            word1 = word1.replace(",", "")
            word2 = word2.replace(".", "")
            word2 = word2.replace(",", "")
            return word1 == word2

        index = 0
        bold_text = []
        for word in corpus_text.split():
            if index < len(lcs_text) and same_as(word, lcs_text[index]):
                bold_text.append("<b>" + word + "</b>")
                index += 1
            else:
                bold_text.append(word)
        return " ".join(bold_text)

    def score(self, lcs_text, corpus_text):
        def same_as(word1, word2):
            word1 = word1.replace(".", "")
            word1 = word1.replace(",", "")
            word2 = word2.replace(".", "")
            word2 = word2.replace(",", "")
            return word1 == word2

        index = 0
        add = False
        score = 0
        side_by_side = 1

        length = 0
        for word in corpus_text.split():
            length = length + 1
            if index < len(lcs_text) and same_as(word, lcs_text[index]):
                # bold_text.append("<b>" + word + "</b>")
                index += 1
                if add == False:
                    add = True
                    side_by_side = 1
                else:
                    side_by_side += 1
            else:
                if add == True:
                    add = False
                    score += (side_by_side * side_by_side)
                # bold_text.append(word)

        return score


    def update_text(self):
        path = self.get_process_folder(self.process_combo_box.currentText())
        algo = self.algo_combo_box.currentText()
        file_suffix = self.get_current_process_suffix()
        filename = self.text_combo_box.currentText()
        filename = filename.replace('.txt', file_suffix)
        file_object = open("../" + path + "/" + filename)

        corpus_text = file_object.read()
        # self.corpus_text.setPlainText(text)
        # self.corpus_text.setHtml(corpus_text)
        cor_length = len(corpus_text.split(" "))
        file_object.close()

        file_object = open("../" + path + "/orig_task" + self.task_combo_box.currentText() + file_suffix)
        text = file_object.read()
        self.wiki_text.setPlainText(text)
        file_object.close()

        running_time_start = time.time()

        if algo == "LCS":
            length, lengthLCS, LCSLIST = prototype.LCS("../" + path + "/" + filename,
                                                       "../" + path + "/orig_task" + self.task_combo_box.currentText() + file_suffix,
                                                       "classic")
        if algo == "LCS-Sentence":
            length, lengthLCS, LCSLIST = prototype.LCS_Sentence("../" + path + "/" + filename,
                                                                "../" + path + "/orig_task" + self.task_combo_box.currentText() + file_suffix,
                                                                "classic")
        running_time_end = time.time()
        
        running_time = int((running_time_end - running_time_start) * 1000)
        #memory_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # memory_usage = new_memory_usage
        # print("MEM = " + str(memory_usage))
        _, s2, s1 = plagiarism_detector.plagiarised_sentences(LCSLIST, corpus_text)
        plagiarism_score = plagiarism_detector.score(LCSLIST, corpus_text)
        is_plagiarised = plagiarism_detector.is_plagiarised(LCSLIST, corpus_text)
        bold_corpus_text = self.get_bold_text(LCSLIST, corpus_text)
        self.corpus_text.setHtml(bold_corpus_text)

        if  is_plagiarised:
            self.is_plagiarised_label.setText("Plagiarised: YES")
        else:
            self.is_plagiarised_label.setText("Plagiarised: NO")


        self.corpus_length_label.setText("Corpus Length:\n" + str(length))
        self.substring_length_label.setText("LCS Length:\n" + str(len(LCSLIST)))
        self.plagiarised_sentences.setText(str(s1) + "/" + str(s2) + " Sentences plagiarised")
        self.plagiarism_score_label.setText("Plagiarism Score:\n" + str(round(plagiarism_score, 2)))
        self.running_time_label.setText("Running Time:\n" + str(running_time) + "ms")
        plotting.update_pieChart(self.pieChart, 1.0, plagiarism_score, "Word grouping score")
        self.pieChartCanvas.draw()

        plotting.update_pieChart(self.pieChart2, s2, s1, "% of sentences plagiarised")
        self.pieChartCanvas2.draw()

        self.neatly_string_list = LCSLIST
        neatly = printing_neatly.print_neatly_dynamic(self.neatly_string_list, self.neatly_slider.value())

        self.substring.setPlainText("\n".join(neatly))
        return

    def tab1_neatly_algo_change(self):
        algo = self.neatly_algo_combo_box.currentText()
        if algo == "Dynamic":
            neatly = printing_neatly.print_neatly_dynamic(self.neatly_string_list, self.neatly_slider.value())
        else:
            neatly = printing_neatly.print_neatly_greedy(self.neatly_string_list, self.neatly_slider.value())
        self.substring.setPlainText("\n".join(neatly))

    def tab1_neatly_slider_change_value(self, value):
        self.neatly_text.setText(str(value))
        algo = self.neatly_algo_combo_box.currentText()
        if algo == "Dynamic":
            neatly = printing_neatly.print_neatly_dynamic(self.neatly_string_list, self.neatly_slider.value())
        else:
            neatly = printing_neatly.print_neatly_greedy(self.neatly_string_list, self.neatly_slider.value())
        self.substring.setPlainText("\n".join(neatly))
        #self.update_text()


    def tab2UI(self):
        view = QtGui.QTableView()
        xl = pd.ExcelFile("../corpus-final09.xls")
        df = xl.parse("File list")
        model = pandas_model.PandasModel2(df, self)
        view.setModel(model)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(view)

        self.tab2.setLayout(layout)

    def tab3UI(self):
        PlotAllLCS = plotting.plotAllLCS(self)
        layout = QtGui.QHBoxLayout()
        layout.addWidget(PlotAllLCS)

        self.tab3.setLayout(layout)

    def tab4UI(self):
        layout = QtGui.QGridLayout()

        PlotByCat = plotting.plotByCategory(self)
        layout.addWidget(PlotByCat)

        self.tab4.setLayout(layout)

    def tab5UI(self):
        layout = QtGui.QGridLayout()

        PlotByCat = plotting.plotByCategory2(self)
        layout.addWidget(PlotByCat)

        self.tab5.setLayout(layout)

def main():
    app = QtGui.QApplication(sys.argv)
    lcs_ui = LCS_UI()
    lcs_ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
