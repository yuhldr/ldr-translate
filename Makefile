PREFIX=$(HOME)/.local
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
	cp debian/control build/ldr-translate/DEBIAN/

	cd build && sudo dpkg -b  ldr-translate ldr-translate.deb

check:
	sudo apt install python3-pip gir1.2-appindicator3-0.1
	pip3 install -r requirements.txt


debug: check
	python3 ./ldr-translate.py


install: check
	mkdir -p $(PREFIX)/bin
	mkdir -p $(PREFIX)/lib/ldr-translate/cache
	mkdir -p $(PREFIX)/share/applications
	mkdir -p $(PREFIX)/share/icons

	cp -r ui api ui_translate.py ldr-translate.py preferences.py config.json $(PREFIX)/lib/ldr-translate/
	cp ui/icon.png $(PREFIX)/share/icons/ldr-translate.png
	cp debian/ldr-translate.desktop $(PREFIX)/share/applications/

	cp debian/ldr $(PREFIX)/bin/ldr
	@echo "cd $(PREFIX)/lib/ldr-translate/" >> $(PREFIX)/bin/ldr
	@echo "python3 ./ldr-translate.py" >> $(PREFIX)/bin/ldr

	@echo "\n\n*****兰译app使用说明*****\n\n1. 软件安装位置：$(PREFIX)/lib/ldr-translate/\n2. 终端输入 ldr-translate 即可运行\n3. 注销并重新登录以后，应用程序中应包含‘兰译’\n4. 复制即可自动翻译、显示主窗口\n5. 系统截图到剪贴板，自动OCR识别并翻译\n6. 更多教程见：https://github.com/yuhlzu/ldr-translate"


uninstall:
	rm -rf $(PREFIX)/lib/ldr-translate/
	rm -f $(PREFIX)/share/icons/ldr-translate.png
	rm -rf $(PREFIX)/bin/ldr
	rm -rf $(PREFIX)/share/applications/ldr-translate.desktop

reinstall: uninstall install

clear:
	rm -rf ./build
	rm -rf ./disk
	rm -rf ./test*
	rm -rf ./tempCodeRunnerFile*
	rm -rf ./cache
	rm -rf *.spec
	rm -rf ./build

