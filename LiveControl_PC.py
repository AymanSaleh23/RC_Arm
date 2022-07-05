import socket, time ,json


from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    
# ------------------ Start Function Configuration --------------------------
    BaseRotationAngle = 0
    BaseLegAngle = 0
    ElbowAngle = 0
    TerminalMode = 0
    AutoMaticMode = 0
    pathNumber = 0
    pathes = []
    singlePath = [{}]
    # Start Socket Initialize
    PERIOD = 0.5
    SERVER = "192.168.1.17"
    PORT   = 8888
    # End Socket Initialize

    #setters Fuctions For 4-main Parameters
    def set_BaseRotationAngle(self):
        
        self.BaseRotationAngle = self.BASE_ROTATION_Angle_Slider.value()
        self.startFunction()
        print("Base rotaion Angle : "+str(self.BaseRotationAngle))
    def set_BaseLegAngle(self):
        self.BaseLegAngle = self.BASE_LEG_ANGLE_Slider_2.value()
        self.startFunction()
        print("Base Leg Angle : "+str(self.BaseLegAngle))
    def set_ElbowAngle(self):
        self.ElbowAngle = self.ELBOW_slider.value()     
        self.startFunction()
        print("Elbow Angle : "+str(self.ElbowAngle))
    def set_TerminalMode(self):
        if(self.TERMINALOFF.isChecked()):
            self.TerminalMode = 0
            self.startFunction()
        else:
            self.TerminalMode = 1
            self.startFunction()
        print("TerminalMode : "+str(self.TerminalMode))
    # def set_AutoMaticMode(self):
    #     if(self.Automatic_Mode_OFF.isChecked()):
    #         # self.Automatic_Mode_Save_Path_Button.setEnabled(False)
    #         self.Start_Button.setEnabled(False)
    #         self.AutoMaticMode = 0
    #     else:
    #         self.AutoMaticMode = 1
    #         # self.Automatic_Mode_Save_Path_Button.setEnabled(True)
    #         self.Start_Button.setEnabled(True)

    #     print("AutoMaticMode : "+str(self.AutoMaticMode))

        
    # Add path Function SAVE FUNCTION at UI
    def addpathFunction(self):

       if(self.AutoMaticMode == 1):
           print("AutoMaticMode is " + str(self.AutoMaticMode))
           print("Add Path Function Start")
           
           path= {'Base_Rotation_Angle':self.BaseRotationAngle,
                  'Base_Leg_Angle':self.BaseLegAngle,
                  'Elbow_Angle':self.ElbowAngle,
                  'Terminal_Mode':self.TerminalMode,
                  'AutoMatic_Mode':self.AutoMaticMode}
           self.pathes.append(path)
           self.pathNumber = int(self.pathNumber+1)
           self.resetDataFunction()
           self.startFunction()
           print('Number of Pathes = ' + str(len(self.pathes)))
        
            

    # Manual Path Function
    def singlePathFunction(self):
         if(self.AutoMaticMode==0):   
            
            print("AutoMaticMode is " + str(self.AutoMaticMode))
            print('Manual Mode')
            path= {'Base_Rotation_Angle':self.BaseRotationAngle,
                   'Base_Leg_Angle':self.BaseLegAngle,
                   'Elbow_Angle':self.ElbowAngle,
                   'Terminal_Mode':self.TerminalMode,
                   'AutoMatic_Mode':self.AutoMaticMode}
            self.singlePath.append(path)   
            
    # Reset Function
    def resetDataFunction(self):
        print("Done, Data successfully Added ")
        self.BaseRotationAngle = 0
        self.BaseLegAngle = 0
        self.ElbowAngle = 0
        self.TerminalMode = 0
        self.BASE_ROTATION_Angle_Slider.setValue(0)
        self.BASE_LEG_ANGLE_Slider_2.setValue(60)
        self.ELBOW_slider.setValue(0)
        self.TERMINALOFF.setChecked(True)
        
    # Reset All Function
    def ResetAll(self):
        print("Done, All Data Reseted")
        self.BaseRotationAngle = 0
        self.BaseLegAngle = 0
        self.ElbowAngle = 0
        self.TerminalMode = 0
        self.BASE_ROTATION_Angle_Slider.setValue(0)
        self.BASE_LEG_ANGLE_Slider_2.setValue(90)
        self.ELBOW_slider.setValue(0)
        self.TERMINALOFF.setChecked(True)
        self.pathes.clear()
        self.startFunction()


    # Start Function

    def startFunction(self):
        self.singlePathFunction()
        print("Start Operation With Socket")
        count= 0
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while count<1:

            count = count+1
            #create a socket
            try:
                #connect this socket to the server(192.168.1.7).
                s.connect((self.SERVER,self.PORT))
                if(self.AutoMaticMode==1):
                       msgJSON = ""
                       if(len(self.pathes) != 0):
                           msgJSON = json.dumps(self.pathes[-1])
                           s.sendall(bytes(msgJSON,'utf-8'))
                           print(bytes(msgJSON,'utf-8'))
                       elif(len(self.pathes)==0):
                           msgJSON = json.dumps(self.pathes)
                           s.sendall(bytes(msgJSON,'utf-8'))
                           print(bytes(msgJSON,'utf-8'))
                elif(self.AutoMaticMode==0):
                    if(len(self.singlePath)!=0):
                        msgJSON = json.dumps(self.singlePath[-1])
                        s.sendall(bytes(msgJSON,'utf-8'))
                        print(bytes(msgJSON,'utf-8'))
                    
                # msgJSON = json.dumps((AutoMaticMode==0) if singlePath else pathes)
                #send request.
                
                #receive responses.
                data = s.recv(1024)
                #Handle responses.
                notificationReply = data.decode()
                #notification reply
                print(notificationReply)
                s.close()
            except Exception as ex:
                print("connection Error")
                time.sleep(2)
                continue
        s.close()

        
    # Stop Function
    def stopFunction(self,):
        print("Operation stoped, Socket closed")
        #close the Socket.
       # s.close()
   
    # Function to send data in run time just in manual moad
    def isManual(self):
        
       if self.AutoMaticMode==0:
              self.BASE_ROTATION_Angle_Slider.valueChanged['int'].connect(self.startFunction)
              self.BASE_LEG_ANGLE_Slider_2.valueChanged['int'].connect(self.startFunction)
              self.ELBOW_slider.valueChanged['int'].connect(self.startFunction)
              self.TERMINALOFF.toggled.connect(self.startFunction)
              print("----------------------------" + str(self.AutoMaticMode)) 
       else:
             print("-***********************-" + str(self.AutoMaticMode)) 
      
				
     
      

      
    # Function to start Automatic pathes on tapped
    def startOperation(self):
        
        print("Start Operation On Tapped Function  With Socket")
        count= 0
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while count<1:

            count = count+1
            #create a socket
            try:
                #connect this socket to the server(192.168.1.7).
                s.connect((self.SERVER,self.PORT))
                if(self.AutoMaticMode==1):
                    msgJSON = json.dumps("1")
                    s.sendall(bytes(msgJSON,'utf-8'))
                    print(bytes(msgJSON,'utf-8'))
                elif(self.AutoMaticMode==0):
                    msgJSON = json.dumps(self.singlePath[-1])
                    s.sendall(bytes(msgJSON,'utf-8'))
                    print(bytes(msgJSON,'utf-8'))
                # msgJSON = json.dumps((AutoMaticMode==0) if singlePath else pathes)
                #send request.
                
                #receive responses.
                data = s.recv(1024)
                #Handle responses.
                notificationReply = data.decode()
                #notification reply
                print(notificationReply)
                s.close()
            except Exception as ex:
                print("connection Error")
                time.sleep(2)
                continue
        s.close()
# ------------------ End Function Configuration --------------------------

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(570, 480)
        MainWindow.setMinimumSize(QtCore.QSize(570, 480))
        MainWindow.setMaximumSize(QtCore.QSize(570, 480))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(570, 480))
        self.centralwidget.setMaximumSize(QtCore.QSize(570, 480))
        self.centralwidget.setObjectName("centralwidget")
        # self.Stop_Button = QtWidgets.QPushButton(self.centralwidget)
#         self.Stop_Button.setGeometry(QtCore.QRect(220, 480, 121, 31))
#         self.Stop_Button.setLayoutDirection(QtCore.Qt.RightToLeft)
#         self.Stop_Button.setAutoFillBackground(False)
#         self.Stop_Button.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(139, 243, 82, 255), stop:1 rgba(255, 255, 255, 0));\n"
# "font: 14pt \"Arial\";\n"
# "border-color: rgb(255, 0, 0);\n"
# "color: rgb(85, 170, 0);")
#         self.Stop_Button.setAutoRepeat(False)
#         self.Stop_Button.setFlat(True)
#         self.Stop_Button.setObjectName("Stop_Button")
        self.ELBOW_Frame = QtWidgets.QFrame(self.centralwidget)
        self.ELBOW_Frame.setEnabled(True)
        self.ELBOW_Frame.setGeometry(QtCore.QRect(0, 200, 611, 71))
        self.ELBOW_Frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ELBOW_Frame.setStyleSheet("")
        self.ELBOW_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.ELBOW_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ELBOW_Frame.setObjectName("ELBOW_Frame")
        self.ELBOW_slider = QtWidgets.QSlider(self.ELBOW_Frame)
        self.ELBOW_slider.setGeometry(QtCore.QRect(200, 20, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ELBOW_slider.setFont(font)
        self.ELBOW_slider.setAccessibleDescription("")
        self.ELBOW_slider.setAutoFillBackground(False)
        self.ELBOW_slider.setMinimum(0)
        self.ELBOW_slider.setMaximum(180)
        self.ELBOW_slider.setSingleStep(0)
        self.ELBOW_slider.setPageStep(0)
        self.ELBOW_slider.setProperty("value", 1)
        self.ELBOW_slider.setSliderPosition(1)
        self.ELBOW_slider.setTracking(True)
        self.ELBOW_slider.setOrientation(QtCore.Qt.Horizontal)
        self.ELBOW_slider.setInvertedAppearance(False)
        self.ELBOW_slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.ELBOW_slider.setTickInterval(7)
        self.ELBOW_slider.setObjectName("ELBOW_slider")
        self.ELBOW_LCDNumber = QtWidgets.QLCDNumber(self.ELBOW_Frame)
        self.ELBOW_LCDNumber.setEnabled(True)
        self.ELBOW_LCDNumber.setGeometry(QtCore.QRect(490, 20, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.ELBOW_LCDNumber.setFont(font)
        self.ELBOW_LCDNumber.setStatusTip("")
        self.ELBOW_LCDNumber.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ELBOW_LCDNumber.setAutoFillBackground(False)
        self.ELBOW_LCDNumber.setFrameShape(QtWidgets.QFrame.Panel)
        self.ELBOW_LCDNumber.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ELBOW_LCDNumber.setLineWidth(2)
        self.ELBOW_LCDNumber.setMidLineWidth(0)
        self.ELBOW_LCDNumber.setSmallDecimalPoint(False)
        self.ELBOW_LCDNumber.setDigitCount(3)
        self.ELBOW_LCDNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.ELBOW_LCDNumber.setProperty("value", 0.0)
        self.ELBOW_LCDNumber.setObjectName("ELBOW_LCDNumber")
        self.ELBOW_Label = QtWidgets.QLabel(self.ELBOW_Frame)
        self.ELBOW_Label.setGeometry(QtCore.QRect(0, 20, 135, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.ELBOW_Label.setFont(font)
        self.ELBOW_Label.setStyleSheet("")
        self.ELBOW_Label.setTextFormat(QtCore.Qt.RichText)
        self.ELBOW_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.ELBOW_Label.setWordWrap(False)
        self.ELBOW_Label.setObjectName("ELBOW_Label")
#         self.Start_Button = QtWidgets.QPushButton(self.centralwidget)
#         self.Start_Button.setGeometry(QtCore.QRect(110, 420, 121, 31))
#         self.Start_Button.setLayoutDirection(QtCore.Qt.RightToLeft)
#         self.Start_Button.setAutoFillBackground(False)
#         self.Start_Button.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(98, 82, 243, 255), stop:1 rgba(255, 255, 255, 0));\n"
# "font: 14pt \"Arial\";\n"
# "border-color: rgb(255, 0, 0);\n"
# "color: rgb(0, 0, 127);\n"
# "")
        # self.Start_Button.setAutoRepeat(False)
        # self.Start_Button.setFlat(True)
        # self.Start_Button.setEnabled(False)
        # self.Start_Button.setObjectName("Start_Button")
        self.BASE_ROTATION_Angle_Frame = QtWidgets.QFrame(self.centralwidget)
        self.BASE_ROTATION_Angle_Frame.setEnabled(True)
        self.BASE_ROTATION_Angle_Frame.setGeometry(QtCore.QRect(-1, 20, 611, 71))
        self.BASE_ROTATION_Angle_Frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.BASE_ROTATION_Angle_Frame.setStyleSheet("")
        self.BASE_ROTATION_Angle_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BASE_ROTATION_Angle_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BASE_ROTATION_Angle_Frame.setObjectName("BASE_ROTATION_Angle_Frame")
        self.BASE_ROTATION_Angle_Slider = QtWidgets.QSlider(self.BASE_ROTATION_Angle_Frame)
        self.BASE_ROTATION_Angle_Slider.setGeometry(QtCore.QRect(200, 20, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.BASE_ROTATION_Angle_Slider.setFont(font)
        self.BASE_ROTATION_Angle_Slider.setAccessibleDescription("")
        self.BASE_ROTATION_Angle_Slider.setAutoFillBackground(False)
        self.BASE_ROTATION_Angle_Slider.setMinimum(0)
        self.BASE_ROTATION_Angle_Slider.setMaximum(180)
        self.BASE_ROTATION_Angle_Slider.setSliderPosition(0)
        self.BASE_ROTATION_Angle_Slider.setTracking(True)
        self.BASE_ROTATION_Angle_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.BASE_ROTATION_Angle_Slider.setInvertedAppearance(False)
        self.BASE_ROTATION_Angle_Slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.BASE_ROTATION_Angle_Slider.setTickInterval(1)
        self.BASE_ROTATION_Angle_Slider.setObjectName("BASE_ROTATION_Angle_Slider")
        self.BASE_ROTATION_Angle_LCDNumber = QtWidgets.QLCDNumber(self.BASE_ROTATION_Angle_Frame)
        self.BASE_ROTATION_Angle_LCDNumber.setEnabled(True)
        self.BASE_ROTATION_Angle_LCDNumber.setGeometry(QtCore.QRect(490, 20, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.BASE_ROTATION_Angle_LCDNumber.setFont(font)
        self.BASE_ROTATION_Angle_LCDNumber.setStatusTip("")
        self.BASE_ROTATION_Angle_LCDNumber.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.BASE_ROTATION_Angle_LCDNumber.setAutoFillBackground(False)
        self.BASE_ROTATION_Angle_LCDNumber.setFrameShape(QtWidgets.QFrame.Panel)
        self.BASE_ROTATION_Angle_LCDNumber.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BASE_ROTATION_Angle_LCDNumber.setLineWidth(3)
        self.BASE_ROTATION_Angle_LCDNumber.setDigitCount(3)
        self.BASE_ROTATION_Angle_LCDNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.BASE_ROTATION_Angle_LCDNumber.setProperty("value", 0.0)
        self.BASE_ROTATION_Angle_LCDNumber.setObjectName("BASE_ROTATION_Angle_LCDNumber")
        self.BASE_ROTATION_Angle_Label = QtWidgets.QLabel(self.BASE_ROTATION_Angle_Frame)
        self.BASE_ROTATION_Angle_Label.setGeometry(QtCore.QRect(0, 20, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.BASE_ROTATION_Angle_Label.setFont(font)
        self.BASE_ROTATION_Angle_Label.setStyleSheet("")
        self.BASE_ROTATION_Angle_Label.setTextFormat(QtCore.Qt.RichText)
        self.BASE_ROTATION_Angle_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.BASE_ROTATION_Angle_Label.setWordWrap(False)
        self.BASE_ROTATION_Angle_Label.setObjectName("BASE_ROTATION_Angle_Label")
        self.HorizontalDivider03 = QtWidgets.QLineEdit(self.centralwidget)
        self.HorizontalDivider03.setEnabled(False)
        self.HorizontalDivider03.setGeometry(QtCore.QRect(-10, 90, 591, 16))
        self.HorizontalDivider03.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.HorizontalDivider03.setObjectName("HorizontalDivider03")
        self.Reset_Button = QtWidgets.QPushButton(self.centralwidget)
        self.Reset_Button.setGeometry(QtCore.QRect(225, 410, 121, 31))
        self.Reset_Button.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.Reset_Button.setAutoFillBackground(False)
        self.Reset_Button.setStyleSheet("\n"
"font: 14pt \"Arial\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 82, 82, 255), stop:1 rgba(255, 255, 255, 0));\n"
"color: rgb(255, 0, 0);")
        self.Reset_Button.setAutoRepeat(False)
        self.Reset_Button.setFlat(True)
        self.Reset_Button.setObjectName("Reset_Button")
        self.TERMINAL_Frame = QtWidgets.QFrame(self.centralwidget)
        self.TERMINAL_Frame.setEnabled(True)
        self.TERMINAL_Frame.setGeometry(QtCore.QRect(0, 290, 611, 71))
        self.TERMINAL_Frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.TERMINAL_Frame.setStyleSheet("")
        self.TERMINAL_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TERMINAL_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TERMINAL_Frame.setObjectName("TERMINAL_Frame")
        self.TERMINAL_Label = QtWidgets.QLabel(self.TERMINAL_Frame)
        self.TERMINAL_Label.setGeometry(QtCore.QRect(0, 20, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.TERMINAL_Label.setFont(font)
        self.TERMINAL_Label.setStyleSheet("")
        self.TERMINAL_Label.setTextFormat(QtCore.Qt.RichText)
        self.TERMINAL_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.TERMINAL_Label.setWordWrap(False)
        self.TERMINAL_Label.setObjectName("TERMINAL_Label")
        self.TERMINALON = QtWidgets.QRadioButton(self.TERMINAL_Frame)
        self.TERMINALON.setGeometry(QtCore.QRect(150, 20, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.TERMINALON.setFont(font)
        self.TERMINALON.setTabletTracking(False)
        self.TERMINALON.setChecked(False)
        self.TERMINALON.setObjectName("TERMINALON")
        self.TERMINALOFF = QtWidgets.QRadioButton(self.TERMINAL_Frame)
        self.TERMINALOFF.setGeometry(QtCore.QRect(290, 20, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.TERMINALOFF.setFont(font)
        self.TERMINALOFF.setTabletTracking(False)
        self.TERMINALOFF.setChecked(True)
        self.TERMINALOFF.setObjectName("TERMINALOFF")
        self.HorizontalDivider02 = QtWidgets.QLineEdit(self.centralwidget)
        self.HorizontalDivider02.setEnabled(False)
        self.HorizontalDivider02.setGeometry(QtCore.QRect(-10, 0, 591, 16))
        self.HorizontalDivider02.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.HorizontalDivider02.setObjectName("HorizontalDivider02")
        # self.HorizontalDivider01 = QtWidgets.QLineEdit(self.centralwidget)
        # self.HorizontalDivider01.setEnabled(False)
        # self.HorizontalDivider01.setGeometry(QtCore.QRect(-10, 360, 591, 16))
        # self.HorizontalDivider01.setStyleSheet("background-color: rgb(125, 125, 125);")
        # self.HorizontalDivider01.setObjectName("HorizontalDivider01")
        self.HorizontalDivider05 = QtWidgets.QLineEdit(self.centralwidget)
        self.HorizontalDivider05.setEnabled(False)
        self.HorizontalDivider05.setGeometry(QtCore.QRect(-10, 270, 591, 16))
        self.HorizontalDivider05.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.HorizontalDivider05.setObjectName("HorizontalDivider05")
        self.BASE_LEG_ANGLE_frame = QtWidgets.QFrame(self.centralwidget)
        self.BASE_LEG_ANGLE_frame.setEnabled(True)
        self.BASE_LEG_ANGLE_frame.setGeometry(QtCore.QRect(0, 110, 611, 71))
        self.BASE_LEG_ANGLE_frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.BASE_LEG_ANGLE_frame.setStyleSheet("")
        self.BASE_LEG_ANGLE_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.BASE_LEG_ANGLE_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BASE_LEG_ANGLE_frame.setObjectName("BASE_LEG_ANGLE_frame")
        self.BASE_LEG_ANGLE_Slider_2 = QtWidgets.QSlider(self.BASE_LEG_ANGLE_frame)
        self.BASE_LEG_ANGLE_Slider_2.setGeometry(QtCore.QRect(200, 20, 261, 31))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.BASE_LEG_ANGLE_Slider_2.setFont(font)
        self.BASE_LEG_ANGLE_Slider_2.setAccessibleDescription("")
        self.BASE_LEG_ANGLE_Slider_2.setAutoFillBackground(False)
        self.BASE_LEG_ANGLE_Slider_2.setMinimum(60)
        self.BASE_LEG_ANGLE_Slider_2.setMaximum(120)
        self.BASE_LEG_ANGLE_Slider_2.setSingleStep(0)
        self.BASE_LEG_ANGLE_Slider_2.setPageStep(1)
        self.BASE_LEG_ANGLE_Slider_2.setProperty("value", 60)
        self.BASE_LEG_ANGLE_Slider_2.setSliderPosition(60)
        self.BASE_LEG_ANGLE_Slider_2.setOrientation(QtCore.Qt.Horizontal)
        self.BASE_LEG_ANGLE_Slider_2.setInvertedAppearance(False)
        self.BASE_LEG_ANGLE_Slider_2.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.BASE_LEG_ANGLE_Slider_2.setTickInterval(2)
        self.BASE_LEG_ANGLE_Slider_2.setObjectName("BASE_LEG_ANGLE_Slider_2")
        self.BASE_LEG_ANGLE_LCDNumber = QtWidgets.QLCDNumber(self.BASE_LEG_ANGLE_frame)
        self.BASE_LEG_ANGLE_LCDNumber.setEnabled(True)
        self.BASE_LEG_ANGLE_LCDNumber.setGeometry(QtCore.QRect(490, 20, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.BASE_LEG_ANGLE_LCDNumber.setFont(font)
        self.BASE_LEG_ANGLE_LCDNumber.setStatusTip("")
        self.BASE_LEG_ANGLE_LCDNumber.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.BASE_LEG_ANGLE_LCDNumber.setAutoFillBackground(False)
        self.BASE_LEG_ANGLE_LCDNumber.setFrameShape(QtWidgets.QFrame.Panel)
        self.BASE_LEG_ANGLE_LCDNumber.setFrameShadow(QtWidgets.QFrame.Raised)
        self.BASE_LEG_ANGLE_LCDNumber.setLineWidth(2)
        self.BASE_LEG_ANGLE_LCDNumber.setMidLineWidth(0)
        self.BASE_LEG_ANGLE_LCDNumber.setSmallDecimalPoint(False)
        self.BASE_LEG_ANGLE_LCDNumber.setDigitCount(3)
        self.BASE_LEG_ANGLE_LCDNumber.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.BASE_LEG_ANGLE_LCDNumber.setProperty("value", 60.0)
        self.BASE_LEG_ANGLE_LCDNumber.setProperty("intValue", 60)
        self.BASE_LEG_ANGLE_LCDNumber.setObjectName("BASE_LEG_ANGLE_LCDNumber")
        self.BASE_LEG_ANGLE_label = QtWidgets.QLabel(self.BASE_LEG_ANGLE_frame)
        self.BASE_LEG_ANGLE_label.setGeometry(QtCore.QRect(0, 20, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.BASE_LEG_ANGLE_label.setFont(font)
        self.BASE_LEG_ANGLE_label.setStyleSheet("")
        self.BASE_LEG_ANGLE_label.setTextFormat(QtCore.Qt.RichText)
        self.BASE_LEG_ANGLE_label.setAlignment(QtCore.Qt.AlignCenter)
        self.BASE_LEG_ANGLE_label.setWordWrap(False)
        self.BASE_LEG_ANGLE_label.setObjectName("BASE_LEG_ANGLE_label")
        self.HorizontalDivider04 = QtWidgets.QLineEdit(self.centralwidget)
        self.HorizontalDivider04.setEnabled(False)
        self.HorizontalDivider04.setGeometry(QtCore.QRect(-10, 180, 591, 16))
        self.HorizontalDivider04.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.HorizontalDivider04.setObjectName("HorizontalDivider04")
        self.HorizontalDivider06 = QtWidgets.QLineEdit(self.centralwidget)
        self.HorizontalDivider06.setEnabled(False)
        self.HorizontalDivider06.setGeometry(QtCore.QRect(-10, 360, 591, 16))
        self.HorizontalDivider06.setStyleSheet("background-color: rgb(125, 125, 125);")
        self.HorizontalDivider06.setObjectName("HorizontalDivider06")
        # self.Automatic_Mode_Frame = QtWidgets.QFrame(self.centralwidget)
        # self.Automatic_Mode_Frame.setEnabled(True)
        # self.Automatic_Mode_Frame.setGeometry(QtCore.QRect(0, 370, 611, 71))
        # self.Automatic_Mode_Frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        # self.Automatic_Mode_Frame.setStyleSheet("")
        # self.Automatic_Mode_Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.Automatic_Mode_Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.Automatic_Mode_Frame.setObjectName("Automatic_Mode_Frame")
        # self.Automatic_Mode_Label = QtWidgets.QLabel(self.Automatic_Mode_Frame)
        # self.Automatic_Mode_Label.setGeometry(QtCore.QRect(0, 20, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        # self.Automatic_Mode_Label.setFont(font)
        # self.Automatic_Mode_Label.setStyleSheet("")
        # self.Automatic_Mode_Label.setTextFormat(QtCore.Qt.RichText)
        # self.Automatic_Mode_Label.setAlignment(QtCore.Qt.AlignCenter)
        # self.Automatic_Mode_Label.setWordWrap(False)
        # self.Automatic_Mode_Label.setObjectName("Automatic_Mode_Label")
        #self.Automatic_Mode_ON = QtWidgets.QRadioButton(self.Automatic_Mode_Frame)
        #self.Automatic_Mode_ON.setGeometry(QtCore.QRect(150, 20, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        # self.Automatic_Mode_ON.setFont(font)
        # self.Automatic_Mode_ON.setTabletTracking(False)
        # self.Automatic_Mode_ON.setChecked(False)
        # self.Automatic_Mode_ON.setObjectName("Automatic_Mode_ON")
      #  self.Automatic_Mode_OFF = QtWidgets.QRadioButton(self.Automatic_Mode_Frame)
        # self.Automatic_Mode_OFF.setGeometry(QtCore.QRect(290, 20, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        # self.Automatic_Mode_OFF.setFont(font)
        # self.Automatic_Mode_OFF.setTabletTracking(False)
        # self.Automatic_Mode_OFF.setChecked(True)
        # self.Automatic_Mode_OFF.setObjectName("Automatic_Mode_OFF")
        # self.Automatic_Mode_Save_Path_Button = QtWidgets.QPushButton(self.Automatic_Mode_Frame)
#         self.Automatic_Mode_Save_Path_Button.setGeometry(QtCore.QRect(390, 20, 121, 31))
#         self.Automatic_Mode_Save_Path_Button.setLayoutDirection(QtCore.Qt.RightToLeft)
#         self.Automatic_Mode_Save_Path_Button.setAutoFillBackground(False)
#         self.Automatic_Mode_Save_Path_Button.setStyleSheet("\n"
# "font: 14pt \"Arial\";\n"
# "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(243, 82, 82, 255), stop:1 rgba(255, 255, 255, 0));\n"
# " \n"
# "color: rgb(132, 0, 2);")
#         self.Automatic_Mode_Save_Path_Button.setAutoRepeat(False)
#         self.Automatic_Mode_Save_Path_Button.setFlat(False)
#         self.Automatic_Mode_Save_Path_Button.setObjectName("Automatic_Mode_Save_Path_Button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 570, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.BASE_ROTATION_Angle_Slider.valueChanged['int'].connect(self.BASE_ROTATION_Angle_LCDNumber.display)
        self.BASE_LEG_ANGLE_Slider_2.valueChanged['int'].connect(self.BASE_LEG_ANGLE_LCDNumber.display)
        self.ELBOW_slider.valueChanged['int'].connect(self.ELBOW_LCDNumber.display)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
# START  Widget Function Sync ----------------------------------------------
        # connect Sliders and RadiButtons with its variables
        self.BASE_ROTATION_Angle_Slider.valueChanged['int'].connect(self.set_BaseRotationAngle)
        self.BASE_LEG_ANGLE_Slider_2.valueChanged['int'].connect(self.set_BaseLegAngle)
        self.ELBOW_slider.valueChanged['int'].connect(self.set_ElbowAngle)
        self.TERMINALOFF.toggled.connect(self.set_TerminalMode)
        # self.Automatic_Mode_OFF.toggled.connect(self.set_AutoMaticMode)
        # if(self.AutoMaticMode == 0):
        #     self.Automatic_Mode_Save_Path_Button.setEnabled(False)
        #     self.Automatic_Mode_OFF.toggled.connect(self.isManual)

        # Save path button Function 
        # self.Automatic_Mode_Save_Path_Button.clicked.connect(self.addpathFunction)
        # Reset Button Function
        self.Reset_Button.clicked.connect(self.ResetAll)
        # Start Button Function 
        # self..clicked.connect(self.startOperation)
        # Handling Sending Operation at run time using sliders and radio buttons
        # self.Automatic_Mode_OFF.toggled.connect(self.isManual)
        # self.Automatic_Mode_ON.setChecked(True)
        

# END  Widget Function Sync ----------------------------------------------

   
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Live Control"))
      #  self.Stop_Button.setText(_translate("MainWindow", "Stop"))
        self.ELBOW_slider.setToolTip(_translate("MainWindow", "BASE_ROTATION_Angle_Slider"))
        self.ELBOW_LCDNumber.setToolTip(_translate("MainWindow", "BASE_ROTATION_Angle_LCDNumber"))
        self.ELBOW_Label.setToolTip(_translate("MainWindow", "BASE_ROTATION_Angle"))
        self.ELBOW_Label.setText(_translate("MainWindow", "ELBOW ANGLE"))
        # self.Start_Button.setText(_translate("MainWindow", "Start"))
        self.BASE_ROTATION_Angle_Label.setText(_translate("MainWindow", "BASE ROTATION  ANGLE"))
        self.Reset_Button.setText(_translate("MainWindow", "Reset"))
        self.TERMINAL_Label.setToolTip(_translate("MainWindow", "BASE_ROTATION_Angle"))
        self.TERMINAL_Label.setText(_translate("MainWindow", "TERMINAL"))
        self.TERMINALON.setText(_translate("MainWindow", "ON"))
        self.TERMINALOFF.setText(_translate("MainWindow", "OFF"))
        self.BASE_LEG_ANGLE_Slider_2.setToolTip(_translate("MainWindow", "BASE_ROTATION_Angle_Slider"))
        self.BASE_LEG_ANGLE_LCDNumber.setToolTip(_translate("MainWindow", "BASE_ROTATION_Angle_LCDNumber"))
        self.BASE_LEG_ANGLE_label.setToolTip(_translate("MainWindow", "BASE_ROTATION_Angle"))
        self.BASE_LEG_ANGLE_label.setText(_translate("MainWindow", "BASE  LEG ANGLE"))
        # self.Automatic_Mode_Label.setToolTip(_translate("MainWindow", "BASE_ROTATION_Angle"))
        # self.Automatic_Mode_Label.setText(_translate("MainWindow", "Automatic Mode"))
        # self.Automatic_Mode_ON.setText(_translate("MainWindow", "ON"))
        # self.Automatic_Mode_OFF.setText(_translate("MainWindow", "OFF"))
        # self.Automatic_Mode_Save_Path_Button.setText(_translate("MainWindow", "Save Path"))
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    