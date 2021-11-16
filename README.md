# 兰译

 <img src="ui/icon.png" width = "36" height = "36" alt="图片名称" align=center />
一个ubuntu的翻译软件，使用Gtk3开发，python语言，翻译用的百度接口

> 已打包deb，经测试ubuntu20.04可以安装，ubuntu 21.10使用gnome4，无法使用该项目，未来会适配

- 复制文本自动翻译(可划词翻译)
- 截图自动识别、并翻译
- 可选追加复制
- 可修改复制内容，重新翻译
- 多语言互译支持，自动识别当前语言
- 设置中自定义接口账号
- （待完善）支持多平台api接口，目前仅支持百度api，足够了……
- 页面随着系统主题（gnome）自动变化

|系统默认主题 yaru-dark|第三方主题layan|第三方主题kimi-dark|
|:-:|:-:|:-:|
![主题2](images/lt.png)|![主题1](images/lt-layan.png)|![主题1](images/lt-kimi.png)

## 安装

在 releases下载`.deb` 的安装包，只有23kb

- [gitee 国内](https://gitee.com/yuhldr/ldr-translate/releases)
- [github 国外](https://github.com/yuhldr/ldr-translate/releases/)

然后在下载目录，右键，终端打开，终端输入如下：

```sh
sudo dpkg -i ./下载的deb文件名

# 如果报错，输入下面的
# 因为此软件依赖：gir1.2-appindicator3-0.1，后续将尽可能摆脱此依赖
# https://packages.debian.org/buster/gir1.2-appindicator3-0.1

sudo apt install -f

# 再安装
sudo dpkg -i ./下载的deb文件名

# 终端输入 ldr 或直接点击“兰译”图标即可运行
# 如果翻译过程中出现错误，请安装python3依赖库requests（目前测试无需安装）
```

> 卸载

```bash
sudo apt remove ldr-translate -y
```

## 其他

> 希望一起完善 snap 打包和 ppa 发布，可联系 yuhldr@qq.com

- snap打包，一直失败，如果您熟悉snap，希望一起完善
- ppa 发布，我设置了，但是不熟悉，目前未能完成

## API账号

翻译页面左上角，可以设置百度的翻译API以及图片识别API，默认账号用的人太多，容易报错

|设置|百度api设置|
|:-:|:-:|
![设置](images/prf_api.png)|![百度api设置](images/api_baidu.png)|

## 功能

运行以后，弹出翻译窗口，自动置顶窗口，5大功能

1. 自动翻译
  
    复制时自动翻译。如需划词翻译，[config.json](./config.json) 里修改 `"translate_way_copy": false,`，不建议划词翻译，有时候有问题

    ![运行](images/lt_more.png)

2. 图片翻译
  
    截图到系统剪贴板，会自动识别并翻译，为了方便将ubuntu2004系统设置的快捷键，修改为一个自己习惯的。

    ![图片翻译](images/ocr.png)

3. 窗口置顶

    复制时自动弹出窗口，并置顶，可常驻后台，可暂停翻译

    ![图片翻译](images/lt_menu.png)

4. 修改编辑

    可以修改复制或者OCR的内容，然后点击右上角重新翻译

5. 追加模式

    有时候一句话在文献里分成上下两页，复制半句翻译有问题，这时候勾选 `追加模式`，接下来复制的内容，会和前一次的复制内容，一起翻译

## 资料

- [Python Gtk+3 API &#xB7; Python GTK+ 3 API](https://athenajc.gitbooks.io/python-gtk-3-api/content/)

- [Welcome to big-doc’s documentation! &mdash; big-doc 0.1 documentation](https://thebigdoc.readthedocs.io/en/latest/index.html)

- [The Python GTK+ 3 Tutorial &mdash; Python GTK+ 3 Tutorial 3.4 documentation](https://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html)
- [linux下deb包的管理及制作 | 一次成功 - Marathon-Davis - 博客园](https://www.cnblogs.com/davis12/p/14365981.html)

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
