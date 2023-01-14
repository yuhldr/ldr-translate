# 手动安装

可以手动编译安装，以opensuse为例，

1. 下载源码，解压，打开终端，进入解压以后的文件夹

2. 安装编译软件 make

    ```bash
    sudo zypper in make
    ```

3. 安装依赖并安装

    - 可以安装 `qt` 版本

        ```bash
        make check-qt && make qt && make install
        ```

    - 也可以安装 `gtk` 版本

        ```bash
        make check-qt && make qt && make install
        ```

如果遇到问题，请查看 [已知问题](qa.md)