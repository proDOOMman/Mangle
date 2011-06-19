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

from PyQt4 import QtCore

import image
from image import ImageFlags

class ConvertThread(QtCore.QRunnable):
    def __init__(self, src, trg, ind, dev, imgFlags, crop_threshold):
        self.emitter = QtCore.QObject()
        QtCore.QRunnable.__init__(self)
        self.source = src
        self.target = trg
        self.index = ind*(int(bool(imgFlags & ImageFlags.Split))+1)
        self.device = dev
        self.imageFlags = imgFlags
        self.threshold = crop_threshold

    def run(self):
        try:
            targets = image.convertImage(self.source, self.target, self.index, self.device, self.imageFlags, self.threshold)
        except RuntimeError, error:
            self.emitter.emit(QtCore.SIGNAL("threadError(QString)"),QtCore.QString(unicode(error)))
            return
        self.emitter.emit(QtCore.SIGNAL("targetSaved(QStringList)"),QtCore.QStringList(targets))
