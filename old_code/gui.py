# https://zenodo.org/record/3268501#.XelbMz7VJhE => PPG data

from cameraX import WebcamX
from deapX import DeapEegX
import cv2

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QFrame, QAction, QTabWidget, QVBoxLayout
from PyQt5.QtWidgets import QGridLayout, QDialog, QLineEdit, QFileDialog, QMenu, QMessageBox, QSizePolicy
from PyQt5.QtWidgets import QComboBox, QCheckBox
from PyQt5.QtCore import QSize, QRect, Qt, QThread, QTimer, pyqtSlot
from PyQt5.QtGui import QFont, QPixmap, QImage, QIcon

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random
import sys
import numpy as np
import time
from io import StringIO
import json
import scipy.io
import pickle

class AppMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        
        # Height, Width for QMainWindow
        self.left = 20
        self.top = 10
        self.width = 1900
        self.height = 1000
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setMinimumSize(QSize(self.width,self.height))
        self.setMaximumSize(QSize(self.width,self.height))
        # Title for QMainWindow
        self.title = "AIATUS YAPAY ZEKA VE BİLGİ TEKNOLOJİLERİ A.Ş."
        self.setWindowTitle(self.title)

        self.appWidget = AppWidget(self)
        self.setCentralWidget(self.appWidget)
        
class AppWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        # Define class
        self.webcam = WebcamX()
        self.deapEeg = DeapEegX()

        # Read config format json
        self.cf = self.deapEeg.config_load()

        # Read language format json, Current Language = TURKISH
        with open('language.json') as language_json:
            self.language = json.load(language_json)
        language_json.close()
        self.language_current = 'Turkish'
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(600,600)
        self.tab_General = QWidget()
        self.tab_EEG = QWidget()
        self.tab_PPG = QWidget()
        self.tab_Camera = QWidget()
        self.tab_EEG_Model = QWidget()
        
        # Add tabs
        self.tabs.addTab(self.tab_General,self.language['tab_General'][self.language_current])
        self.tabs.addTab(self.tab_EEG,self.language['tab_EEG'][self.language_current])
        self.tabs.addTab(self.tab_PPG,self.language['tab_PPG'][self.language_current])
        self.tabs.addTab(self.tab_Camera,self.language['tab_Camera'][self.language_current])
        self.tabs.addTab(self.tab_EEG_Model,self.language['tab_EEG_Model'][self.language_current])

        # Add tabs to widget
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        # Define QFont
        self.font = QFont()
        self.font.setPointSize(12)
        self.font.setBold(True)
        self.font.setWeight(75)

#*********************************************************************************************
# GENERAL TAB
#*********************************************************************************************
        # Define QComboBox
        self.combo_language = QComboBox(self.tab_General)
        self.combo_language.addItem("Turkish")
        self.combo_language.addItem("English")
        self.combo_language.move(50,50)
        self.combo_language.activated[str].connect(self.on_combo_language_changed)
        
#*********************************************************************************************
# EEG TAB
#*********************************************************************************************
        # Define QPushButtons
        self.pushButton_EEG_start = QPushButton(self.language["pushButton_EEG_start"][self.language_current],self.tab_EEG)
        self.pushButton_EEG_start.setGeometry(QRect(200, 20, 150, 50))
        self.pushButton_EEG_start.setFont(self.font)
        self.pushButton_EEG_start.clicked.connect(self.on_pushButton_EEG_start_clicked)

        self.pushButton_EEG_stop = QPushButton(self.language["pushButton_EEG_stop"][self.language_current],self.tab_EEG)
        self.pushButton_EEG_stop.setGeometry(QRect(550, 20, 150, 50))
        self.pushButton_EEG_stop.setFont(self.font)
        self.pushButton_EEG_stop.clicked.connect(self.on_pushButton_EEG_stop_clicked)
        
#*********************************************************************************************
# EEG MODEL TAB
#*********************************************************************************************
        # Define QPushButtons
        self.pushButton_EEG_Model_process_raw_data = QPushButton(
            self.language["pushButton_EEG_Model_process_raw_data"][self.language_current],
            self.tab_EEG_Model)
        self.pushButton_EEG_Model_process_raw_data.setGeometry(QRect(50, 50, 200, 50))
        self.pushButton_EEG_Model_process_raw_data.setFont(self.font)
        self.pushButton_EEG_Model_process_raw_data.clicked.connect(self.on_pushButton_EEG_start_clicked)
        
        self.pushButton_EEG_Model_add_class_label = QPushButton(
            self.language["pushButton_EEG_Model_add_class_label"][self.language_current],
            self.tab_EEG_Model)
        self.pushButton_EEG_Model_add_class_label.setGeometry(QRect(50, 125, 200, 50))
        self.pushButton_EEG_Model_add_class_label.setFont(self.font)
        self.pushButton_EEG_Model_add_class_label.clicked.connect(self.on_pushButton_EEG_start_clicked)
        
        self.pushButton_EEG_Model_train = QPushButton(
            self.language["pushButton_EEG_Model_train"][self.language_current],
            self.tab_EEG_Model)
        self.pushButton_EEG_Model_train.setGeometry(QRect(50, 275, 200, 50))
        self.pushButton_EEG_Model_train.setFont(self.font)
        self.pushButton_EEG_Model_train.clicked.connect(self.on_pushButton_EEG_start_clicked)
        
        self.pushButton_EEG_Model_test = QPushButton(
            self.language["pushButton_EEG_Model_test"][self.language_current],
            self.tab_EEG_Model)
        self.pushButton_EEG_Model_test.setGeometry(QRect(50, 350, 200, 50))
        self.pushButton_EEG_Model_test.setFont(self.font)
        self.pushButton_EEG_Model_test.clicked.connect(self.on_pushButton_EEG_start_clicked)
        
        self.pushButton_EEG_Model_result = QPushButton(
            self.language["pushButton_EEG_Model_result"][self.language_current],
            self.tab_EEG_Model)
        self.pushButton_EEG_Model_result.setGeometry(QRect(50, 425, 200, 50))
        self.pushButton_EEG_Model_result.setFont(self.font)
        self.pushButton_EEG_Model_result.clicked.connect(self.on_pushButton_EEG_start_clicked)
        
        # Define QLabel
        self.label_EEG_Model_select = QLabel(self.tab_EEG_Model)
        self.label_EEG_Model_select.setText(self.language["label_EEG_Model_select"][self.language_current])
        self.label_EEG_Model_select.setGeometry(QRect(50, 200, 125, 50))
        self.label_EEG_Model_select.setFont(self.font)
        # Define QComboBox
        self.combo_EEG_Model_select = QComboBox(self.tab_EEG_Model)
        self.combo_EEG_Model_select.addItem("SVM")
        self.combo_EEG_Model_select.addItem("KNN")
        self.combo_EEG_Model_select.addItem("PCA + KNN")
        self.combo_EEG_Model_select.addItem("PCA + SVM")
        self.combo_EEG_Model_select.setGeometry(QRect(175, 200, 125, 50))
        self.combo_EEG_Model_select.setFont(self.font)
        self.combo_EEG_Model_select.activated[str].connect(self.on_combo_language_changed)
        
#*********************************************************************************************
# PPG TAB
#*********************************************************************************************
        pass
#*********************************************************************************************
# CAMERA TAB
#*********************************************************************************************
        # Define QPushButtons
        self.pushButton_camera_open = QPushButton(self.language["pushButton_camera_open"][self.language_current],self.tab_Camera)
        self.pushButton_camera_open.setGeometry(QRect(400, 50, 150, 50))
        self.pushButton_camera_open.setFont(self.font)

        self.pushButton_camera_close = QPushButton(self.language["pushButton_camera_close"][self.language_current],self.tab_Camera)
        self.pushButton_camera_close.setGeometry(QRect(200, 50, 150, 50))
        self.pushButton_camera_close.setFont(self.font)
        self.pushButton_camera_close.setEnabled(False)

        # Define QLABEL for WEBCAM frame
        self.label_img = QLabel(self.tab_Camera)
        self.label_img.setGeometry(QRect(50, 130, 640, 480))
        self.label_img.setFrameShape(QFrame.Box)
        self.label_img.setText("")

        # Define QCheckBox
        self.checkBox_face_detect = QCheckBox(self.language["checkBox_face_detect"][self.language_current],self.tab_Camera)
        self.checkBox_face_detect.setChecked(False)
        self.checkBox_face_detect.move(600, 50)

        # SIGNALS
        self.pushButton_camera_open.clicked.connect(self.on_pushButton_camera_open_clicked)
        self.pushButton_camera_close.clicked.connect(self.on_pushButton_camera_close_clicked)
        # self.checkBox_face_detect.stateChanged.connect(self.on_checkbox_face_detect_clicked)

        # Timer for update frame
        self.acquisition_timer = QTimer()
        self.acquisition_timer.timeout.connect(self.update_frame)

        # Timer for update Plot
        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plot)
         
#*********************************************************************************************
# GENERAL TAB FUNCTION
#*********************************************************************************************
    def on_combo_language_changed(self):

        self.language_current = self.combo_language.currentText()

        self.tabs.setTabText(0,self.language['tab_General'][self.language_current])
        self.tabs.setTabText(1,self.language['tab_EEG'][self.language_current])
        self.tabs.setTabText(2,self.language['tab_PPG'][self.language_current])
        self.tabs.setTabText(3,self.language['tab_Camera'][self.language_current])
        self.tabs.setTabText(4,self.language['tab_EEG_Model'][self.language_current])

        # TAB EEG
        self.pushButton_EEG_start.setText(self.language['pushButton_EEG_start'][self.language_current])
        self.pushButton_EEG_stop.setText(self.language['pushButton_EEG_stop'][self.language_current])
        # TAB EEG Model
        self.pushButton_EEG_Model_process_raw_data.setText(self.language['pushButton_EEG_Model_process_raw_data'][self.language_current])
        self.pushButton_EEG_Model_add_class_label.setText(self.language['pushButton_EEG_Model_add_class_label'][self.language_current])
        self.pushButton_EEG_Model_train.setText(self.language['pushButton_EEG_Model_train'][self.language_current])
        self.pushButton_EEG_Model_test.setText(self.language['pushButton_EEG_Model_test'][self.language_current])
        self.pushButton_EEG_Model_result.setText(self.language['pushButton_EEG_Model_result'][self.language_current])
        self.label_EEG_Model_select.setText(self.language['label_EEG_Model_select'][self.language_current])
        # TAB Camera
        self.pushButton_camera_open.setText(self.language['pushButton_camera_open'][self.language_current])
        self.pushButton_camera_close.setText(self.language['pushButton_camera_close'][self.language_current])
        self.checkBox_face_detect.setText(self.language['checkBox_face_detect'][self.language_current])
        
#*********************************************************************************************
# EEG TAB FUNCTION
#*********************************************************************************************
    def on_pushButton_EEG_start_clicked(self):
        # time plot
        self.canvas_time = Canvas(self.tab_EEG,width=9,height=8,dpi=90)
        self.canvas_time.move(75,75)
        # fft plot
        self.canvas_fft = Canvas(self.tab_EEG,width=9,height=4,dpi=90)
        self.canvas_fft.move(900,75)
        # Arousal - Valance plot
        self.canvas_AV = Canvas(self.tab_EEG,width=5,height=5,dpi=100)
        self.canvas_AV.move(900,440)

        self.plot_nUser = 'Load_initial_value' # Initial value
        self.plot_timer.start(1)

    def update_plot(self):
        
        # initial load nUser 
        if self.plot_nUser == 'Load_initial_value':
            
            self.plot_nTime = self.cf["nTime_head"]
            self.plot_nTrial = self.cf["nTrial_test_head"]-1
            self.plot_nUser  = self.cf["nUser_test_head"]
            
            filename = self.cf["raw_data_eeg_path"] + "s"+'{:02d}'.format(self.plot_nUser)+".dat"
            f = open(filename, 'rb')
            self.plot_eeg = pickle.load(f, encoding='latin1')
            print('Initial load test filename =' + str(filename))
            f.close()
            
        print(" nUser =", str(self.plot_nUser),"\n",
              "nTrial =", str(self.plot_nTrial),"\n",
              "nTime =", str(self.plot_nTime))
        
        if self.plot_nTime + self.cf["nTime_step"] < self.cf["nTime_end"]:
            
            self.canvas_time.plot_time(eeg=self.plot_eeg,tr=self.plot_nTrial,i=self.plot_nTime,cf=self.cf)
            self.canvas_fft.plot_fft(eeg=self.plot_eeg,tr=self.plot_nTrial,i=self.plot_nTime,cf=self.cf)
            self.canvas_AV.plot_AV(eeg=self.plot_eeg,tr=self.plot_nTrial)
            
            self.plot_nTime = self.plot_nTime + self.cf["nTime_step"] # increase nTime
            
        else:
            
            if self.plot_nTrial < self.cf["nTrial_test_end"]-1:
                
                self.plot_nTime = self.cf["nTime_head"] # zero nTime
                self.plot_nTrial = self.plot_nTrial + self.cf["nTrial_test_step"] # increase nTrial
                
            else:
            
                if self.plot_nUser < self.cf["nUser_test_end"]:
                
                    self.plot_nTime = self.cf["nTime_head"] # zero nTime
                    self.plot_nTrial = self.cf["nTrial_test_head"]-1 # zero nTrial
                    self.plot_nUser = self.plot_nUser + self.cf["nUser_test_step"] # increase nUser
                    
                    filename = self.cf["raw_data_eeg_path"] + "s"+'{:02d}'.format(self.plot_nUser)+".dat"
                    f = open(filename, 'rb')
                    self.plot_eeg = pickle.load(f, encoding='latin1')
                    print('Load test filename =' + str(filename))
                    f.close()
                
                else:
                    print('TEST PLOT FINISHED')
                    self.plot_nUser = 'Load_initial_value'
                    self.plot_timer.stop()
                    
    def on_pushButton_EEG_stop_clicked(self):
        self.plot_timer.stop()
        
#*********************************************************************************************
# EEG TAB FUNCTION
#*********************************************************************************************
    def on_pushButton_EEG_Model_process_raw_data_clicked(self):
        
        self.pushButton_EEG_Model_process_raw_data.setEnabled(False)
        self.pushButton_camera_close.setEnabled(True)
    
    def on_pushButton_EEG_Model_add_class_label_clicked(self):
        pass
    
    def on_pushButton_EEG_Model_train_clicked(self):
        pass
    
    def on_pushButton_EEG_Model_test_clicked(self):
        pass
    
    def on_pushButton_EEG_Model_result_clicked(self):
        pass
    
#*********************************************************************************************
# PPG TAB FUNCTION
#*********************************************************************************************
    def ppg_plot(self):
        pass
#*********************************************************************************************
# CAMERA TAB FUNCTION
#*********************************************************************************************
    def on_pushButton_camera_open_clicked(self):
        self.webcam.acquisition()
        self.acquisition_timer.start(1)
        self.pushButton_camera_open.setEnabled(False)
        self.pushButton_camera_close.setEnabled(True)
                                                       
    def on_pushButton_camera_close_clicked(self):
        self.webcam.close()
        self.acquisition_timer.stop()
        self.pushButton_camera_close.setEnabled(False)
        self.pushButton_camera_open.setEnabled(True)

    def update_frame(self):
        self.frame = self.webcam.get_frame()

        if (self.checkBox_face_detect.isChecked()==True):
            self.xBox = self.webcam.get_xBox()
            cv2.rectangle(self.frame,(self.xBox[0], self.xBox[1]),(self.xBox[0]+self.xBox[2],self.xBox[1]+self.xBox[3]),(0,255,0),2);

        self.show_frame()

    def show_frame(self):  
        QImg = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
        pixMap = QPixmap.fromImage(QImg)
        #pixMap = pixMap.scaled(320,240, Qt.KeepAspectRatio)
        self.label_img.setPixmap(pixMap)
        
class Canvas(FigureCanvas):
    def __init__(self,parent = None, width=10,height=10,dpi=100):

        fig = Figure(figsize=(width,height),dpi=dpi)
        FigureCanvas.__init__(self,fig)
        self.setParent(parent)

        #FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        #FigureCanvas.updateGeometry(self)

    def plot_time(self,eeg,tr,i,cf):
        j = 0
        for ch in cf["nChannel_ON"]:
            j = j+1
            ax = self.figure.add_subplot(len(cf["nChannel_ON"]),1,j)
            ax.clear()
            if (j==0):
                ax.set_title('EEG Data Signals')
            ax.plot(np.array(list(range(cf["nTime_step"]))),eeg['data'][tr][cf["nChannel_ON"][ch]][i:i+cf["nTime_step"]],label=ch,color= 'C'+str(j))
            ax.set_ylabel(ch)
            ax.set_ylim([-200,200])
            ax.grid()
        
        self.draw()
        self.show()

    def plot_fft(self,eeg,tr,i,cf):

        Fs = 60  # Sampling rate (60 Hz)
        ax = self.figure.add_subplot(1,1,1)
        ax.clear()
        ax.set_title('FFT Plot')
        ax.set_xlabel('Freq (Hz)')
        ax.set_ylabel('Amplitude (\u03bcV)')
        j = 0
        for ch in cf["nChannel_ON"]:
            j = j+1
            data = eeg['data'][tr][cf["nChannel_ON"][ch]][i:i+cf["nTime_step"]]
            fft_values = np.absolute(np.fft.rfft(data)) # Real amplitudes of FFT (only in postive frequencies)
            fft_freq = np.fft.rfftfreq(len(data), 1.0/Fs) # Frequencies for amplitudes in Hz
            ax.plot(fft_freq,20*np.log10(abs(fft_values)),label=ch,color= 'C'+str(j))

        ax.set_ylim([-20,100])    
        ax.grid()

        self.draw()
        self.show()

    def plot_AV(self,eeg,tr):
        ax = self.figure.add_subplot(1,1,1)
        ax.clear()
        valance = eeg['labels'][tr][0]
        arousal = eeg['labels'][tr][1]
        #print(" arousal = ", str(arousal),'\n',"valance = ", str(valance))
        ax.scatter(valance,arousal, marker='o', c='b', s=32, label='AV')
        ax.set_title('Arousal-Valance Plot')
        ax.set_xlabel('Valance')
        ax.set_ylabel('Arousal')
        ax.set_ylim([1,9]) 
        ax.set_xlim([1,9])
        ax.vlines(5,1,9,colors='r')
        ax.hlines(5,1,9,colors='r')
        ax.grid() 

        self.draw()
        self.show()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = AppMainWindow()
    w.show()
    sys.exit(app.exec_())
