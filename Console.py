#導入模塊
try:
    import getpass,subprocess,configparser,pefile,platform,win32gui,UAC_UI,win32process,psutil,base64,win32api,win32con,win32timezone
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5 import QtWidgets,QtCore
    from Main_UI import Ui_MainWindow
    from systeminfo import Ui_info
    import about
    import Setting_Console
    import os
    from library import fun_list
    from img import explode
    from ctypes import windll
except Exception as error:
    print('An error occurred!\nreason:' + str(error))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.UAC = ''
        self.ui.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAcceptDrops(True)
        self.setup_control()
    def setup_control(self):
        # System_app
        self.ui.SystemApp_Button.clicked.connect(self.changeSystemApp)
        self.ui.Taskmgr_Button.clicked.connect(self.Taskmgr)
        self.ui.Regedit_Button.clicked.connect(self.regedit)
        self.ui.Cmd_Button.clicked.connect(self.cmd)
        self.ui.Powershell_Button.clicked.connect(self.Powershell)
        self.ui.Control_Button.clicked.connect(self.control)
        self.ui.MMC_Button.clicked.connect(self.MMC)
        self.ui.Gpedit_Button.clicked.connect(self.Gpedit)
        self.ui.Calc_Button.clicked.connect(self.Calc)
        self.ui.Compmgmt_Button.clicked.connect(self.Compmgmt)
        self.ui.Devmgmt_Button.clicked.connect(self.Devmgmt)
        self.ui.Dxdiag_Button.clicked.connect(self.Dxdiag)
        self.ui.Lusrmgr_Button.clicked.connect(self.Lusrmgr)
        self.ui.Magnify_Button.clicked.connect(self.Magnify)
        self.ui.Msinfo32_Button.clicked.connect(self.Msinfo32)
        self.ui.Winver_Button.clicked.connect(self.Winver)
        self.ui.Msconfig_Button.clicked.connect(self.msconfig)

        # Utilities
        self.ui.Utilities_Button.clicked.connect(self.changeUtilities)
        self.ui.Fix_limit_Button.clicked.connect(self.fixlimit)
        self.ui.Fix_file_open_way_Button.clicked.connect(self.fiximg)
        self.ui.Reopen_explorer_Button.clicked.connect(self.resetexplorer)
        self.ui.Clear_user_password_Button.clicked.connect(self.cleanUserPassword)
        self.ui.Fix_file_icon_Button.clicked.connect(self.fixicon)
        self.ui.Fix_IEFO_Button.clicked.connect(self.fixexeimg)
        self.ui.recover_Wallpaper_Button.clicked.connect(self.recover_Wallpaper)

        # System
        self.ui.System_Button.clicked.connect(self.changeSystem)
        self.ui.Shutdownbut.clicked.connect(self.Shutdown)
        self.ui.resetbut.clicked.connect(self.reset)
        self.ui.LogOff_Buttun.clicked.connect(self.logoff)
        self.ui.End_not_system_process_Buttun.clicked.connect(self.end_not_system_process)
        self.ui.Disable_exe_run_text_Buttun.clicked.connect(self.Disable_exe_run)
        self.ui.RunDos.clicked.connect(self.Rundos)
        self.ui.systeminfobut.clicked.connect(self.systeminfogrt)
        self.ui.Explorer_setting_show_file_extension_check.clicked.connect(self.Explorer_setting_show_file_extension)
        self.ui.Explorer_setting_show_hide_file_check.clicked.connect(self.Explorer_setting_show_hide_file)
        self.ui.Explorer_setting_show_hide_system_file_check.clicked.connect(self.Explorer_setting_show_hide_system_file)
        self.ui.Disable_exe_run_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.Disable_exe_run_list.customContextMenuRequested.connect(self.Disable_exe_run_del)

        # Window
        self.ui.about_us.triggered.connect(self.about)
        self.ui.Close_Button.clicked.connect(self.close)
        self.ui.minimize_Button.clicked.connect(self.showMinimized)
        self.ui.Menu_Button.clicked.connect(self.showMenu)

        # Process
        self.ui.Process_manage_Button.clicked.connect(self.changeProcess)
        self.ui.Process_list.clicked.connect(self.processhwnd)
        self.ui.Process_list.clicked.connect(self.processuser)
        self.ui.Process_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.Process_list.customContextMenuRequested.connect(self.generateMenu)

        #WindowBlocking
        self.ui.WindowBlocking_Button.clicked.connect(self.changeWindowBlocking)
        self.ui.windowkillbut.clicked.connect(self.window_blocking)
        self.ui.windowlistview.clicked.connect(self.windowview)
        self.ui.windowkillview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.windowkillview.customContextMenuRequested.connect(self.delexekill)
        self.ui.stoping.toggled.connect(self.setRunning)
        self.ui.Running.toggled.connect(self.setRunning)

        # analyze
        self.ui.File_analyze_Button.clicked.connect(self.changeFile_analyze)
        self.ui.execheck.clicked.connect(self.check)

        # dialog
        self.ui.setUAC.clicked.connect(self.uac)

        # other
        self.slm=QStringListModel()
        self.quantity = 0
        self.listprocess()
        self.quantity = len(self.qList_exe)
        self.ui.Process_total_View.setText(str(self.quantity))

        # Qtimer
        self.timer=QTimer()
        self.timer.timeout.connect(self.listprocess)
        self.timer.start(200)
        self.applist=QTimer()
        self.applist.timeout.connect(self.windowlist)
        self.applist.start(1000)
        self.DisableQTimer=QTimer()
        self.DisableQTimer.timeout.connect(self.update_Disable_exe_list)
        self.DisableQTimer.start(1000)
        self.exekill=QTimer()
        self.exekill.timeout.connect(self.killwindow)
        self.Setting=QTimer()
        self.Setting.timeout.connect(self.setting_update)
        self.Setting.start(1000)

        # init
        try:
            self.config = configparser.RawConfigParser()
            self.config.optionxform = str
            self.config.read('stg.ini')
            self.Main_top = self.config.get('Setting','Main_top')
            self.Minimize = self.config.get('Setting','Minimize')
            self.Language_value = self.config.get('Setting','Language')
        except:
            with open('stg.ini',mode='w',encoding='utf-8') as file:
                file.write('[app]\n\n[Setting]\nMinimize = True\nMain_top = False\nLanguage = Traditional_Chinese') 
            self.config = configparser.RawConfigParser()
            self.config.optionxform = str
            self.config.read('stg.ini')
            self.Main_top = self.config.get('Setting','Main_top')
            self.Minimize = self.config.get('Setting','Minimize')
            self.Language_value = self.config.get('Setting','Language')
        self.Language_init()
        self.The_Another_check = 0
        self.ui.stoping.setChecked(True)
        self.user32dll = windll.LoadLibrary(r"C:\Windows\System32\user32.dll") 
        self.hwnd_title2 = dict() 
        self.ui.Menu_Button.setAutoRaise(True)
        self.beautification()
        self.init_explorer_setting()

        # ini
        try:
            self.config = configparser.RawConfigParser()
            self.config.optionxform = str
            self.config.read('stg.ini')
            self.Main_top = self.config.get('Setting','Main_top')
            self.Minimize = self.config.get('Setting','Minimize')
            self.Language_value = self.config.get('Setting','Language')
            if self.Main_top == 'True':
                self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Window)
                self.setFixedSize(self.width(), self.height())
                self.setAttribute(Qt.WA_TranslucentBackground)
                self.showNormal()
            elif self.Main_top == 'False':
                self.setWindowFlags(QtCore.Qt.Window | Qt.FramelessWindowHint)
                self.setFixedSize(self.width(), self.height())
                self.setAttribute(Qt.WA_TranslucentBackground)
                self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
                self.showNormal()   
            if self.Minimize == 'True':
                self.trayIcon.show()
        except:
            with open('stg.ini',mode='w',encoding='utf-8') as file:
                file.write('[app]\n\n[Setting]\nMinimize = True\nMain_top = False\nLanguage = Traditional_Chinese') 

        self.ui.Utilities.hide()
        self.ui.System.hide()
        self.ui.SystemApp.hide()
        self.ui.WindowBlocking.hide()
        self.ui.File_analyze.hide()

    def Language_init(self):
        if self.Language_value == 'Traditional_Chinese':
            self.language = 3
            self.chinese_t()
        elif self.Language_value == 'English':
            self.language = 1
            self.english()
        elif self.Language_value == 'Simplified_Chinese':
            self.language = 2
            self.chinese_s()

    def init_explorer_setting(self):
        try:
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
        except:
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer',0,win32con.KEY_ALL_ACCESS)
            win32api.RegCreateKey(key,'Advanced')
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
        for i in range(0,win32api.RegQueryInfoKey(key)[1]):
            if win32api.RegEnumValue(key,i)[0] == 'HideFileExt':
                if win32api.RegEnumValue(key,i)[1] == 0:
                    self.ui.Explorer_setting_show_file_extension_check.setChecked(True)
            if win32api.RegEnumValue(key,i)[0] == 'Hidden':
                if win32api.RegEnumValue(key,i)[1] == 1:
                    self.ui.Explorer_setting_show_hide_file_check.setChecked(True)
            if win32api.RegEnumValue(key,i)[0] == 'ShowSuperHidden':
                if win32api.RegEnumValue(key,i)[1] == 1:
                    self.ui.Explorer_setting_show_hide_system_file_check.setChecked(True)

    def Explorer_setting_show_file_extension(self):
        import win32api,win32con
        if self.ui.Explorer_setting_show_file_extension_check.isChecked():
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'Advanced')
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'HideFileExt', 0, win32con.REG_DWORD, 0)
        elif self.ui.Explorer_setting_show_file_extension_check.isCheckable():
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'Advanced')
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'HideFileExt', 0, win32con.REG_DWORD, 1)

    def Explorer_setting_show_hide_file(self):
        import win32api,win32con
        if self.ui.Explorer_setting_show_hide_file_check.isChecked():
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'Advanced')
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'Hidden', 0, win32con.REG_DWORD, 1)
        elif self.ui.Explorer_setting_show_hide_file_check.isCheckable():
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'Advanced')
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'Hidden', 0, win32con.REG_DWORD, 2)

    def Explorer_setting_show_hide_system_file(self):
        import win32api,win32con
        if self.ui.Explorer_setting_show_hide_system_file_check.isChecked():
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'Advanced')
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'ShowSuperHidden', 0, win32con.REG_DWORD, 1)
        elif self.ui.Explorer_setting_show_hide_system_file_check.isCheckable():
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
            except:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer',0,win32con.KEY_ALL_ACCESS)
                win32api.RegCreateKey(key,'Advanced')
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced',0,win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, 'ShowSuperHidden', 0, win32con.REG_DWORD, 2)

    def setting_update(self):
        if not os.path.isfile(r'./stg.ini'):
            with open('stg.ini',mode='w',encoding='utf-8') as file:
                file.write('[app]')
                file.write('\n\n[Setting]\nMinimize = True\nMain_top = False')
        self.config = configparser.RawConfigParser()
        self.config.optionxform = str
        self.config.read('stg.ini')
        self.Main_top2 = self.config.get('Setting','Main_top')
        self.Minimize2 = self.config.get('Setting','Minimize')
        if self.Main_top2 != self.Main_top:
            self.Main_top = self.Main_top2
            if self.Main_top == 'True':
                self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Window)
                self.setFixedSize(self.width(), self.height())
                self.setAttribute(Qt.WA_TranslucentBackground)
                self.showNormal()
            elif self.Main_top == 'False':
                self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Window)
                self.setFixedSize(self.width(), self.height())
                self.setAttribute(Qt.WA_TranslucentBackground)
                self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
                self.showNormal()
        if self.Minimize2 != self.Minimize:
            self.Minimize = self.Minimize2
            if self.Minimize == 'True':
                self.trayIcon.show()
            else:
                QMessageBox.information(None,'Wanring','重啟生效',QMessageBox.Ok)

    def get_pic(self,pic_code, pic_name):
        image = open(pic_name, 'wb')
        image.write(base64.b64decode(pic_code))
        image.close()

    def changeProcess(self):
        self.ui.Utilities.hide()
        self.ui.System.hide()
        self.ui.SystemApp.hide()
        self.ui.WindowBlocking.hide()
        self.ui.File_analyze.hide()
        self.ui.Process.show()

    def changeUtilities(self):
        self.ui.Process.hide()
        self.ui.System.hide()
        self.ui.SystemApp.hide()
        self.ui.File_analyze.hide()
        self.ui.WindowBlocking.hide()
        self.ui.Utilities.show()

    def changeSystem(self):
        self.ui.Process.hide()
        self.ui.Utilities.hide()
        self.ui.SystemApp.hide()
        self.ui.File_analyze.hide()
        self.ui.WindowBlocking.hide()
        self.ui.System.show()

    def changeSystemApp(self):
        self.ui.Process.hide()
        self.ui.Utilities.hide()
        self.ui.WindowBlocking.hide()
        self.ui.System.hide()
        self.ui.File_analyze.hide()
        self.ui.SystemApp.show()

    def changeWindowBlocking(self):
        self.ui.Process.hide()
        self.ui.Utilities.hide()
        self.ui.System.hide()
        self.ui.SystemApp.hide()
        self.ui.File_analyze.hide()
        self.ui.WindowBlocking.show()

    def changeFile_analyze(self):
        self.ui.Process.hide()
        self.ui.Utilities.hide()
        self.ui.System.hide()
        self.ui.SystemApp.hide()
        self.ui.WindowBlocking.hide()
        self.ui.File_analyze.show()

    def window_blocking(self):
        config = configparser.RawConfigParser()
        config.optionxform = str
        config.read('stg.ini')
        try:
            if self.windowlistname == '':
                pass
            else:
                config.set('app', self.windowlistname, True)
                config.write(open('stg.ini', 'w'))
                self.windowlistname = ''
        except:
            self.windowinfo = self.ui.windowkillname.text()
            print(self.windowinfo)
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
        if not os.path.isfile(r'./stg.ini'):
            with open('stg.ini',mode='w',encoding='utf-8') as file:
                file.write('[app]')
                file.write('\n\n[Setting]\nMinimize = True\nMain_top = False')
        self.configlist=QStringListModel()
        config = configparser.RawConfigParser()
        config.optionxform = str
        try:
            config.read('stg.ini')
        except Exception as error:
            QMessageBox.critical(self,'error','發生錯誤!\n原因:' + str(error),QMessageBox.Ok)
        try:
            section = config.options('app')
        except:
            config.add_section('app')
            config.add_section('Setting')
            config.set('Setting', 'Minimize', True)
            config.set('Setting', 'Main_top', False)
            config.write(open('stg.ini', 'w'))
            section = config.options('app')
        self.configlist.setStringList(section)
        self.ui.windowkillview.setModel(self.configlist)

    def windownowupdate(self):
        self.windownowlistmodel=QStringListModel()
        self.windowlistview = []
        self.windowlisthwnd = []
        self.windowlistpid = []
        self.hwnd_title2 = dict() 
        win32gui.EnumWindows(self.windowrunning,0)
        for h,t in self.hwnd_title2.items():
            if t != '' and t != 'Defender' and t != 'Program Manager' and t != '設定' and t != '小算盤' and t != '電影與電視' and t != '電池計量表'  and t != 'Network Flyout':
                self.windowlistview.append(t)
                self.windowlisthwnd.append(h)
                th,hwndpid = win32process.GetWindowThreadProcessId(h)
                self.windowlistpid.append(hwndpid)
        self.windownowlistmodel.setStringList(self.windowlistview)
        self.ui.windowlistview.setModel(self.windownowlistmodel)

    def windowrunning(self,hwnd,mouse):
        if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindow(hwnd):
            self.hwnd_title2.update({hwnd:win32gui.GetWindowText(hwnd)})

    def windowview(self):
        self.windownowview = self.ui.windowlistview.selectedIndexes()
        for i in self.windownowview:
            item = i.row()
            self.windowlistitem = self.windowlistview[item]
            self.windowlistitemhwnd = self.windowlisthwnd[item]
            self.windowlistitempid = self.windowlistpid[item]
            for p in psutil.process_iter():
                if p.pid == self.windowlistitempid:
                    self.windowlistname = p.name()
                    print(self.windowlistname)
                    
    
    def killwindow(self):
        try:
            config = configparser.RawConfigParser()
            config.optionxform = str
            config.read('stg.ini')
            self.hwnd_title2 = dict() 
            win32gui.EnumWindows(self.windowrunning,0)
            for i in config.options('app'):
                for p in psutil.process_iter():
                    for h,t in self.hwnd_title2.items():
                        th,hwndpid = win32process.GetWindowThreadProcessId(h)
                        try:
                            if i == p.name():
                                if p.pid == hwndpid:
                                    self.user32dll.EndTask(h,False,True)
                                else:
                                    continue
                        except:
                            pass
                    if i == p.name():
                        try:
                            p.kill()
                        except:
                            pass
        except:
            pass

    def delexekill(self,pos):
        config = configparser.RawConfigParser()
        config.optionxform = str
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
            self.exekill.start(100)
        elif self.ui.stoping.isChecked():
            self.exekill.stop()

    def OpenProcess0(self,exe):
        win32process.CreateProcess(exe,"", None, None, 0,win32process.CREATE_NO_WINDOW, None, None,win32process.STARTUPINFO())

    def listprocess(self):
        try:
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
                    # try:
                    #     large, small = win32gui.ExtractIconEx(p.exe(),0)
                    #     win32gui.DestroyIcon(small[0])
                    #     hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0) )
                    #     hbmp = win32ui.CreateBitmap()
                    #     hbmp.CreateCompatibleBitmap( hdc, 32, 32 )
                    #     hdc = hdc.CreateCompatibleDC()
                    #     hdc.SelectObject( hbmp )
                    #     hdc.DrawIcon( (0,0), large[0] )
                    #     hbmp.SaveBitmapFile( hdc, "save.bmp" )
                    # except:
                    #     pass
                except:
                    self.qList.append(p.name() +"   "+ str(p.pid))
                    self.qList_pid.append(p.pid)
                    self.qList_exe.append('None')
                    self.qList_name.append(p.name())
                    self.qList_user.append(p.username())
            if len(self.qList_exe) != self.quantity:
                self.quantity = len(self.qList_exe)
                self.ui.Process_total_View.setText(str(self.quantity))
                self.slm.setStringList(self.qList)
                self.ui.Process_list.setModel(self.slm)
        except:
            pass

    def fixlimit(self):
        if self.language == 1:
            text = 'Are you sure you want to remove system restrictions?'
        if self.language == 2:
            text = '確定要解除系統限制嗎?'
        if self.language == 3:
            text = '确定要解除系统限制吗?'
        question = QMessageBox.warning(self,'FixLimit',text,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384:
            try:
                import win32api,win32con
                try:
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
                except:
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegCreateKey(key,'Explorer')
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
                try:
                    win32api.RegDeleteValue(key, 'NoControlPanel')
                except:
                    pass
                    
                try:
                    win32api.RegDeleteValue(key, 'NoDrives')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoControlPanel')
                except:
                    pass                
                try:
                    win32api.RegDeleteValue(key, 'NoFileMenu')
                except:
                    pass                
                try:
                    win32api.RegDeleteValue(key, 'NoFind')
                except:
                    pass                
                try:
                    win32api.RegDeleteValue(key, 'NoRealMode')
                except:
                    pass                
                try:
                    win32api.RegDeleteValue(key, 'NoRecentDocsMenu')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoSetFolders')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoSetFolderOptions')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoViewOnDrive')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoClose')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoRun')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoDesktop')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoLogOff')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoFolderOptions')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoViewContexMenu')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'HideClock')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoStartMenuMorePrograms')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoStartMenuMyGames')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoStartMenuMyMusic')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoStartMenuNetworkPlaces')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoStartMenuPinnedList')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoActiveDesktop')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoSetActiveDesktop')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoActiveDesktopChanges')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoChangeStartMenu')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'ClearRecentDocsOnExit')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoFavoritesMenu')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoRecentDocsHistory')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoSetTaskbar')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoSMHelp')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoTrayContextMenu')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoViewContextMenu')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoWindowsUpdate')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoWinKeys')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'StartMenuLogOff')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoSimpleNetlDList')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoLowDiskSpaceChecks')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'DisableLockWorkstation')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoManageMyComputerVerb')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'RestrictRun')
                except:
                    pass
                win32api.RegCloseKey(key)


                try:
                    key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
                except:
                    key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegCreateKey(key,'Explorer')
                    key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS)
                try:
                    win32api.RegDeleteValue(key, 'NoControlPanel')
                except:
                    pass
                    
                try:
                    win32api.RegDeleteValue(key, 'NoDrives')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoControlPanel')
                except:
                    pass                
                try:
                    win32api.RegDeleteValue(key, 'NoFileMenu')
                except:
                    pass                
                try:
                    win32api.RegDeleteValue(key, 'NoFind')
                except:
                    pass                
                try:
                    win32api.RegDeleteValue(key, 'NoRealMode')
                except:
                    pass                
                try:
                    win32api.RegDeleteValue(key, 'NoRecentDocsMenu')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoSetFolders')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoSetFolderOptions')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoViewOnDrive')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoClose')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoRun')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoDesktop')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoLogOff')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoFolderOptions')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoViewContexMenu')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'HideClock')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoStartMenuMorePrograms')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoStartMenuMyGames')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoStartMenuMyMusic')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoStartMenuNetworkPlaces')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoStartMenuPinnedList')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoActiveDesktop')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoSetActiveDesktop')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoActiveDesktopChanges')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoChangeStartMenu')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'ClearRecentDocsOnExit')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoFavoritesMenu')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoRecentDocsHistory')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoSetTaskbar')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoSMHelp')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoTrayContextMenu')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoViewContextMenu')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoWindowsUpdate')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoWinKeys')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'StartMenuLogOff')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoSimpleNetlDList')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoLowDiskSpaceChecks')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'DisableLockWorkstation')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'NoManageMyComputerVerb')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'RestrictRun')
                except:
                    pass
                win32api.RegCloseKey(key)


                try:
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',0,win32con.KEY_ALL_ACCESS)
                except:
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegCreateKey(key,'System')
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',0,win32con.KEY_ALL_ACCESS)
                try:
                    win32api.RegDeleteValue(key, 'DisableTaskMgr')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'DisableRegistryTools')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'DisableChangePassword')
                except:
                    pass
                try:
                    win32api.RegDeleteValue(key, 'Wallpaper')
                except:
                    pass
                win32api.RegCloseKey(key)


                try:
                    key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',0,win32con.KEY_ALL_ACCESS)
                except:
                    key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegCreateKey(key,'System')
                    key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System',0,win32con.KEY_ALL_ACCESS)
                try:
                    win32api.RegDeleteValue(key, 'DisableTaskMgr')
                except:
                    pass       
                try:
                    win32api.RegDeleteValue(key, 'DisableRegistryTools')
                except:
                    pass        
                try:
                    win32api.RegDeleteValue(key, 'DisableChangePassword')
                except:
                    pass           
                try:
                    win32api.RegDeleteValue(key, 'Wallpaper')
                except:
                    pass
                win32api.RegCloseKey(key)


                try:
                    key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop',0,win32con.KEY_ALL_ACCESS)
                except:
                    key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegCreateKey(key,'ActiveDesktop')
                    key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\ActiveDesktop',0,win32con.KEY_ALL_ACCESS)
                try:
                    win32api.RegDeleteValue(key, 'NoComponents')
                except:
                    pass          
                try:
                    win32api.RegDeleteValue(key, 'NoAddingComponents')
                except:
                    pass                  
                win32api.RegCloseKey(key)


                try:
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Policies\Microsoft\Windows\System',0,win32con.KEY_ALL_ACCESS)
                except:
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Policies\Microsoft\Windows',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegCreateKey(key,'System')
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Policies\Microsoft\Windows\System',0,win32con.KEY_ALL_ACCESS)
                try:
                    win32api.RegDeleteValue(key, 'DisableCMD')
                except:
                    pass                    
                win32api.RegCloseKey(key)
        

                try:
                    key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Policies\Microsoft\Windows\System',0,win32con.KEY_ALL_ACCESS)
                except:
                    key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Policies\Microsoft\Windows',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegCreateKey(key,'System')
                    key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Policies\Microsoft\Windows\System',0,win32con.KEY_ALL_ACCESS)
                try:
                    win32api.RegDeleteValue(key, 'DisableCMD')
                except:
                    pass    
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
                try:
                    win32api.RegDeleteValue(key, 'Restrict_Run')
                except:
                    pass
                win32api.RegCloseKey(key)

                if self.language == 1:
                    text = 'Fix system limitation successfully!'
                if self.language == 2:
                    text = '修復系統限制成功!'
                if self.language == 3:
                    text = '修复系统限制成功!'
                QMessageBox.information(self,'Done',text,QMessageBox.Ok,QMessageBox.Ok)
            except:
                if self.language == 1:
                    text = 'An error occurred'
                if self.language == 2:
                    text = '發生錯誤'
                if self.language == 3:
                    text = '发生错误'
                QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def recover_Wallpaper(self):
        if self.language == 1:
            text = 'Are you sure you want to restore the default wallpaper?'
        if self.language == 2:
            text = '確定要恢復默認桌布嗎?'
        if self.language == 3:
            text = '确定要恢复默认壁纸吗?'
        question = QMessageBox.warning(self,'wallpaper',text,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384:
            try:
                try:
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Wallpapers',0,win32con.KEY_ALL_ACCESS)
                except:
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegCreateKey(key,'Wallpapers')
                    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Wallpapers',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'BackgroundHistoryPath0', win32con.REG_SZ, r'c:\windows\web\wallpaper\windows\img0.jpg')
                self.user32dll.SystemParametersInfoW(20, 0, r'c:\windows\web\wallpaper\windows\img0.jpg', 0)
                if self.language == 1:
                    text = 'Fix Wallpapers successfully!'
                if self.language == 2:
                    text = '恢復桌布成功!'
                if self.language == 3:
                    text = '恢复壁纸成功!'
                QMessageBox.information(self,'Done',text,QMessageBox.Ok,QMessageBox.Ok)
            except:
                if self.language == 1:
                    text = 'An error occurred'
                if self.language == 2:
                    text = '發生錯誤'
                if self.language == 3:
                    text = '发生错误'
                QMessageBox.critical(self,'error',text,QMessageBox.Ok)

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
                win32api.RegSetValue(key, '.ini', win32con.REG_SZ, 'inifile')
                win32api.RegSetValue(key, 'inifile', win32con.REG_SZ, 'Configuration Settings')
                win32api.RegSetValue(key, '.msc', win32con.REG_SZ, 'MSCfile')
                win32api.RegSetValue(key, 'MSCfile', win32con.REG_SZ, 'Microsoft Common Console Document')
                keyopen = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\exefile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\comfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\scrfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" /S')
                keyopen = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\\batfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\cmdfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\inifile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, r'%SystemRoot%\system32\NOTEPAD.EXE %1')
                keyopen = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\VBSfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, r'"%SystemRoot%\System32\WScript.exe" "%1" %*')

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
                win32api.RegSetValue(key, '.ini', win32con.REG_SZ, 'inifile')
                win32api.RegSetValue(key, 'inifile', win32con.REG_SZ, 'Configuration Settings')
                win32api.RegSetValue(key, '.msc', win32con.REG_SZ, 'MSCfile')
                win32api.RegSetValue(key, 'MSCfile', win32con.REG_SZ, 'Microsoft Common Console Document')
                try:
                    keyopen = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Classes\exefile\shell\open',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                    keyopen = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Classes\comfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                    keyopen = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Classes\scrfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" /S')
                    keyopen = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Classes\batfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                    keyopen = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Classes\cmdfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                    keyopen = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Classes\inifile\shell\open',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, r'%SystemRoot%\System32\NOTEPAD.EXE %1')
                    keyopen = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,'SOFTWARE\Classes\VBSfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                    win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, r'"%SystemRoot%\System32\WScript.exe" "%1" %*')
                except:
                    pass

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
                win32api.RegSetValue(key, '.ini', win32con.REG_SZ, 'inifile')
                win32api.RegSetValue(key, 'inifile', win32con.REG_SZ, 'Configuration Settings')
                keyopen = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'exefile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'comfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'scrfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" /S')
                keyopen = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'batfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'cmdfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, '"%1" %*')
                keyopen = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'inifile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, r'%SystemRoot%\system32\NOTEPAD.EXE %1')
                keyopen = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'VBSfile\shell\open',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(keyopen, 'command', win32con.REG_SZ, r'"%SystemRoot%\System32\WScript.exe" "%1" %*')
                win32api.RegCloseKey(key)
                win32api.RegCloseKey(keyopen)
                if self.language == 1:
                    text = 'Repair file open method successfully!'
                if self.language == 2:
                    text = '修復文件打開方式成功!'
                if self.language == 3:
                    text = '修复文件打开方式成功!'
                QMessageBox.information(self,'Fixexeopen',text,QMessageBox.Ok,QMessageBox.Ok)
            except Exception as error:
                print(error)
                if self.language == 1:
                    text = 'An error occurred'
                if self.language == 2:
                    text = '發生錯誤'
                if self.language == 3:
                    text = '发生错误'
                QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def english(self):
        self.language = 1
        _translate = QtCore.QCoreApplication.translate
        self.ui.Process_name.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">name</span></ p></body></html>"))
        self.ui.Process_PID.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">PID</span></ p></body></html>"))
        self.ui.Process_path.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-size:12pt;\"> exe path</span></p></body></html>"))
        self.ui.Hwnd.setText(_translate("MainWindow", "<html><head/><body><p>handle:</p></body></html>"))
        self.ui.UserName.setText(_translate("MainWindow", "<html><head/><body><p>Username:</p></body></html>"))
        self.ui.Process_total.setText(_translate("MainWindow", "<html><head/><body><p>Total number of processes:</p></body></html>"))
        self.ui.Fix_limit_Button.setText(_translate("MainWindow", "Release system limit"))
        self.ui.Fix_file_icon_Button.setText(_translate("MainWindow", "Fixer Icon"))
        self.ui.Clear_user_password_Button.setText(_translate("MainWindow", "Clear user password"))
        self.ui.Reopen_explorer_Button.setText(_translate("MainWindow", "Restart Explorer"))
        self.ui.Fix_IEFO_Button.setText(_translate("MainWindow", "Fix Image Hijacking"))
        self.ui.Fix_file_open_way_Button.setText(_translate("MainWindow", "Fix open way"))
        self.ui.recover_Wallpaper_Button.setText(_translate("MainWindow", "Recover default wallpaper"))
        self.ui.Shutdownbut.setText(_translate("MainWindow", "Force Shutdown"))
        self.ui.resetbut.setText(_translate("MainWindow", "Force restart"))
        self.ui.setUAC.setText(_translate("MainWindow", "Set UAC"))
        self.ui.systeminfobut.setText(_translate("MainWindow", "System Info"))
        self.ui.LogOff_Buttun.setText(_translate("MainWindow", "Force logout"))
        self.ui.End_not_system_process_Buttun.setText(_translate("MainWindow", "End all non-system processes"))
        self.ui.CMD_box.setTitle(_translate("MainWindow", "CMD Command"))
        self.ui.Dostext.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Please enter CMD command</span ></p></body></html>"))
        self.ui.RunDos.setText(_translate("MainWindow", "Execute"))
        self.ui.Output_text.setText(_translate("MainWindow", "<html><head/><body><p>Output(beta):</p></body></html>"))
        self.ui.Disable_exe_box.setTitle(_translate("MainWindow", "Disable program to run"))
        self.ui.Disable_exe_run_text.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Please enter the process name to be disabled </span></p></body></html>"))
        self.ui.Disable_exe_run_text_Buttun.setText(_translate("MainWindow", "OK"))
        self.ui.Disable_exe_run_list_text.setText(_translate("MainWindow", "<html><head/><body><p>Disabled program run list:</p></body></html>"))
        self.ui.Explorer_setting_show_file_extension_check.setText(_translate("MainWindow", "Show file extension"))
        self.ui.Explorer_setting_show_hide_file_check.setText(_translate("MainWindow", "Show hidden files"))
        self.ui.Explorer_setting_show_hide_system_file_check.setText(_translate("MainWindow", "Show system protected files"))
        self.ui.Taskmgr_Button.setText(_translate("MainWindow", "Taskmgr"))
        self.ui.Powershell_Button.setText(_translate("MainWindow", "Powershell"))
        self.ui.Regedit_Button.setText(_translate("MainWindow", "Regedit"))
        self.ui.Cmd_Button.setText(_translate("MainWindow", "Cmd"))
        self.ui.Gpedit_Button.setText(_translate("MainWindow", "Gpedit"))
        self.ui.Control_Button.setText(_translate("MainWindow", "Control"))
        self.ui.MMC_Button.setText(_translate("MainWindow", "MMC"))
        self.ui.Calc_Button.setText(_translate("MainWindow", "Calc"))
        self.ui.Compmgmt_Button.setText(_translate("MainWindow", "Compmgmt"))
        self.ui.Devmgmt_Button.setText(_translate("MainWindow", "Devmgmt"))
        self.ui.Dxdiag_Button.setText(_translate("MainWindow", "Dxdiag"))
        self.ui.Lusrmgr_Button.setText(_translate("MainWindow", "Lusrmgr"))
        self.ui.Magnify_Button.setText(_translate("MainWindow", "Magnify"))
        self.ui.Msinfo32_Button.setText(_translate("MainWindow", "Msinfo32"))
        self.ui.Winver_Button.setText(_translate("MainWindow", "Winver"))
        self.ui.hint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Running status:</span> </p></body></html>"))
        self.ui.stoping.setText(_translate("MainWindow", "stop"))
        self.ui.Running.setText(_translate("MainWindow", "Running"))
        self.ui.windowhint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">Please enter the pop-up window to be blocked Process name</span></p></body></html>"))
        self.ui.windowhint_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">or directly select the running window </span></p></body></html>"))
        self.ui.windowkillbut.setText(_translate("MainWindow", "OK"))
        self.ui.windowkilllist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Pop-up blocker list</span ></p></body></html>"))
        self.ui.WinTWS.setText(_translate("MainWindow", "WinTWS"))
        self.ui.execheckabout.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">DLL called by the analyzed file and functions and descriptions</span></p></body></html>"))
        self.ui.execheckname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">Filename:</span> </p></body></html>"))
        self.ui.execheckpath.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">File path:</span> </p></body></html>"))
        self.ui.execheck.setText(_translate("MainWindow", "File Analysis"))
        self.ui.Danger_degree.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">hint:</span>< /p></body></html>"))
        self.ui.Danger_degreeview.setText(_translate("MainWindow", "0"))
        self.ui.Process_manage_Button.setText(_translate("MainWindow", "Process Management"))
        self.ui.Utilities_Button.setText(_translate("MainWindow", "Utilities"))
        self.ui.System_Button.setText(_translate("MainWindow", "System"))
        self.ui.File_analyze_Button.setText(_translate("MainWindow", "File Analysis"))
        self.ui.SystemApp_Button.setText(_translate("MainWindow", "System App"))
        self.ui.WindowBlocking_Button.setText(_translate("MainWindow", "Popup Blocking"))
        self.ui.about_us.setText(_translate("MainWindow", "about"))
        self.ui.action_t.setText(_translate("MainWindow", "t"))

    def chinese_t(self):
        self.language = 2
        _translate = QtCore.QCoreApplication.translate
        self.ui.Process_name.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">名稱</span></p></body></html>"))
        self.ui.Process_PID.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">PID</span></p></body></html>"))
        self.ui.Process_path.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-size:12pt;\">exe路徑</span></p></body></html>"))
        self.ui.Hwnd.setText(_translate("MainWindow", "<html><head/><body><p>句柄:</p></body></html>"))
        self.ui.UserName.setText(_translate("MainWindow", "<html><head/><body><p>使用者名稱:</p></body></html>"))
        self.ui.Process_total.setText(_translate("MainWindow", "<html><head/><body><p>進程總數:</p></body></html>"))
        self.ui.Fix_limit_Button.setText(_translate("MainWindow", "解除系統限制"))
        self.ui.Fix_file_icon_Button.setText(_translate("MainWindow", "修復程式圖標"))
        self.ui.Clear_user_password_Button.setText(_translate("MainWindow", "清除用戶密碼"))
        self.ui.Reopen_explorer_Button.setText(_translate("MainWindow", "重啟資源管理器"))
        self.ui.Fix_IEFO_Button.setText(_translate("MainWindow", "修復映像劫持"))
        self.ui.Fix_file_open_way_Button.setText(_translate("MainWindow", "修復打開方式"))
        self.ui.recover_Wallpaper_Button.setText(_translate("MainWindow", "恢復默認桌布"))
        self.ui.Shutdownbut.setText(_translate("MainWindow", "強制關機"))
        self.ui.resetbut.setText(_translate("MainWindow", "強制重啟"))
        self.ui.setUAC.setText(_translate("MainWindow", "設定UAC"))
        self.ui.systeminfobut.setText(_translate("MainWindow", "系統資訊"))
        self.ui.LogOff_Buttun.setText(_translate("MainWindow", "強制登出"))
        self.ui.End_not_system_process_Buttun.setText(_translate("MainWindow", "結束所有非系統進程"))
        self.ui.CMD_box.setTitle(_translate("MainWindow", "CMD命令"))
        self.ui.Dostext.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">請輸入CMD命令</span></p></body></html>"))
        self.ui.RunDos.setText(_translate("MainWindow", "執行"))
        self.ui.Output_text.setText(_translate("MainWindow", "<html><head/><body><p>輸出(beta):</p></body></html>"))
        self.ui.Disable_exe_box.setTitle(_translate("MainWindow", "禁止程式運行"))
        self.ui.Disable_exe_run_text.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">請輸入要禁止的進程名</span></p></body></html>"))
        self.ui.Disable_exe_run_text_Buttun.setText(_translate("MainWindow", "確定"))
        self.ui.Disable_exe_run_list_text.setText(_translate("MainWindow", "<html><head/><body><p>禁止程式運行的名單:</p></body></html>"))
        self.ui.Explorer_setting_show_file_extension_check.setText(_translate("MainWindow", "顯示文件副檔名"))
        self.ui.Explorer_setting_show_hide_file_check.setText(_translate("MainWindow", "顯示隱藏檔案"))
        self.ui.Explorer_setting_show_hide_system_file_check.setText(_translate("MainWindow", "顯示受系統保護的文件"))
        self.ui.Taskmgr_Button.setText(_translate("MainWindow", "Taskmgr"))
        self.ui.Powershell_Button.setText(_translate("MainWindow", "Powershell"))
        self.ui.Regedit_Button.setText(_translate("MainWindow", "Regedit"))
        self.ui.Cmd_Button.setText(_translate("MainWindow", "Cmd"))
        self.ui.Gpedit_Button.setText(_translate("MainWindow", "Gpedit"))
        self.ui.Control_Button.setText(_translate("MainWindow", "Control"))
        self.ui.MMC_Button.setText(_translate("MainWindow", "MMC"))
        self.ui.Calc_Button.setText(_translate("MainWindow", "Calc"))
        self.ui.Compmgmt_Button.setText(_translate("MainWindow", "Compmgmt"))
        self.ui.Devmgmt_Button.setText(_translate("MainWindow", "Devmgmt"))
        self.ui.Dxdiag_Button.setText(_translate("MainWindow", "Dxdiag"))
        self.ui.Lusrmgr_Button.setText(_translate("MainWindow", "Lusrmgr"))
        self.ui.Magnify_Button.setText(_translate("MainWindow", "Magnify"))
        self.ui.Msinfo32_Button.setText(_translate("MainWindow", "Msinfo32"))
        self.ui.Winver_Button.setText(_translate("MainWindow", "Winver"))
        self.ui.hint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">運行狀態:</span></p></body></html>"))
        self.ui.stoping.setText(_translate("MainWindow", "停止"))
        self.ui.Running.setText(_translate("MainWindow", "運行"))
        self.ui.windowhint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">請輸入要攔截的彈窗進程名</span></p></body></html>"))
        self.ui.windowhint_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">或直接選擇正在運行的窗口</span></p></body></html>"))
        self.ui.windowkillbut.setText(_translate("MainWindow", "確定"))
        self.ui.windowkilllist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">彈窗攔截名單</span></p></body></html>"))
        self.ui.WinTWS.setText(_translate("MainWindow", "WinTWS"))
        self.ui.execheckabout.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">受分析的文件調用的DLL及函數及說明</span></p></body></html>"))
        self.ui.execheckname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">文件名:</span></p></body></html>"))
        self.ui.execheckpath.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">文件路徑:</span></p></body></html>"))
        self.ui.execheck.setText(_translate("MainWindow", "文件分析"))
        self.ui.Danger_degree.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">提示:</span></p></body></html>"))
        self.ui.Danger_degreeview.setText(_translate("MainWindow", "0"))
        self.ui.Process_manage_Button.setText(_translate("MainWindow", "進程管理"))
        self.ui.Utilities_Button.setText(_translate("MainWindow", "實用工具"))
        self.ui.System_Button.setText(_translate("MainWindow", "系統"))
        self.ui.File_analyze_Button.setText(_translate("MainWindow", "文件分析"))
        self.ui.SystemApp_Button.setText(_translate("MainWindow", "系統程式"))
        self.ui.WindowBlocking_Button.setText(_translate("MainWindow", "彈窗攔截"))
        self.ui.about_us.setText(_translate("MainWindow", "about"))
        self.ui.action_t.setText(_translate("MainWindow", " t"))

    def chinese_s(self):
        self.language = 3
        _translate = QtCore.QCoreApplication.translate
        self.ui.Process_name.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">名称</span></p></body></html>"))
        self.ui.Process_PID.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">PID</span></p></body></html>"))
        self.ui.Process_path.setText(_translate("MainWindow", "<html><head/><body><p align=\"justify\"><span style=\" font-size:12pt;\">exe路径</span></p></body></html>"))
        self.ui.Hwnd.setText(_translate("MainWindow", "<html><head/><body><p>句柄:</p></body></html>"))
        self.ui.UserName.setText(_translate("MainWindow", "<html><head/><body><p>使用者名称:</p></body></html>"))
        self.ui.Process_total.setText(_translate("MainWindow", "<html><head/><body><p>进程总数:</p></body></html>"))
        self.ui.Fix_limit_Button.setText(_translate("MainWindow", "解除系统限制"))
        self.ui.Fix_file_icon_Button.setText(_translate("MainWindow", "修复程式图标"))
        self.ui.Clear_user_password_Button.setText(_translate("MainWindow", "清除用户密码"))
        self.ui.Reopen_explorer_Button.setText(_translate("MainWindow", "重启资源管理器"))
        self.ui.Fix_IEFO_Button.setText(_translate("MainWindow", "修复映像劫持"))
        self.ui.Fix_file_open_way_Button.setText(_translate("MainWindow", "修复打开方式"))
        self.ui.recover_Wallpaper_Button.setText(_translate("MainWindow", "恢复默认壁纸"))
        self.ui.Shutdownbut.setText(_translate("MainWindow", "强制关机"))
        self.ui.resetbut.setText(_translate("MainWindow", "强制重启"))
        self.ui.setUAC.setText(_translate("MainWindow", "设定UAC"))
        self.ui.systeminfobut.setText(_translate("MainWindow", "系统资讯"))
        self.ui.LogOff_Buttun.setText(_translate("MainWindow", "强制登出"))
        self.ui.End_not_system_process_Buttun.setText(_translate("MainWindow", "结束所有非系统进程"))
        self.ui.CMD_box.setTitle(_translate("MainWindow", "CMD命令"))
        self.ui.Dostext.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">请输入CMD命令</span></p></body></html>"))
        self.ui.RunDos.setText(_translate("MainWindow", "执行"))
        self.ui.Output_text.setText(_translate("MainWindow", "<html><head/><body><p>输出(beta):</p></body></html>"))
        self.ui.Disable_exe_box.setTitle(_translate("MainWindow", "禁止软件运行"))
        self.ui.Disable_exe_run_text.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">请输入要禁止的进程名</span></p></body></html>"))
        self.ui.Disable_exe_run_text_Buttun.setText(_translate("MainWindow", "确定"))
        self.ui.Disable_exe_run_list_text.setText(_translate("MainWindow", "<html><head/><body><p>禁止软件运行的名单:</p></body></html>"))
        self.ui.Explorer_setting_show_file_extension_check.setText(_translate("MainWindow", "显示文件后缀名"))
        self.ui.Explorer_setting_show_hide_file_check.setText(_translate("MainWindow", "显示隐藏档案"))
        self.ui.Explorer_setting_show_hide_system_file_check.setText(_translate("MainWindow", "显示受系统保护的文件"))
        self.ui.Taskmgr_Button.setText(_translate("MainWindow", "Taskmgr"))
        self.ui.Powershell_Button.setText(_translate("MainWindow", "Powershell"))
        self.ui.Regedit_Button.setText(_translate("MainWindow", "Regedit"))
        self.ui.Cmd_Button.setText(_translate("MainWindow", "Cmd"))
        self.ui.Gpedit_Button.setText(_translate("MainWindow", "Gpedit"))
        self.ui.Control_Button.setText(_translate("MainWindow", "Control"))
        self.ui.MMC_Button.setText(_translate("MainWindow", "MMC"))
        self.ui.Calc_Button.setText(_translate("MainWindow", "Calc"))
        self.ui.Compmgmt_Button.setText(_translate("MainWindow", "Compmgmt"))
        self.ui.Devmgmt_Button.setText(_translate("MainWindow", "Devmgmt"))
        self.ui.Dxdiag_Button.setText(_translate("MainWindow", "Dxdiag"))
        self.ui.Lusrmgr_Button.setText(_translate("MainWindow", "Lusrmgr"))
        self.ui.Magnify_Button.setText(_translate("MainWindow", "Magnify"))
        self.ui.Msinfo32_Button.setText(_translate("MainWindow", "Msinfo32"))
        self.ui.Winver_Button.setText(_translate("MainWindow", "Winver"))
        self.ui.hint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">运行状态:</span></p></body></html>"))
        self.ui.stoping.setText(_translate("MainWindow", "停止"))
        self.ui.Running.setText(_translate("MainWindow", "运行"))
        self.ui.windowhint.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">请输入要拦截的弹窗进程名</span></p></body></html>"))
        self.ui.windowhint_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">或直接选择正在运行的窗口</span></p></body></html>"))
        self.ui.windowkillbut.setText(_translate("MainWindow", "确定"))
        self.ui.windowkilllist.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">弹窗拦截名单</span></p></body></html>"))
        self.ui.WinTWS.setText(_translate("MainWindow", "WinTWS"))
        self.ui.execheckabout.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">受分析的文件调用的DLL及函数及说明</span></p></body></html>"))
        self.ui.execheckname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">文件名:</span></p></body></html>"))
        self.ui.execheckpath.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">文件路径:</span></p></body></html>"))
        self.ui.execheck.setText(_translate("MainWindow", "文件分析"))
        self.ui.Danger_degree.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt;\">提示:</span></p></body></html>"))
        self.ui.Danger_degreeview.setText(_translate("MainWindow", "0"))
        self.ui.Process_manage_Button.setText(_translate("MainWindow", "进程管理"))
        self.ui.Utilities_Button.setText(_translate("MainWindow", "实用工具"))
        self.ui.System_Button.setText(_translate("MainWindow", "系统"))
        self.ui.File_analyze_Button.setText(_translate("MainWindow", "文件分析"))
        self.ui.SystemApp_Button.setText(_translate("MainWindow", "系统程式"))
        self.ui.WindowBlocking_Button.setText(_translate("MainWindow", "弹窗拦截"))
        self.ui.about_us.setText(_translate("MainWindow", "about"))
        self.ui.action_t.setText(_translate("MainWindow", " t"))

    def killprocess(self,exe):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        result = subprocess.call('%s%s' % ("taskkill /F /IM ",exe),startupinfo=si)
        return result

    def Taskmgr(self):
        try:
            self.OpenProcess0(exe=r'C:/Windows/System32/taskmgr.exe')
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
            self.OpenProcess0(exe=r'C:/Windows/System32/control.exe')
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
            win32api.ShellExecute( 0, 'open' , 'gpedit.msc' , None ,None , 1 )
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def Calc(self):
        try:
            self.OpenProcess0(exe=r'C:/Windows/System32/calc.exe')
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def Compmgmt(self):
        try:
            win32api.ShellExecute( 0, 'open' , r'C:/Windows/System32/compmgmt.msc' , None ,None , 1 )
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def Devmgmt(self):
        try:
            win32api.ShellExecute( 0, 'open' , r'C:/Windows/System32/devmgmt.msc' , None ,None , 1 )
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)
    
    def Dxdiag(self):
        try:
            self.OpenProcess0(exe=r'C:/Windows/System32/dxdiag.exe')
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def Lusrmgr(self):
        try:
            win32api.ShellExecute( 0, 'open' , r'C:/Windows/System32/lusrmgr.msc' , None ,None , 1 )
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def Magnify(self):
        try:
            win32api.ShellExecute( 0, 'open' , r'C:/Windows/System32/Magnify.exe' , None ,None , 1 )
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)
    
    def Msinfo32(self):
        try:
            self.OpenProcess0(exe=r'C:/Windows/System32/msinfo32.exe')
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def Winver(self):
        try:
            self.OpenProcess0(exe=r'C:/Windows/System32/winver.exe')
        except:
            if self.language == 1:
                text = 'An error occurred!'
            if self.language == 2:
                text = '發生錯誤!'
            if self.language == 3:
                text = '发生错误!'
            QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def msconfig(self):
        try:
            self.OpenProcess0(exe=r'C:/Windows/System32/msconfig.exe')
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
            self.OpenProcess0(r'C:/Windows/explorer.exe')
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
        try:
            self.ui.Hwnd_View.setText('')
            self.item = self.ui.Process_list.selectedIndexes()
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
                    self.ui.Hwnd_View.setText(str(h))
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
                text = 'locate file'
            if self.language == 2:
                text = '定位文件'
            if self.language == 3:
                text = '定位文件'
            exefile = QAction(text,self)
            self.popMenu.addAction(self.killp)
            self.popMenu.addAction(exefile)
            self.exe = self.popMenu.exec_(self.ui.Process_list.mapToGlobal(pos))
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
                    if self.exefile == 'None':
                        if self.language == 1:
                            text = 'Unable to open the specified path!'
                        if self.language == 2:
                            text = '無法打開指定路徑!'
                        if self.language == 3:
                            text = '无法打开指定路径!'
                        QMessageBox.critical(self,'error',text,QMessageBox.Ok)
                    else:
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
        except:
            pass

    def processhwnd(self):
        try:
            self.ui.Hwnd_View.setText('')
            self.item = self.ui.Process_list.selectedIndexes()
            for i in self.item:
                item = i.row()
                pid = self.qList_pid[item]
            self.hwnd_title = dict() 
            win32gui.EnumWindows(self.get_all_hwnd,0)
            for hwnd,title in self.hwnd_title.items():
                th,hwndpid = win32process.GetWindowThreadProcessId(hwnd)
                if hwndpid == pid:        
                    self.ui.Hwnd_View.setText(str(hwnd))
        except:
            pass

    def processuser(self):
        try:
            self.ui.UserName_View.setText('')
            item = self.ui.Process_list.selectedIndexes()
            for i in item:
                item = i.row()
                username = self.qList_user[item]
            self.ui.UserName_View.setText(username)
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
                key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'inifile',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, '%SystemRoot%\system32\imageres.dll,-69')
            except:
                pass
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CLASSES_ROOT,'VBSfile',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, '%SystemRoot%\System32\WScript.exe,2')
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
            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\inifile',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, '%SystemRoot%\system32\imageres.dll,-69')
            except:
                pass
            try:
                key = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,'SOFTWARE\Classes\VBSfile',0,win32con.KEY_ALL_ACCESS)
                win32api.RegSetValue(key, 'DefaultIcon', win32con.REG_SZ, '%SystemRoot%\System32\WScript.exe,2')
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
    
    def logoff(self):
        if self.language == 1:
            text = 'Are you sure you want to force restart?'
        if self.language == 2:
            text = '確定要強制登出嗎?'
        if self.language == 3:
            text = '确定要强制注销吗?'
        question = QMessageBox.warning(self,'LogonOff',text,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384:
            try:
                si = subprocess.STARTUPINFO()
                si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                subprocess.call('Shutdown -l -f',startupinfo=si)
            except:
                if self.language == 1:
                    text = 'An error occurred!'
                if self.language == 2:
                    text = '發生錯誤!'
                if self.language == 3:
                    text = '发生错误!'
                QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def end_not_system_process(self):
        if self.language == 1:
            text = 'Ending all non-system processes may have unintended consequences, continue?'
        if self.language == 2:
            text = '結束所有非系統進程可能會帶來意料之外的後果，是否繼續?'
        if self.language == 3:
            text = '结束所有非系统进程可能会带来意料之外的后果，是否继续?'
        question = QMessageBox.warning(self,'End_process',text,QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
        if question == 16384:
            try:    
                WinTWS_pid = os.getpid()
                for p in psutil.process_iter():
                    try:
                        if self.check_system_process(p,WinTWS_pid):
                            # print(p.exe())
                            p.kill()
                    except Exception as error:
                        print(error)
                        if self.language == 1:
                            text = 'An error occurred!\nreason:{}'.format(str(error))
                        if self.language == 2:
                            text = '發生錯誤!\n原因:{}'.format(str(error))
                        if self.language == 3:
                            text = '发生错误!\n原因:{}'.format(str(error))
                        QMessageBox.critical(self,'error',text,QMessageBox.Ok)
            except:
                if self.language == 1:
                    text = 'An error occurred!'
                if self.language == 2:
                    text = '發生錯誤!'
                if self.language == 3:
                    text = '发生错误!'
                QMessageBox.critical(self,'error',text,QMessageBox.Ok)

    def check_system_process(self,process,pid):
        if process.name() == 'System':
            return False
        if process.name() == 'System Idle Process':
            return False
        if process.name() == 'Registry':
            return False
        if process.name() == 'MsMpEng.exe':
            return False
        if process.name() == 'NisSrv.exe':
            return False
        if process.pid == pid:
            return False
        if process.exe() == r'C:\Windows\System32\svchost.exe':
            return False
        if process.exe() == r'C:\Windows\System32\smss.exe':
            return False
        if process.exe() == r'C:\Windows\System32\RuntimeBroker.exe':
            return False
        if process.exe() == r'C:\Windows\System32\csrss.exe':
            return False
        if process.exe() == r'C:\Windows\System32\wininit.exe':
            return False
        if process.exe() == r'C:\Windows\System32\conhost.exe':
            return False
        if process.exe() == r'C:\Windows\explorer.exe':
            return False
        if process.exe() == r'C:\Windows\System32\ctfmon.exe':
            return False
        if process.exe() == r'C:\Windows\System32\winlogon.exe':
            return False
        if process.exe() == r'C:\Windows\System32\audiodg.exe':
            return False
        if process.exe() == r'C:\Windows\System32\services.exe':
            return False
        if process.exe() == r'C:\Windows\ImmersiveControlPanel\SystemSettings.exe':
            return False
        if process.exe() == r'C:\Windows\System32\ntoskrnl.exe':
            return False
        if process.exe() == r'C:\Windows\SystemApps\ShellExperienceHost_cw5n1h2txyewy\ShellExperienceHost.exe':
            return False
        if process.exe() == r'C:\Windows\System32\fontdrvhost.exe':
            return False
        if process.exe() == r'C:\Windows\RtkBtManServ.exe':
            return False
        if process.exe() == r'C:\Windows\System32\DriverStore\FileRepository\dal.inf_amd64_b5484efd38adbe8d\jhi_service.exe':
            return False
        if process.exe() == r'C:\Program Files\Microsoft SQL Server\90\Shared\sqlwriter.exe':
            return False
        if process.exe() == r'C:\Windows\System32\DriverStore\FileRepository\lms.inf_amd64_fddb643595e0b8d0\LMS.exe':
            return False
        if process.exe() == r'C:\Windows\System32\DriverStore\FileRepository\mewmiprov.inf_amd64_f866bf1588e6868a\WMIRegistrationService.exe':
            return False
        if process.exe() == r'C:\Windows\System32\WUDFHost.exe':
            return False
        if process.exe() == r'C:\Windows\System32\oobe\UserOOBEBroker.exe':
            return False
        if process.exe() == r'C:\Windows\System32\lsass.exe':
            return False
        if process.exe() == r'C:\Windows\System32\wbem\WmiPrvSE.exe':
            return False
        if process.exe() == r'C:\Windows\System32\wbem\unsecapp.exe':
            return False
        if process.exe() == r'C:\Windows\System32\SettingSyncHost.exe':
            return False
        if process.exe() == r'C:\Windows\System32\SgrmBroker.exe':
            return False
        if process.exe() == r'C:\Windows\System32\SearchProtocolHost.exe':
            return False
        if process.exe() == r'C:\Windows\System32\SearchIndexer.exe':
            return False
        if process.exe() == r'C:\Windows\System32\SystemSettingsBroker.exe':
            return False
        if process.exe() == r'C:\Windows\System32\SearchFilterHost.exe':
            return False
        if process.exe() == r'C:\Windows\SysWOW64\wbem\WmiPrvSE.exe':
            return False
        if process.exe() == r'C:\Windows\System32\ApplicationFrameHost.exe':
            return False
        if process.exe() == r'C:\Windows\System32\dasHost.exe':
            return False
        if process.exe() == r'MemCompression':
            return False
        if process.exe() == r'C:\Windows\System32\dwm.exe':
            return False
        if process.exe() == r'C:\Windows\System32\sihost.exe':
            return False
        if process.exe() == r'C:\Windows\System32\taskhostw.exe':
            return False
        if process.exe() == r'C:\Windows\System32\smartscreen.exe':
            return False
        return True
        
    def Disable_exe_run(self):
        exe_name = self.ui.Disable_exe_run_text_input.text()
        if not exe_name == '':
            key = win32api.RegOpenKey(win32con.HKEY_USERS,None,0,win32con.KEY_ALL_ACCESS | win32con.WRITE_OWNER)
            for item in win32api.RegEnumKeyEx(key):
                item2 = item[0]
                if item2[-4:] == '1001':
                    try:
                        key = win32api.RegOpenKey(win32con.HKEY_USERS,item2 + r'\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS | win32con.WRITE_OWNER)
                    except:
                        key = win32api.RegOpenKey(win32con.HKEY_USERS,item2 + r'\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies',0,win32con.KEY_ALL_ACCESS | win32con.WRITE_OWNER)
                        win32api.RegCreateKey(key,'Explorer')
                        key = win32api.RegOpenKey(win32con.HKEY_USERS,item2 + r'\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS | win32con.WRITE_OWNER)
                    win32api.RegSetValueEx(key, 'DisallowRun', 0, win32con.REG_DWORD, 1)
                    try:
                        key = win32api.RegOpenKey(win32con.HKEY_USERS,item2 + r'\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun',0,win32con.KEY_ALL_ACCESS | win32con.WRITE_OWNER)
                    except:
                        key = win32api.RegOpenKey(win32con.HKEY_USERS,item2 + r'\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer',0,win32con.KEY_ALL_ACCESS | win32con.WRITE_OWNER)
                        win32api.RegCreateKey(key,'DisallowRun')
                        key = win32api.RegOpenKey(win32con.HKEY_USERS,item2 + r'\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun',0,win32con.KEY_ALL_ACCESS | win32con.WRITE_OWNER)
                    try:
                        win32api.RegSetValueEx(key, exe_name, 0, win32con.REG_SZ, exe_name)
                    except:
                        if self.language == 1:
                            text = 'access denied'
                        if self.language == 2:
                            text = '存取被拒'
                        if self.language == 3:
                            text = '存取被拒'   
                        QMessageBox.critical(self,'error',text,QMessageBox.Ok)
                    self.update_Disable_exe_list()
            win32api.RegCloseKey(key)

    def update_Disable_exe_list(self):
        self.Disables = [] 
        try:
            key = win32api.RegOpenKey(win32con.HKEY_USERS,None,0,win32con.KEY_ALL_ACCESS | win32con.WRITE_OWNER)
            for item in win32api.RegEnumKeyEx(key):
                item2 = item[0]
                if item2[-4:] == '1001':
                    key = win32api.RegOpenKey(win32con.HKEY_USERS,item2 + r'\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun',0,win32con.KEY_ALL_ACCESS | win32con.WRITE_OWNER)
                    if win32api.RegQueryInfoKey(key)[1] == 0:
                        self.Disable_list=QStringListModel()
                        self.Disable_list.setStringList(self.Disables)
                        self.ui.Disable_exe_run_list.setModel(self.Disable_list)
                    for i in range(0,win32api.RegQueryInfoKey(key)[1]):
                        self.Disables.append(win32api.RegEnumValue(key,i)[0])
                        self.Disable_list=QStringListModel()
                        self.Disable_list.setStringList(self.Disables)
                        self.ui.Disable_exe_run_list.setModel(self.Disable_list)
        except:
            pass

    def Disable_exe_run_del(self,pos):
        try:
            self.Disable_item = self.ui.Disable_exe_run_list.selectedIndexes()
            for i in self.Disable_item:
                item = i.row()
                self.Disable_row = self.Disables[item]
            key = win32api.RegOpenKey(win32con.HKEY_USERS,None,0,win32con.KEY_ALL_ACCESS | win32con.WRITE_OWNER)
            for item in win32api.RegEnumKeyEx(key):
                item2 = item[0]
                if item2[-4:] == '1001':
                    key = win32api.RegOpenKey(win32con.HKEY_USERS,item2 + r'\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun',0,win32con.KEY_ALL_ACCESS | win32con.WRITE_OWNER)
            self.Disable_Menu = QMenu()
            if self.language == 1:
                text = 'delete'
            if self.language == 2:
                text = '刪除'
            if self.language == 3:
                text = '删除'
            self.Delete_Disable = QAction(text,self)
            self.Disable_Menu.addAction(self.Delete_Disable)
            self.exe = self.Disable_Menu.exec_(self.ui.Disable_exe_run_list.mapToGlobal(pos))
            if self.exe == self.Delete_Disable:
                win32api.RegDeleteValue(key,self.Disable_row)
                win32api.RegCloseKey(key)
        except:
            pass
        

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

    def uac(self):
        self.widget = QtWidgets.QDialog()
        self.UAC = UAC_UI.Ui_Dialog()
        self.UAC.setupUi(self.widget)
        self.widget.show()

    def about(self):
        self.about_q = QtWidgets.QMainWindow()
        self.about_GUI = about.Ui_About()
        self.about_GUI.setupUi(self.about_q)
        self.about_q.show()

    # def Rundos_th(self):
    #     import threading
    #     Aasd = threading.Thread(target=self.Rundos)
    #     Aasd.start()
    #     return

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
                p = subprocess.Popen(dos,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        )
                out = p.stdout.read()
                self.ui.Output.setText(str(out))
                # subprocess.call(dos,startupinfo=si)
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
                if self.language == 1:
                    text = 'An error occurred!'
                if self.language == 2:
                    text = '發生錯誤!'
                if self.language == 3:
                    text = '发生错误!'
                QMessageBox.critical(self,'error',text,QMessageBox.Ok)
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

    def egg_1(self):
        import webbrowser,random
        for i in range(50):
            q = QMessageBox.critical(self,'explorer.exe','"0x00{}" 指令所引用的 "0x00{}" 記憶體。該記憶體不能為 "written"。\n'.format(random.randint(100000,999999),random.randint(100000,999999)),QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
            if not q == 16384:
                break
        if q == 16384:
            QMessageBox.information(self,'explorer.exe','Windows 已成功修復該記憶體位置。',QMessageBox.Ok)
            a = random.randint(1,100)
            if a != 2:
                webbrowser.open("http://btly.xyz/r/Krgy1du")
            else:
                webbrowser.open("https://www.youtube.com/watch?v=xWTiOqJqkk0")
            
    def showMenu(self):
        self.StMenu = QMenu()

        if self.The_Another_check == 9:
            text = "explorer.exe"
            different = QAction(text,self)
            self.StMenu.addAction(different)

        if self.language == 1:
            text = 'Settings'
        if self.language == 2:
            text = '設定'
        if self.language == 3:
            text = '设置'
        Main_settings = QAction(text,self)
        if self.language == 1:
            text = 'About'
        if self.language == 2:
            text = '關於'
        if self.language == 3:
            text = '关于'
        Main_about = QAction(text,self)
        self.StMenu.addAction(Main_settings)
        self.StMenu.addAction(Main_about)
        pos = QtCore.QPoint(0, 30)
        self.The_Another_check = self.The_Another_check + 1
        Qusetion = self.StMenu.exec_(self.ui.Menu_Button.mapToGlobal(pos))
        if Qusetion == Main_about:
            self.about()
        if Qusetion == Main_settings:
            self.Setting_window = Setting_Console.setting_controller()
            self.Setting_window.show()
        try:
            if Qusetion == different:
                self.egg_1()
        except:
            pass


    def createTrayIcon(self):
        if self.language == 1:
            text = 'Open the main screen(&R)'
        if self.language == 2:
            text = '打開主畫面(&R)'
        if self.language == 3:
            text = '打开主画面(&R)'
        aRestore = QAction(text, self, triggered = self.showNormal)
        if self.language == 1:
            text = 'exit(&Q)'
        if self.language == 2:
            text = '退出(&Q)'
        if self.language == 3:
            text = '退出(&Q)'
        aQuit = QAction(text, self, triggered = QApplication.instance().quit)
        
        menu = QMenu(self)
        menu.addAction(aRestore)
        menu.addAction(aQuit)
        
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.sysIcon)
        self.trayIcon.setContextMenu(menu)
        self.trayIcon.activated.connect(self.showUI)
    
    def closeEvent(self, event):
        if self.trayIcon.isVisible():
            self.hide()
            event.ignore()

    def showUI(self,reason):
        if reason == 3:
            self.showNormal()

    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #獲取鼠標相對窗口的位置
            event.accept()
        
    def mouseMoveEvent(self, QMouseEvent):
        try:
            if Qt.LeftButton and self.m_flag: 
                self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
                QMouseEvent.accept()
        except:
            pass
        
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor))


    def beautification(self):
        self.ui.Process_list.setStyleSheet('''
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

        self.get_pic(explode, r'C:\Windows\Temp\exe.png')
        self.sysIcon = QIcon(r'C:\Windows\Temp\exe.png')
        self.createTrayIcon()
        self.setWindowIcon(self.sysIcon)

    def paintEvent(self, event):
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        pat = QPainter(self)
        pat.setRenderHint(pat.Antialiasing)
        pat.fillPath(path, QBrush(Qt.white))
        color = QColor(0, 0, 0, 20)

        i_path = QPainterPath()
        i_path.setFillRule(Qt.WindingFill)
        ref = QRectF(10-1, 10-1, self.width()-(10-1)*2, self.height()-(10-1)*2)
        i_path.addRect(ref)
        # i_path.addRoundedRect(ref, event.size().width(), event.size().height())
        color.setAlpha(150 - 1**0.5*50)
        pat.setPen(color)
        pat.drawPath(i_path)

        # 圓角
        pat2 = QPainter(self)
        pat2.setRenderHint(pat2.Antialiasing) # 抗鋸齒
        pat2.setBrush(Qt.white)
        pat2.setPen(Qt.transparent)
        rect = self.rect()
        rect.setLeft(10)
        rect.setTop(10)
        rect.setWidth(rect.width()-10)
        rect.setHeight(rect.height()-10)
        pat2.drawRoundedRect(rect, 4, 4)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())