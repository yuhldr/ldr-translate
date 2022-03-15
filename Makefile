PREFIX=/opt
APP_PATH=/opt


snap:
	mkdir -p build/snap/ldr-translate/

	cp -r ui api ui_translate.py ldr-translate.py preferences.py config.json build/snap/ldr-translate

	cp debian/ldr build/snap/ldr-translate/
	@echo "cd $(APP_PATH)/ldr-translate/" >> build/snap/ldr-translate/ldr
	@echo "python3 ./ldr-translate.py" >> build/snap/ldr-translate/ldr

	cp snapcraft.yaml build/snap


check-gtk:
	sudo apt install gir1.2-appindicator3-0.1 python3-psutil python3-requests

check-qt:
	pip3 install pyQt5


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

deb:gtk
	rm -rf build/deb
	mkdir -p build/deb
	mkdir -p build/deb/ldr-translate/DEBIAN
	cp -r build/ldr-translate/* build/deb/ldr-translate/
	cp data/pkg/debian/control/* build/deb/ldr-translate/DEBIAN/
	cd build/deb && dpkg -b  ldr-translate ldr-translate.deb && ls -l  --block-size=k *.deb && rm -r ldr-translate

rpm:
	@echo 暂不支持，请输入以下命令，即可安装
	@echo 'make check-qt && make qt && make install'



install: uninstall
	sudo mkdir -p /usr/bin/
	sudo mkdir -p /usr/share/icons/
	sudo cp -r ./build/ldr-translate$(PREFIX)/ldr-translate $(PREFIX)/
	sudo cp build/ldr-translate/usr/bin/* /usr/bin/
	sudo cp build/ldr-translate/usr/share/icons/* /usr/share/icons/
	sudo cp build/ldr-translate/usr/share/applications/* /usr/share/applications/


uninstall:
	sudo rm -rf $(PREFIX)/ldr-translate
	sudo rm -rf /usr/bin/ldr /usr/share/icons/ldr-translate.png /usr/share/applications/ldr-translate.desktop ~/.config/autostart/ldr-translate.desktop


clear:
	rm -rf ./build
	rm -rf ./disk
	rm -rf ./test*
	rm -rf ./tempCodeRunnerFile*
	rm -rf ./cache
	rm -rf *.spec
	rm -rf ./build

