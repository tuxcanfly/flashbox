# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Javed Khan <tuxcanfly@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
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

        self.ready_message = self.status.get_text()

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
        subprocess.Popen(["xdg-open", path])

    def on_liststore_row_deleted(self, *args, **kwargs):
        if self.num_videos > 0:
            self.num_videos -= 1
        self.update_status()

    def fill_store(self):
        self.liststore.clear()

        self.num_videos = 0
        for pid in get_pids():
            for file_name in get_file_names(pid):
                path = '/proc/%s/fd/%s' %(pid, file_name)
                self.num_videos += 1
                self.liststore.append([path, self.icon, True])

        self.update_status()

        return True

    def update_status(self):
        if self.num_videos:
            self.status.set_text(_("%s videos found" % (self.num_videos)))
        else:
            self.status.set_text(self.ready_message)
