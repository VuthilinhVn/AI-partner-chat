# AI Partner Chat

一个基于 Streamlit 和 DeepSeek 大语言模型构建的 AI 智能伴侣聊天应用，支持个性化角色设定、多轮对话、会话管理以及流式回复展示。

## 功能特点

- 基于 Streamlit 的 Web 聊天界面
- 可自定义伴侣昵称和性格设定
- 支持多轮上下文对话
- 支持创建、加载、删除聊天会话
- 会话历史以 JSON 文件形式持久化保存
- 支持 AI 流式输出，回复更自然、更接近即时聊天体验
- 通过系统提示词控制回复风格，强化“伴侣角色”表现

## 技术栈

- Python 3.9+
- Streamlit
- OpenAI Python SDK
- DeepSeek API

## 项目结构

```text
AI-partner-chat/
├── AI-partner-chat.py   # 主应用入口
├── sessions/            # 运行时自动生成，保存会话数据
├── README.md            # 项目说明
└── .gitignore           # 可选：忽略本地生成文件
```

## 环境准备

1. 安装 Python 3.9 及以上版本
2. 安装依赖：

```bash
pip install streamlit openai
```

3. 配置 DeepSeek API Key

在 Windows PowerShell 中设置环境变量：

```powershell
$env:DEEPSEEK_API_KEY="your_deepseek_api_key"
```

在 Bash / zsh 中设置：

```bash
export DEEPSEEK_API_KEY="your_deepseek_api_key"
```

## 运行方式

在项目根目录执行：

```bash
streamlit run AI-partner-chat.py
```

然后在浏览器中打开 Streamlit 提供的本地地址即可使用。

## 使用说明

1. 在侧边栏中设置伴侣昵称和性格特征
2. 点击“创建新的对话”可开始新的聊天
3. 历史会话会显示在侧边栏中，支持切换和删除
4. 在聊天框中输入内容，即可与 AI 伴侣进行对话

## 注意事项

- 当前应用依赖 `DEEPSEEK_API_KEY` 环境变量
- 运行时会自动创建 `sessions/` 目录，用于存储会话记录
- 若需要更改 AI 的回复风格，可调整代码中的 `system_prompt` 模板

## 许可证

本项目仅供学习和个人开发使用，具体使用协议请自行根据实际情况确定。

## 可能的扩展方向

- 支持更丰富的角色设定模板
- 增加语音输入/输出
- 增加消息历史导出与导入
- 支持多种模型切换
- 增加用户账户与云端存储
