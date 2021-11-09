PREFIX=$(HOME)/.local/share/ldr-translate



debug:
	pip3 install -r requirements.txt
	python3 ./ldr-translate.py

install:
	pip3 install -r requirements.txt

	mkdir -p $(PREFIX)	
	cp main.py $(PREFIX)
	cp config.py $(PREFIX)
	cp ldr-translate.py $(PREFIX)
	cp -r ui $(PREFIX)
	cp -r api $(PREFIX)

	echo "#!/bin/bash" > $(PREFIX)/lt.sh
	echo "cd $(PREFIX)" >> $(PREFIX)/lt.sh
	echo "nohup python ./ldr-translate.py &" >> $(PREFIX)/lt.sh
	chmod +x $(PREFIX)/lt.sh

	mkdir -p $(HOME)/.local/bin
	echo "#!/bin/bash" > $(HOME)/.local/bin/ldr-translate
	echo "$(PREFIX)/lt.sh" >> $(HOME)/.local/bin/ldr-translate
	chmod +x $(HOME)/.local/bin/ldr-translate

	mkdir -p $(HOME)/.local/share/applications
	cp ldr-translate.desktop $(HOME)/.local/share/applications/
	echo "Icon=$(PREFIX)/ui/icon.png" >> $(HOME)/.local/share/applications/ldr-translate.desktop

uninstall:
	rm -rf $(PREFIX)
	rm -f $(HOME)/.local/share/applications/ldr-translate.desktop
	rm -f $(HOME)/.local/bin/ldr-translate

reinstall: uninstall install