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
import logging
import os
from argparse import ArgumentParser
from ui_translate import Translate, VERSION

gi.require_version('AppIndicator3', '0.1')
gi.require_version('Keybinder', '3.0')

from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk, Keybinder


class LdrTranlate(object):
    hide = True

    def _create_menu(self):
        """Creates the main menu and shows it."""
        # create menu {{{
        menu = Gtk.Menu()
        # add preferences menu item
        pref_menu = Gtk.MenuItem(label='翻译：显示/隐藏')
        pref_menu.connect('activate', self.on_translate_activated)
        menu.add(pref_menu)

        # add help menu item
        help_menu = Gtk.MenuItem(label='帮助：' + VERSION)
        help_menu.connect('activate', self._on_help)
        menu.add(help_menu)

        # add preference menu item
        exit_menu = Gtk.MenuItem(label='退出')
        exit_menu.connect('activate', self.on_exit)
        menu.add(exit_menu)

        menu.show_all()
        self.ind.set_menu(menu)
        logging.info("Menu shown")
        # }}} menu done!

    def __init__(self):
        self.translate_win = None
        self._help_dialog = None

        self.ind = appindicator.Indicator.new(
            "ldr-tranlate", os.path.abspath('ui/icon.svg'),
            appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.ind.set_ordering_index(1)

        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)

        self._create_menu()

        key = Keybinder
        key.bind("<alt>q", self.on_translate_activated)
        key.init()

        self.on_translate_activated()

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

    def on_translate_activated(self, event=None):
        if (self.translate_win is None or self.translate_win.is_hide):
            self.translate_win = Translate()
            self.translate_win.start()
        else:
            self.translate_win.close()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config",
                        default=None,
                        help="Use custom config file.")
    parser.add_argument("--version",
                        default=False,
                        action='store_true',
                        help='Show version and exit.')

    options = parser.parse_args()

    if options.version:
        print(VERSION)
        exit(0)

    logging.info("start")

    app = LdrTranlate()
    try:
        Gtk.main()
    except KeyboardInterrupt:
        app.on_exit()
