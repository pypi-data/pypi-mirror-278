# Send S3

跨平台的对象存储上传工具

 - 支持 Windows、Linux、MacOS
 - 可以用于图片上传（图床）、文件分享等
 - 带有日志记录功能，可以查看上传历史
 - 支持通过系统自带的工具快速上传文件（Windows：「发送到」；MacOS：「快捷指令」）


## 安装
我们推荐使用 [pipx](https://pypa.github.io/pipx/) 安装 Send S3，请参见其官网来安装 pipx。

```bash
# 安装方法 1：使用 pipx 安装 (推荐)
pipx install send-s3

# 安装方法 2：使用 pip 安装
pip3 install send-s3
```

## 使用
安装完成后，请运行初始化命令：

```bash
send-s3 init
```

初始化命令会创建应用目录：
 - Windows：`%APPDATA%\send-s3`
 - MacOS / Linux：`$XDG_CONFIG_HOME/.config/send-s3` 或 `~/.config/send-s3`

请确保 `config.toml` 文件存在于应用目录中，且 `secret-id`、`secret-key`、`bucket`、`region` 等参数已经配置正确，否则无法上传文件。

如果输入 `send-s3 init` 后提示找不到命令，可能是 PATH 环境变量没有生效或没有配置，请依次检查：
 - 重新启动当前 shell，如 `exec zsh` 或 `exec bash`
 - 重新启动当前终端，在 GUI 下应退出终端应用（iTerm2 下按 <kbd>Command ⌘</kbd> + <kbd>Q</kbd>、Windows Terminal 下关闭窗口）
 - 查看 PATH 变量
    - 使用 pipx，需要根据 pipx 的提示将 `~/.local/bin` 添加到 PATH
    - Windows 版的 Python 默认不会将 `Scripts` 添加到 PATH，需要手动添加。打开 [设置——系统——关于](ms-settings:about) 点击右侧「高级系统设置」，添加 `C:\Users\<用户名>\AppData\Roaming\Python\<Python版本>\Scripts` 到 PATH
    - 如果使用了手动创建虚拟环境安装（安装方法 3），请将 `~/.cos-uploader/bin` 添加到 PATH

配置完成后，可以使用 `cos-uploader` 命令来上传文件。

```bash
# 上传文件试试，测试配置是否正确
echo "Hello World" > hello.txt
send-s3 upload hello.txt
```

### Windows 平台功能
在运行 `send-s3 init` 后，会在「资源管理器」中添加「发送到」菜单项，可以在「资源管理器」中右键文件，然后选择「发送到」，再选择「Send S3」来上传文件。

### MacOS 平台功能

请导入 [Send S3 快捷指令](https://www.icloud.com/shortcuts/b84eab4b8df141d89a25f048047ea4ff)

导入完成后，请打开「快捷指令」App，选择左上角菜单中的「快捷指令——设置——高级」，勾选「允许运行脚本」。

配置完成 `config.toml` 后，在 Finder 中右键想要上传的文件，在菜单中选择「快速操作」，然后选择「Send S3」即可上传该文件。

### Typora 集成
在 Typora 的「设置——图像——删除服务设定——命令」（上传服务选择「自定义命令」）中，添加以下命令：
    
```bash
send-s3 upload --typora
```

这样，Send S3 的输出结果可以被 Typora 识别，从而自动插入图片。

您需要修改 `send-s3` 的路径来使其正常工作。

## 查看历史
Send S3 会记录上传历史，可以通过 `send-s3 log` 命令来查看。输出记录按照时间戳降序排列。

`send-s3 log` 默认输出 100 条记录，可以通过 `-l` 参数来限制输出的记录数量。

```bash
send-s3 log -l 10
```

您可以设置查询的起止时间：

```bash
send-s3 log --from 2012-07-12 --to 2024-07-12
send-s3 log --from 2012-07-12T11:00:00 --to 2024-07-12T19:00:00
```

您可以通过 `send-s3 log --json` 来输出 JSON 格式的记录，以供其他程序处理。

```bash
cos-uploader-history -n 10 -r
```

## 许可
Send S3 使用 MIT 协议
