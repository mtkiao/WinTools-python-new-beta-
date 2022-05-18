import configparser,os
from PyQt5 import QtWidgets, QtGui, QtCore
from Setting import Ui_Setting_main

class setting_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Setting_main()
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setup_control()

    def setup_control(self):
        self.ui.Minimize_Check.stateChanged.connect(self.main_update)
        self.ui.Main_Top_Check.stateChanged.connect(self.main_update)
        self.ui.English_Radio.clicked.connect(self.language)
        self.ui.Simplified_Chinese_Radio.clicked.connect(self.language)
        self.ui.Traditional_Chinese_Radio.clicked.connect(self.language)

        if not os.path.isfile(r'./stg.ini'):
            self.Create_ini_file()
        self.config = configparser.RawConfigParser()
        self.config.optionxform = str
        self.config.read('stg.ini')
        try:
            self.Setting_check()
        except:
            self.Create_ini_file()
            self.Setting_check()

    def Create_ini_file(self):
        with open('stg.ini',mode='w',encoding='utf-8') as file:
            file.write('[app]\n\n[Setting]\nMinimize = True\nMain_top = False\nLanguage = Traditional_Chinese')

    def Setting_check(self):
        self.Main_top = self.config.get('Setting','Main_top')
        self.Minimize = self.config.get('Setting','Minimize')
        self.Language_value = self.config.get('Setting','Language')

        if self.Main_top == 'True':
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.ui.Main_Top_Check.setChecked(True)
        if self.Minimize == 'True':
            self.ui.Minimize_Check.setChecked(True)
        
        if self.Language_value == 'Traditional_Chinese':
            self.ui.Traditional_Chinese_Radio.setChecked(True)
        elif self.Language_value == 'English':
            self.ui.English_Radio.setChecked(True)
        elif self.Language_value == 'Simplified_Chinese':
            self.ui.Simplified_Chinese_Radio.setChecked(True)

    def main_update(self):
        if self.ui.Main_Top_Check.isChecked():
            self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            self.showNormal()
            self.config.set('Setting','Main_top',True)
            self.config.write(open('stg.ini', 'w'))
        elif self.ui.Main_Top_Check.isCheckable():
            self.setWindowFlags(QtCore.Qt.Window)
            self.showNormal()
            self.config.set('Setting','Main_top',False)
            self.config.write(open('stg.ini', 'w'))
        if self.ui.Minimize_Check.isChecked():
            self.config.set('Setting','Minimize',True)
            self.config.write(open('stg.ini', 'w'))
        elif self.ui.Minimize_Check.isCheckable():
            self.config.set('Setting','Minimize',False)
            self.config.write(open('stg.ini', 'w'))

    def language(self):
        if self.ui.English_Radio.isChecked():
            self.config.set('Setting','Language', 'English')
            self.config.write(open('stg.ini', 'w'))
        elif self.ui.Simplified_Chinese_Radio.isChecked():
            self.config.set('Setting','Language', 'Simplified_Chinese')
            self.config.write(open('stg.ini', 'w'))
        elif self.ui.Traditional_Chinese_Radio.isChecked():
            self.config.set('Setting','Language', 'Traditional_Chinese')
            self.config.write(open('stg.ini', 'w'))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = setting_controller()
    window.show()
    sys.exit(app.exec())