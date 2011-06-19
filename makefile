all: \
	clean \
	mangle/ui/resources_rc.py \
	mangle/ui/about_ui.py \
	mangle/ui/options_ui.py \
	mangle/ui/book_ui.py \
	mangle/ui/downloader_ui.py \
	locale

mangle/ui/resources_rc.py: mangle/dev/res/resources.qrc
	pyrcc4 $< -o $@

mangle/ui/about_ui.py: mangle/dev/ui/about.ui
	pyuic4 $< -o $@

mangle/ui/options_ui.py: mangle/dev/ui/options.ui
	pyuic4 $< -o $@

mangle/ui/book_ui.py: mangle/dev/ui/book.ui
	pyuic4 $< -o $@

mangle/ui/downloader_ui.py: mangle/dev/ui/downloader.ui
	pyuic4 $< -o $@

locale:
	LANGUAGE="ru_RU"
	pylupdate4 ./mangle/*.py ./mangle/ui/*.py -ts ./mangle/mangle_${LANGUAGE}.ts
	lrelease ./mangle/mangle_${LANGUAGE}.ts

clean:
	rm ./mangle/ui/*
	touch ./mangle/ui/__init__.py

deb:
	python setup.py --command-packages=stdeb.command bdist_deb
