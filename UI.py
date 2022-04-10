# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(849, 629)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Dos = QtWidgets.QLineEdit(self.centralwidget)
        self.Dos.setGeometry(QtCore.QRect(10, 540, 113, 31))
        self.Dos.setObjectName("Dos")
        self.Dostext = QtWidgets.QLabel(self.centralwidget)
        self.Dostext.setGeometry(QtCore.QRect(10, 515, 81, 21))
        self.Dostext.setObjectName("Dostext")
        self.RunDos = QtWidgets.QPushButton(self.centralwidget)
        self.RunDos.setGeometry(QtCore.QRect(130, 540, 75, 31))
        self.RunDos.setObjectName("RunDos")
        self.filebut = QtWidgets.QPushButton(self.centralwidget)
        self.filebut.setGeometry(QtCore.QRect(10, 360, 81, 31))
        self.filebut.setObjectName("filebut")
        self.Toolsmenu = QtWidgets.QTabWidget(self.centralwidget)
        self.Toolsmenu.setGeometry(QtCore.QRect(0, 0, 851, 351))
        self.Toolsmenu.setTabPosition(QtWidgets.QTabWidget.North)
        self.Toolsmenu.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.Toolsmenu.setElideMode(QtCore.Qt.ElideNone)
        self.Toolsmenu.setDocumentMode(False)
        self.Toolsmenu.setTabsClosable(False)
        self.Toolsmenu.setMovable(False)
        self.Toolsmenu.setTabBarAutoHide(False)
        self.Toolsmenu.setObjectName("Toolsmenu")
        self.process = QtWidgets.QWidget()
        self.process.setObjectName("process")
        self.processname = QtWidgets.QLabel(self.process)
        self.processname.setGeometry(QtCore.QRect(30, 0, 61, 31))
        self.processname.setAlignment(QtCore.Qt.AlignCenter)
        self.processname.setObjectName("processname")
        self.processPID = QtWidgets.QLabel(self.process)
        self.processPID.setGeometry(QtCore.QRect(150, 0, 51, 31))
        self.processPID.setAlignment(QtCore.Qt.AlignCenter)
        self.processPID.setObjectName("processPID")
        self.processlist = QtWidgets.QListView(self.process)
        self.processlist.setGeometry(QtCore.QRect(0, 30, 845, 241))
        self.processlist.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.processlist.setMouseTracking(False)
        self.processlist.setStyleSheet("")
        self.processlist.setInputMethodHints(QtCore.Qt.ImhNone)
        self.processlist.setLineWidth(1)
        self.processlist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.processlist.setObjectName("processlist")
        self.processfile = QtWidgets.QLabel(self.process)
        self.processfile.setGeometry(QtCore.QRect(280, 4, 61, 21))
        self.processfile.setAlignment(QtCore.Qt.AlignCenter)
        self.processfile.setObjectName("processfile")
        self.hwnd = QtWidgets.QLabel(self.process)
        self.hwnd.setGeometry(QtCore.QRect(10, 280, 41, 21))
        self.hwnd.setObjectName("hwnd")
        self.hwndview = QtWidgets.QLineEdit(self.process)
        self.hwndview.setEnabled(False)
        self.hwndview.setGeometry(QtCore.QRect(60, 280, 113, 20))
        self.hwndview.setObjectName("hwndview")
        self.Toolsmenu.addTab(self.process, "")
        self.Tools = QtWidgets.QWidget()
        self.Tools.setObjectName("Tools")
        self.resetexplorerbut = QtWidgets.QPushButton(self.Tools)
        self.resetexplorerbut.setGeometry(QtCore.QRect(510, 10, 91, 31))
        self.resetexplorerbut.setObjectName("resetexplorerbut")
        self.cleanuserpwbut = QtWidgets.QPushButton(self.Tools)
        self.cleanuserpwbut.setGeometry(QtCore.QRect(410, 10, 91, 31))
        self.cleanuserpwbut.setObjectName("cleanuserpwbut")
        self.fixlimitbut = QtWidgets.QPushButton(self.Tools)
        self.fixlimitbut.setGeometry(QtCore.QRect(10, 10, 91, 31))
        self.fixlimitbut.setObjectName("fixlimitbut")
        self.fiximgbut = QtWidgets.QPushButton(self.Tools)
        self.fiximgbut.setGeometry(QtCore.QRect(110, 10, 91, 31))
        self.fiximgbut.setObjectName("fiximgbut")
        self.fixiconbut = QtWidgets.QPushButton(self.Tools)
        self.fixiconbut.setGeometry(QtCore.QRect(310, 10, 91, 31))
        self.fixiconbut.setObjectName("fixiconbut")
        self.fixexeimgbut = QtWidgets.QPushButton(self.Tools)
        self.fixexeimgbut.setGeometry(QtCore.QRect(210, 10, 91, 31))
        self.fixexeimgbut.setObjectName("fixexeimgbut")
        self.Toolsmenu.addTab(self.Tools, "")
        self.System = QtWidgets.QWidget()
        self.System.setObjectName("System")
        self.Shutdownbut = QtWidgets.QPushButton(self.System)
        self.Shutdownbut.setGeometry(QtCore.QRect(10, 10, 81, 31))
        self.Shutdownbut.setObjectName("Shutdownbut")
        self.resetbut = QtWidgets.QPushButton(self.System)
        self.resetbut.setGeometry(QtCore.QRect(100, 10, 81, 31))
        self.resetbut.setObjectName("resetbut")
        self.setUAC = QtWidgets.QPushButton(self.System)
        self.setUAC.setGeometry(QtCore.QRect(190, 10, 81, 31))
        self.setUAC.setObjectName("setUAC")
        self.systeminfobut = QtWidgets.QPushButton(self.System)
        self.systeminfobut.setGeometry(QtCore.QRect(10, 280, 81, 31))
        self.systeminfobut.setObjectName("systeminfobut")
        self.Toolsmenu.addTab(self.System, "")
        self.Sysexe = QtWidgets.QWidget()
        self.Sysexe.setObjectName("Sysexe")
        self.Taskbut = QtWidgets.QPushButton(self.Sysexe)
        self.Taskbut.setGeometry(QtCore.QRect(10, 10, 81, 31))
        self.Taskbut.setObjectName("Taskbut")
        self.Powershellbut = QtWidgets.QPushButton(self.Sysexe)
        self.Powershellbut.setGeometry(QtCore.QRect(100, 10, 81, 31))
        self.Powershellbut.setObjectName("Powershellbut")
        self.regebut = QtWidgets.QPushButton(self.Sysexe)
        self.regebut.setGeometry(QtCore.QRect(190, 10, 81, 31))
        self.regebut.setObjectName("regebut")
        self.cmdbut = QtWidgets.QPushButton(self.Sysexe)
        self.cmdbut.setGeometry(QtCore.QRect(280, 10, 81, 31))
        self.cmdbut.setObjectName("cmdbut")
        self.Gpeditbut = QtWidgets.QPushButton(self.Sysexe)
        self.Gpeditbut.setGeometry(QtCore.QRect(370, 10, 81, 31))
        self.Gpeditbut.setObjectName("Gpeditbut")
        self.controlbut = QtWidgets.QPushButton(self.Sysexe)
        self.controlbut.setGeometry(QtCore.QRect(460, 10, 81, 31))
        self.controlbut.setObjectName("controlbut")
        self.MMCbut = QtWidgets.QPushButton(self.Sysexe)
        self.MMCbut.setGeometry(QtCore.QRect(550, 10, 81, 31))
        self.MMCbut.setObjectName("MMCbut")
        self.Toolsmenu.addTab(self.Sysexe, "")
        self.Windowkill = QtWidgets.QWidget()
        self.Windowkill.setObjectName("Windowkill")
        self.windowkillname = QtWidgets.QLineEdit(self.Windowkill)
        self.windowkillname.setGeometry(QtCore.QRect(10, 190, 181, 31))
        self.windowkillname.setObjectName("windowkillname")
        self.windowhint = QtWidgets.QLabel(self.Windowkill)
        self.windowhint.setEnabled(True)
        self.windowhint.setGeometry(QtCore.QRect(10, 160, 191, 21))
        self.windowhint.setObjectName("windowhint")
        self.windowkillbut = QtWidgets.QPushButton(self.Windowkill)
        self.windowkillbut.setGeometry(QtCore.QRect(200, 190, 81, 31))
        self.windowkillbut.setObjectName("windowkillbut")
        self.windowkillview = QtWidgets.QListView(self.Windowkill)
        self.windowkillview.setEnabled(True)
        self.windowkillview.setGeometry(QtCore.QRect(360, 30, 471, 291))
        self.windowkillview.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.windowkillview.setObjectName("windowkillview")
        self.windowkilllist = QtWidgets.QLabel(self.Windowkill)
        self.windowkilllist.setGeometry(QtCore.QRect(360, 5, 211, 21))
        self.windowkilllist.setObjectName("windowkilllist")
        self.hint = QtWidgets.QLabel(self.Windowkill)
        self.hint.setGeometry(QtCore.QRect(10, 60, 81, 21))
        self.hint.setObjectName("hint")
        self.Ruunninginfo = QtWidgets.QGroupBox(self.Windowkill)
        self.Ruunninginfo.setEnabled(True)
        self.Ruunninginfo.setGeometry(QtCore.QRect(10, 80, 191, 41))
        self.Ruunninginfo.setTitle("")
        self.Ruunninginfo.setObjectName("Ruunninginfo")
        self.stoping = QtWidgets.QRadioButton(self.Ruunninginfo)
        self.stoping.setGeometry(QtCore.QRect(100, 10, 83, 21))
        self.stoping.setObjectName("stoping")
        self.Running = QtWidgets.QRadioButton(self.Ruunninginfo)
        self.Running.setGeometry(QtCore.QRect(10, 10, 83, 21))
        self.Running.setObjectName("Running")
        self.Toolsmenu.addTab(self.Windowkill, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 849, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_3 = QtWidgets.QMenu(self.menu)
        self.menu_3.setObjectName("menu_3")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.video_view = QtWidgets.QAction(MainWindow)
        self.video_view.setObjectName("video_view")
        self.Close = QtWidgets.QAction(MainWindow)
        self.Close.setObjectName("Close")
        self.about_us = QtWidgets.QAction(MainWindow)
        self.about_us.setObjectName("about_us")
        self.English = QtWidgets.QAction(MainWindow)
        self.English.setObjectName("English")
        self.Chinese_T = QtWidgets.QAction(MainWindow)
        self.Chinese_T.setObjectName("Chinese_T")
        self.Chinese_S = QtWidgets.QAction(MainWindow)
        self.Chinese_S.setObjectName("Chinese_S")
        self.menu_3.addAction(self.English)
        self.menu_3.addAction(self.Chinese_T)
        self.menu_3.addAction(self.Chinese_S)
        self.menu.addAction(self.menu_3.menuAction())
        self.menu.addAction(self.Close)
        self.menu_2.addAction(self.about_us)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        self.Toolsmenu.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Dostext.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">CMD命令</span></p></body></html>"))
        self.RunDos.setText(_translate("MainWindow", "執行"))
        self.filebut.setText(_translate("MainWindow", "程式分析"))
        self.processname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">名稱</span></p></body></html>"))
        self.processPID.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">PID</span></p></body></html>"))
        self.processfile.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-size:12pt;\">exe路徑</span></p></body></html>"))
        self.hwnd.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">句柄:</span></p></body></html>"))
        self.Toolsmenu.setTabText(self.Toolsmenu.indexOf(self.process), _translate("MainWindow", "Tab 1"))
        self.resetexplorerbut.setText(_translate("MainWindow", "重啟資源管理器"))
        self.cleanuserpwbut.setText(_translate("MainWindow", "解除用戶密碼"))
        self.fixlimitbut.setText(_translate("MainWindow", "解除系統限制"))
        self.fiximgbut.setText(_translate("MainWindow", "修復打開方式"))
        self.fixiconbut.setText(_translate("MainWindow", "修復程式圖標"))
        self.fixexeimgbut.setText(_translate("MainWindow", "修復映像劫持"))
        self.Toolsmenu.setTabText(self.Toolsmenu.indexOf(self.Tools), _translate("MainWindow", "Tab 2"))
        self.Shutdownbut.setText(_translate("MainWindow", "強制關機"))
        self.resetbut.setText(_translate("MainWindow", "強制重啟"))
        self.setUAC.setText(_translate("MainWindow", "設定UAC"))
        self.systeminfobut.setText(_translate("MainWindow", "系統資訊"))
        self.Toolsmenu.setTabText(self.Toolsmenu.indexOf(self.System), _translate("MainWindow", "頁面"))
        self.Taskbut.setText(_translate("MainWindow", "Taskmgr"))
        self.Powershellbut.setText(_translate("MainWindow", "Powershell"))
        self.regebut.setText(_translate("MainWindow", "Regedit"))
        self.cmdbut.setText(_translate("MainWindow", "Cmd"))
        self.Gpeditbut.setText(_translate("MainWindow", "Gpedit"))
        self.controlbut.setText(_translate("MainWindow", "Control"))
        self.MMCbut.setText(_translate("MainWindow", "MMC"))
        self.Toolsmenu.setTabText(self.Toolsmenu.indexOf(self.Sysexe), _translate("MainWindow", "頁面"))
        self.windowhint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">請輸入要攔截窗口的名稱</span></p></body></html>"))
        self.windowkillbut.setText(_translate("MainWindow", "確定"))
        self.windowkilllist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">目前已知要攔截的窗口信息</span></p></body></html>"))
        self.hint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">運行狀態:</span></p></body></html>"))
        self.stoping.setText(_translate("MainWindow", "停止"))
        self.Running.setText(_translate("MainWindow", "運行"))
        self.Toolsmenu.setTabText(self.Toolsmenu.indexOf(self.Windowkill), _translate("MainWindow", "頁面"))
        self.menu.setTitle(_translate("MainWindow", "功能"))
        self.menu_3.setTitle(_translate("MainWindow", "語言"))
        self.menu_2.setTitle(_translate("MainWindow", "關於"))
        self.video_view.setText(_translate("MainWindow", "video view"))
        self.Close.setText(_translate("MainWindow", "關閉"))
        self.about_us.setText(_translate("MainWindow", "about"))
        self.English.setText(_translate("MainWindow", "English"))
        self.Chinese_T.setText(_translate("MainWindow", "traditional Chinese"))
        self.Chinese_S.setText(_translate("MainWindow", "Simplified Chinese"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())