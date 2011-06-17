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

import os
from PyQt4 import QtGui, QtCore

import image
from convertthread import ConvertThread
from image import ImageFlags
import zipfile

class DialogConvert(QtGui.QProgressDialog):
    def __init__(self, parent, book, directory):
        QtGui.QProgressDialog.__init__(self)
        self.book = book
        self.directory = directory
        self.setWindowTitle('Exporting book...')
        self.setMaximum(len(self.book.images))
        self.setValue(0)
        self.threadPool = QtCore.QThreadPool(self)
        self.threadPool.setExpiryTimeout(-1)

    def showEvent(self, event):
        directory = os.path.join(unicode(self.directory), unicode(self.book.title))
        target = os.path.join(directory, '%05d.png')
        try:
            if not os.path.isdir(directory):
                os.makedirs(directory)
        except OSError:
            QtGui.QMessageBox.critical(self, 'Mangle', 'Cannot create directory %s' % directory)
            self.close()
            return
            
        if self.book.imageFlags & ImageFlags.Cbz:
            filename = os.path.join(os.path.join(unicode(self.directory), unicode(self.book.title)),unicode(self.book.title)+".cbz")
            if not self.book.overwrite and os.path.isfile(filename):
                self.close()
                return
            self.cbz = zipfile.ZipFile(filename, "w")
            
        try:
            base = os.path.join(directory, unicode(self.book.title))
            mangaSaveName = base + '.manga_save'
            if self.book.overwrite or not os.path.isfile(mangaSaveName):
                mangaSave = open(mangaSaveName, 'w')
                if self.book.imageFlags & ImageFlags.Cbz:
                    saveData = u'LAST=00000.png'
                else:
                    saveData = u'LAST=/mnt/us/pictures/%s/%s' % (self.book.title, os.path.split(target)[1])
                mangaSave.write(saveData.encode('utf-8'))
                mangaSave.close()
        except IOError:
            QtGui.QMessageBox.critical(self, 'Mangle', 'Cannot write manga file(s) to directory %s' % directory)
            self.close()
            return
        print "Using %s threads..."%self.threadPool.maxThreadCount()
        for index in xrange(0,len(self.book.images)):
            if self.book.overwrite or not os.path.isfile(target%index):
                source = unicode(self.book.images[index])
                ct = ConvertThread(source,target,index, str(self.book.device), self.book.imageFlags)
                QtCore.QObject.connect(ct.emitter,QtCore.SIGNAL("targetSaved(QStringList)"),self.postprocessImages)
                QtCore.QObject.connect(ct.emitter,QtCore.SIGNAL("threadError(QString)"),self.threadError)
                self.threadPool.start(ct)

    def threadError(self,error):
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

    def packPage(self,page):
        self.cbz.write(page,os.path.split(page)[1])
        os.remove(page)

    def postprocessImages(self,images):
        self.setValue(self.value()+1)
        self.setLabelText('Processed %s...' % os.path.split(str(images[0]))[1])
        for page in images:
            if self.book.imageFlags & ImageFlags.Cbz:
                self.packPage(str(page))        
            if self.value() == -1:
                self.allThreadsFinished()

    def allThreadsFinished(self):
        print "Converting finished!"
        if self.book.imageFlags & ImageFlags.Cbz:
            self.cbz.close()
