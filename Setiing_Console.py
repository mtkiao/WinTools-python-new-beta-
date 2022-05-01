import configparser,os
from PyQt5 import QtWidgets, QtGui, QtCore

from Setting import Ui_Setting_main

class setting_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() # in python3, super(Class, self).xxx = super().xxx
        self.ui = Ui_Setting_main()
        self.ui.setupUi(self)
        self.setup_control()

    def setup_control(self):
        if not os.path.isfile(r'./stg.ini'):
            with open('stg.ini',mode='w',encoding='utf-8') as file:
                file.write('[app]')
                file.write('\n\n[Setting]\nMinimize = True\nMain_top = False')
        self.config = configparser.RawConfigParser()
        self.config.optionxform = str
        self.config.read('stg.ini')
        self.Main_top = self.config.get('Setting','Main_top')
        self.Minimize = self.config.get('Setting','Minimize')

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = setting_controller()
    window.show()
    sys.exit(app.exec())