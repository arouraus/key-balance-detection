# Key Balance Detection

一个用于查询和管理AI模型API的工具，支持命令行和图形界面两种模式。

## 主要功能

- 查询基于[one-api](https://github.com/songquanpeng/one-api#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95)部署的第三方转发API的key额度
- 获取可用模型列表
- 测试模型响应
- 支持多API Key管理
- 中英文双语界面
- 支持多家AI公司模型（OpenAI、Anthropic、DeepSeek等）

## 安装

1. 确保已安装Python 3.10或更高版本
2. 克隆本仓库：
   ```bash
   git clone https://github.com/yourusername/key-balance-detection.git
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
4.构建windows平台的可执行文件：（可选）
   ```bash
   # 安装打包工具
   pip install pyinstaller
   # 将GUI应用打包为单个exe可执行文件
   pyinstaller -F -w OptimizedMain.py
   ```

## 使用方法

### 命令行模式
运行`main.py`：
```bash
python main.py
```

### 图形界面模式
运行`OptimizedMain.py`：
```bash
python OptimizedMain.py
```

## 项目结构

```
.
├── main.py                # 命令行版本主程序
├── OptimizedMain.py       # 图形界面版本主程序
├── pyproject.toml         # 项目配置和依赖
├── README.md              # 项目说明文档
└── .gitignore             # Git忽略文件配置
```

## 依赖

- requests >= 2.32.3
- tabulate >= 0.9.0
- wxpython >= 4.2.2

## 贡献

欢迎提交Issue和Pull Request。

## 许可证

[MIT](LICENSE)
