
# 安装

建议使用 [自动打包](https://github.com/yuhldr/ldr-translate/releases/tag/%E8%87%AA%E5%8A%A8%E6%89%93%E5%8C%85) 的预览版，预览版并非不稳定，只是因为我懒得天天 release 更新

> `qt` 版本不是只能在 `kde` 桌面使用，`gtk` 版本也并不是只能在 `gnome` 桌面使用，都可以试试，`划词翻译` 目前仅支持 `gtk` 版本。

## archlinux系列

> 优先支持 `archlinux最新版`， manjaro 等支持 `pacman` 的系统大概也可以

> 已经发布在 `aur`，但是只包含 `稳定版`，而且 `aur` 在国内可能无法使用

### 离线安装

可以使用预览版，及时修复bugs

- 在 [github-release](https://github.com/yuhldr/ldr-translate/releases/) 下载 `.zst` 的安装包（包含 `gtk` 和 `qt` 两种）
- 然后在下载目录，右键，终端打开，终端输入：

    ```bash
    sudo pacman -U ./下载的zst文件名
    ```

### 在线安装

使用 `yay` 通过 `aur`，自动更新，但是只能使用稳定版

- qt版本：推荐 `kde` 桌面使用

    ```bash
    yay -S ldr-translate-qt
    ```

- gtk版本，推荐 `gnome` 桌面使用

    ```bash
    yay -S ldr-translate-gtk
    ```

`gnome` 桌面注意安装依赖 `gnome-shell-extension-appindicator`


## ubuntu 系列

> 优先支持 `ubuntu最新版`，其他支持 `deb` 的系统可能也可以用

> 注意，没有刻意适配 `wayland`，对于 `ubuntu22.04` 建议注销重新登录，输入密码前，右下角，选择 `xorg`

1. 在 [github-release](https://github.com/yuhldr/ldr-translate/releases/) 下载 `.deb` 的安装包（包含 `gtk` 和 `qt` 两种）

2. 然后在下载目录，右键，终端打开，终端输入：

    ```bash
    sudo apt install ./下载的deb文件名
    ```

3. 终端输入 `ldr` 或直接点击“兰译”图标即可运行

## fedora系列

> 优先支持 `fedora最新版`，centos、Rocky等其他 `rpm` 的系统可能也可以用

1. 在 [github-release](https://github.com/yuhldr/ldr-translate/releases/) 下载 `.rpm` 的安装包（包含 `gtk` 和 `qt` 两种）

2. 然后在下载目录，右键，终端打开，终端输入：

    - fedora

        ```bash
        sudo dnf install ./下载的rpm文件名
        ```
    - rocky、centos

        ```bash
        sudo yum install ./下载的rpm文件名
        ```


## 其他系统

一键编译：[看这里](md/build.md)
