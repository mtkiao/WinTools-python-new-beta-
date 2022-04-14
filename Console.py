#導入模塊
import getpass,subprocess,configparser,pefile,platform,win32gui,UAC_UI,qdarkstyle,win32process,psutil
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QFileDialog,QMessageBox,QMenu,QAction
from systeminfo import Ui_info
from os import path
from fun import fun_list
from PyQt5.QtCore import QStringListModel,QTimer,Qt
from Main_UI import Ui_MainWindow
from ctypes import windll

# 判斷是否有管理員權限
def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.UAC = ''
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setup_control()

    def setup_control(self):
        # TODO
        self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.Tools),"工具")
        self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.process),"進程")
        self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.System),"系統")
        self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.Sysexe),"系統程式")
        self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.Windowkill),"窗口攔截")
        self.ui.Close.triggered.connect(self.close)
        self.ui.English.triggered.connect(self.english)
        self.ui.Chinese_T.triggered.connect(self.chinese_t)
        self.ui.Chinese_S.triggered.connect(self.chinese_s)
        self.ui.Taskbut.clicked.connect(self.Taskmgr)
        self.ui.fixlimitbut.clicked.connect(self.fixlimit)
        self.ui.fiximgbut.clicked.connect(self.fiximg)
        self.ui.regebut.clicked.connect(self.regedit)
        self.ui.cmdbut.clicked.connect(self.cmd)
        self.ui.Powershellbut.clicked.connect(self.Powershell)
        self.ui.resetexplorerbut.clicked.connect(self.resetexplorer)
        self.ui.cleanuserpwbut.clicked.connect(self.cleanUserPassword)
        self.ui.fixiconbut.clicked.connect(self.fixicon)
        self.ui.fixexeimgbut.clicked.connect(self.fixexeimg)
        self.ui.controlbut.clicked.connect(self.control)
        self.ui.MMCbut.clicked.connect(self.MMC)
        self.ui.Gpeditbut.clicked.connect(self.Gpedit)
        self.ui.Shutdownbut.clicked.connect(self.Shutdown)
        self.ui.resetbut.clicked.connect(self.reset)
        self.ui.RunDos.clicked.connect(self.Rundos)
        self.ui.execheck.clicked.connect(self.check)
        self.ui.systeminfobut.clicked.connect(self.systeminfogrt)
        self.ui.about_us.triggered.connect(self.about)
        self.ui.processlist.clicked.connect(self.processhwnd)
        self.ui.processlist.clicked.connect(self.processuser)
        self.ui.windowkillbut.clicked.connect(self.window_blocking)
        self.ui.stoping.toggled.connect(self.setRunning)
        self.ui.Running.toggled.connect(self.setRunning)
        self.ui.processlist.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.processlist.customContextMenuRequested.connect(self.generateMenu)
        self.ui.windowkillview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.windowkillview.customContextMenuRequested.connect(self.delexekill)
        #dialog
        self.ui.setUAC.clicked.connect(self.uac)
        #timer
        self.beautificationA=QTimer()
        self.beautificationA.timeout.connect(self.beautification)
        self.beautificationA.start(1000)
        self.timer=QTimer()
        self.timer.timeout.connect(self.listprocess)
        self.timer.start(1000)
        self.applist=QTimer()
        self.applist.timeout.connect(self.windowlist)
        self.applist.start(1000)
        self.exekill=QTimer()
        self.exekill.timeout.connect(self.killwindow)
        #other
        self.language = 2
        self.ui.stoping.setChecked(True)
        self.user32dll = windll.LoadLibrary(r"C:\Windows\System32\user32.dll") 

    def window_blocking(self):
        config = configparser.RawConfigParser()
        config.read('stg.ini')
        self.windowinfo = self.ui.windowkillname.text()
        if self.windowinfo != '':
            config.set('app', self.windowinfo, True)
            config.write(open('stg.ini', 'w'))
        else:
            if self.language == 1:
                text = 'Please enter a name!'
            if self.language == 2:
                text = '請輸入名稱!'
            if self.language == 3:
                text = '请输入名称!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def windowlist(self):
        if not path.isfile(r'./stg.ini'):
            with open('stg.ini',mode='w',encoding='utf-8') as file:
                file.write('[app]')
        self.configlist=QStringListModel()
        config = configparser.RawConfigParser()
        try:
            config.read('stg.ini')
        except Exception as error:
            QMessageBox.critical(self,'error','發生錯誤!\n原因:' + str(error),QMessageBox.Ok)
        section = config.options('app')
        self.configlist.setStringList(section)
        self.ui.windowkillview.setModel(self.configlist)
    
    def killwindow(self):
        config = configparser.RawConfigParser()
        config.read('stg.ini')
        for i in config.options('app'):
            for p in psutil.process_iter():
                try:
                    if i == p.name():
                        p.kill()
                except:
                    pass

    def delexekill(self,pos):
        config = configparser.RawConfigParser()
        config.read('stg.ini')
        self.exeitem = self.ui.windowkillview.selectedIndexes()
        for i in self.exeitem:
            exeitem = i.data()
        self.exekillview = QMenu()
        if self.language == 1:
            text = 'delete'
        if self.language == 2:
            text = '刪除'
        if self.language == 3:
            text = '删除'
        delexe = QAction(text,self)
        self.exekillview.addAction(delexe)
        ques = self.exekillview.exec_(self.ui.windowkillview.mapToGlobal(pos))
        if ques == delexe:
            try:
                for i in config.options('app'):
                    if i == exeitem:
                        config.remove_option('app', i)
                        config.write(open('stg.ini', 'w'))
            except:
                pass
        
    def setRunning(self):
        if self.ui.Running.isChecked():
            self.exekill.start(500)
        elif self.ui.stoping.isChecked():
            self.exekill.stop()

    def OpenProcess0(self,exe):
        win32process.CreateProcess(exe,"", None, None, 0,win32process.CREATE_NO_WINDOW, None, None,win32process.STARTUPINFO())

    def listprocess(self):
        self.slm=QStringListModel()
        self.qList = []
        self.qList_pid = []
        self.qList_exe = []
        self.qList_name = []
        self.qList_user = []
        for p in psutil.process_iter():
            try:
                self.qList.append(p.name() +"   "+ str(p.pid) +"        "+ p.exe())
                self.qList_pid.append(p.pid)
                self.qList_exe.append(p.exe())
                self.qList_name.append(p.name())
                self.qList_user.append(p.username())
            except:
                pass
        self.slm.setStringList(self.qList)
        self.ui.processlist.setModel(self.slm)
        # #獲取數量
        # count = self.slm.rowCount()

    def fixlimit(self):
        if self.language == 1:
            text = 'Are you sure you want to remove system restrictions?'
        if self.language == 2:
            text = '確定要解除系統限制嗎?'
        if self.language == 3:
            text = '确定要解除系统限制吗?'
        question = QMessageBox.warning(self,'FixLimit',text,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384:
            import win32api,win32con
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'Explorer')
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'NoControlPanel', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoDrives', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoFileMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoFind', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoRealMode', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoRecentDocsMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoSetFolders', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoSetFolderOptions', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoViewOnDrive', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoClose', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoRun', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoDesktop', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoLogOff', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoFolderOptions', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoViewContextMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'HideClock', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoStartMenuMorePrograms', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoStartMenuMyGames', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoStartMenuMyMusic', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoStartMenuNetworkPlaces', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoStartMenuPinnedList', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoActiveDesktop', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoActiveDesktopChanges', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoChangeStartMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'ClearRecentDocsOnExit', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoFavoritesMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoRecentDocsHistory', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoSetTaskbar', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoSMHelp', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoTrayContextMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoViewContextMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoWindowUpdate', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoWinKeys', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'StartMenuLogOff', 0, win32con.REG_DWORD, 0)
            win32api.RegCloseKey(key)

            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'Explorer')
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
            key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'NoControlPanel', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoDrives', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoFileMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoFind', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoRealMode', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoRecentDocsMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoSetFolders', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoSetFolderOptions', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoViewOnDrive', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoClose', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoRun', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoDesktop', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoLogOff', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoFolderOptions', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoViewContextMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'HideClock', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoStartMenuMorePrograms', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoStartMenuMyGames', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoStartMenuMyMusic', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoStartMenuNetworkPlaces', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoStartMenuPinnedList', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoActiveDesktop', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoActiveDesktopChanges', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoChangeStartMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'ClearRecentDocsOnExit', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoFavoritesMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoRecentDocsHistory', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoSetTaskbar', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoSMHelp', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoTrayContextMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoViewContextMenu', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoWindowUpdate', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoWinKeys', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'StartMenuLogOff', 0, win32con.REG_DWORD, 0)
            win32api.RegCloseKey(key)

            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'System')
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'DisableTaskMgr', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'DisableRegistryTools', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'DisableChangePassword', 0, win32con.REG_DWORD, 0)
            win32api.RegCloseKey(key)

            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'System')
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'DisableTaskMgr', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'DisableRegistryTools', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'DisableChangePassword', 0, win32con.REG_DWORD, 0)
            win32api.RegCloseKey(key)

            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'ActiveDesktop')
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'NoComponents', 0, win32con.REG_DWORD, 0)
            win32api.RegSetValueEx(key, 'NoAddingComponents', 0, win32con.REG_DWORD, 0)
            win32api.RegCloseKey(key)

            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Policies\Microsoft\Windows\System',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Policies\Microsoft\Windows',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'System')
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Policies\Microsoft\Windows\System',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'DisableCMD', 0, win32con.REG_DWORD, 0)
            win32api.RegCloseKey(key)
    
            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Policies\Microsoft\Windows\System',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Policies\Microsoft\Windows',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'System')
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Policies\Microsoft\Windows\System',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'DisableCMD', 0, win32con.REG_DWORD, 0)
            win32api.RegCloseKey(key)

            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Policies\Microsoft\MMC\{8FC0B734-A0E1-11D1-A7D3-0000F87571E3}',0,win32con.KEY_ALL_ACCESS)
            except:
                try:
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Policies\Microsoft\MMC',0,win32con.KEY_ALL_ACCESS)
                except:
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Policies\Microsoft',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegCreateKey(key,'MMC')
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Policies\Microsoft\MMC',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'{8FC0B734-A0E1-11D1-A7D3-0000F87571E3}')
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Policies\Microsoft\MMC\{8FC0B734-A0E1-11D1-A7D3-0000F87571E3}',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'Restrict_Run', 0, win32con.REG_DWORD, 0)
            win32api.RegCloseKey(key)

            if self.language == 1:
                text = 'Fix system limitation successfully!'
            if self.language == 2:
                text = '修復系統限制成功!'
            if self.language == 3:
                text = '修复系统限制成功!'
            QMessageBox.information(self,'Done',text,QMessageBox.Ok,QMessageBox.Ok)

    def fiximg(self):
        if self.language == 1:
            text = 'Are you sure you want to repair the file open method?'
        if self.language == 2:
            text = '確定要修復文件打開方式嗎?'
        if self.language == 3:
            text = '确定要修复文件打开方式吗?'
        question = QMessageBox.warning(self,'Fixexeopen',text,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384:
            import win32api,win32con
            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'jpegfile', win32con.REG_SZ, 'JPEG Image')
                win32api.RegSetValue(key, '.exe', win32con.REG_SZ, 'exefile')
                win32api.RegSetValue(key, 'exefile', win32con.REG_SZ, 'Application')
                win32api.RegSetValue(key, '.com', win32con.REG_SZ, 'comfile')
                win32api.RegSetValue(key, 'comfile', win32con.REG_SZ, 'MS-DOS Application')
                win32api.RegSetValue(key, '.scr', win32con.REG_SZ, 'scrfile')
                win32api.RegSetValue(key, 'scrfile', win32con.REG_SZ, 'Screen saver')
                win32api.RegSetValue(key, '.zip', win32con.REG_SZ, 'CompressedFolder')
                win32api.RegSetValue(key, '.dll', win32con.REG_SZ, 'dllfile')
                win32api.RegSetValue(key, 'dllfile', win32con.REG_SZ, 'Application Extension')
                win32api.RegSetValue(key, '.sys', win32con.REG_SZ, 'sysfile')
                win32api.RegSetValue(key, 'sysfile', win32con.REG_SZ, 'System file')
                win32api.RegSetValue(key, '.bat', win32con.REG_SZ, 'batfile')
                win32api.RegSetValue(key, 'batfile', win32con.REG_SZ, 'Windows Batch File')
                win32api.RegSetValue(key, 'VBS', win32con.REG_SZ, 'VB Script Language')
                win32api.RegSetValue(key, 'VBSfile', win32con.REG_SZ, 'VBScript Script File')
                win32api.RegSetValue(key, '.txt', win32con.REG_SZ, 'txtfile')
                win32api.RegSetValue(key, 'txtfile', win32con.REG_SZ, 'Text Document')
                win32api.RegSetValue(key, '.msc', win32con.REG_SZ, 'MSCfile')
                win32api.RegSetValue(key, 'MSCfile', win32con.REG_SZ, 'Microsoft Common Console Document')
                win32api.RegSetValue(key, 'txtfile', win32con.REG_SZ, 'Text Document')
                keyopen = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\exefile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\comfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\scrfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" /S')

                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Classes',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'jpegfile', win32con.REG_SZ, 'JPEG Image')
                win32api.RegSetValue(key, '.exe', win32con.REG_SZ, 'exefile')
                win32api.RegSetValue(key, 'exefile', win32con.REG_SZ, 'Application')
                win32api.RegSetValue(key, '.com', win32con.REG_SZ, 'comfile')
                win32api.RegSetValue(key, 'comfile', win32con.REG_SZ, 'MS-DOS Application')
                win32api.RegSetValue(key, '.scr', win32con.REG_SZ, 'scrfile')
                win32api.RegSetValue(key, 'scrfile', win32con.REG_SZ, 'Screen saver')
                win32api.RegSetValue(key, '.zip', win32con.REG_SZ, 'CompressedFolder')
                win32api.RegSetValue(key, '.dll', win32con.REG_SZ, 'dllfile')
                win32api.RegSetValue(key, 'dllfile', win32con.REG_SZ, 'Application Extension')
                win32api.RegSetValue(key, '.sys', win32con.REG_SZ, 'sysfile')
                win32api.RegSetValue(key, 'sysfile', win32con.REG_SZ, 'System file')
                win32api.RegSetValue(key, '.bat', win32con.REG_SZ, 'batfile')
                win32api.RegSetValue(key, 'batfile', win32con.REG_SZ, 'Windows Batch File')
                win32api.RegSetValue(key, 'VBS', win32con.REG_SZ, 'VB Script Language')
                win32api.RegSetValue(key, 'VBSfile', win32con.REG_SZ, 'VBScript Script File')
                win32api.RegSetValue(key, '.txt', win32con.REG_SZ, 'txtfile')
                win32api.RegSetValue(key, 'txtfile', win32con.REG_SZ, 'Text Document')
                win32api.RegSetValue(key, '.msc', win32con.REG_SZ, 'MSCfile')
                win32api.RegSetValue(key, 'MSCfile', win32con.REG_SZ, 'Microsoft Common Console Document')
                win32api.RegSetValue(key, 'txtfile', win32con.REG_SZ, 'Text Document')
                keyopen = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\exefile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\comfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\scrfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" /S')

                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FileExts',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, '.exe', win32con.REG_SZ, '')
                win32api.RegSetValue(key, '.zip', win32con.REG_SZ, '')
                win32api.RegSetValue(key, '.dll', win32con.REG_SZ, '')
                win32api.RegSetValue(key, '.sys', win32con.REG_SZ, '')
                win32api.RegSetValue(key, '.bat', win32con.REG_SZ, '')
                win32api.RegSetValue(key, '.txt', win32con.REG_SZ, '')
                win32api.RegSetValue(key, '.msc', win32con.REG_SZ, '')

                key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,None,0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'jpegfile', win32con.REG_SZ, 'JPEG Image')
                win32api.RegSetValue(key, '.exe', win32con.REG_SZ, 'exefile')
                win32api.RegSetValue(key, 'exefile', win32con.REG_SZ, 'Application')
                win32api.RegSetValue(key, '.com', win32con.REG_SZ, 'comfile')
                win32api.RegSetValue(key, 'comfile', win32con.REG_SZ, 'MS-DOS Application')
                win32api.RegSetValue(key, '.scr', win32con.REG_SZ, 'scrfile')
                win32api.RegSetValue(key, 'scrfile', win32con.REG_SZ, 'Screen saver')
                win32api.RegSetValue(key, '.zip', win32con.REG_SZ, 'CompressedFolder')
                win32api.RegSetValue(key, '.dll', win32con.REG_SZ, 'dllfile')
                win32api.RegSetValue(key, 'dllfile', win32con.REG_SZ, 'Application Extension')
                win32api.RegSetValue(key, '.sys', win32con.REG_SZ, 'sysfile')
                win32api.RegSetValue(key, 'sysfile', win32con.REG_SZ, 'System file')
                win32api.RegSetValue(key, '.bat', win32con.REG_SZ, 'batfile')
                win32api.RegSetValue(key, 'batfile', win32con.REG_SZ, 'Windows Batch File')
                win32api.RegSetValue(key, '.cmd', win32con.REG_SZ, 'cmdfile')
                win32api.RegSetValue(key, 'cmdfile', win32con.REG_SZ, 'Windows Command Script')
                win32api.RegSetValue(key, '.vbs', win32con.REG_SZ, 'VBSfile')
                win32api.RegSetValue(key, 'VBS', win32con.REG_SZ, 'VB Script Language')
                win32api.RegSetValue(key, 'VBSfile', win32con.REG_SZ, 'VBScript Script File')
                win32api.RegSetValue(key, '.txt', win32con.REG_SZ, 'txtfile')
                win32api.RegSetValue(key, 'txtfile', win32con.REG_SZ, 'Text Document')
                win32api.RegSetValue(key, '.msc', win32con.REG_SZ, 'MSCfile')
                win32api.RegSetValue(key, 'MSCfile', win32con.REG_SZ, 'Microsoft Common Console Document')
                win32api.RegSetValue(key, 'txtfile', win32con.REG_SZ, 'Text Document')
                keyopen = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'exefile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'comfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'scrfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" /S')
                win32api.RegCloseKey(key)
                win32api.RegCloseKey(keyopen)
                if self.language == 1:
                    text = 'Repair file open method successfully!'
                if self.language == 2:
                    text = '修復文件打開方式成功!'
                if self.language == 3:
                    text = '修复文件打开方式成功!'
                QMessageBox.information(self,'Fixexeopen',text,QMessageBox.Ok,QMessageBox.Ok)
            except:
                if self.language == 1:
                    text = 'An error occurred'
                if self.language == 2:
                    text = '發生錯誤'
                if self.language == 3:
                    text = '发生错误'
                QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def english(self):
        if self.language == 1:
            text = 'Are you sure you want to switch languages?'
        if self.language == 2:
            text = '確定要切換語言嗎?'
        if self.language == 3:
            text = '确定要切换语言吗?'
        qusetion = QMessageBox.warning(self,'warning',text,QMessageBox.Yes|QMessageBox.No)
        if qusetion == 16384:
            self.language = 1
            _translate = QtCore.QCoreApplication.translate
            self.ui.Dostext.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">command</span></p></body></html>"))
            self.ui.RunDos.setText(_translate("MainWindow", "Run"))
            self.ui.exeuser.setText(_translate("MainWindow", "exe analyse:"))
            self.ui.processname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">name</span></p></body></html>"))
            self.ui.processPID.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">PID</span></p></body></html>"))
            self.ui.processfile.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-size:12pt;\">exe Path</span></p></body></html>"))
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.process), _translate("MainWindow", "Process"))
            self.ui.resetexplorerbut.setText(_translate("MainWindow", "Reboot Explorer"))
            self.ui.cleanuserpwbut.setText(_translate("MainWindow", "purge user password"))
            self.ui.fixlimitbut.setText(_translate("MainWindow", "relieve System limit"))
            self.ui.fiximgbut.setText(_translate("MainWindow", "repair file open manner"))
            self.ui.fixiconbut.setText(_translate("MainWindow", "repair file icon"))
            self.ui.fixexeimgbut.setText(_translate("MainWindow", "repair IFEO"))
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.Tools), _translate("MainWindow", "Tools"))
            self.ui.Taskbut.setText(_translate("MainWindow", "Taskmgr"))
            self.ui.Powershellbut.setText(_translate("MainWindow", "Powershell"))
            self.ui.regebut.setText(_translate("MainWindow", "Regedit"))
            self.ui.cmdbut.setText(_translate("MainWindow", "Cmd"))
            self.ui.Gpeditbut.setText(_translate("MainWindow", "Gpedit"))
            self.ui.controlbut.setText(_translate("MainWindow", "Control"))
            self.ui.MMCbut.setText(_translate("MainWindow", "MMC"))
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.Sysexe), _translate("MainWindow", "System exe"))
            self.ui.Shutdownbut.setText(_translate("MainWindow", "compulsion shutdown"))
            self.ui.resetbut.setText(_translate("MainWindow", "compulsion reboot"))
            self.ui.setUAC.setText(_translate("MainWindow", "set UAC"))
            self.ui.systeminfobut.setText(_translate("MainWindow", "System info"))
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.System), _translate("MainWindow", "System"))
            self.ui.menu.setTitle(_translate("MainWindow", "function"))
            self.ui.menu_3.setTitle(_translate("MainWindow", "language"))
            self.ui.menu_2.setTitle(_translate("MainWindow", "about"))
            self.ui.Close.setText(_translate("MainWindow", "Close"))
            self.ui.about_us.setText(_translate("MainWindow", "about"))
            self.ui.English.setText(_translate("MainWindow", "English"))
            self.ui.Chinese_T.setText(_translate("MainWindow", "traditional Chinese"))
            self.ui.Chinese_S.setText(_translate("MainWindow", "Simplified Chinese"))
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.Windowkill), _translate("MainWindow", "window blocking"))
            self.ui.hint.setText(_translate("MainWindow", "Operating status"))
            self.ui.Running.setText(_translate("MainWindow", "Run"))
            self.ui.stoping.setText(_translate("MainWindow", "Stop"))
            self.ui.windowkillbut.setText(_translate("MainWindow", "Ok"))
            self.ui.windowkilllist.setText(_translate("MainWindow", "Blocking window list"))
            self.ui.windowhint.setText(_translate("MainWindow", "Please enter the name of the window you want to block"))
            self.ui.execheckname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">file name:</span></p></body></html>"))
            self.ui.execheckpath.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">file Path:</span></p></body></html>"))
            self.ui.execheckabout.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">DLLs and functions called by the analyzed file and descriptions</span></p></body></html>"))
            self.ui.Danger_degree.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Dangerous:</span></p></body></html>"))
            self.ui.Danger_degreeview.setText(_translate("MainWindow", "0"))
            self.ui.Danger_degreehint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">Description: Dangerous degree index range: 0~10</span></p></body></html>"))
            self.ui.execheck.setText(_translate("MainWindow", "file analysis"))
            self.ui.hwnd.setText(_translate("MainWindow", "hwnd:"))
            self.ui.fixlimitbut.setGeometry(QtCore.QRect(10, 10, 110, 30))
            self.ui.fiximgbut.setGeometry(QtCore.QRect(130, 10, 140, 30))
            self.ui.resetexplorerbut.setGeometry(QtCore.QRect(610, 10, 100, 30))
            self.ui.cleanuserpwbut.setGeometry(QtCore.QRect(480, 10, 120, 30))
            self.ui.fixiconbut.setGeometry(QtCore.QRect(380, 10, 90, 30))
            self.ui.fixexeimgbut.setGeometry(QtCore.QRect(280, 10, 90, 30))
            self.ui.Shutdownbut.setGeometry(QtCore.QRect(10, 10, 130, 30))
            self.ui.resetbut.setGeometry(QtCore.QRect(150, 10, 120, 30))
            self.ui.setUAC.setGeometry(QtCore.QRect(280, 10, 80, 30))

    def chinese_t(self):
        if self.language == 1:
            text = 'Are you sure you want to switch languages?'
        if self.language == 2:
            text = '確定要切換語言嗎?'
        if self.language == 3:
            text = '确定要切换语言吗?'
        qusetion = QMessageBox.warning(self,'warning',text,QMessageBox.Yes|QMessageBox.No)
        if qusetion == 16384:
            self.language = 2
            _translate = QtCore.QCoreApplication.translate
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.Tools),"工具")
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.process),"進程")
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.System),"系統")
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.Sysexe),"系統程式")
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.Windowkill),"窗口攔截")
            self.ui.execheck.setText(_translate("MainWindow", "文件分析"))
            self.ui.processname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">名稱</span></p></body></html>"))
            self.ui.processPID.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">PID</span></p></body></html>"))
            self.ui.processfile.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-size:12pt;\">exe路徑</span></p></body></html>"))
            self.ui.hwnd.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">句柄:</span></p></body></html>"))
            self.ui.exeuser.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">使用者名稱:</span></p></body></html>"))
            self.ui.resetexplorerbut.setText(_translate("MainWindow", "重啟資源管理器"))
            self.ui.cleanuserpwbut.setText(_translate("MainWindow", "清除用戶密碼"))
            self.ui.fixlimitbut.setText(_translate("MainWindow", "解除系統限制"))
            self.ui.fiximgbut.setText(_translate("MainWindow", "修復打開方式"))
            self.ui.fixiconbut.setText(_translate("MainWindow", "修復程式圖標"))
            self.ui.fixexeimgbut.setText(_translate("MainWindow", "修復映像劫持"))
            self.ui.Shutdownbut.setText(_translate("MainWindow", "強制關機"))
            self.ui.resetbut.setText(_translate("MainWindow", "強制重啟"))
            self.ui.setUAC.setText(_translate("MainWindow", "設定UAC"))
            self.ui.systeminfobut.setText(_translate("MainWindow", "系統資訊"))
            self.ui.Dostext.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">CMD命令</span></p></body></html>"))
            self.ui.RunDos.setText(_translate("MainWindow", "執行"))
            self.ui.Taskbut.setText(_translate("MainWindow", "Taskmgr"))
            self.ui.Powershellbut.setText(_translate("MainWindow", "Powershell"))
            self.ui.regebut.setText(_translate("MainWindow", "Regedit"))
            self.ui.cmdbut.setText(_translate("MainWindow", "Cmd"))
            self.ui.Gpeditbut.setText(_translate("MainWindow", "Gpedit"))
            self.ui.controlbut.setText(_translate("MainWindow", "Control"))
            self.ui.MMCbut.setText(_translate("MainWindow", "MMC"))
            self.ui.windowhint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">請輸入要攔截窗口的名稱</span></p></body></html>"))
            self.ui.windowkillbut.setText(_translate("MainWindow", "確定"))
            self.ui.windowkilllist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">攔截窗口名單</span></p></body></html>"))
            self.ui.hint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">運行狀態:</span></p></body></html>"))
            self.ui.stoping.setText(_translate("MainWindow", "停止"))
            self.ui.Running.setText(_translate("MainWindow", "運行"))
            self.ui.execheckname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">文件名:</span></p></body></html>"))
            self.ui.execheckpath.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">文件路徑:</span></p></body></html>"))
            self.ui.execheckabout.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">受分析的文件調用的DLL及函數及說明</span></p></body></html>"))
            self.ui.Danger_degree.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">危險程度:</span></p></body></html>"))
            self.ui.Danger_degreeview.setText(_translate("MainWindow", "0"))
            self.ui.Danger_degreehint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">說明:危險程度指標範圍:0~10</span></p></body></html>"))
            self.ui.menu.setTitle(_translate("MainWindow", "功能"))
            self.ui.menu_3.setTitle(_translate("MainWindow", "語言"))
            self.ui.menu_2.setTitle(_translate("MainWindow", "關於"))
            self.ui.video_view.setText(_translate("MainWindow", "video view"))
            self.ui.Close.setText(_translate("MainWindow", "關閉"))
            self.ui.about_us.setText(_translate("MainWindow", "about"))
            self.ui.English.setText(_translate("MainWindow", "English"))
            self.ui.Chinese_T.setText(_translate("MainWindow", "traditional Chinese"))
            self.ui.Chinese_S.setText(_translate("MainWindow", "Simplified Chinese"))
            self.ui.hwnd.setText(_translate("MainWindow", "句柄:"))
            self.ui.fixlimitbut.setGeometry(QtCore.QRect(10, 10, 90, 30))
            self.ui.fiximgbut.setGeometry(QtCore.QRect(110, 10, 90, 30))
            self.ui.resetexplorerbut.setGeometry(QtCore.QRect(510, 10, 90, 30))
            self.ui.cleanuserpwbut.setGeometry(QtCore.QRect(410, 10, 90, 30))
            self.ui.fixiconbut.setGeometry(QtCore.QRect(310, 10, 90, 30))
            self.ui.fixexeimgbut.setGeometry(QtCore.QRect(210, 10, 90, 30))
            self.ui.Shutdownbut.setGeometry(QtCore.QRect(10, 10, 80, 30))
            self.ui.resetbut.setGeometry(QtCore.QRect(100, 10, 80, 30))
            self.ui.setUAC.setGeometry(QtCore.QRect(190, 10, 80, 30))

    def chinese_s(self):
        if self.language == 1:
            text = 'Are you sure you want to switch languages?'
        if self.language == 2:
            text = '確定要切換語言嗎?'
        if self.language == 3:
            text = '确定要切换语言吗?'
        qusetion = QMessageBox.warning(self,'warning',text,QMessageBox.Yes|QMessageBox.No)
        if qusetion == 16384:
            self.language = 3
            _translate = QtCore.QCoreApplication.translate
            self.ui.execheck.setText(_translate("MainWindow", "文件分析"))
            self.ui.Dostext.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">CMD命令</span></p></body></html>"))
            self.ui.RunDos.setText(_translate("MainWindow", "执行"))
            self.ui.exeuser.setText(_translate("MainWindow", "软件分析"))
            self.ui.processname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">名称</span></p></body></html>"))
            self.ui.processPID.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">PID</span></p></body></html>"))
            self.ui.processfile.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-size:12pt;\">exe路径</span></p></body></html>"))
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.process), _translate("MainWindow", "进程"))
            self.ui.resetexplorerbut.setText(_translate("MainWindow", "重启Explorer"))
            self.ui.cleanuserpwbut.setText(_translate("MainWindow", "清除用户密码"))
            self.ui.fixlimitbut.setText(_translate("MainWindow", "解除系统限制"))
            self.ui.fiximgbut.setText(_translate("MainWindow", "修复打开方式"))
            self.ui.fixiconbut.setText(_translate("MainWindow", "修复软件图标"))
            self.ui.fixexeimgbut.setText(_translate("MainWindow", "修复映像劫持"))
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.Tools), _translate("MainWindow", "工具"))
            self.ui.Taskbut.setText(_translate("MainWindow", "Taskmgr"))
            self.ui.Powershellbut.setText(_translate("MainWindow", "Powershell"))
            self.ui.regebut.setText(_translate("MainWindow", "Regedit"))
            self.ui.cmdbut.setText(_translate("MainWindow", "Cmd"))
            self.ui.Gpeditbut.setText(_translate("MainWindow", "Gpedit"))
            self.ui.controlbut.setText(_translate("MainWindow", "Control"))
            self.ui.MMCbut.setText(_translate("MainWindow", "MMC"))
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.Sysexe), _translate("MainWindow", "系统软件"))
            self.ui.Shutdownbut.setText(_translate("MainWindow", "强制关机"))
            self.ui.resetbut.setText(_translate("MainWindow", "强制重启"))
            self.ui.setUAC.setText(_translate("MainWindow", "设定UAC"))
            self.ui.systeminfobut.setText(_translate("MainWindow", "系统信息"))
            self.ui.Toolsmenu.setTabText(self.ui.Toolsmenu.indexOf(self.ui.System), _translate("MainWindow", "系统"))
            self.ui.menu.setTitle(_translate("MainWindow", "功能"))
            self.ui.menu_3.setTitle(_translate("MainWindow", "语言"))
            self.ui.menu_2.setTitle(_translate("MainWindow", "关于"))
            self.ui.Close.setText(_translate("MainWindow", "关闭"))
            self.ui.about_us.setText(_translate("MainWindow", "关于"))
            self.ui.English.setText(_translate("MainWindow", "英语"))
            self.ui.Chinese_T.setText(_translate("MainWindow", "繁体中文"))
            self.ui.Chinese_S.setText(_translate("MainWindow", "简体中文"))
            self.ui.execheckname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">文件名:</span></p></body></html>"))
            self.ui.execheckpath.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">文件路径:</span></p></body></html>"))
            self.ui.execheckabout.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">受分析的文件调用的DLL及函数及说明</span></p></body></html>"))
            self.ui.Danger_degree.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">危险程度:</span></p></body></html>"))
            self.ui.Danger_degreeview.setText(_translate("MainWindow", "0"))
            self.ui.Danger_degreehint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt;\">说明:危险程度指标范围:0~10</span></p></body></html>"))
            self.ui.menu.setTitle(_translate("MainWindow", "功能"))
            self.ui.windowhint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">请输入要拦截窗口的名称</span></p></body></html>"))
            self.ui.windowkillbut.setText(_translate("MainWindow", "确定"))
            self.ui.windowkilllist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">拦截窗口名单</span></p></body></html>"))
            self.ui.hint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">运行状态:</span></p></body></html>"))
            self.ui.stoping.setText(_translate("MainWindow", "停止"))
            self.ui.Running.setText(_translate("MainWindow", "运行"))
            self.ui.hwnd.setText(_translate("MainWindow", "句柄:"))
            self.ui.fixlimitbut.setGeometry(QtCore.QRect(10, 10, 90, 30))
            self.ui.fiximgbut.setGeometry(QtCore.QRect(110, 10, 90, 30))
            self.ui.resetexplorerbut.setGeometry(QtCore.QRect(510, 10, 90, 30))
            self.ui.cleanuserpwbut.setGeometry(QtCore.QRect(410, 10, 90, 30))
            self.ui.fixiconbut.setGeometry(QtCore.QRect(310, 10, 90, 30))
            self.ui.fixexeimgbut.setGeometry(QtCore.QRect(210, 10, 90, 30))
            self.ui.Shutdownbut.setGeometry(QtCore.QRect(10, 10, 80, 30))
            self.ui.resetbut.setGeometry(QtCore.QRect(100, 10, 80, 30))
            self.ui.setUAC.setGeometry(QtCore.QRect(190, 10, 80, 30))

    def killprocess(self,exe):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = subprocess.call('%s%s' % ("taskkill /F /IM ",exe),startupinfo=si)
        return result

    def Taskmgr(self):
        try:
            self.OpenProcess0(exe=r'C:/Windows/System32/Taskmgr.exe')
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)


    def regedit(self):
        try:
            self.OpenProcess0(exe=r'C:/Windows/regedit.exe')
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def cmd(self):
        try:
            import win32api
            win32api.ShellExecute( 0, 'open' , r'c:/Windows/System32/cmd.exe' , None ,None , 1 )
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def Powershell(self):
        try:
            import win32api
            win32api.ShellExecute( 0, 'open' , 'Powershell' , None ,None , 1 )
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def control(self):
        try:
            self.OpenProcess0(exe=r'C:/Windows/System32/Control.exe')
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def MMC(self):
        try:
            self.OpenProcess0(exe=r'C:/Windows/System32/mmc.exe')
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def Gpedit(self):
        try:
            import win32api
            win32api.ShellExecute( 0, 'open' , 'gpedit.msc' , None ,None , 1 )
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def resetexplorer(self):
        try:
            self.killprocess('explorer.exe')
            self.OpenProcess0(r'c:/Windows/explorer.exe')
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def cleanUserPassword(self):
        if self.language == 1:
            text = 'Are you sure you want to clear the current user\'s password?'
        if self.language == 2:
            text = '確定清除當前用戶的密碼嗎?'
        if self.language == 3:
            text = '确定清除当前用户的密码吗?'
        question = QMessageBox.warning(self,'Password',text,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384:
            try:
                Username = getpass.getuser()
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.call('net user ' + Username + " \"\"",startupinfo=si)
                if self.language == 1:
                    text = 'Clear user password successfully!'
                if self.language == 2:
                    text = '清除用戶密碼成功!'
                if self.language == 3:
                    text = '清除用户密码成功!'
                QMessageBox.information(self,'Password',text,QMessageBox.Ok,QMessageBox.Ok)
            except:
                if self.language == 1:
                    text = 'An error occurred'
                if self.language == 2:
                    text = '發生錯誤'
                if self.language == 3:
                    text = '发生错误'
                QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def get_all_hwnd(self,hwnd,mouse):
        self.hwnd_title.update({hwnd:win32gui.GetWindowText(hwnd)})

    def generateMenu(self,pos):  
        self.ui.hwndview.setText('')
        self.item = self.ui.processlist.selectedIndexes()
        for i in self.item:
            item = i.row()
            self.pid = self.qList_pid[item]
            self.exefile = self.qList_exe[item]
            self.exename = self.qList_name[item]

        self.hwnd_title = dict() 
        win32gui.EnumWindows(self.get_all_hwnd,0)
        for h,title in self.hwnd_title.items():
            th,hwndpid = win32process.GetWindowThreadProcessId(h)
            if hwndpid == self.pid:       
                self.ui.hwndview.setText(str(h))
                hwnd = h
        self.processuser()
        self.popMenu = QMenu()
        if self.language == 1:
            text = 'end process'
        if self.language == 2:
            text = '結束進程'
        if self.language == 3:
            text = '结束进程'
        self.killp = QAction(text,self)
        if self.language == 1:
            text = 'open exe path'
        if self.language == 2:
            text = '打開exe路徑'
        if self.language == 3:
            text = '打开exe路径'
        exefile = QAction(text,self)
        self.popMenu.addAction(self.killp)
        self.popMenu.addAction(exefile)
        self.exe = self.popMenu.exec_(self.ui.processlist.mapToGlobal(pos))
        error = 0
        if self.exe == self.killp:
            try:
                self.user32dll.EndTask(hwnd,False,True)
                if self.language == 1:
                    text = 'Terminate the program:'
                if self.language == 2:
                    text = '終止程式:'
                if self.language == 3:
                    text = '终止软件:'
                if self.language == 1:
                    text2 = 'success'
                if self.language == 2:
                    text2 = '成功'
                if self.language == 3:
                    text2 = '成功'          
                QMessageBox.information(self,'Done',text + self.exename + text2,QMessageBox.Ok)
                error = 0
            except:
                error = 1
            if error == 1:
                try:
                    for p in psutil.process_iter():
                        if p.pid == self.pid:
                            p.kill()
                            if self.language == 1:
                                text = 'Terminate the program:'
                            if self.language == 2:
                                text = '終止程式:'
                            if self.language == 3:
                                text = '终止软件:'
                            if self.language == 1:
                                text2 = 'success'
                            if self.language == 2:
                                text2 = '成功'
                            if self.language == 3:
                                text2 = '成功'                            
                            error = 0
                            QMessageBox.information(self,'Done',text + p.name() + text2,QMessageBox.Ok)
                except:
                    error = 1
            if error == 1:
                if self.language == 1:
                    text = 'access denied'
                if self.language == 2:
                    text = '存取被拒'
                if self.language == 3:
                    text = '存取被拒'   
                QMessageBox.critical(self,'error',text,QMessageBox.Ok)
        if self.exe == exefile:
            try:
                a = len(self.exename)
                b = len(self.exefile)
                self.exefile = self.exefile[0:b - a]
                subprocess.call('explorer ' + self.exefile,shell=True)
            except:
                if self.language == 1:
                    text = 'An error occurred!'
                if self.language == 2:
                    text = '發生錯誤!'
                if self.language == 3:
                    text = '发生错误!'
                QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def processhwnd(self):
        try:
            self.ui.hwndview.setText('')
            self.item = self.ui.processlist.selectedIndexes()
            for i in self.item:
                item = i.row()
                pid = self.qList_pid[item]
            self.hwnd_title = dict() 
            win32gui.EnumWindows(self.get_all_hwnd,0)
            for hwnd,title in self.hwnd_title.items():
                th,hwndpid = win32process.GetWindowThreadProcessId(hwnd)
                if hwndpid == pid:        
                    self.ui.hwndview.setText(str(hwnd))
        except:
            pass

    def processuser(self):
        try:
            self.ui.exeuserview.setText('')
            item = self.ui.processlist.selectedIndexes()
            for i in item:
                item = i.row()
                username = self.qList_user[item]
            self.ui.exeuserview.setText(username)
        except:
            pass

    def fixicon(self):
        if self.language == 1:
            text = 'Are you sure you want to fix the program icon?'
        if self.language == 2:
            text = '確定要修復程式圖標嗎?'
        if self.language == 3:
            text = '确定要修复软件图标吗?'
        question = QMessageBox.warning(self,'FixIcon',text,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384:
            import win32api,win32con
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'exefile',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, '%1')
            except:
                pass
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'comfile',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, '%SystemRoot%\System32\shell32.dll,2')
            except:
                pass
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'txtfile',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, '%SystemRoot%\system32\imageres.dll,-102')
            except:
                pass
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'dllfile',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, 'C:\Windows\system32\imageres.dll,-67')
            except:
                pass
            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\exefile',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, '%1')
            except:
                pass
            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\comfile',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, '%SystemRoot%\System32\shell32.dll,2')
            except:
                pass
            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\\txtfile',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, '%SystemRoot%\system32\imageres.dll,-102')
            except:
                pass
            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\dllfile',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, 'C:\Windows\system32\imageres.dll,-67')
            except:
                pass
            win32api.CloseHandle(key)
            if self.language == 1:
                text = 'Repair done!'
            if self.language == 2:
                text = '修復完成!'
            if self.language == 3:
                text = '修复完成!'
            QMessageBox.information(self,'Done',text,QMessageBox.Ok,QMessageBox.Ok)

    def fixexeimg(self):
        if self.language == 1:
            text = 'Are you sure you want to fix IFEO?'
        if self.language == 2:
            text = '確定要修復映像劫持嗎?'
        if self.language == 3:
            text = '确定要修复映像劫持吗?'
        question = QMessageBox.warning(self,'Fixexeimg',text,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384:
            import win32api,win32con
            key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options',0,win32con.KEY_ALL_ACCESS | win32con.WRITE_OWNER)
            count = win32api.RegQueryInfoKey(key)[0]
            while count >= 0:
                try:
                    subKeyName = win32api.RegEnumKey(key, count)
                except:
                    pass
                try:
                    win32api.RegDeleteKey(key, subKeyName)
                    count = count - 1
                except:
                    count = count - 1
            if self.language == 1:
                text = 'Repair done!'
            if self.language == 2:
                text = '修復完成!'
            if self.language == 3:
                text = '修复完成!'
            QMessageBox.information(self,'Done',text,QMessageBox.Ok,QMessageBox.Ok)

    def Shutdown(self):
        if self.language == 1:
            text = 'Are you sure you want to force shutdown?'
        if self.language == 2:
            text = '確定要強制關機嗎?'
        if self.language == 3:
            text = '确定要强制关机吗?'
        question = QMessageBox.warning(self,'Shutdown',text,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384:
            try:
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.call('Shutdown -s -f -t 0',startupinfo=si)
            except:
                if self.language == 1:
                    text = 'An error occurred!'
                if self.language == 2:
                    text = '發生錯誤!'
                if self.language == 3:
                    text = '发生错误!'
                QMessageBox.critical(self,'error',text,QMessageBox.Ok)


    def reset(self):
        if self.language == 1:
            text = 'Are you sure you want to force restart?'
        if self.language == 2:
            text = '確定要強制重啟嗎?'
        if self.language == 3:
            text = '确定要强制重启吗?'
        question = QMessageBox.warning(self,'Reset',text,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384:
            try:
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.call('Shutdown -r -f -t 0',startupinfo=si)
            except:
                if self.language == 1:
                    text = 'An error occurred!'
                if self.language == 2:
                    text = '發生錯誤!'
                if self.language == 3:
                    text = '发生错误!'
                QMessageBox.critical(self,'error',text,QMessageBox.Ok)
    
    def systeminfogrt(self):
        self.info = QtWidgets.QMainWindow()
        self.infoui = Ui_info()
        self.infoui.setupUi(self.info)
        self.info.show()
        cpu = psutil.cpu_count(logical=False)
        cpu_logical = psutil.cpu_count()
        systeminfo = platform.version()
        systembit = platform.architecture()
        # self.cpuuse = psutil.cpu_percent(interval=0.5, percpu=True)
        # self.cpu_freq = psutil.cpu_freq()
        # self.ram = psutil.virtual_memory()

        _translate = QtCore.QCoreApplication.translate
        self.infoui.cpus.setText(_translate("info", "<html><head/><body><p align=\"justify\"><span style=\" font-size:12pt;\">" + str(cpu) + "</span></p></body></html>"))
        self.infoui.cpu_logs.setText(_translate("info", "<html><head/><body><p align=\"justify\"><span style=\" font-size:12pt;\">" + str(cpu_logical) + "</span></p></body></html>"))
        self.infoui.systemversions.setText(_translate("info", "<html><head/><body><p align=\"justify\"><span style=\" font-size:12pt;\">" + str(systeminfo) + "</span></p></body></html>"))
        self.infoui.system_bits.setText(_translate("info", "<html><head/><body><p align=\"justify\"><span style=\" font-size:12pt;\">" + str(systembit) + "</span></p></body></html>"))

    def uac(self):
        self.widget = QtWidgets.QDialog()
        self.UAC = UAC_UI.Ui_Dialog()
        self.UAC.setupUi(self.widget)
        self.widget.show()

    def about(self):
        QMessageBox.about(self,'about','made by mtkiao129(litesans)')

    def Rundos(self):
        dos = self.ui.Dos.text()
        if dos == "":
            if self.language == 1:
                text = 'Please enter a command!'
            if self.language == 2:
                text = '請輸入命令!'
            if self.language == 3:
                text = '请输入命令!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok,QMessageBox.Ok)
        else:
            try:
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.call(dos,startupinfo=si)
                if self.language == 1:
                    text = 'execution succeed!'
                if self.language == 2:
                    text = '執行成功!'
                if self.language == 3:
                    text = '执行成功!'
                QMessageBox.information(self,'Done',text,QMessageBox.Ok,QMessageBox.Ok)
            except:
                if self.language == 1:
                    text = 'Not a valid command or access denied'
                if self.language == 2:
                    text = '不是有效命令或存取被拒'
                if self.language == 3:
                    text = '不是有效命令或存取被拒'
                QMessageBox.critical(self,'error', '\"' + dos + '\"' + text,QMessageBox.Ok,QMessageBox.Ok)
    
    def check(self):
        filepath, filetype= QFileDialog.getOpenFileName(self,"文件分析","./",'EXE Files *.exe;;COM Files *.com;;SCR Files *.scr')     
        if not filepath:
            pass
        elif filepath != '':
            filename = filepath
            a = 0
            while True:
                if filename[a] == '/':
                    a = a + 1
                    filename = filepath[a:]
                    self.ui.exechecknameview.setText(filename)
                    break
                else:
                    a = a - 1
            self.ui.execheckpathview.setText(filepath)
            try:
                exefile = pefile.PE(filepath) 
            except:
                QMessageBox.critical(self,'error','發生錯誤',QMessageBox.Ok)
            self.execheck=QStringListModel()
            self.execheckdll = []
            self.execheckfun = []
            try:
                for entry in exefile.DIRECTORY_ENTRY_IMPORT: 
                    try:
                        self.execheckdll.append(str(entry.dll))
                    except:
                        pass
                    for function in entry.imports: 
                        try:
                            self.execheckfun.append(str(function.name) + '  說明:' +fun_list[str(function.name)])
                        except:
                            self.execheckfun.append(str(function.name) + '  說明: (未知)')
            except:
                pass
            self.execheck.setStringList(self.execheckdll + self.execheckfun)
            self.ui.execheckview.setModel(self.execheck)


    def beautification(self):
        # self.ui.centralwidget.setStyleSheet('''
        # QWidget#centralwidget{
        #     color:#232C51;
        #     border-top:1px solid darkGray;
        #     border-bottom:1px solid darkGray;
        #     border-right:1px solid darkGray;
        #     border-top-right-radius:10px;
        #     border-bottom-right-radius:10px;
        #     border-left:1px solid darkGray;
        #     border-top-left-radius:10px;
        #     border-bottom-left-radius:10px;
        # }
        # ''')


        self.ui.processlist.setStyleSheet('''
        QWidget::item
        {
        background-color: #393d49;
        color: #00BFFF;
        border: transparent;
        border-bottom: 1px solid #dbdbdb;
        padding: 5px;
        }

        QWidget::item:hover
        {
        background-color: #5F5F5F;
        padding: 6px;
        }

        QWidget::item:selected
        {
        border-left: 5px solid #777777;
        }

        QListView
        {
        outline: none;
        }
        ''')

        self.ui.processlist.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.setStyleSheet('''
        qdarkstyle.load_stylesheet_pyqt5()
        ''')

if is_admin:
    if __name__ == '__main__':
        import sys
        app = QtWidgets.QApplication(sys.argv)
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5',palette=qdarkstyle.LightPalette))
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
else:
    windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__)