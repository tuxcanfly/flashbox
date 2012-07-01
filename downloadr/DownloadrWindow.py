# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import os
import subprocess
import gettext

from gettext import gettext as _
gettext.textdomain('downloadr')

from gi.repository import Gtk, GObject # pylint: disable=E0611
import logging
logger = logging.getLogger('downloadr')

from downloadr_lib import Window
from downloadr.AboutDownloadrDialog import AboutDownloadrDialog
from downloadr.PreferencesDownloadrDialog import PreferencesDownloadrDialog

from flashcache import get_pids, get_file_names

COL_PATH = 0
COL_PIXBUF = 1
COL_IS_DIRECTORY = 2
REFRESH_TIMEOUT = 1000 # 1s


# See downloadr_lib.Window.py for more details about how this class works
class DownloadrWindow(Window):
    __gtype_name__ = "DownloadrWindow"

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(DownloadrWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutDownloadrDialog
        self.PreferencesDialog = PreferencesDownloadrDialog

        self.current_directory = os.path.realpath(os.path.expanduser('~'))
        self.icon = self.get_icon("video-x-generic")

        self.liststore = self.builder.get_object("liststore")
        self.iconview = self.builder.get_object("iconview")
        self.status = self.builder.get_object("status")

        self.iconview.set_text_column(COL_PATH)
        self.iconview.set_pixbuf_column(COL_PIXBUF)

        self.fill_store()

        GObject.threads_init()
        GObject.timeout_add(REFRESH_TIMEOUT, self.fill_store)

        # Code for other initialization actions should be added here.

    def get_icon(self, icon):
        return Gtk.IconTheme.get_default().load_icon(icon, 48, 0)

    def on_iconview_item_activated(self, widget, item):
        model = widget.get_model()
        path = model[item][COL_PATH]
        subprocess.Popen(["gnome-open", path])

    def fill_store(self):
        self.liststore.clear()

        num_videos = 0
        for pid in get_pids():
            for file_name in get_file_names(pid):
                path = '/proc/%s/fd/%s' %(pid, file_name)
                num_videos += 1
                self.liststore.append([path, self.icon, True])

        if num_videos:
            self.status.set_text(_("%s videos found" % (num_videos)))

        return True
