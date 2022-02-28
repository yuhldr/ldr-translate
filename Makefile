PREFIX=/opt
APP_PATH=/opt


snap:
	mkdir -p build/snap/ldr-translate/

	cp -r ui api ui_translate.py ldr-translate.py preferences.py config.json build/snap/ldr-translate

	cp debian/ldr build/snap/ldr-translate/
	@echo "cd $(APP_PATH)/ldr-translate/" >> build/snap/ldr-translate/ldr
	@echo "python3 ./ldr-translate.py" >> build/snap/ldr-translate/ldr

	cp snapcraft.yaml build/snap


build: clear
	mkdir -p build/ldr-translate/usr/bin
	mkdir -p build/ldr-translate/usr/share/applications
	mkdir -p build/ldr-translate/usr/share/icons
	mkdir -p build/ldr-translate$(APP_PATH)/ldr-translate

	cp data/ldr build/ldr-translate/usr/bin/
	@echo "cd $(APP_PATH)/ldr-translate/" >> build/ldr-translate/usr/bin/ldr
	@echo "python3 ./main.py" >> build/ldr-translate/usr/bin/ldr

	cp data/icon/icon.png build/ldr-translate/usr/share/icons/ldr-translate.png
	cp data/ldr-translate.desktop build/ldr-translate/usr/share/applications/

	cp -r api data/icon data/config.json build/ldr-translate$(APP_PATH)/ldr-translate/


gtk: build
	cp -r gui/gtk/* build/ldr-translate$(APP_PATH)/ldr-translate/

qt: build
	cp gui/qt/* build/ldr-translate$(APP_PATH)/ldr-translate/

deb:
	mkdir -p build/deb/ldr-translate/DEBIAN
	cp -r build/ldr-translate/* build/deb/ldr-translate/
	cp data/pkg/debian/control/* build/deb/ldr-translate/DEBIAN/
	cd build/deb && dpkg -b  ldr-translate ldr-translate.deb && ls -l  --block-size=k *.deb && rm -r ldr-translate

rpm:


check:
	sudo apt install python3-pip gir1.2-appindicator3-0.1
	pip3 install -r requirements.txt


debug: check
	python3 ./ldr-translate.py


install: uninstall
	mkdir -p ~/.local/bin/
	mkdir -p ~/.local/share/icons/
	sudo cp -r ./build/ldr-translate$(PREFIX)/ldr-translate $(PREFIX)/
	cp build/ldr-translate/usr/bin/* ~/.local/bin/
	cp build/ldr-translate/usr/share/icons/* ~/.local/share/icons/
	cp build/ldr-translate/usr/share/applications/* ~/.local/share/applications/


uninstall:
	sudo rm -rf $(PREFIX)/ldr-translate
	rm -rf ~/.local/bin/ldr ~/.local/share/icons/ldr-translate.png ~/.local/share/applications/ldr-translate.desktop ~/.config/autostart/ldr-translate.desktop

reinstall: uninstall install

clear:
	rm -rf ./build
	rm -rf ./disk
	rm -rf ./test*
	rm -rf ./tempCodeRunnerFile*
	rm -rf ./cache
	rm -rf *.spec
	rm -rf ./build

