# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/yuh/code/test/pyqt/translate.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets

from api import translate
from qt_utils import MyThread
from utils import tools, config
from utils.locales import t_ui


def to_copy(is_selected):
    translate.set_no_translate_this(is_selected)


def from_copy(is_selected):
    translate.set_no_translate_this(is_selected)


class UiMainWindow(object):

    def setup_ui(self, mainWindow):
        mainWindow.setObjectName("MainWindow")
        mainWindow.resize(400, 360)
        mainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/icon.svg"))
        mainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.te_from = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.te_from.setObjectName("te_from")
        self.verticalLayout.addWidget(self.te_from)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cbb_translate_server = QtWidgets.QComboBox(self.centralwidget)
        self.cbb_translate_server.setObjectName("cbb_translate")
        self.horizontalLayout.addWidget(self.cbb_translate_server)

        self.cbb_translate_to_lang = QtWidgets.QComboBox(self.centralwidget)
        self.cbb_translate_to_lang.setObjectName("cbb_translate_to_lang")
        self.horizontalLayout.addWidget(self.cbb_translate_to_lang)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20,
                                           QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cb_add = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_add.setObjectName("cb_add")
        self.horizontalLayout.addWidget(self.cb_add)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.te_to = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.te_to.setObjectName("te_to")
        self.verticalLayout.addWidget(self.te_to)
        mainWindow.setCentralWidget(self.centralwidget)

        self.te_from.copyAvailable.connect(from_copy)
        self.te_to.copyAvailable.connect(to_copy)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "兰译"))

        self.pushButton.setText(
            _translate("MainWindow", t_ui("btn_translate_label")))
        self.cb_add.setText(_translate("MainWindow", t_ui("cb_add_label")))

        self.cbb_translate_to_lang.currentIndexChanged.connect(
            self.on_cbb_translate_lang_changed)

        self.cbb_translate_server.addItems(
            tools.get_translate_server_dict_by_locale().keys())
        s = tools.get_current_translate_server_locale()
        self.cbb_translate_server.setCurrentText(s)
        self.cbb_translate_server.currentIndexChanged.connect(
            self.on_cbb_translate_server_changed)
        self.set_cbb_translate_to_lang_data()

        self.te_to.setPlainText(_translate("MainWindow", t_ui("notice_to")))
        self.te_from.setPlainText(_translate("MainWindow",
                                             t_ui("notice_from")))
        self.pushButton.clicked.connect(self.btn_translate)

    def on_cbb_translate_lang_changed(self):
        tools.set_to_lang(self.cbb_translate_to_lang.currentText())

        # self.btnTranslate()

    def set_cbb_translate_to_lang_data(self, i=-1):
        self.cbb_translate_to_lang.clear()

        self.cbb_translate_to_lang.addItems(
            tools.get_to_lang_dict_by_locale().keys())

        if i < 0:
            i = tools.get_current_to_lang_index()
        self.cbb_translate_to_lang.setCurrentIndex(i)

    def on_cbb_translate_server_changed(self):
        tools.set_translate_server(self.cbb_translate_server.currentText())
        i = tools.get_current_to_lang_index(tools.translate_to_lang_cache)

        self.set_cbb_translate_to_lang_data(i)

    def is_add(self):
        return self.cb_add.isChecked()

    def ocr_image(self, img_path):
        def next_(param):
            ok, s = param
            self.set_ui((s, "文本识别成功！"))
            self.translate_text(s)

        s = config.get_ocr_notice()
        self.set_ui((s, s))
        self.thread = MyThread(translate.ocr2, img_path)
        self.thread.signal.connect(next_)
        self.thread.start()

    def set_ui(self, param):
        text_from, text_to = param

        if text_from is not None and len(text_from) > 0:
            self.te_from.setPlainText(text_from)
            if text_to is not None and len(text_to) > 0:
                self.te_to.setPlainText(text_to)

    def translate_text(self, text_from=None):
        if translate.no_translate_this:
            translate.set_no_translate_this(False)
            return

        self.set_ui((text_from, "翻译中..."))
        print("翻译中...", text_from)
        self.thread = MyThread(translate.text2, (text_from, self.is_add()))
        self.thread.signal.connect(self.set_ui)
        self.thread.start()

    def btn_translate(self):
        text_from = self.te_from.toPlainText()
        self.translate_text(text_from)
