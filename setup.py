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

import sys

if sys.platform.startswith('win'):
    from distutils.core import setup
    import py2exe
    sys.argv.append('py2exe')
    sys.path.append("C:\\WINDOWS\\WinSxS\\x86_Microsoft.VC90.CRT_1fc8b3b9a1e18e3b_9.0.21022.8_x-ww_d08d0375")
    setup(
        windows=[{'script': 'mangle.pyw'}],
        options={'py2exe': {'bundle_files': 3, 'includes': ['sip']}},
        zipfile=None,
		data_files = [
			('', ['mangle\\mangle_ru_RU.qm']),
            ('imageformats', [
                'imageformats\\qgif4.dll',
				'imageformats\\qico4.dll',
				'imageformats\\qjpeg4.dll',
				'imageformats\\qmng4.dll',
				'imageformats\\qsvg4.dll',
				'imageformats\\qtiff4.dll'
                ])
		]
    )
else:
    from setuptools import setup, find_packages
    setup(
        name = "Mangle",
        version = "2.4.2",
        packages = find_packages(),
        scripts = ['mangle.pyw'],
        author = "Alex Yatskov, Stanislav (proDOOMman) Kosolapov",
        author_email = "proDOOMman@gmail.com",
        description = "Mangle - manga converter and optimiser for Kindle devices",
        license = "GPLv3",
        keywords = "manga kindle amazon graphics",
        url = "https://github.com/proDOOMman/Mangle",
        data_files = [('share/mangle', ['mangle/mangle_ru_RU.qm']),
                      ('/usr/share/applications/',['mangle.desktop']),
                        ('/usr/share/pixmaps/',['mangle.xmp'])]
#        install_requires = ['PyQt','PIL']
    )
