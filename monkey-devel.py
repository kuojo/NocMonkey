#!/usr/bin/python

import os
import os.path
import sys
from PyQt4 import QtGui, QtCore

#Initalize Stuff

clear = lambda: os.system('cls')

class Acknowledgements(object):
        def __init__(self,flatfile):
                self.flatfile = str(flatfile)
                self.initilize(self.flatfile)
                self.clipboard = QtGui.QApplication.clipboard() 

                #acks = self.write_acks()
                #self.menu(acks)

        def write_acks(self):
                acks = []
                with open(str(self.flatfile),"r") as f:
                        for line in f:
                                if line == "\n" or line == "":
                                    continue
                                acks.append(line.split(','))
                        return acks

        def add_to_acks(self, string):
                f = open(self.flatfile, "a+")
                f.write(str(string) + ",\n")
                f.close()

        def rewrite_acks(self, acks):
                f = open(self.flatfile, "w+")
                for i in range(len(acks)):
                        f.write(",".join(acks[i]))
                f.close()

        def add_to_clipboard(self, text): #Orginally I used Tk and this was nesscary
                self.clipboard.setText(str(text).rstrip("\n"))


        def is_int(self, value):
                try:
                        value=int(value)
                        return True
                except ValueError:
                        return False
        
        def nope(self):
                print "\nNot an Option\n"
                raw_input("Press enter to continue")

        def menu(self, acks):
                copied = ""
                while True:
                        clear()
                        print copied
                        print "Options: Add, Remove, Quit/Exit, Ack Number"
                        for i in range(len(acks)):
                        	print i," ", acks[i],

                        response = raw_input("\nAcknowledgement: ")
        
                        if self.is_int(response) and int(response) <= len(acks)-1:
                                self.add_to_clipboard(acks[int(response)].rstrip('\n'))
                                copied = "'%s' copied to clipboard\n" % (acks[int(response)].rstrip('\n'))
								
                        elif response.lower() == "add":
                                response = raw_input("Add what?: ")
                                self.add_to_acks(response)
                                acks.append(response + "\n")

                        elif response.lower() == "remove":
                                response = raw_input("Number to remove: ")
                                if self.is_int(response) and int(response) <= len(acks)-1:
                                        del acks[int(response)]
                                        self.rewrite_acks(acks)
                                else:
                                        self.nope()
                        
                        elif response.lower() == "quit" or response.lower() == "exit":
                                break

                        else:
                                self.nope()

                return 0
        def initilize(self, flatfile):
            foo = os.path.isfile(flatfile)
            acks = []
            if foo == False:
                acks = [['Looking into it', '\n'], 
                        ['Ignoring per playbook', '\n'], 
                        ['Ignoring per announcement', '\n'], 
                        ['Watching for 5 mins', '\n'],
                        ['Watching for 6 mins', '\n'],
                        ['Watching for 10 mins', '\n'], 
                        ['Watching for 30 mins', '\n'],
                        ['Watching for 90 mins', '\n'],
                        ['Watching for 2 hours', '\n'],
                        ['^^^ Restarting Tomcat', '\n'],
                        ['^^^ Restarting Tomcat and Hp Document Renderer', '\n'],
                        ['^^^ Restaring Amavisd', '\n'],
                        ['^^^ Running Simple Test', '\n'],
                        ['^^^ Checking Healthchecks', '\n'],
                        ['^^^ Checking Connectivity', '\n'],
                        ['^^^ Running Disk Cleanup', '\n'],
                        ['^^^ Writing Ticket', '\n'],
                        ['### Contacting DevOps', '\n'],
                        ['Expected Trigger. Due to Deployment', '\n'],
                        ['Passed Healthcheck', '\n'],
                        ['DevOps are Aware', '\n']]
                self.rewrite_acks(acks)

class Window(QtGui.QMainWindow):
        def __init__(self):
                super(Window, self).__init__()

                self.acks = Acknowledgements("acks.txt")
                self.initUI()

        def initUI(self):

                self.ack =  self.acks.write_acks()
                self.btns = []
                self.ackButtons = [QtGui.QWidget(), QtGui.QWidget()]
                self.vbox = [QtGui.QVBoxLayout(),QtGui.QVBoxLayout(),QtGui.QVBoxLayout()]
                self.vbox[0].setSpacing(0)
                self.vbox[1].setSpacing(0)
                self.ackButtons[0].setLayout(self.vbox[0])
                self.ackButtons[1].setLayout(self.vbox[1])
                self.stackWidget = QtGui.QStackedWidget()
                
                
                self.closingButton = QtGui.QPushButton("Ok")
                self.closingButton.setStatusTip("Accept Changes")
                self.closingButton.clicked.connect(self.changeLayout)
                self.closingButton.resize(self.closingButton.sizeHint())

                self.title=QtGui.QLabel(self)
                self.title.setFixedSize(150,20)
                #self.title.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Plain)
                self.vbox[1].addWidget(self.title)

                for i in range(len(self.ack)): #This needs to be placed in a try/except IndexError
                        self.btns.append([QtGui.QPushButton(str(self.ack[i][0])), QtGui.QCheckBox(str(self.ack[i][0]))])
                        self.btns[i][0].setToolTip(str(self.ack[i][1]).rstrip('\n'))
                        self.btns[i][0].setStatusTip(str(self.ack[i][1]).rstrip('\n'))
                        self.btns[i][0].clicked.connect(self.buttonClicked)
                        self.btns[i][0].resize(self.btns[i][0].sizeHint())
                        self.vbox[0].addWidget(self.btns[i][0])
                        
                        self.btns[i][1].stateChanged.connect(self.buttonChecked)
                        self.vbox[1].addWidget(self.btns[i][1])
                self.spacer = QtGui.QWidget()
                self.vbox[1].addWidget(self.spacer)
                self.vbox[1].addWidget(self.closingButton)
                self.stackWidget.addWidget(self.ackButtons[0])
                self.stackWidget.addWidget(self.ackButtons[1])

                self.setCentralWidget(self.stackWidget)
                
                #Dropped the 'n' because of the addAction method, and because I am lazy                    
                addActio = QtGui.QAction(QtGui.QIcon("add.png"), '&Add a Trigger', self)
                addActio.setShortcut("Ctrl+A")
                addActio.setStatusTip("Add Acknowledgement")
                addActio.triggered.connect(self.appendButton)

                removeActio = QtGui.QAction(QtGui.QIcon("remove.png"), "&Remove Button", self)
                removeActio.setShortcut("Ctrl+R")
                removeActio.setStatusTip("Remove Acknowledgement")
                removeActio.triggered.connect(self.removeButton)
                self.rmButton = False

                hintActio = QtGui.QAction(QtGui.QIcon("tooltip.png"), "&Add Button Hint", self)
                hintActio.setShortcut("Ctrl+H")
                hintActio.setStatusTip("Add a hint to the trigger")
                hintActio.triggered.connect(self.addTooltip)
                self.addHint = False

                editActio = QtGui.QAction("&Edit Buttons", self)
                editActio.setShortcut("Ctrl+E")
                editActio.setStatusTip("Change the text on the buttons")
                editActio.triggered.connect(self.editButton)
                self.viButton = False

                #This action doesn't work, don't try it
                topActio = QtGui.QAction(QtGui.QIcon("ontop.png"), "&Top", self)
                topActio.setShortcut("Ctrl+T")
                topActio.setStatusTip("Place application always on top")
                topActio.triggered.connect(self.alwaysOnTop)
                self.onTop = False
                
                exitActio = QtGui.QAction(QtGui.QIcon("need_to_add.png"), '&Exit', self)
                exitActio.setShortcut("Ctrl+Q")
                exitActio.setStatusTip("Exit application")
                exitActio.triggered.connect(self.close)

                self.statusBar()

                menubar = self.menuBar()
                filemenu = menubar.addMenu('&File')
                filemenu.addAction(exitActio)
                editmenu = menubar.addMenu('&Edit')
                editmenu.addAction(addActio)
                editmenu.addAction(editActio)
                editmenu.addAction(hintActio)
                editmenu.addAction(removeActio)
                
                self.setWindowTitle('Noc Monkey')
                self.setWindowIcon(QtGui.QIcon('monkey-head.png'))

                #self.acks.clipboard.connect(self.acks.clipboard, QtCore.SIGNAL("dataChanged()"), self.clipStats)
                self.acks.clipboard.dataChanged.connect(self.clipStatus)

                self.show()
                
        def buttonClicked(self):
                sender = self.sender()
                self.acks.add_to_clipboard(sender.text())
                self.statusBar().showMessage("'" + sender.text() +"' was copied")

        def appendButton(self):
                if self.stackWidget.currentIndex() != 0:
                        self.changeLayout()
                text, ok = QtGui.QInputDialog.getText(self, 'Add Acknowledgement', 'Enter new acknowledgement:')
                if ok:
                        self.acks.add_to_acks(text)
                        self.ack.append([str(text), "\n"])
                        self.btns.append([QtGui.QPushButton(str(text).rstrip('\n')),QtGui.QCheckBox(str(text))])
                        i=len(self.btns)-1
                        self.btns[i][0].clicked.connect(self.buttonClicked)
                        self.btns[i][1].stateChanged.connect(self.buttonChecked)
                        self.btns[i][0].resize(self.btns[i][0].sizeHint())
                        self.vbox[1].removeWidget(self.spacer)
                        self.vbox[1].removeWidget(self.closingButton)
                        self.vbox[0].addWidget(self.btns[i][0])
                        self.vbox[1].addWidget(self.btns[i][1])
                        self.vbox[1].addWidget(self.spacer)
                        self.vbox[1].addWidget(self.closingButton)
                else:
                        pass
        def removeButton(self):
                self.title.setText("Remove Acknowledgement")
                self.rmButton = True
                self.addHint = False
                self.viButton = False
                self.stackWidget.setCurrentIndex(1)
        def addTooltip(self):
            self.title.setText("Add a Hint to a Trigger")
            self.rmButton = False
            self.addHint = True
            self.viButton = False
            self.stackWidget.setCurrentIndex(1)
        def editButton(self):
            self.title.setText("Change Button text")
            self.rmButton = False
            self.addHint = False
            self.viButton = True
            self.stackWidget.setCurrentIndex(1)

        def clipStatus(self):
                if self.acks.clipboard.mimeData().hasText():
                        self.statusBar().showMessage(self.acks.clipboard.text())
                else:
                        pass
        def alwaysOnTop(self): #This function doesn't work. Causes app to disappear. Not sure why. Sorry :(
            if self.onTop == False:
                self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                self.onTop = True
            else:
                self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
                self.onTop = False
        def changeLayout(self):
            self.rmButton = False
            self.addHint = False
            self.viButton = False
            self.title.setText("")
            self.stackWidget.setCurrentIndex(0)
        def buttonChecked(self):
            sender = self.sender()
            if self.rmButton == True:
                
                for i in range(len(self.ack)):
                    try:
                        self.ack[i].index(str(sender.text()))
                        del self.ack[i]
                        self.vbox[0].removeWidget(self.btns[i][0])
                        self.vbox[1].removeWidget(self.btns[i][1])
                        self.btns[i][0].deleteLater()
                        self.btns[i][1].deleteLater()
                        del self.btns[i]
                        self.acks.rewrite_acks(self.ack)
                    except ValueError:
                        pass

            if self.addHint == True:
                for i in range(len(self.ack)):
                    try:
                        self.ack[i].index(str(sender.text()))
                        text, ok = QtGui.QInputDialog.getText(self, 'Add ToolTip', 'Whats the tooltip:', QtGui.QLineEdit.Normal, str(self.btns[i][0].statusTip()))
                        if ok:
                            self.ack[i][1] = str(text) + "\n"
                            self.btns[i][0].setToolTip(str(text))
                            self.btns[i][0].setStatusTip(str(text))
                            self.btns[i][1].setToolTip(str(text))
                            self.btns[i][1].setStatusTip(str(text))
                            self.btns[i][1].toggle()
                            self.acks.rewrite_acks(self.ack)
                            
                        else:
                            self.btns[i][1].toggle() 
                    except ValueError:
                        pass
            if self.viButton == True:
                for i in range(len(self.ack)):
                    try:
                        self.ack[i].index(str(sender.text()))
                        text, ok = QtGui.QInputDialog.getText(self, 'Change Button text', 'Edit Button Text:', QtGui.QLineEdit.Normal, str(self.btns[i][0].text()))
                        if ok:
                            self.ack[i][0] = str(text)
                            self.btns[i][0].setText(str(text))
                            self.btns[i][1].setText(str(text))
                            self.btns[i][1].toggle()
                            self.acks.rewrite_acks(self.ack)
                        else:
                            self.btns[i][1].toggle()
                    except ValueError:
                        pass

def main():
        app = QtGui.QApplication(sys.argv)
        window = Window()
        sys.exit(app.exec_())

if __name__ == '__main__':
        main()
