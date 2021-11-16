PREFIX=/opt
DEB_PATH=/opt


build: clear
	mkdir -p build/ldr-translate/DEBIAN
	mkdir -p build/ldr-translate/usr/bin
	mkdir -p build/ldr-translate/usr/share/applications
	mkdir -p build/ldr-translate/usr/share/icons
	mkdir -p build/ldr-translate$(DEB_PATH)/ldr-translate/cache

	cp -r ui api ui_translate.py ldr-translate.py preferences.py config.json build/ldr-translate$(DEB_PATH)/ldr-translate/

	cp debian/ldr build/ldr-translate/usr/bin/
	@echo "cd $(DEB_PATH)/ldr-translate/" >> build/ldr-translate/usr/bin/ldr
	@echo "python3 ./ldr-translate.py" >> build/ldr-translate/usr/bin/ldr

	cp ui/icon.png build/ldr-translate/usr/share/icons/ldr-translate.png
	cp debian/ldr-translate.desktop build/ldr-translate/usr/share/applications/
	cp debian/control/* build/ldr-translate/DEBIAN/

	cd build && sudo dpkg -b  ldr-translate ldr-translate.deb && ls -l  --block-size=k *.deb

check:
	sudo apt install python3-pip gir1.2-appindicator3-0.1
	pip3 install -r requirements.txt


debug: check
	python3 ./ldr-translate.py


install: check build
	sudo dpkg -i ./build/ldr-translate.deb



uninstall:
	sudo apt remove ldr-translate 

reinstall: uninstall install

clear:
	rm -rf ./build
	rm -rf ./disk
	rm -rf ./test*
	rm -rf ./tempCodeRunnerFile*
	rm -rf ./cache
	rm -rf *.spec
	rm -rf ./build

