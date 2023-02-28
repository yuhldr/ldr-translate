# 手动安装

可以手动编译安装，以 `opensuse` 为例，

1. 下载源码，解压，打开终端，进入解压以后的文件夹

2. 安装编译软件 make

    ```bash
    sudo zypper in make
    ```

3. 安装依赖并安装

    - 可以安装 `qt` 版本
  
        > `make check-qt` 是在检查部分 `python` 依赖

        ```bash
        make check-qt && make build && make qt && make install
        ```

    - 也可以安装 `gtk` 版本

        > `make check-gtk` 是在检查部分 `python` 依赖

        ```bash
        make check-gtk && make build && make gtk && make install
        ```

4. 请自己检查依赖问题：

> 不同系统在软件名有差别

   - qt版本：
      - python3
      - python3-requests
      - python3-pyqt5

   - gtk版本
      - python3
      - python3-requests
      - python3-gi
      - gnome-shell-extension-appindicator
      - gir1.2-appindicator3-0.1 或 gir1.2-ayatanaappindicator3-0.1
      - gir1.2-keybinder-3.0

如果遇到问题，请查看 [已知问题](qa.md)