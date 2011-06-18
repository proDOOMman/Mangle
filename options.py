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


from PyQt4 import QtGui, QtCore
from PIL import Image
from image import ImageFlags, KindleData
from ui.options_ui import Ui_DialogOptions
import image as Img
import zipfile

class DialogOptions(QtGui.QDialog, Ui_DialogOptions):
    def __init__(self, parent, book):
        QtGui.QDialog.__init__(self, parent)
        self.book = book
        self.setupUi(self)
        self.connect(self, QtCore.SIGNAL('accepted()'), self.onAccept)
        self.moveOptionsToDialog()
        self.updatePreview()
        QtCore.QObject.connect(self.comboBoxDevice,QtCore.SIGNAL('currentIndexChanged(int)'),self.updatePreview)
        #QtCore.QObject.connect(self.checkboxCbz,QtCore.SIGNAL('toggled(bool)'),self.updatePreview)
        QtCore.QObject.connect(self.checkboxCrop,QtCore.SIGNAL('toggled(bool)'),self.updatePreview)
        QtCore.QObject.connect(self.checkboxFrame,QtCore.SIGNAL('toggled(bool)'),self.updatePreview)
        QtCore.QObject.connect(self.checkboxOrient,QtCore.SIGNAL('toggled(bool)'),self.updatePreview)
        #QtCore.QObject.connect(self.checkboxOverwrite,QtCore.SIGNAL('toggled(bool)'),self.updatePreview)
        QtCore.QObject.connect(self.checkboxQuantize,QtCore.SIGNAL('toggled(bool)'),self.updatePreview)
        QtCore.QObject.connect(self.checkboxResize,QtCore.SIGNAL('toggled(bool)'),self.updatePreview)
        QtCore.QObject.connect(self.checkboxReverse,QtCore.SIGNAL('toggled(bool)'),self.updatePreview)
        QtCore.QObject.connect(self.checkboxSplit,QtCore.SIGNAL('toggled(bool)'),self.updatePreview)
        QtCore.QObject.connect(self.thresholdSpinBox,QtCore.SIGNAL('valueChanged(double)'),self.updatePreview)
        QtCore.QObject.connect(self.prevPreviewButton,QtCore.SIGNAL('clicked()'),self.prevImage)
        QtCore.QObject.connect(self.nextPreviewButton,QtCore.SIGNAL('clicked()'),self.nextImage)
        QtCore.QObject.connect(self.previewSpinBox,QtCore.SIGNAL('valueChanged(int)'),self.changeImage)
        self.previewSpinBox.setMaximum(len(self.book.images)-1)
        #TODO: preview pics popup


    def changeImage(self, index):
        if index == -1:
            self.prevOrig.setPixmap(QtGui.QPixmap(":/img/preview/page.png"))
        else:
            imagename = unicode(self.book.images[index])
            if imagename.startswith("ZIP://") and " NAME://" in imagename:
                try:
                    archivename, filename = imagename.split(" NAME://")
                    archivename = archivename[6:]
                    archive = zipfile.ZipFile(archivename)
                    qt_image = QtGui.QImage()
                    qt_image.loadFromData(archive.read(filename))
                    qt_pix = QtGui.QPixmap.fromImage(qt_image)
                except RuntimeError:
                    self.prevOrig.setPixmap(QtGui.QPixmap())
                self.prevOrig.setPixmap(qt_pix)
            else:
                self.prevOrig.setPixmap(QtGui.QPixmap(self.book.images[index]))
        self.updatePreview()


    def prevImage(self):
        self.previewSpinBox.setValue(self.previewSpinBox.value()-1)


    def nextImage(self):
        self.previewSpinBox.setValue(self.previewSpinBox.value()+1)


    def updatePreview(self):
        self.prevPage1.setPixmap(QtGui.QPixmap())
        self.prevPage2.setPixmap(QtGui.QPixmap())
        device = str(self.comboBoxDevice.itemText(self.comboBoxDevice.currentIndex()))
        try:
            size, palette = KindleData.Profiles[device]
        except KeyError:
            raise RuntimeError('Unexpected output device %s' % device)
        try:
            qt_picture = self.prevOrig.originalPixmap().toImage().convertToFormat(QtGui.QImage.Format_ARGB32)
            image = Image.fromstring("RGBA", (qt_picture.width(),qt_picture.height()), qt_picture.bits().asstring(qt_picture.byteCount()))
        except BaseException, error:
            print str(error)
            raise RuntimeError('Cannot read image')
        image = Img.formatImage(image)
        count = 1
        split = False
        widthDev, heightDev = size
        widthImg, heightImg = image.size
        flags = self.getImageFlags()
        if flags & ImageFlags.Split and (widthImg > heightImg) != (widthDev > heightDev):
            count += 1
            split = True
        boxlist = [(0,0,widthImg/2,heightImg),(widthImg/2,0,widthImg,heightImg)]
        while count>0:
            if split:
                if flags & ImageFlags.Reverse:
                    tmp_image = image.crop(boxlist[(count+1)%2])
                else:
                    tmp_image = image.crop(boxlist[count%2])
            else:
                tmp_image = image
            if flags & ImageFlags.Crop:
                tmp_image = Img.cropWhiteSpace(tmp_image,self.thresholdSpinBox.value())
            if flags & ImageFlags.Orient:
                tmp_image = Img.orientImage(tmp_image, size)
            if flags & ImageFlags.Resize:
                tmp_image = Img.resizeImage(tmp_image, size)
            if flags & ImageFlags.Frame:
                tmp_image = Img.frameImage(tmp_image, tuple(palette[:3]), tuple(palette[-3:]), size)
            if flags & ImageFlags.Quantize:
                tmp_image = Img.quantizeImage(tmp_image, palette)
            count -= 1
            try:
                PILstring = tmp_image.convert("RGB").tostring("jpeg", "RGB")
                qt_image = QtGui.QImage()
                qt_image.loadFromData(QtCore.QByteArray(PILstring))
                qt_pix = QtGui.QPixmap.fromImage(qt_image)
                if not (flags & ImageFlags.Split) or count == 1:
                    self.prevPage1.setPixmap(qt_pix)
                else:
                    self.prevPage2.setPixmap(qt_pix)
            except BaseException, error:
                print str(error)

    def onAccept(self):
        self.moveDialogToOptions()


    def moveOptionsToDialog(self):
        self.lineEditTitle.setText(self.book.title or 'Untitled')
        self.comboBoxDevice.setCurrentIndex(max(self.comboBoxDevice.findText(self.book.device), 0))
        self.checkboxOverwrite.setChecked(QtCore.Qt.Checked if self.book.overwrite else QtCore.Qt.Unchecked)
        self.checkboxOrient.setChecked(QtCore.Qt.Checked if self.book.imageFlags & ImageFlags.Orient else QtCore.Qt.Unchecked)
        self.checkboxResize.setChecked(QtCore.Qt.Checked if self.book.imageFlags & ImageFlags.Resize else QtCore.Qt.Unchecked)
        self.checkboxQuantize.setChecked(QtCore.Qt.Checked if self.book.imageFlags & ImageFlags.Quantize else QtCore.Qt.Unchecked)
        self.checkboxFrame.setChecked(QtCore.Qt.Checked if self.book.imageFlags & ImageFlags.Frame else QtCore.Qt.Unchecked)
        self.checkboxSplit.setChecked(QtCore.Qt.Checked if self.book.imageFlags & ImageFlags.Split else QtCore.Qt.Unchecked)
        self.checkboxReverse.setChecked(QtCore.Qt.Checked if self.book.imageFlags & ImageFlags.Reverse else QtCore.Qt.Unchecked)
        self.checkboxCbz.setChecked(QtCore.Qt.Checked if self.book.imageFlags & ImageFlags.Cbz else QtCore.Qt.Unchecked)
        self.checkboxCrop.setChecked(QtCore.Qt.Checked if self.book.imageFlags & ImageFlags.Crop else QtCore.Qt.Unchecked)
        self.thresholdSpinBox.setValue(self.book.cropThreshold)


    def getImageFlags(self):
        imageFlags = 0
        if self.checkboxOrient.checkState() == QtCore.Qt.Checked:
            imageFlags |= ImageFlags.Orient
        if self.checkboxResize.checkState() == QtCore.Qt.Checked:
            imageFlags |= ImageFlags.Resize
        if self.checkboxQuantize.checkState() == QtCore.Qt.Checked:
            imageFlags |= ImageFlags.Quantize
        if self.checkboxFrame.checkState() == QtCore.Qt.Checked:
            imageFlags |= ImageFlags.Frame
        if self.checkboxSplit.checkState() == QtCore.Qt.Checked:
            imageFlags |= ImageFlags.Split
        if self.checkboxReverse.checkState() == QtCore.Qt.Checked:
            imageFlags |= ImageFlags.Reverse
        if self.checkboxCbz.checkState() == QtCore.Qt.Checked:
            imageFlags |= ImageFlags.Cbz
        if self.checkboxCrop.checkState() == QtCore.Qt.Checked:
            imageFlags |= ImageFlags.Crop
        return imageFlags

    def moveDialogToOptions(self):
        title = self.lineEditTitle.text()
        device = self.comboBoxDevice.itemText(self.comboBoxDevice.currentIndex())
        overwrite = self.checkboxOverwrite.checkState() == QtCore.Qt.Checked
        cropThreshold = self.thresholdSpinBox.value()

        imageFlags = self.getImageFlags()

        modified = (
            self.book.title != title or
            self.book.device != device or
            self.book.overwrite != overwrite or
            self.book.imageFlags != imageFlags or
            self.book.cropThreshold != cropThreshold
        )

        if modified:
            self.book.modified = True
            self.book.title = title
            self.book.device = device
            self.book.overwrite = overwrite
            self.book.imageFlags = imageFlags
            self.book.cropThreshold = cropThreshold
