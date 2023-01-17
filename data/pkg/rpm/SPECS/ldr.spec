%define Name ldr-translate
%define _topdir %(echo $PWD)/..

Name:     %{Name}-PKG_TYPE
Version:
Release: 1
Summary:  一个非常好用的翻译软件，看文献的好帮手
Summary(zh_CN):  一个非常好用的翻译软件，看文献的好帮手
License:  GPLv3+
URL:      https://github.com/yuhldr/%{Name}
Requires:

%description
翻译软件

%description -l zh_CN
一个非常好用的翻译软件，专注于文献翻译，可以复制翻译、截图翻译，支持百度、腾讯等翻译接口


%files
/opt/%{Name}
/usr/bin/ldr
/usr/share/applications/%{Name}.desktop
/usr/share/icons/%{Name}.png


%install
cp -r %{_builddir}/%{Name}/* %{buildroot}
