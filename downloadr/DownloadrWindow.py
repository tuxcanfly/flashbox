# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('downloadr')

from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('downloadr')

from downloadr_lib import Window
from downloadr.AboutDownloadrDialog import AboutDownloadrDialog
from downloadr.PreferencesDownloadrDialog import PreferencesDownloadrDialog

# See downloadr_lib.Window.py for more details about how this class works
class DownloadrWindow(Window):
    __gtype_name__ = "DownloadrWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(DownloadrWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutDownloadrDialog
        self.PreferencesDialog = PreferencesDownloadrDialog

        # Code for other initialization actions should be added here.

