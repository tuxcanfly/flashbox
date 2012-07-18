# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('flashbox')

import logging
logger = logging.getLogger('flashbox')

from flashbox_lib.AboutDialog import AboutDialog

# See flashbox_lib.AboutDialog.py for more details about how this class works.
class AboutFlashboxDialog(AboutDialog):
    __gtype_name__ = "AboutFlashboxDialog"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the about dialog"""
        super(AboutFlashboxDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

