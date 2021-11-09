# 兰译

一个ubuntu的翻译软件，使用Gtk3开发，python语言

## 账号

添加自己的百度翻译api，在 [config.py](./config.py) 里面填写，百度翻译api怎么获取，自己百度

> 里面有一个，是我自己的的密钥，用的人多了就会翻译失败，建议用自己的

## 依赖

> 使用gtk3、python开发，非ubuntu系统可能也能用，ubuntu使用很方便，安装python相关依赖即可，如下

```bash
pip install -r requirements.txt
```

## 运行

> 测试环境 `ubuntu20.04`

```bash
./run.sh
```

临时测试的话，可以在当前目录，运行 [ldrTranslate.py](./ldrTranslate.py) 文件

![运行](images/lt_more.png)

## 翻译

运行以后，弹出翻译窗口，自动置顶窗口，4大功能

- 复制时自动翻译，如需划词翻译，[config.py](./config.py) 里修改 `translate_select=True`
- `Alt Q` 快捷键，隐藏翻译窗口，再次快捷键，显示
- 可以修改，然后点击右上角重新翻译
- 左上角`追加`点击以后，接下来复制的内容，会和前一次的复制内容，一起翻译

![运行](images/lt.png)

## 资料

- [Welcome to big-doc’s documentation! &mdash; big-doc 0.1 documentation](https://thebigdoc.readthedocs.io/en/latest/index.html)

- [The Python GTK+ 3 Tutorial &mdash; Python GTK+ 3 Tutorial 3.4 documentation](https://python-gtk-3-tutorial.readthedocs.io/en/latest/index.html)