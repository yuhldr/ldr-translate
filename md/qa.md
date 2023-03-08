# 已知问题

> 没有刻意适配 `wayland` 版本，可能存在各种神奇问题。建议注销，重新登录输入密码前，右下角，选择 `xorg`

软件分为 `qt` 和 `gtk` 两个版本，依赖如下（以 `ubuntu22.04` 为例）

- `python3`
- `python3-requests`
- `python3-cryptography`

对于 `qt` 版本，额外需要

  - `python3-pyqt5`

对于 `gtk` 版本，如果是 `gnome` 桌面

- `gnome-shell-extension-appindicator`
- `gir1.2-appindicator3-0.1` 或 `gir1.2-ayatanaappindicator3-0.1`
- `gir1.2-keybinder-3.0`
- `python3-gi`


## 每次复制都翻译很烦人

菜单栏，可以选择，暂不翻译

gtk|qt
:-:|:-:
![图片翻译](images/gtk2.png)|![图片翻译](images/qt2.png)


## 部分系统打开无反应

先排查：终端输入 `ldr`，一般是依赖问题

- 对于 `gtk` 版本

    以 `ubuntu22.04` 为例

    ```bash
    sudo apt install gnome-shell-extension-appindicator gir1.2-appindicator3-0.1 python3 python3-gi python3-requests
    ```
    
    `python3-gi` 对于其他系统：[点我，看这里](https://pygobject.readthedocs.io/en/latest/getting_started.html#ubuntu-getting-started)

- 对于 `qt` 版本

    ```bash
    sudo apt install python3 python3-pyqt5 python3-requests
    ```

    后期可能需要 `pyQt6`


## 状态栏看不到兰朵儿图标（T）

因为最新版 `gnome` 40 默认不显示菜单，需要安装软件 [gnome-shell-extension-appindicator](https://github.com/ubuntu/gnome-shell-extension-appindicator)

- `ubuntu 22.04`

    ```bash
    sudo apt install gnome-shell-extension-appindicator
    ```

- `archlinux` 的 `gnome` 桌面环境

    ```bash
    sudo pacman -S gnome-shell-extension-appindicator
    ```

其他系统自己百度

## qt版本，使用fcitx输入法的用户，无法输入中文

以 `archlinux-2022-05-25` 为例，注意当前python为 `python3.10`

```bash
ln -s /usr/lib/qt/plugins/platforminputcontexts/libfcitxplatforminputcontextplugin.so ~/.local/lib/python3.10/site-packages/PyQt5/Qt5/plugins/platforminputcontexts/
```

重新打开兰朵儿即可


## 复制以后，鼠标移动到兰译，才能翻译

ubuntu22.04

- 方法一：请不要使用 `wayland` 方式登录，登录输入密码前，右下角，选择 `xorg`
- 方法二：使用 `qt` 版本（注意， `qt` 版本在  `wayland` 环境也存在一些神奇问题）


## 安装以后找不到图标

点键盘 `window图标`，然后在系统搜索里，输入 `ldr`，即可看到 `兰译`

## 谷歌没法用

最近需要代理，百度解决，有代理的，看下面的


## 需要使用代理

修改 `/usr/bin/ldr` 文件

当前为：

```bash
#!/bin/bash
# export http_proxy="http://127.0.0.1:7890"
# export https_proxy="http://127.0.0.1:7890"
cd /opt/ldr-translate && python3 main.py
```

其中 `http://127.0.0.1:7890` 修改为你自己的代理链接

注意去掉这两行前面 `#` 的注释

## 软件页面并不好看

请按照如下自行百度

- 如果是在 `gnome` 桌面（如ubuntu22.04）使用 `gtk` 版本，总是白灰色

    搜索：`ubuntu22.04 主题美化`

    注意，不同版本的ubuntu不一样，以前好像不叫这个名字：`gnome-tweaks`，


- 如果在 `gnome` 桌面（如ubuntu22.04）安装了 `qt` 版本

    > 注意：`qt` 版本只推荐在 `kde` 桌面环境

    搜索：`gnome主题如何适配qt软件`

    好像用到这个软件：`qt5ct`，可以参考 [这里](https://www.jianshu.com/p/f4dff8ccea86)：

- 如果是在 `kde` 桌面，使用了 `gtk` 版本（此桌面环境不推荐此版本）

    > 注意：`gtk` 版本只推荐在 `gnome` 桌面环境

    搜索：`kde桌面如何为gtk软件设置主题`
