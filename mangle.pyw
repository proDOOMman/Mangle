#!/usr/bin/env python

# Copyright (C) 2010  Alex Yatskov
# Copyright (C) 2011  Stanislav (proDOOMman) Kosolapov <prodoomman@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4.QtCore import QTranslator
from PyQt4.QtCore import QLocale

from mangle.book import MainWindowBook

def main():
    application = QtGui.QApplication(sys.argv)
    tr = QTranslator()
    if sys.platform.startswith('win'):
        tr.load("mangle_%s.qm"%str(QLocale.system().name()))
    else:
        tr.load("mangle_%s.qm"%str(QLocale.system().name()),'/usr/share/mangle')
    application.installTranslator(tr)
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    window = MainWindowBook(filename)
    window.show()
    return application.exec_()

if __name__ == "__main__":
    sys.exit(main())