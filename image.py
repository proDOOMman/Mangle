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

from PIL import Image, ImageDraw, ImageStat, ImageFile
import zipfile

class ImageFlags:
    Orient = 1 << 0
    Resize = 1 << 1
    Frame = 1 << 2
    Quantize = 1 << 3
    Split = 1 << 4
    Reverse = 1 << 5
    Cbz = 1 << 6
    Crop = 1 << 7


class KindleData:
    Palette4 = [
        0x00, 0x00, 0x00,
        0x55, 0x55, 0x55,
        0xaa, 0xaa, 0xaa,
        0xff, 0xff, 0xff
    ]

    Palette15 = [
        0x00, 0x00, 0x00,
        0x11, 0x11, 0x11,
        0x22, 0x22, 0x22,
        0x33, 0x33, 0x33,
        0x44, 0x44, 0x44,
        0x55, 0x55, 0x55,
        0x66, 0x66, 0x66,
        0x77, 0x77, 0x77,
        0x88, 0x88, 0x88,
        0x99, 0x99, 0x99,
        0xaa, 0xaa, 0xaa,
        0xbb, 0xbb, 0xbb,
        0xcc, 0xcc, 0xcc,
        0xdd, 0xdd, 0xdd,
        0xff, 0xff, 0xff,
    ]

    Profiles = {
        'Kindle 1': ((600, 800), Palette4),
        'Kindle 2': ((600, 800), Palette15),
        'Kindle 3': ((600, 800), Palette15),
        'Kindle DX': ((824, 1200), Palette15),
        'Kindle DXG': ((824, 1200), Palette15)
    }


def quantizeImage(image, palette):
    colors = len(palette) / 3
    if colors < 256:
        palette = palette + palette[:3] * (256 - colors)

    palImg = Image.new('P', (1, 1))
    palImg.putpalette(palette)

    return image.quantize(palette=palImg)


def resizeImage(image, size):
    widthDev, heightDev = size
    widthImg, heightImg = image.size

    if widthImg <= widthDev and heightImg <= heightDev:
        return image

    ratioImg = float(widthImg) / float(heightImg)
    ratioWidth = float(widthImg) / float(widthDev)
    ratioHeight = float(heightImg) / float(heightDev)

    if ratioWidth > ratioHeight:
        widthImg = widthDev
        heightImg = int(widthDev / ratioImg)
    elif ratioWidth < ratioHeight:
        heightImg = heightDev
        widthImg = int(heightDev * ratioImg)
    else:
        widthImg, heightImg = size

    return image.resize((widthImg, heightImg), Image.ANTIALIAS)


def formatImage(image):
    if image.mode == 'RGB':
        return image
    return image.convert('RGB')


def orientImage(image, size):
    widthDev, heightDev = size
    widthImg, heightImg = image.size

    if (widthImg > heightImg) != (widthDev > heightDev):
        return image.rotate(90, Image.BICUBIC, True)

    return image


def frameImage(image, foreground, background, size):
    widthDev, heightDev = size
    widthImg, heightImg = image.size

    pastePt = (
        max(0, (widthDev - widthImg) / 2),
        max(0, (heightDev - heightImg) / 2)
    )

    corner1 = (
        pastePt[0] - 1,
        pastePt[1] - 1
    )

    corner2 = (
        pastePt[0] + widthImg + 1,
        pastePt[1] + heightImg + 1
    )

    imageBg = Image.new(image.mode, size, background)
    imageBg.paste(image, pastePt)

    draw = ImageDraw.Draw(imageBg)
    draw.rectangle([corner1, corner2], outline=foreground)

    return imageBg

def cropWhiteSpace(image):
#    print "Old size: %sx%s"%(image.size[0],image.size[1])
    widthImg, heightImg = image.size
    delta = 10
    diff = delta
    threshold = 5
    # top
    while ImageStat.Stat(image.crop((0,0,widthImg,diff))).var[0] < threshold \
    and diff < heightImg:
        diff += delta
    diff -= delta
#    print "Top crop: %s"%diff
    image = image.crop((0,diff,widthImg,heightImg))
    widthImg, heightImg = image.size
    diff = delta
    # left
    while ImageStat.Stat(image.crop((0,0,diff,heightImg))).var[0] < threshold \
    and diff < widthImg:
        diff += delta
    diff -= delta
#    print "Left crop: %s"%diff
    image = image.crop((diff,0,widthImg,heightImg))
    widthImg, heightImg = image.size
    diff = delta
    # down
    while ImageStat.Stat(image.crop((0,heightImg-diff,widthImg,heightImg))).var[0] < threshold \
    and diff < heightImg:
        diff += delta
    diff -= delta
#    print "Down crop: %s"%diff
    image = image.crop((0,0,widthImg,heightImg-diff))
    widthImg, heightImg = image.size
    diff = delta
    # right
    while ImageStat.Stat(image.crop((widthImg-diff,0,widthImg,heightImg))).var[0] < threshold \
    and diff < widthImg:
        diff += delta
    diff -= delta
#    print "Right crop: %s"%diff
    image = image.crop((0,0 ,widthImg-diff,heightImg))
#    print "New size: %sx%s"%(image.size[0],image.size[1])
    return image

def convertImage(source, target, index, device, flags):
    try:
        size, palette = KindleData.Profiles[device]
    except KeyError:
        raise RuntimeError('Unexpected output device %s' % device)

    try:
        if source.startswith("ZIP://") and " NAME://" in source:
            archivename, filename = source.split(" NAME://")
            archivename = archivename[6:]
            image_io = ImageFile.Parser()
            archive = zipfile.ZipFile(archivename)
            image_io.feed(archive.read(filename))
            image = image_io.close()
        else:
            image = Image.open(source)
    except IOError:
        raise RuntimeError('Cannot read image file %s' % source)
    image = formatImage(image)
    delta = 0
    count = 1
    split = False
    widthDev, heightDev = size
    widthImg, heightImg = image.size
    if flags & ImageFlags.Split and (widthImg > heightImg) != (widthDev > heightDev):
        count += 1
        split = True
    boxlist = [(0,0,widthImg/2,heightImg),(widthImg/2,0,widthImg,heightImg)]
    targets = []
    while count>0:
        if split:
            if flags & ImageFlags.Reverse:
                tmp_image = image.crop(boxlist[(count+1)%2])
            else:
                tmp_image = image.crop(boxlist[count%2])
        else:
            tmp_image = image
        if flags & ImageFlags.Crop:
            tmp_image = cropWhiteSpace(tmp_image)
        if flags & ImageFlags.Orient:
            tmp_image = orientImage(tmp_image, size)
        if flags & ImageFlags.Resize:
            tmp_image = resizeImage(tmp_image, size)
        if flags & ImageFlags.Frame:
            tmp_image = frameImage(tmp_image, tuple(palette[:3]), tuple(palette[-3:]), size)
        if flags & ImageFlags.Quantize:
            tmp_image = quantizeImage(tmp_image, palette)
        try:
            tmp_image.save(target%(index+delta))
        except IOError:
            raise RuntimeError('Cannot write image file %s' % target%(index+delta))
        targets.append(target%(index+delta))
        delta += 1
        count -= 1

    return targets
