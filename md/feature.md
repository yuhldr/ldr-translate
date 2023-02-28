# 功能

## 设置api

- `有道`：可以直接用，但是不稳定：
- `谷歌`：需要代理，请见 [常见问题](qa.md)
- `百度`：免费申请，填写api，[申请方式参见这里](https://doc.tern.1c7.me/zh/folder/setting/#百度)
- `腾讯`：免费申请，填写api，[申请方式参见这里](https://doc.tern.1c7.me/zh/folder/setting/#腾讯云)


## 常规设置

- 点击通知栏 `设置` 可以检查更新，可以开机自启，可以设置自己的百度腾讯api

- 通知栏图标颜色，设置中可以修改，但是重新打开才生效

|gtk|qt
|:-:|:-:|
![图片翻译](images/gtk3.png)|![图片翻译](images/qt3.png)


## 自动翻译

- 复制时自动翻译并弹出窗口。
- gtk版本支持划词翻译（仅x11窗口，gnome如 `ubuntu22.04` 注销重新登录输入密码时，右下角请选择xorg），不建议划词翻译，有时候有问题

|gtk|qt
|:-:|:-:|
![图片翻译](images/gtk2.png)|![图片翻译](images/qt2.png)

## 快捷键翻译

目前只是 `gtk` 版本做了简单的支持，使用方法

- 先复制准备翻译的文本或图片0（比如ctl-c）
- 然后 `Ctrl Alt M` 激发翻译

如果你要修改快捷键，直接编辑配置文件，注意是 `json` 文件

> 非常不建议修改这个文件，容易出问题！请 `提前备份` 这个文件，或者如果出问题，请删除这个文件，然后重新添加 `api` 密钥

- 打开 `~/.config/ldr-translate/config.json` 文件，建议 [vscode](https://code.visualstudio.com/) 等支持 `json` 高亮的编辑器打开，如果安装了 [vscode](https://code.visualstudio.com/)，可以使用下面的命令

    ```bash
    code ~/.config/ldr-translate/config.json
    ```

- 以 vscode 打开为例，可以右键选择 `格式化`，方便编辑
- 然后在 `setting` 中添加键值对 `,"key_gtk": "<Ctrl><Alt>M"`，其中 `<Ctrl><Alt>M`  是你准备的快捷键，修改后如图
- `完全退出` 兰朵儿，重新打开
    > 注意，如果没有生效，大概率是因为你的快捷键与系统中其他快捷键 `冲突`，或者 `config.json`文件编写错误，比如 `"key_gtk"` 前面要有个英文逗号 `,`

    ![快捷键t](images/config-gtk-key.png)

## 图片翻译

截图到系统剪贴板，会自动识别并翻译

默认支持百度ocr在线翻译，设置中可以修改为离线翻译，但是离线翻译

- 安装依赖 `pip3 install easyocr`
- 首次识别，极慢

为了方便将 `ubuntu22.04` 系统设置的快捷键，修改为一个自己习惯的。

![图片翻译](images/ocr.png)


## 修改编辑

可以修改复制或者OCR的内容，然后点击左上角刷新按钮，重新翻译

## 追加模式

有时候一句话在文献里分成上下两页，复制半句翻译有问题，这时候勾选 `追加模式`，接下来复制的内容，会和前一次的复制内容，一起翻译
