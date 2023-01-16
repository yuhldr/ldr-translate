# 兰译 <img src="data/icon/icon.png" width = "36" height = "36" alt="图片名称" align=center />

 一个翻译软件，使用Gtk3开发（最近开发了QT版本），python语言，翻译用的百度、腾讯接口

## 特点

- 界面美观、依赖少，可 `复制翻译`、`划词翻译`，小白也能用
- 优先支持 `ubuntu22.04`、`archlinux`，含 `gnome` 和 `kde` 两种桌面环境（其他系统理论上也能用）
- 支持 `百度` `腾讯` 两个翻译平台

|版本|翻译页面|状态栏菜单|设置
|:-:|:-:|:-:|:-:|
gtk版本|![gtk1](md/images/gtk1.png)|![gtk2](md/images/gtk2.png)|![gtk3](md/images/gtk3.png)
qt版本|![qt1](md/images/qt1.png)|![qt2](md/images/qt2.png)|![qt3](md/images/qt3.png)



## 安装

- archlinux 或 manjaro 系统 等支持 `pacman` 的系统
  
  > 已经发布在 `aur`，但是只包含 `稳定版`，而且 `aur` 在国内可能无法使用

     1. 离线安装

          可以使用预览版，及时修复bugs

        - 在 [github-release](https://github.com/yuhldr/ldr-translate/releases/) 下载 `.zst` 的安装包（包含 `gtk` 和 `qt` 两种）
        - 然后在下载目录，右键，终端打开，终端输入：

          ```bash
          sudo pacman -U ./下载的zst文件名
          ```

     2. 在线安装

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


- ubuntu22.04 或其他支持 `deb` 的系统

    > 注意，没有刻意适配 `wayland`，对于 `ubuntu22.04` 建议注销重新登录，输入密码前，右下角，选择 `xorg`

   1. 在 [github-release](https://github.com/yuhldr/ldr-translate/releases/) 下载 `.deb` 的安装包（包含 `gtk` 和 `qt` 两种）

   2. 然后在下载目录，右键，终端打开，终端输入：

        ```bash
        sudo dpkg -i ./下载的deb文件名
        ```

   3. 如果报错，输入：

        ```bash
        sudo apt install -f
        ```

   4. 再安装（这一步或许可以省略）

        ```bash
        sudo dpkg -i ./下载的deb文件名
        ```

   5. 终端输入 `ldr` 或直接点击“兰译”图标即可运行


- centos、Rocky、fedora等支持 `rpm` 的系统

     > 注意，没有刻意适配依赖问题，可以看下面常见问题，里面有相关的依赖说明

   1. 在 [github-release](https://github.com/yuhldr/ldr-translate/releases/) 下载 `.deb` 的安装包（包含 `gtk` 和 `qt` 两种）

   2. 然后在下载目录，右键，终端打开，终端输入：

     - fedora

        ```bash
        sudo dnf install ./下载的rpm文件名
        ```
     - rocky、centos

        ```bash
        sudo dnf -i ./下载的rpm文件名
        ```


- 其他系统 [看这里](md/build.md)

## 常见问题

[看这里](md/qa.md)


## 使用说明

[看这里](md/feature.md)


## 其他

[开发资料看这里](md/other.md)

> 希望一起完善 snap 打包和 ppa 发布，可联系 yuhldr@qq.com

- snap打包，一直失败，如果您熟悉snap，希望一起完善
- ppa 发布，我设置了，但是不熟悉，目前未能完成


## Sponsor
The project is develop by [JetBrains Ide](https://www.jetbrains.com/?from=puck)

[![](https://www.jetbrains.com/company/brand/img/logo1.svg)](https://www.jetbrains.com/?from=puck)
