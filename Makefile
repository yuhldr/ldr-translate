PREFIX=$(HOME)/.local/share/ldr-translate
DESKTOP=$(HOME)/.local/share/applications

check:
	sudo apt install gir1.2-keybinder-3.0 python3-pip
	pip3 install -r requirements.txt


debug: check
	python3 ./ldr-translate.py


install: check
	mkdir -p $(PREFIX)/data
	cp -r ui api ui_translate.py config.py ldr-translate.py $(PREFIX)

	echo "#!/bin/bash" > $(PREFIX)/lt.sh
	echo "cd $(PREFIX)" >> $(PREFIX)/lt.sh
	echo "nohup python3 ./ldr-translate.py &" >> $(PREFIX)/lt.sh
	chmod +x $(PREFIX)/lt.sh

	mkdir -p $(HOME)/.local/bin
	echo "#!/bin/bash" > $(HOME)/.local/bin/ldr-translate
	echo "$(PREFIX)/lt.sh" >> $(HOME)/.local/bin/ldr-translate
	chmod +x $(HOME)/.local/bin/ldr-translate

	mkdir -p $(DESKTOP)
	cp ldr-translate.desktop $(DESKTOP)
	echo "Icon=$(PREFIX)/ui/icon.png" >> $(DESKTOP)/ldr-translate.desktop
	echo "Exec=$(PREFIX)/lt.sh" >> $(DESKTOP)/ldr-translate.desktop

	echo "\n\n*****兰译app使用说明*****\n\n1. 软件安装位置：$(PREFIX)\n2. 终端输入 ldr-translate 即可运行\n3. 注销并重新登录以后，应用程序中应包含‘兰译’\n4. 复制即可自动翻译、Alt Q快捷键自动隐藏/显示主窗口\n5. 系统截图并复制到剪贴板，自动OCR识别并翻译\n6. 更多教程见：https://github.com/yuhlzu/ldr-translate"


uninstall:
	rm -rf $(PREFIX)
	rm -f $(DESKTOP)/ldr-translate.desktop
	rm -f $(HOME)/.local/bin/ldr-translate

reinstall: uninstall install