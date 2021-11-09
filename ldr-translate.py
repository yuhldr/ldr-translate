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
from main import Translate, VERSION

gi.require_version('AppIndicator3', '0.1')
gi.require_version('Keybinder', '3.0')

from gi.repository import AppIndicator3 as appindicator
from gi.repository import Gtk, Keybinder


class LdrTranlate(object):
    hide = False

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
        self._translate_win = None
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
        """Raise a dialog with info about the app."""
        if self._help_dialog is not None:
            self._help_dialog.present()
            return

        self._help_dialog = Gtk.MessageDialog(
            None, Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, None)

        self._help_dialog.set_title("帮助")
        self._help_dialog.set_markup("帮助文档，暂时省略")
        self._help_dialog.run()
        self._help_dialog.destroy()
        self._help_dialog = None

    def on_translate_activated(self, event=None):
        """Raises the preferences dialog. If it's already open, it's
        focused"""
        print("********** " + str(self._translate_win))
        if self._translate_win is not None:
            print("显示")
            self.hide = not self.hide

            if(self.hide):
                self._translate_win.close()
                print("隐藏")
                return
            else:
                self._translate_win.present()
        else:
            print("创建")
            self._translate_win = Translate()

        self.hide = False


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
