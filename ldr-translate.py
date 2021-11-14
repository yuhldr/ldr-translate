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
from api import config
from pathlib import Path
from api.server.baidu import translate
# import faulthandler
# # 在import之后直接添加以下启用代码即可 python3 -X faulthandler ldr-translate.py
# faulthandler.enable()

gi.require_versions({"Gtk": "3.0", "AppIndicator3": "0.1"})
from ui_translate import Translate

from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk, Gdk, GdkPixbuf


class LdrTranlate(Gtk.Application):
    is_auto_translate = False
    update = False

    def __init__(self):
        self.translate_win = None
        self._help_dialog = None

        self.indicator = appindicator.Indicator.new(
            "ldr-tranlate", os.path.abspath('ui/icon.svg'),
            appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_label("翻译中", "")
        self.indicator.set_ordering_index(1)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        self._create_menu()

        self.getClipboard().connect("owner-change",
                                    self._active_translate_windows)
        self._active_auto_translate()

    def get_version_data(self):
        # 这个会卡，外网
        s, self.update = config.get_update_version()
        self.help_menu.set_label(s)
        if (self.update):
            self.indicator.set_label("有更新", "")

    def _create_menu(self):
        menu = Gtk.Menu()

        pref_menu = Gtk.MenuItem(label='翻译窗口：显示/关闭')
        pref_menu.connect('activate', self._active_translate_windows)
        menu.add(pref_menu)

        self.menu_auto_translate = Gtk.MenuItem(label="自动翻译：已开启")
        self.menu_auto_translate.connect('activate',
                                         self._active_auto_translate)
        menu.add(self.menu_auto_translate)

        menu.add(Gtk.SeparatorMenuItem())

        config_version = config.get_config_version()

        self.help_menu = Gtk.MenuItem(label="关于：V" + config_version["name"])
        self.help_menu.connect('activate', self._on_help)
        menu.add(self.help_menu)

        exit_menu = Gtk.MenuItem(label='完全退出')
        exit_menu.connect('activate', self.on_exit)
        menu.add(exit_menu)

        menu.show_all()
        self.indicator.set_menu(menu)

    def on_exit(self, event=None, data=None):
        try:
            Gtk.main_quit()
        except RuntimeError:
            pass

    def _on_preference(self, event=None, data=None):
        pass

    def _on_help(self, event=None, data=None):

        s = "1. 复制即可自动翻译，状态栏可暂停复制即翻译\n2. 截图到系统剪贴板，自动OCR识别并翻译"
        logo = GdkPixbuf.Pixbuf.new_from_file_at_size("./ui/icon.png", 64, 64)

        config_version = config.get_config_version()

        dialog = Gtk.AboutDialog()

        dialog.set_logo(logo)
        dialog.set_program_name("兰译")
        dialog.set_version("V " + config_version["name"])
        dialog.set_license_type(Gtk.License.GPL_3_0)
        dialog.set_comments(s)

        dialog.set_website(config_version["home_url"])
        dialog.set_website_label(config_version["home_name"])
        dialog.set_copyright("© 2021-2022 兰朵儿")

        dialog.set_authors(["yuh"])
        # 翻译
        dialog.set_translator_credits("yuh")
        # 文档
        dialog.set_documenters(["yuh"])
        # 美工
        dialog.set_artists(["yuh"])
        dialog.connect('response', lambda dialog, data: dialog.destroy())
        dialog.show_all()

    def _active_auto_translate(self, view=None):
        self.is_auto_translate = not self.is_auto_translate
        s = "自动翻译：已开启"
        ind_label = "翻译中"
        if (not self.is_auto_translate):
            s = "自动翻译：已关闭"
            ind_label = "暂停翻译"
        elif (self.update):
            ind_label = "有更新"

        self.indicator.set_label(ind_label, "")
        self.menu_auto_translate.set_label(s)

        self._active_translate_windows()

    def _active_translate_windows(self,
                                  clipboard=None,
                                  event=None):
        # 3种情况会调用这个函数
        #   复制
        is_copy = clipboard is not None and event is not None
        # 点击暂停翻译
        is_active_auto = clipboard is None and event is None
        # 点击打开或隐藏翻译页面
        is_active_windows = clipboard is not None and event is None

        windows_is_closed = self.translate_win is None or self.translate_win.is_hide

        if(is_copy):
            if (self.is_auto_translate):
                if (windows_is_closed):
                    self.translate_win = Translate()
                    self.translate_win.open()
                self.translate_win.copy_auto_translate(clipboard)
        elif(is_active_auto):
            if(self.is_auto_translate):
                if (windows_is_closed):
                    self.translate_win = Translate()
                    self.translate_win.open()
                    self.translate_win.copy_auto_translate()
            elif (not windows_is_closed):
                self.translate_win.close()
        elif(is_active_windows):
            if (windows_is_closed):
                self.translate_win = Translate()
                self.translate_win.open()
                self.translate_win.copy_auto_translate()
            else:
                self.translate_win.close()

    def getClipboard(self):
        if (config.get_config_setting()["translate_way_copy"]):
            return Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        else:
            return Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)

if __name__ == "__main__":
    if not Path("cache").exists():
        os.makedirs("cache")
    app = LdrTranlate()
    try:
        Gtk.main()
    except KeyboardInterrupt:
        app.on_exit()
