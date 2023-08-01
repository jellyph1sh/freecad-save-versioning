from PySide import QtGui, QtCore
import FreeCAD
import os

class FileVersioning():
    def __init__(self, path, file):
        self.path = path
        fileParts = file.split(".")
        self.fileName = fileParts[0]
        self.fileExt = fileParts[1]
        self.fileNameParts = self.fileName.split("-")
        self.fileName = self.fileNameParts[0] + "-"

    def HaveVersion(self):
        if len(self.fileNameParts) == 1:
            return False
        if len(self.fileNameParts) > 2:
            return None
        return True

    def GetVersion(self):
        if len(self.fileNameParts) == 1:
            self.version = ""
            return
        self.version = self.fileNameParts[1]

    def AddVersion(self):
        versionAscii = ord(self.version[-1]) + 1
        if versionAscii > 90:
            return False
        self.version = chr(versionAscii).join(self.version.rsplit(chr(versionAscii-1), 1))
        return True

    def Save(self):
        self.fileName += self.version + "." + self.fileExt
        self.fullPath = self.path + "/" + self.fileName
        FreeCAD.ActiveDocument.saveAs(self.fullPath)



class SaveWindow(QtGui.QDialog):
    def __init__(self):
        super(SaveWindow, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.mainLayout = QtGui.QVBoxLayout()

        self.buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        self.buttonBox.setCenterButtons(True)

        self.CreateButtons()
    
        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)
        self.setGeometry(50, 100, 225, 50)
        self.setFixedSize(225, 50)
        self.setWindowTitle("Versioning")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def CreateButtons(self):
        saveNVButton = QtGui.QPushButton("New Version")
        saveNVButton.clicked.connect(self.SaveNewVersion)

        saveNSVButton = QtGui.QPushButton("New Sub Version")
        saveNSVButton.clicked.connect(self.SaveNewSubVersion)

        self.buttonBox.addButton(saveNVButton, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(saveNSVButton, QtGui.QDialogButtonBox.ActionRole)

    def IsValidDocument(self, document):
        if document is None:
            return False
        return True
    
    def SetupDocument(self):
        if not self.IsValidDocument(FreeCAD.ActiveDocument):
            QtGui.QMessageBox.information(None, "", "No active document!")
            return False
        
        self.fullPath = FreeCAD.ActiveDocument.FileName
        self.path = os.path.dirname(self.fullPath) + "/"
        self.file = os.path.basename(self.fullPath)
        return True


    def SaveNewVersion(self):
        if not self.SetupDocument():
            return

        file = FileVersioning(self.path, self.file)
        haveVersion = file.HaveVersion()
        if haveVersion is None:
            QtGui.QMessageBox.information(None, "", "Please rename your file without '-'!")
            return
        elif not haveVersion:
            file.version = "A"
        else:
            file.GetVersion()
            if not file.AddVersion():
                QtGui.QMessageBox.information(None, "", "You can't create new version (Maximum value reached)! Please create new sub version!")
                return
        file.Save()
        QtGui.QMessageBox.information(None, "", f"New version successfully saved! ({file.fullPath})")

    def SaveNewSubVersion(self):
        if not self.SetupDocument():
            return

        file = FileVersioning(self.path, self.file)
        haveVersion = file.HaveVersion()
        if haveVersion is None:
            QtGui.QMessageBox.information(None, "", "Please rename your file without '-'!")
            return
        file.GetVersion()
        file.version += "A"
        file.Save()
        QtGui.QMessageBox.information(None, "", f"New sub version successfully saved! ({file.fullPath})")


saveWindow = SaveWindow()
saveWindow.exec_()