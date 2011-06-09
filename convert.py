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

import os
from PyQt4 import QtGui, QtCore

import image
from image import ImageFlags
import zipfile

class DialogConvert(QtGui.QProgressDialog):
    def __init__(self, parent, book, directory):
        QtGui.QProgressDialog.__init__(self)

        self.book = book
        self.directory = directory

        self.timer = None
        self.setWindowTitle('Exporting book...')
        self.setMaximum(len(self.book.images))
        self.setValue(0)
        self.delta = 0


    def showEvent(self, event):
        if self.timer == None:
            self.timer = QtCore.QTimer()
            self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.onTimer)
            self.timer.start(0)


    def onTimer(self):
        index = self.value()
        directory = os.path.join(unicode(self.directory), unicode(self.book.title))
        target = os.path.join(directory, '%05d.png')
        source = unicode(self.book.images[index])

        if index == 0:
            try:
                if not os.path.isdir(directory):
                    os.makedirs(directory)
            except OSError:
                QtGui.QMessageBox.critical(self, 'Mangle', 'Cannot create directory %s' % directory)
                self.close()
                return
            
            if self.book.imageFlags & ImageFlags.Cbz:
                self.cbz = zipfile.ZipFile(os.path.join(os.path.join(unicode(self.directory), unicode(self.book.title)),unicode(self.book.title)+".cbz"), "w")
            
            try:
                base = os.path.join(directory, unicode(self.book.title))

                mangaName = base + '.manga'
                if self.book.overwrite or not os.path.isfile(mangaName):
                    manga = open(mangaName, 'w')
                    manga.write('\x00')
                    manga.close()

                mangaSaveName = base + '.manga_save'
                if self.book.overwrite or not os.path.isfile(mangaSaveName):
                    mangaSave = open(base + '.manga_save', 'w')
                    if self.book.imageFlags & ImageFlags.Cbz:
                        saveData = u'LAST=00000.png' # for cbz format
                    else:
                        saveData = u'LAST=/mnt/us/pictures/%s/%s' % (self.book.title, os.path.split(target)[1])
                    mangaSave.write(saveData.encode('utf-8'))
                    mangaSave.close()

            except IOError:
                QtGui.QMessageBox.critical(self, 'Mangle', 'Cannot write manga file(s) to directory %s' % directory)
                self.close()
                return False

        self.setLabelText('Processing %s...' % os.path.split(source)[1])

        try:
            if self.book.overwrite or not os.path.isfile(target):
                diff, targets = image.convertImage(source, target, index+self.delta, str(self.book.device), self.book.imageFlags)
                self.delta += diff
                if self.book.imageFlags & ImageFlags.Cbz:
                    for t in targets:
                        self.cbz.write(t,os.path.split(t)[1])
                        os.remove(t)
        except RuntimeError, error:
            result = QtGui.QMessageBox.critical(
                self,
                'Mangle',
                str(error),
                QtGui.QMessageBox.Abort | QtGui.QMessageBox.Ignore,
                QtGui.QMessageBox.Ignore
            )
            if result == QtGui.QMessageBox.Abort:
                self.close()
                return
        if index == len(self.book.images) and self.book.imageFlags & ImageFlags.Cbz:
            self.cbz.close()
        self.setValue(index + 1)
