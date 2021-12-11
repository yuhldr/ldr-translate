PREFIX=/opt
DEB_PATH=/opt


snap:
	mkdir -p build/snap/ldr-translate/

	cp -r ui api ui_translate.py ldr-translate.py preferences.py config.json build/snap/ldr-translate

	cp debian/ldr build/snap/ldr-translate/
	@echo "cd $(DEB_PATH)/ldr-translate/" >> build/snap/ldr-translate/ldr
	@echo "python3 ./ldr-translate.py" >> build/snap/ldr-translate/ldr

	cp snapcraft.yaml build/snap


build: clear
	mkdir -p build/deb/ldr-translate/DEBIAN
	mkdir -p build/deb/ldr-translate/usr/bin
	mkdir -p build/deb/ldr-translate/usr/share/applications
	mkdir -p build/deb/ldr-translate/usr/share/icons
	mkdir -p build/deb/ldr-translate$(DEB_PATH)/ldr-translate

	cp -r ui api ui_translate.py ldr-translate.py preferences.py config.json build/deb/ldr-translate$(DEB_PATH)/ldr-translate/

	cp debian/ldr build/deb/ldr-translate/usr/bin/
	@echo "cd $(DEB_PATH)/ldr-translate/" >> build/deb/ldr-translate/usr/bin/ldr
	@echo "python3 ./ldr-translate.py" >> build/deb/ldr-translate/usr/bin/ldr

	cp ui/icon.png build/deb/ldr-translate/usr/share/icons/ldr-translate.png
	cp debian/ldr-translate.desktop build/deb/ldr-translate/usr/share/applications/
	cp debian/control/* build/deb/ldr-translate/DEBIAN/

	cd build/deb && dpkg -b  ldr-translate ldr-translate.deb && ls -l  --block-size=k *.deb && rm -r ldr-translate

check:
	sudo apt install python3-pip gir1.2-appindicator3-0.1
	pip3 install -r requirements.txt


debug: check
	python3 ./ldr-translate.py


install: check build
	sudo dpkg -i ./build/deb/ldr-translate.deb



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

