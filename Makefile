VERSION_NAME=1.7.1
VERSION_CODE=17
NAME=ldr-translate
PREFIX=/opt
APP_PATH=/opt


snap:
	mkdir -p build/snap/$(NAME)/

	cp -r ui api ui_translate.py ldr-translate.py preferences.py config.json build/snap/$(NAME)

	cp debian/ldr build/snap/$(NAME)/
	@echo "cd $(APP_PATH)/$(NAME)/" >> build/snap/$(NAME)/ldr
	@echo "python3 ./ldr-translate.py" >> build/snap/$(NAME)/ldr

	cp snapcraft.yaml build/snap


build:
	mkdir -p disk
	mkdir -p build/$(NAME)/usr/bin
	mkdir -p build/$(NAME)/usr/share/applications
	mkdir -p build/$(NAME)/usr/share/icons
	mkdir -p build/$(NAME)$(APP_PATH)/$(NAME)

	cp data/ldr build/$(NAME)/usr/bin/

	cp data/icon/icon.png build/$(NAME)/usr/share/icons/$(NAME).png
	cp data/$(NAME).desktop build/$(NAME)/usr/share/applications/

	cp -r utils api data/icon data/config.json data/version.json data/locales build/$(NAME)$(APP_PATH)/$(NAME)/

	sed -i "/code/s/:\s*[0-9]*,/: $(VERSION_CODE),/g" build/$(NAME)$(APP_PATH)/$(NAME)/version.json
	sed -i "/name/s/[0-9]\.[0-9]\.[0-9]/$(VERSION_NAME)/g" build/$(NAME)$(APP_PATH)/$(NAME)/version.json

	find build/$(NAME) -name "*.pyc" -type f -delete


gtk:
	mkdir -p build/gtk/
	cp -r build/$(NAME) build/gtk/
	cp gui/gtk/*.ui build/gtk/$(NAME)$(APP_PATH)/$(NAME)/
	cp gui/gtk/*.py build/gtk/$(NAME)$(APP_PATH)/$(NAME)/

qt:
	mkdir -p build/qt/
	cp -r build/$(NAME) build/qt/
	cp gui/qt/*.py build/qt/$(NAME)$(APP_PATH)/$(NAME)/


install: uninstall
	sudo mkdir -p /usr/bin/
	sudo mkdir -p /usr/share/icons/
	sudo cp -r ./build/$(NAME)$(PREFIX)/$(NAME) $(PREFIX)/
	sudo cp build/$(NAME)/usr/bin/* /usr/bin/
	sudo cp build/$(NAME)/usr/share/icons/* /usr/share/icons/
	sudo cp build/$(NAME)/usr/share/applications/* /usr/share/applications/


deb-gtk:
	mkdir -p build/deb/
	cp -r build/gtk build/deb/

	mkdir -p build/deb/gtk/$(NAME)/DEBIAN
	cp data/pkg/debian/* build/deb/gtk/$(NAME)/DEBIAN/

	cd build/deb/gtk/$(NAME)/DEBIAN/ && \
	sed -i "s/^version:/version: $(VERSION_NAME)/g" ./control && \
	sed -i "s/^Depends:/Depends: gir1.2-appindicator3-0.1,python3,python3-gi,python3-requests/g" ./control

	cd build/deb/gtk && \
	dpkg -b $(NAME) $(NAME)-gtk.deb

	cp build/deb/gtk/$(NAME)-gtk.deb disk/$(NAME)-gtk-$(VERSION_NAME).deb


deb-qt:
	mkdir -p build/deb/
	cp -r build/qt/ build/deb/

	mkdir -p build/deb/qt/$(NAME)/DEBIAN
	cp data/pkg/debian/* build/deb/qt/$(NAME)/DEBIAN/

	cd build/deb/qt/$(NAME)/DEBIAN/ && \
	sed -i "s/^version:/version: $(VERSION_NAME)/g" ./control && \
	sed -i "s/^Depends:/Depends: python3,python3-pyqt5,python3-requests/g" ./control

	cd build/deb/qt && \
	dpkg -b $(NAME) $(NAME)-qt.deb

	cp build/deb/qt/$(NAME)-qt.deb disk/$(NAME)-qt-$(VERSION_NAME).deb


aur-gtk:
	mkdir -p build/aur/gtk

	cd build/aur/gtk && \
	cp ../../../data/pkg/aur/PKGBUILD ./ && \
	sed -i "s/^pkgname=/pkgname=$(NAME)-gtk/g" PKGBUILD && \
	sed -i "s/^pkgver=/pkgver=$(VERSION_NAME)/g" PKGBUILD && \
	sed -i "s/^depends=()/depends=(python python-requests python-gobject libappindicator-gtk3)/g" PKGBUILD  && \
	sed -i "s/^optdepends=()/optdepends=(gnome-shell-extension-appindicator)/g" PKGBUILD  && \
	sed -i "s/^conflicts=()/conflicts=($(NAME)-qt)/g" PKGBUILD  && \
	sed -i "s#PKG_PATH#\$(shell pwd)/build/gtk#g" PKGBUILD  && \
	sed -i "s/PKG_TYPE/gtk/g" PKGBUILD  && \
	makepkg -f
	cp build/aur/gtk/*.zst disk/

aur-qt:
	mkdir -p build/aur/qt

	cd build/aur/qt && \
	cp ../../../data/pkg/aur/PKGBUILD ./ && \
	sed -i "s/^pkgname=/pkgname=$(NAME)-qt/g" PKGBUILD && \
	sed -i "s/^pkgver=/pkgver=$(VERSION_NAME)/g" PKGBUILD && \
	sed -i "s/^depends=()/depends=(python python-requests python-pyqt5)/g" PKGBUILD && \
	sed -i "s/^conflicts=()/conflicts=($(NAME)-gtk)/g" PKGBUILD && \
	sed -i "s#PKG_PATH#\$(shell pwd)/build/qt#g" PKGBUILD  && \
	sed -i "s/PKG_TYPE/qt/g" PKGBUILD  && \
	makepkg -f
	cp build/aur/qt/*.zst disk/

rpm-gtk:
	mkdir -p build/rpm/gtk/BUILD
	cp -r build/gtk/$(NAME) build/rpm/gtk/BUILD/

	cd build/rpm/gtk && \
	cp -r ../../../data/pkg/rpm/SPECS ./ && \
	cd SPECS && \
	sed -i "s/PKG_TYPE/gtk/g" ldr.spec && \
	sed -i "s/^Version:/Version: $(VERSION_NAME)/g" ldr.spec && \
	sed -i "s/^Requires:/Requires: python3 python3-requests python3-gobject libappindicator-gtk3/g" ldr.spec && \
	rpmbuild -bb ldr.spec

	cp build/rpm/gtk/RPMS/x86_64/*.rpm disk/


rpm-qt:
	mkdir -p build/rpm/qt/BUILD
	cp -r build/qt/$(NAME) build/rpm/qt/BUILD/

	cd build/rpm/qt && \
	cp -r ../../../data/pkg/rpm/SPECS ./ && \
	cd SPECS && \
	sed -i "s/PKG_TYPE/qt/g" ldr.spec && \
	sed -i "s/^Version:/Version: $(VERSION_NAME)/g" ldr.spec && \
	sed -i "s/^Requires:/Requires: python3 python3-requests python3-qt5/g" ldr.spec && \
	rpmbuild -bb ldr.spec

	cp build/rpm/qt/RPMS/x86_64/*.rpm disk/

all:
	make clear
	make build
	make gtk
	make deb-gtk
	make aur-gtk
	make rpm-gtk
	make qt
	make deb-qt
	make aur-qt
	make rpm-qt


uninstall:
	sudo rm -rf $(PREFIX)/$(NAME)
	sudo rm -rf /usr/bin/ldr /usr/share/icons/$(NAME).png /usr/share/applications/$(NAME).desktop ~/.config/autostart/$(NAME).desktop


clear:
	rm -rf ./build
	rm -rf ./test*
	rm -rf ./tempCodeRunnerFile*



check-gtk:
	pip3 install requests PyGObject

check-qt:
	pip3 install requests PyQt5


.PHONY:build