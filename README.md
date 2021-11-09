# 兰译

一个ubuntu的翻译软件，使用Gtk3开发，python语言，翻译用的百度接口

目前没打包，直接 `make install` 即可

- 复制文本自动翻译
- 可划词翻译
- 可选追加复制
- 可修改复制内容，重新翻译
- （待完善）截图自动识别、并翻译
- （待完善）多语言互译支持，目前仅支持其他语言翻译为中文

![运行](images/lt.png)

## 账号

添加自己的百度翻译api，在 [config.py](./config.py) 里面填写，里面目前有一个，是我自己的的密钥，用的人多了就会翻译失败，建议用自己的

> 百度翻译api怎么获取，[点我，看这里，这个链接如果打不开，百度怎么获取](https://ripperhe.gitee.io/bob/#/service/translate/baidu)


## 测试与安装

> 确保安装的有 `make3`

### 测试

临时测试的话，可以在当前目录，运行 [ldr-translate.py](./ldr-translate.py) 文件

```sh
make debug
```

运行以后，弹出翻译窗口，自动置顶窗口，4大功能

- 复制时自动翻译，如需划词翻译，[config.py](./config.py) 里修改 `translate_select=True`，不建议划词翻译，有时候有问题
- `Alt Q` 快捷键，隐藏翻译窗口，再次快捷键，显示
- 可以修改，然后点击右上角重新翻译
- 左上角`追加`点击以后，接下来复制的内容，会和前一次的复制内容，一起翻译

![运行](images/lt_more.png)

### 安装

```bash
# 安装路径为 `$(HOME)/.local/share/ldr-translate`
make install
```

终端输入

```bash
# 如果无反应，注意 `~/.local/bin` 是否在环境变量中
ldr-translate
``` 

或者直接找到 `兰译` 图标，点击即可运行
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

- [Welcome to big-doc’s documentation! &mdash; big-doc 0.1 documentation](https://thebigdoc.readthedocs.io/en/latest/index.html)

- [The Python GTK+ 3 Tutorial &mdash; Python GTK+ 3 Tutorial 3.4 documentation](https://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html)