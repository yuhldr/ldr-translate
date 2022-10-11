import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QSystemTrayIcon, QApplication, QMessageBox

from utils import config

import ui_translate
from api import translate
import ui_preferences


class SystemTray(object):
    # 程序托盘类
    def __init__(self, app, w):
        self.app = app
        self.w = w
        # 禁止默认的closed方法，只能使用qapp.quit()的方法退出程序
        QApplication.setQuitOnLastWindowClosed(False)
        self.w.show()  # 不设置显示则为启动最小化到托盘
        self.tp = QSystemTrayIcon(self.w)
        self.initUI()
        self.run()

    def initUI(self):
        # 设置托盘图标
        self.tp.setIcon(QIcon('./icon/tray.png'))

    def quitApp(self):
        # 退出程序
        self.w.show()  # w.hide() #设置退出时是否显示主窗口
        re = QMessageBox.warning(self.w, "提示", "退出兰译",
                                 QMessageBox.Yes | QMessageBox.No,
                                 QMessageBox.No)
        if re == QMessageBox.Yes:
            self.tp.setVisible(False)  # 隐藏托盘控件，托盘图标刷新不及时，提前隐藏
            self.app.quit()  # 退出程序

    def message(self):
        # 提示信息被点击方法
        print("弹出的信息被点击了")

    def act(self, reason):
        # 主界面显示方法
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            self.w.show()

    def setAuto(self):
        global isAuto
        isAuto = self.auto.isChecked()

    def _on_prefrrence(self):
        self.preferences = ui_preferences.Ui_MainWindow()

        self.preferences.setupUi(self.preferences)

        self.preferences.show()

    def run(self):
        self.auto = QAction('复制即翻译', triggered=self.setAuto)
        self.auto.setEnabled(True)
        self.auto.setCheckable(True)
        self.auto.setChecked(True)

        a0 = QAction('翻译设置', triggered=self._on_prefrrence)

        a1 = QAction('显示兰译', triggered=self.w.show)
        a2 = QAction('退出兰译', triggered=self.quitApp)

        tpMenu = QMenu()
        tpMenu.addAction(self.auto)
        tpMenu.addAction(a0)
        tpMenu.addAction(a1)
        tpMenu.addAction(a2)
        self.tp.setContextMenu(tpMenu)
        self.tp.show()  # 不调用show不会显示系统托盘消息，图标隐藏无法调用

        # 信息提示
        # 参数1：标题
        # 参数2：内容
        # 参数3：图标（0没有图标 1信息图标 2警告图标 3错误图标），0还是有一个小图标
        self.tp.showMessage('兰译', '复制自动翻译', icon=0)
        # 绑定提醒信息点击事件
        self.tp.messageClicked.connect(self.message)
        # 绑定托盘菜单点击事件
        self.tp.activated.connect(self.act)
        sys.exit(self.app.exec_())  # 持续对app的连接


isAuto = True


# 当剪切板变动会执行该方法
def change_deal():
    if (isAuto):
        data = clipboard.mimeData()

        formats = data.formats()

        # 如果是文本格式，把内容打印出来
        if ('text/uri-list' not in formats):
            if (MainWindow.isHidden()):
                MainWindow.show()

        if ('application/x-qt-image' in formats):
            # 必须有.png
            img_path = config.app_home_dir + "/copy_img.png"
            clipboard.image().save(img_path)
            ui.ocr_image(img_path)
        else:
            text_from = data.text()
            ui.translate_text(text_from)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    MainWindow = QMainWindow()
    ui = ui_translate.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    clipboard = app.clipboard()
    clipboard.dataChanged.connect(change_deal)

    ti = SystemTray(app, MainWindow)
