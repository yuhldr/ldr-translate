PREFIX=$(HOME)/.local/share/ldr-translate
DESKTOP=$(HOME)/.local/share/applications
CONFIG=$(PREFIX)/config.json

check:
	sudo apt install python3-pip gir1.2-appindicator3-0.1
	pip3 install -r requirements.txt


debug: check
	python3 ./ldr-translate.py


install: check
	rm -rf cache

	mkdir -p $(PREFIX)/cache
	cp -r ui api ui_translate.py ldr-translate.py preferences.py config.json $(PREFIX)

	@echo "#!/bin/bash" > $(PREFIX)/lt.sh
	@echo "cd $(PREFIX)" >> $(PREFIX)/lt.sh
	@echo "nohup python3 ./ldr-translate.py &" >> $(PREFIX)/lt.sh
	chmod +x $(PREFIX)/lt.sh

	@echo "#!/bin/bash" > $(PREFIX)/ldr-translate
	@echo "$(PREFIX)/lt.sh" >> $(PREFIX)/ldr-translate
	chmod +x $(PREFIX)/ldr-translate
	mkdir -p $(HOME)/.local/bin

	sudo mkdir -p /usr/bin
	sudo ln -s $(PREFIX)/ldr-translate /usr/bin/ldr-translate


	mkdir -p $(DESKTOP)
	cp ldr-translate.desktop $(DESKTOP)
	@echo "Icon=$(PREFIX)/ui/icon.png" >> $(DESKTOP)/ldr-translate.desktop
	@echo "Exec=$(PREFIX)/lt.sh" >> $(DESKTOP)/ldr-translate.desktop

	rm -rf cache

	@echo "\n\n*****兰译app使用说明*****\n\n1. 软件安装位置：$(PREFIX)\n2. 终端输入 ldr-translate 即可运行\n3. 注销并重新登录以后，应用程序中应包含‘兰译’\n4. 复制即可自动翻译、显示主窗口\n5. 系统截图到剪贴板，自动OCR识别并翻译\n6. 更多教程见：https://github.com/yuhlzu/ldr-translate"


uninstall:
	mkdir -p ./cache
    ifeq ($(CONFIG), $(wildcard $(CONFIG)))
		cp $(CONFIG) ./cache/
    endif
	python3 -c "from api import config; config.old2new()"

	rm -rf $(PREFIX)
	rm -f $(DESKTOP)/ldr-translate.desktop
	rm -f $(HOME)/.local/bin/ldr-translate
	sudo rm -f /usr/bin/ldr-translate

reinstall: uninstall install

