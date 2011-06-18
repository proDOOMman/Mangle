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

from PyQt4 import QtGui, QtCore

class ImageContainer(QtGui.QLabel):
    def __init__(self,parent):
        QtGui.QLabel.__init__(self,parent)

    def resizeEvent(self,event):
        if ( not self.original_pixmap == None ) and (not self.original_pixmap.isNull()):
            QtGui.QLabel.setPixmap(self,self.original_pixmap.scaled(self.size(),aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation))
    
    def setPixmap(self,pixmap):
        self.original_pixmap = pixmap
        if pixmap.isNull():
            QtGui.QLabel.setPixmap(self,pixmap)
        else:
            QtGui.QLabel.setPixmap(self,pixmap.scaled(self.size(),aspectRatioMode=QtCore.Qt.KeepAspectRatio,transformMode=QtCore.Qt.SmoothTransformation))

    def originalPixmap(self):
        return self.original_pixmap