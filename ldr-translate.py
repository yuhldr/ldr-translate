#!/usr/bin/python3
# coding: utf-8
#
# A simple indicator applet displaying cpu and memory information
#
# Author: Alex Eftimie <alex@eftimie.ro>
# Fork Author: fossfreedom <foss.freedom@gmail.com>
# Original Homepage: http://launchpad.net/indicator-sysmonitor
# Fork Homepage: https://github.com/fossfreedom/indicator-sysmonitor
# License: GPL v3
#
import gi
import os
import config

gi.require_versions({"Gtk": "3.0", "AppIndicator3": "0.1"})
from ui_translate import Translate, VERSION
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk, Gdk


class LdrTranlate(object):
    is_auto_translate = False

    def _create_menu(self):
        menu = Gtk.Menu()

        pref_menu = Gtk.MenuItem(label='翻译窗口：显示/关闭')
        pref_menu.connect('activate', self.on_translate_activated)
        menu.add(pref_menu)

        self.menu_auto_translate = Gtk.MenuItem()
        self.menu_auto_translate.connect('activate', self.set_auto_translate)
        self.set_auto_translate()
        menu.add(self.menu_auto_translate)

        help_menu = Gtk.MenuItem(label='帮助文档：V' + VERSION)
        help_menu.connect('activate', self._on_help)
        menu.add(help_menu)

        exit_menu = Gtk.MenuItem(label='退出')
        exit_menu.connect('activate', self.on_exit)
        menu.add(exit_menu)

        menu.show_all()
        self.ind.set_menu(menu)

    def __init__(self):
        self.translate_win = None
        self._help_dialog = None

        self.ind = appindicator.Indicator.new(
            "ldr-tranlate", os.path.abspath('ui/icon.svg'),
            appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.ind.set_ordering_index(1)

        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

        self._create_menu()

        self.on_translate_activated()

        # 注意不要把剪贴板监听放在翻译窗口，因为它关闭还是能接收信号，或许是销毁的有问题，但是放在这里真的很好！还能自动弹出
        self.getClipboard().connect("owner-change",
                                    self.on_translate_activated)

    def on_exit(self, event=None, data=None):
        try:
            Gtk.main_quit()
        except RuntimeError:
            pass

    def _on_help(self, event=None, data=None):
        if self._help_dialog is not None:
            self._help_dialog.present()
            return

        s = "1. 软件安装位置：~/.local/share/ldr-translate\n2. 终端输入 ldr-translate 即可运行\n3. 注销并重新登录以后，应用程序中应包含‘兰译’\n4. 复制即可自动翻译、Alt Q快捷键自动隐藏/显示主窗口\n5. 系统截图并复制到剪贴板，自动OCR识别并翻译\n6. 更多教程见：https://github.com/yuhlzu/ldr-translate"

        self._help_dialog = Gtk.MessageDialog(None, Gtk.DialogFlags.MODAL,
                                              Gtk.MessageType.INFO,
                                              Gtk.ButtonsType.OK, s)

        self._help_dialog.set_title("帮助")
        self._help_dialog.run()
        self._help_dialog.destroy()
        self._help_dialog = None

    def on_translate_activated(self, cb=None, event=None):
        if (self.is_auto_translate):
            if (self.translate_win is None or self.translate_win.is_hide):
                self.translate_win = Translate()
                self.translate_win.open()
            elif (event is None):
                self.translate_win.close()
            else:
                self.translate_win.copy_auto_translate(cb, event)
        else:
            print("暂停翻译")

    def set_auto_translate(self, event=None, view=None):
        print(view)
        print(event)
        self.is_auto_translate = not self.is_auto_translate
        s = "自动翻译：开启"
        if(not self.is_auto_translate):
            s = "自动翻译：关闭"
            self.ind.set_label("暂停翻译", "")
        else:
            self.ind.set_label("翻译中", "")

        self.menu_auto_translate.set_label(s)
        if (self.translate_win is not None):
            self.translate_win.translate_by_s(s)

    def getClipboard(self):
        if (config.translate_select):
            return Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        else:
            return Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)


if __name__ == "__main__":
    app = LdrTranlate()
    try:
        Gtk.main()
    except KeyboardInterrupt:
        app.on_exit()
