#!/usr/bin/python

import os
import sys
from PyQt4 import QtGui, QtCore

#Initalize Stuff

clear = lambda: os.system('cls')

class Acknowledgements(object):
        def __init__(self,flatfile):
                self.flatfile = str(flatfile)
                
                self.clipboard = QtGui.QApplication.clipboard() 

                #acks = self.write_acks()
                #self.menu(acks)

        def write_acks(self):
                acks = []
                with open(str(self.flatfile),"r") as f:
                        for line in f:
                                acks.append(line)
                        return acks

        def add_to_acks(self, string):
                f = open(self.flatfile, "a+")
                f.write(str(string) + "\n")
                f.close()

        def rewrite_acks(self, acks):
                f = open(self.flatfile, "w+")
                for i in range(len(acks)):
                        f.write(str(acks[i]))
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

#main function
	
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

class Window(QtGui.QMainWindow):
        def __init__(self):
                super(Window, self).__init__()

                self.acks = Acknowledgements("acks.txt")
                self.initUI()

        def initUI(self):

                self.ack =  self.acks.write_acks()
                self.btns = []
                ackButtons = QtGui.QWidget()
                self.vbox = QtGui.QVBoxLayout()
                self.vbox.setSpacing(0)
                ackButtons.setLayout(self.vbox)
                

                for i in range(len(self.ack)):
                        self.btns.append(QtGui.QPushButton(str(self.ack[i]).rstrip('\n')))
                        self.btns[i].clicked.connect(self.buttonClicked)
                        self.btns[i].resize(self.btns[i].sizeHint())
                        self.vbox.addWidget(self.btns[i])

                

                self.setCentralWidget(ackButtons)
                
                #Dropped the 'n' because of the addAction method, and because I am lazy                    
                addActio = QtGui.QAction(QtGui.QIcon("add.png"), '&Add', self)
                addActio.setShortcut("Ctrl+A")
                addActio.setStatusTip("Add Acknowledgement")
                addActio.triggered.connect(self.appendButton)

                removeActio = QtGui.QAction(QtGui.QIcon("remove.png"), "&Rm", self)
                removeActio.setShortcut("Ctrl+R")
                removeActio.setStatusTip("Remove Acknowledgement")
                removeActio.triggered.connect(self.removeButton)

                editAction = QtGui.QAction(QtGui.QIcon("tooltip.png"), "&Edit", self)
                editAction.setShortcut("Ctrl+E")
                editAction.setStatusTip("Set Trigger Tooltip")
                editAction.triggered.connect(self.addTooltip)
                
                exitAction = QtGui.QAction(QtGui.QIcon("need_to_add.png"), '&Exit', self)
                exitAction.setShortcut("Ctrl+Q")
                exitAction.setStatusTip("Exit application")
                exitAction.triggered.connect(self.close)

                self.statusBar()

                menubar = self.menuBar()
                menubar.addAction(addActio)
                menubar.addAction(removeActio)
                menubar.addAction(editAction)
                menubar.addAction(exitAction)
                
                self.setWindowTitle('Noc Monkey')
                self.setWindowIcon(QtGui.QIcon('monkey.png'))

                #self.acks.clipboard.connect(self.acks.clipboard, QtCore.SIGNAL("dataChanged()"), self.clipStats)
                self.acks.clipboard.dataChanged.connect(self.clipStatus)

                self.show()
                
        def buttonClicked(self):
                sender = self.sender()
                self.acks.add_to_clipboard(sender.text())
                self.statusBar().showMessage("'" + sender.text() +"' was copied")

        def appendButton(self):
                text, ok = QtGui.QInputDialog.getText(self, 'Add Acknowledgement', 'Enter new acknowledgement:')
                if ok:
                        self.acks.add_to_acks(text)
                        self.ack.append(str(text)+ "\n")
                        self.btns.append(QtGui.QPushButton(str(text).rstrip('\n')))
                        i=len(self.btns)-1
                        self.btns[i].clicked.connect(self.buttonClicked)
                        self.btns[i].resize(self.btns[i].sizeHint())
                        self.vbox.addWidget(self.btns[i])
                else:
                        pass
        def removeButton(self):
                text, ok = QtGui.QInputDialog.getText(self, 'Remove Acknowledgement', 'What trigger:')
                if ok:
                        try:
                                num = self.ack.index(text + "\n")
                                del self.ack[num]
                                self.vbox.removeWidget(self.btns[num])
                                self.btns[num].deleteLater()
                                del self.btns[num]
                                self.acks.rewrite_acks(self.ack)
                        except ValueError:
                                self.statusBar().showMessage("Not a valid trigger")
                                self.removeButton()
                                
                else:
                        pass
        def addTooltip(self):
                text, ok = QtGui.QInputDialog.getText(self, 'Add ToolTip', 'What trigger:')
                if ok:
                        try:
                                num = self.ack.index(text + "\n")
                                text,ok = QtGui.QInputDialog.getText(self, 'Add ToolTip', 'Whats the tooltip:')
                                        
                                if ok:
                                        self.btns[num].setToolTip(str(text))
                                        self.btns[num].setStatusTip(str(text))
                                else:
                                        pass
                        except ValueError:
                                self.statusBar().showMessage("Not a valid trigger")
                                self.addTooltip
                else:
                        pass
        def clipStatus(self):
                if self.acks.clipboard.mimeData().hasText():
                        self.statusBar().showMessage(self.acks.clipboard.text())
                else:
                        pass

def main():
        app = QtGui.QApplication(sys.argv)
        window = Window()
        sys.exit(app.exec_())

if __name__ == '__main__':
        main()