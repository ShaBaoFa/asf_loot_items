# ASF Bot Command Handler

这是一个用于管理和执行 ArchiSteamFarm (ASF) bot 命令的 Python 脚本。

## 功能特点

- 支持通过 ASF-IPC 接口执行 bot 命令
- 自动重试机制，失败时会自动重试最多5次
- 递减等待时间（从8分钟开始，每次减少2分钟）
- 实时显示等待倒计时
- 失败记录保存功能

## 安装要求
```
pip3 install -U ASF_IPC
```

## 配置文件

需要创建一个 JSON 格式的配置文件，例如 `config.json`：


```json
{
"ipc": "http://127.0.0.1:1242", // ASF IPC 地址
"password": "your_password", // IPC 密码
"items": "" // 物品相关参数 2923300 2 banana 730 2 csgo
}
```


## 使用方法

1. 运行脚本：

```
python main.py
```


2. 按提示输入：
   - 配置文件名称（不需要输入 .json 后缀）
   - Bot 名称

## 错误处理

- 当命令执行失败时，程序会自动重试
- 重试等待时间：
  - 第1次：8分钟
  - 第2次：6分钟
  - 第3次：4分钟
  - 第4次：2分钟
- 5次失败后，bot 名称会被记录到 `{config}FailList.txt` 文件中

## 注意事项

- 确保 ASF 正在运行且 IPC 接口可访问
- 配置文件中的 IPC 地址和密码必须正确
- 需要 Python 3.6 或更高版本