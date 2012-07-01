# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import os
import gettext

from gettext import gettext as _
gettext.textdomain('downloadr')

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('downloadr')

from downloadr_lib import Window
from downloadr.AboutDownloadrDialog import AboutDownloadrDialog
from downloadr.PreferencesDownloadrDialog import PreferencesDownloadrDialog

COL_PATH = 0
COL_PIXBUF = 1
COL_IS_DIRECTORY = 2


# See downloadr_lib.Window.py for more details about how this class works
class DownloadrWindow(Window):
    __gtype_name__ = "DownloadrWindow"

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(DownloadrWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutDownloadrDialog
        self.PreferencesDialog = PreferencesDownloadrDialog

        self.current_directory = os.path.realpath(os.path.expanduser('~'))
        self.fileicon = self.get_icon(Gtk.STOCK_FILE)
        self.diricon = self.get_icon(Gtk.STOCK_DIRECTORY)

        self.liststore = self.builder.get_object("liststore")
        self.iconview = self.builder.get_object("iconview")

        self.iconview.set_text_column(COL_PATH)
        self.iconview.set_pixbuf_column(COL_PIXBUF)

        self.fill_store()

        # Code for other initialization actions should be added here.

    def get_icon(self, icon):
        return Gtk.IconTheme.get_default().load_icon(icon, 48, 0)

    def fill_store(self):
        self.liststore.clear()

        if self.current_directory == None:
            return

        for fl in os.listdir(self.current_directory):

            if not fl[0] == '.':
                if os.path.isdir(os.path.join(self.current_directory, fl)):
                    self.liststore.append([fl, self.diricon, True])
                else:
                    self.liststore.append([fl, self.fileicon, False])
