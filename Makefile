PREFIX=$(HOME)/.local/share/ldr-translate
DESKTOP=$(HOME)/.local/share/applications
CONFIG=$(PREFIX)/config.json
cacheConfig=$(HOME)/.cache/ldr-translate/config.json
autoStartUp=$(HOME)/.config/autostart/

check:
	sudo apt install python3-pip gir1.2-appindicator3-0.1
	pip3 install -r requirements.txt


debug: check
	python3 ./ldr-translate.py


install: check
	mkdir -p $(PREFIX)/cache/

	@echo "#!/bin/bash" > $(PREFIX)/lt.sh
	@echo "cd $(PREFIX)" >> $(PREFIX)/lt.sh
	@echo "nohup python3 ./ldr-translate.py &" >> $(PREFIX)/lt.sh
	chmod +x $(PREFIX)/lt.sh

	@echo "#!/bin/bash" > $(PREFIX)/ldr-translate
	@echo "$(PREFIX)/lt.sh" >> $(PREFIX)/ldr-translate
	chmod +x $(PREFIX)/ldr-translate

	sudo mkdir -p /usr/bin
	sudo ln -s $(PREFIX)/ldr-translate /usr/bin/ldr-translate

	cp -r ui api ui_translate.py ldr-translate.py preferences.py config.json $(PREFIX)

	mkdir -p $(DESKTOP)
	cp ldr-translate.desktop $(DESKTOP)
	@echo "Icon=$(PREFIX)/ui/icon.png" >> $(DESKTOP)/ldr-translate.desktop
	@echo "Exec=$(PREFIX)/lt.sh" >> $(DESKTOP)/ldr-translate.desktop
	mkdir -p $(autoStartUp)
	cp $(DESKTOP)/ldr-translate.desktop $(autoStartUp)

	cd $(PREFIX) && python3 -c "from api import config; config.old2new()"

	@echo "\n\n*****兰译app使用说明*****\n\n1. 软件安装位置：$(PREFIX)\n2. 终端输入 ldr-translate 即可运行\n3. 注销并重新登录以后，应用程序中应包含‘兰译’\n4. 复制即可自动翻译、显示主窗口\n5. 系统截图到剪贴板，自动OCR识别并翻译\n6. 更多教程见：https://github.com/yuhlzu/ldr-translate"


uninstall:
	mkdir -p $(HOME)/.cache/ldr-translate/
    ifeq ($(CONFIG), $(wildcard $(CONFIG)))
		mv $(CONFIG) $(cacheConfig)
    endif

	rm -rf $(PREFIX)
	rm -f $(DESKTOP)/ldr-translate.desktop
	sudo rm -f /usr/bin/ldr-translate
	rm -rf $(autoStartUp)/ldr-translate.desktop

reinstall: uninstall install

clear:
	rm -rf ./build
	rm -rf ./disk
	rm -rf ./test*
	rm -rf ./tempCodeRunnerFile*
	rm -rf ./cache
	rm -rf *.spec

