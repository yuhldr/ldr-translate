#!/usr/bin/python3
# coding: utf-8
#
# A simple indicator applet displaying cpu and memory information
#
# Author: yuh <yuhldr@gmail.com>
# Original Homepage: https://yuhldr.github.io/
# Fork Homepage: https://github.com/yuhldr/ldr-translate
# License: GPL v3

import gi
import os
# import faulthandler
# # 在import之后直接添加以下启用代码即可 python3 -X faulthandler ldr-translate.py
# faulthandler.enable()
from utils import locales, version, config
from utils.locales import t_ui

try:
    gi.require_version('AyatanaAppIndicator3', '0.1')
    from gi.repository import AyatanaAppIndicator3 as appindicator
except ValueError:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3 as appindicator

gi.require_version("Gtk", "3.0")

from ui_translate import Translate
from preferences import Preference

from gi.repository import Gtk, Gdk, GdkPixbuf


class LdrTranlate(Gtk.Application):

    def __init__(self):
        self.translate_win = None
        self._help_dialog = None
        self.auto_translate = 0

        self.clip_copy = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.clip_select = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        self.handler_id_clip = None

        self.indicator = appindicator.Indicator.new(
            "ldr-tranlate", os.path.abspath(config.get_tray_icon_file()),
            appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.indicator.set_label("翻译中", "")
        self.indicator.set_ordering_index(1)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        self._create_menu()

    def _create_menu(self):
        menu = Gtk.Menu()

        pref_menu = Gtk.MenuItem(label='显示翻译窗口')
        pref_menu.connect('activate', self._active_translate_windows)
        menu.add(pref_menu)
        menu.add(Gtk.SeparatorMenuItem())

        menu_t_0 = Gtk.RadioMenuItem(label="复制即翻译")
        menu_t_0.connect('activate', self._set_auto_translate, 0)
        menu.append(menu_t_0)
        menu_t_0.set_active(True)

        menu_t_1 = Gtk.RadioMenuItem(label='划词翻译', group=menu_t_0)
        menu_t_1.connect('activate', self._set_auto_translate, 1)
        menu.append(menu_t_1)

        menu_t_2 = Gtk.RadioMenuItem(label='暂不翻译', group=menu_t_0)
        menu_t_2.connect('activate', self._set_auto_translate, 2)
        menu.append(menu_t_2)

        menu.add(Gtk.SeparatorMenuItem())

        menu_prf = Gtk.MenuItem(label=t_ui("setting_label"))
        menu_prf.connect('activate', self._on_preference)
        menu.add(menu_prf)

        help_menu = Gtk.MenuItem(label="关于：V" + version.get_value("name"))
        help_menu.connect('activate', self._on_help)
        menu.add(help_menu)

        exit_menu = Gtk.MenuItem(label='完全退出')
        exit_menu.connect('activate', self.on_exit)
        menu.add(exit_menu)

        menu.show_all()
        self.indicator.set_menu(menu)
        self._active_translate_windows()

    def on_exit(self, event=None, data=None):
        try:
            Gtk.main_quit()
        except RuntimeError:
            pass

    def _on_preference(self, event=None, data=None):
        Preference(self)

    def _on_help(self, event=None, data=None):

        logo = GdkPixbuf.Pixbuf.new_from_file_at_size("./icon/icon.png", 64,
                                                      64)

        version_home_url = version.get_value("home_url")
        version_name = version.get_value("name")

        dialog = Gtk.AboutDialog()

        dialog.set_logo(logo)
        dialog.set_license_type(Gtk.License.GPL_3_0)

        dialog.set_program_name("兰译")
        dialog.set_copyright("© 2021-2022 兰朵儿")

        dialog.set_version("V " + version_name)
        dialog.set_website(version_home_url)

        dialog.set_comments(locales.t("version.msg"))
        dialog.set_website_label(
            locales.t("version.home_name"))

        dialog.set_authors(["yuh"])
        # 翻译
        dialog.set_translator_credits("yuh")
        # 文档
        dialog.set_documenters(["yuh"])
        # 美工
        dialog.set_artists(["yuh"])
        dialog.connect('response', lambda dialog, data: dialog.destroy())
        dialog.show_all()

    def _set_auto_translate(self, view=None, n=0):

        if (self.handler_id_clip is not None):
            self.getClipboard().disconnect(self.handler_id_clip)

        self.auto_translate = n

        if (n != 2):
            self.handler_id_clip = self.getClipboard().connect(
                "owner-change", self._active_translate_windows)
            self.update()
        else:
            self.handler_id_clip = None

    def _active_translate_windows(self, a=None, b=None):

        if (self.translate_win is None or self.translate_win.is_hide):
            self.translate_win = Translate()
            self.translate_win.open()
        if b is None:
            a = None
        self.translate_win.copy_auto_translate(a)

    def getClipboard(self):
        if (self.auto_translate == 0):
            return self.clip_copy
        elif (self.auto_translate == 1):
            return self.clip_select

    def update(self):
        ind_label = "复制翻译"
        if (self.auto_translate == 2):
            ind_label = "暂停翻译"
        elif (self.auto_translate == 1):
            ind_label = "划词翻译"

        self.indicator.set_label(ind_label, "")


# ******* 监测  *******

if __name__ == "__main__":

    app = LdrTranlate()

    try:
        Gtk.main()
    except KeyboardInterrupt:
        app.on_exit()
