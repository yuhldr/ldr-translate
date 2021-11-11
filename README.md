# 兰译

 <img src="ui/icon.png" width = "36" height = "36" alt="图片名称" align=center />
一个ubuntu的翻译软件，使用Gtk3开发，python语言，翻译用的百度接口

目前没打包，直接 `make install` 即可

- 复制文本自动翻译
- 可划词翻译
- 可选追加复制
- 可修改复制内容，重新翻译
- 截图自动识别、并翻译
- 多语言互译支持，自动识别当前语言
- （待完善）支持多平台api接口，目前仅支持百度api，足够了……
- （待完善）设置中自定义接口账号
- 页面随着系统主题（gnome）自动变化

|系统默认主题 yaru|第三方主题layan|第三方主题kimi|
|:-:|:-:|:-:|
![主题2](images/lt.png)|![主题1](images/lt-layan.png)|![主题1](images/lt-kimi.png)

## 账号

在 [config.py](./config.py) 里面填写，里面目前有一个，是我自己的的密钥，用的人多了就会翻译失败，建议用自己的

### 百度翻译api

每秒钟一个账号只能翻译一次，建议用自己的

> 百度翻译api怎么获取，[点我，看这里，这个链接如果打不开，百度怎么获取](https://ripperhe.gitee.io/bob/#/service/translate/baidu)

### 百度图片识别api

OCR图片识别并翻译，按照下面的教程修改为自己的，一个人一月1000次，企业认证的话5万次，所以能复制的，不要OCR

> 百度图片识别api怎么获取，[点我，看这里，这个链接如果打不开，百度怎么获取](https://cloud.baidu.com/doc/OCR/s/dk3iqnq51)

## 测试与安装

> 确保安装的有 `make3`

### 测试

临时测试的话，可以在当前目录，运行 [ldr-translate.py](./ldr-translate.py) 文件，或者直接如下

```sh
make debug
```

运行以后，弹出翻译窗口，自动置顶窗口，5大功能

1. 自动翻译
  
    复制时自动翻译。如需划词翻译，[config.py](./config.py) 里修改 `translate_select=True`，不建议划词翻译，有时候有问题

    ![运行](images/lt_more.png)

2. 图片翻译
  
    使用系统的截图，截图到剪贴版，会自动识别并翻译，为了方便将ubuntu2004系统设置的快捷键，修改为一个自己习惯的。

    ![图片翻译](images/ocr.png)

3. 窗口置顶

    复制时自动弹出窗口，并置顶，可常驻后台，可暂停翻译

    ![图片翻译](images/lt_menu.png)

4. 修改编辑

    可以修改复制或者OCR的内容，然后点击右上角重新翻译

5. 追加模式

    有时候一句话在文献里分成上下两页，复制半句翻译有问题，这时候点击左上角 `追加`，接下来复制的内容，会和前一次的复制内容，一起翻译

### 安装

> sudo权限仅为创建链接、核对依赖

```bash
# 安装路径为 `$(HOME)/.local/share/ldr-translate`
make install
```

终端输入

```bash
# 如果无反应，注意 `/usr/bin` 是否在环境变量中
ldr-translate
```

或者直接找到 `兰译` 图标 
 <img src="ui/icon.png" width = "36" height = "36" alt="图片名称" align=center />，点击即可运行

> 大概需要注销当前用户重新登录，才可以看到图标，不懂什么意思的话，直接重启……

### 卸载

```bash
make uninstall
```

### 重装、更新

```bash
make reinstall
```

## 资料

- [Python Gtk+3 API &#xB7; Python GTK+ 3 API](https://athenajc.gitbooks.io/python-gtk-3-api/content/)

- [Welcome to big-doc’s documentation! &mdash; big-doc 0.1 documentation](https://thebigdoc.readthedocs.io/en/latest/index.html)

- [The Python GTK+ 3 Tutorial &mdash; Python GTK+ 3 Tutorial 3.4 documentation](https://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html)

## 其他

python直接打包，体积有点大，不到1M的东西，它给打包了100多M……

```bash
#建立虚拟环境
pipenv install
#进入虚拟环境（上一步可省略,因为没有虚拟环境的话会自动建立一个）
pipenv shell
#安装模块
pip install requests pyquery pysimplegui fake_useragent
#打包的模块也要安装
pip install pyinstaller
#开始打包
pyinstaller -F  ./ldr-translate.py 
```