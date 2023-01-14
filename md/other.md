# 其他

## 资料

- [indicator-sysmonitor](https://github.com/fossfreedom/indicator-sysmonitor)

- [Python Gtk+3 API &#xB7; Python GTK+ 3 API](https://athenajc.gitbooks.io/python-gtk-3-api/content/)

- [Welcome to big-doc’s documentation! &mdash; big-doc 0.1 documentation](https://thebigdoc.readthedocs.io/en/latest/index.html)

- [The Python GTK+ 3 Tutorial &mdash; Python GTK+ 3 Tutorial 3.4 documentation](https://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html)
- [linux下deb包的管理及制作 | 一次成功 - Marathon-Davis - 博客园](https://www.cnblogs.com/davis12/p/14365981.html)
- [iconfont-阿里巴巴矢量图标库](https://www.iconfont.cn/)
- [ArchLinux aur打包简易指南](https://segmentfault.com/a/1190000010991745)

## 开发工具

- 功能开发：vscode
- ui开发：glade
- deb打包方法：见 Makefile: `make build`

  - control，用了记录软件标识，版本号，平台，依赖信息等数据，这是最主要的文件配置，必不可少；
  - preinst，在解包data.tar.gz 前运行的脚本；
  - postinst，在解包数据后运行的脚本；
  - prerm，卸载时，在删除文件之前运行的脚本；
  - postrm，在删除文件之后运行的脚本；在 Cydia 系统中，Cydia 的作者 Saurik 另外- 添加了一个脚本，extrainst_，作用与 postinst 类似。
  - copyright文件: 不用说，版权信息，相当重要
  - changelog文件: 这是一个必需文件(ppa必须，此处打包不需要)，包含软件版本号，修订号，发行版和优先级。
  - rules文件: 这实际上是另外一个Makefile脚本，用来给dpkg-buildpackage用的.
  - compat文件: 这个文件留着是有用的
  - dirs文件：这个文件指出我们需要的但是在缺省情况下不会自动创建的目录

