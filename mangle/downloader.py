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

import os, re, urllib
from PyQt4 import QtGui, QtCore
from ui.downloader_ui import Ui_Downloader

class Downloader(QtGui.QWidget, Ui_Downloader):
    avaliableSites = [ "readmanga.ru" , "mintmanga.com" , "mangareader.net" ]
    def __init__(self, sitename, manganame, output_directory):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        if not sitename in self.avaliableSites:
            raise RuntimeError("Can't download manga from %s" % sitename)
        if sitename == "mangareader.net":
            self.downloadThread = MangareaderThread(sitename,manganame,output_directory)
        else:
            self.downloadThread = ReadmangaThread(sitename,manganame,output_directory)
        QtCore.QObject.connect(self.downloadThread,QtCore.SIGNAL("pagesCounted(int)"),self.pageProgressBar.setMaximum)
        QtCore.QObject.connect(self.downloadThread,QtCore.SIGNAL("picsCounted(int)"),self.picProgressBar.setMaximum)
        QtCore.QObject.connect(self.downloadThread,QtCore.SIGNAL("log(QString)"),self.log.append)
        QtCore.QObject.connect(self.downloadThread,QtCore.SIGNAL("currentPageChanged(int)"),self.pageProgressBar.setValue)
        QtCore.QObject.connect(self.downloadThread,QtCore.SIGNAL("currentPicChanged(int)"),self.picProgressBar.setValue)
        QtCore.QObject.connect(self.downloadThread,QtCore.SIGNAL("pageLabelChanged(QString)"),self.pageLabel.setText)
        QtCore.QObject.connect(self.downloadThread,QtCore.SIGNAL("picLabelChanged(QString)"),self.picLabel.setText)
        QtCore.QObject.connect(self.downloadThread,QtCore.SIGNAL("finish(QString)"),self.finish)
        self.log.append("Downloading manga '%s' from site %s to %s"%(manganame,
                                                           sitename,
                                                           output_directory))

    def finish(self,message):
        if len(message) == 0:
            self.log.append("Finished!")
        else:
            self.log.append(message)

    def download(self):
        self.downloadThread.start()

    def closeEvent(self,event):
        self.downloadThread.terminate()

class DownloadThread(QtCore.QThread):
    def __init__(self, site, name, outdir):
        QtCore.QThread.__init__(self)
        self.site = site
        self.name = name
        self.outdir = outdir

class MangareaderThread(DownloadThread):
    def __init__(self, site, name, outdir):
        DownloadThread.__init__(self,site,name,outdir)

    def download(self, url, filename):
        try:
            urllib.urlretrieve(url, filename)
        except IOError, error:
            print "Error: %s"%str(error)
            return False
        return True

    def run(self):
        try:
            from BeautifulSoup import BeautifulSoup
        except ImportError:
            self.emit(QtCore.SIGNAL("finish(QString)"),'BeautifulSoup library not found!')
            return
        base_url = "http://mangareader.net"
        manga = self.name
        download_dir = "%s/%s/"%(self.outdir,manga)
        try:
            soup = BeautifulSoup(urllib.urlopen("%s/%s"%(base_url, manga)).read())
        except:
            self.emit(QtCore.SIGNAL("finish(QString)"),'Error while downloading or parsing')
            return
        cl = soup.find('div', id='chapterlist')
        if cl == None:
            self.emit(QtCore.SIGNAL("finish(QString)"),'Manga not found')
            return
        chapterList = cl.findAll('a')
        self.emit(QtCore.SIGNAL("pagesCounted(int)"),len(chapterList))
        for a in chapterList:
            html = urllib.urlopen("%s%s"%(base_url, a['href'])).read()
            chapter = BeautifulSoup(html)
            chapter_num = re.findall(r"document\['chapterno'\] = (\d+);", html)[0]
            cur_dir = "%s%s/"%(download_dir, chapter_num)
            if not os.path.isdir(cur_dir):
                try:
                    os.makedirs(cur_dir)
                except:
                    self.emit(QtCore.SIGNAL("finish(QString)"),"Error while creating dir %s"%cur_dir)
                    return
            menu = chapter.find('select', id="pageMenu")
            self.emit(QtCore.SIGNAL("log(QString)"),QtCore.QString("Chapter %s"%chapter_num))
            self.emit(QtCore.SIGNAL("currentPageChanged(int)"),chapterList.index(a))
            self.emit(QtCore.SIGNAL("pageLabelChanged(QString)"),QtCore.QString(a['href']))
            self.emit(QtCore.SIGNAL("picLabelChanged(QString)"),QtCore.QString("..."))
            self.emit(QtCore.SIGNAL("picsCounted(int)"),0)
            self.emit(QtCore.SIGNAL("currentPicChanged(int)"),1)
            pages = menu.findAll('option')
            self.emit(QtCore.SIGNAL("picsCounted(int)"),len(pages)-1)
            for option in pages:
                page = BeautifulSoup(urllib.urlopen("%s%s"%(base_url, option['value'])).read())
                img = page.find('img', id='img')['src']
                name = "%03d_%s"%(int(option.text), os.path.split(img)[1])
                self.emit(QtCore.SIGNAL("picLabelChanged(QString)"),QtCore.QString(img))
                self.emit(QtCore.SIGNAL("currentPicChanged(int)"),pages.index(option))
                if not os.path.isfile(cur_dir+name):
                    self.emit(QtCore.SIGNAL("log(QString)"),"%s -> %s"%(img,cur_dir+name))
                    while not self.download(img, cur_dir+name):
                        self.emit(QtCore.SIGNAL("log(QString)"),"Repeat...")
                    self.emit(QtCore.SIGNAL("targetCompleted(QString)"),cur_dir+name)
                else:
                    self.emit(QtCore.SIGNAL("log(QString)"),"Skip: %s"%img)
                    self.emit(QtCore.SIGNAL("targetCompleted(QString)"),cur_dir+name)
                pass
        self.emit(QtCore.SIGNAL("pageLabelChanged(QString)"),QtCore.QString('Finished'))
        self.emit(QtCore.SIGNAL("picLabelChanged(QString)"),QtCore.QString('Finished'))
        self.emit(QtCore.SIGNAL("currentPageChanged(int)"),len(chapterList))
        self.emit(QtCore.SIGNAL("finish(QString)"),'')

class ReadmangaThread(DownloadThread):
    def __init__(self, site, name, outdir):
        DownloadThread.__init__(self,site,name,outdir)

    def run(self):
        i = 0 # file enumerator
        rssurl = "http://%s/rss/manga?name=%s"%(self.site,self.name)
        rssobj = urllib.urlopen(rssurl)
        rssstr = rssobj.read()
        rssreg = re.compile("<link>(.*?)</link>")
        dirreg = re.compile("(%s.*)$"%self.name,re.I)
        rsslist = rssreg.findall(rssstr)
        rsslist.reverse()
        rsslist = rsslist[:-1]
        if len(rsslist) == 0:
            self.emit(QtCore.SIGNAL("finish(QString)"),'Manga not found')
            return
        self.emit(QtCore.SIGNAL("pagesCounted(int)"),len(rsslist))
        for pageurl in rsslist:
            self.emit(QtCore.SIGNAL("log(QString)"),QtCore.QString("Page %s"%pageurl))
            self.emit(QtCore.SIGNAL("currentPageChanged(int)"),rsslist.index(pageurl))
            self.emit(QtCore.SIGNAL("pageLabelChanged(QString)"),QtCore.QString(pageurl))
            self.emit(QtCore.SIGNAL("picLabelChanged(QString)"),QtCore.QString("..."))
            self.emit(QtCore.SIGNAL("picsCounted(int)"),0)
            self.emit(QtCore.SIGNAL("currentPicChanged(int)"),1)
            path = self.outdir+"/"+dirreg.findall(pageurl)[0]+"/"
            if not os.path.isdir(path):
                try:
                    os.makedirs(path)
                except:
                    self.emit(QtCore.SIGNAL("finish(QString)"),"Error while creating dir %s"%path)
                    return
            pageobj = urllib.urlopen(pageurl+"?mature=1")
            pagestr = pageobj.read()
            pagereg = re.compile(r"var pics = \[(.*?)\]")
            linksstr = pagereg.findall(pagestr)
            linksreg = re.compile(r"url:\"(.*?)\"")
            try:
                picsurls = linksreg.findall(linksstr[0])
                self.emit(QtCore.SIGNAL("picsCounted(int)"),len(picsurls)-1)
                for picurl in picsurls:
                    self.emit(QtCore.SIGNAL("picLabelChanged(QString)"),QtCore.QString(picurl))
                    self.emit(QtCore.SIGNAL("currentPicChanged(int)"),picsurls.index(picurl))
                    i += 1
                    target = path+("%s"%i).rjust(5,"0")+"_"+os.path.split(picurl)[1]
                    self.emit(QtCore.SIGNAL("log(QString)"),"%s -> %s"%(picurl,target))
                    urllib.urlretrieve(picurl,target)
                    self.emit(QtCore.SIGNAL("targetCompleted(QString)"),target)
            except:
                self.emit(QtCore.SIGNAL("finish(QString)"),"Error while parse %s"%pageurl)
        self.emit(QtCore.SIGNAL("pageLabelChanged(QString)"),QtCore.QString('Finished'))
        self.emit(QtCore.SIGNAL("picLabelChanged(QString)"),QtCore.QString('Finished'))
        self.emit(QtCore.SIGNAL("currentPageChanged(int)"),len(rsslist))
        self.emit(QtCore.SIGNAL("finish(QString)"),'')
