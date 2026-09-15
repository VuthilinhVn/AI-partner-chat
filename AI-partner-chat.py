"""
本项目是一个基于 Streamlit 和 Deepseek 大语言模型构建的 AI 智能伴侣聊天应用 --> AI Partner Chat Application. 用户可以与 AI 伴侣进行自然语言对话，AI 伴侣会根据用户的输入生成个性化的回复。用户可以自定义伴侣的昵称和性格特征，系统会根据这些信息调整 AI 的回复风格。
项目中实现以下功能：
1. 基于 Streamlit 的 Web 界面：用户可以通过浏览器与 AI 进行交互，界面简洁直观，支持流式输出，实时展示 AI 的回复内容
2. 个性化角色设定：用户可以在侧边栏自定义伴侣昵称和性格特征（如"活泼可爱"），AI 会根据设定生成符合性格的个性化回复
3. 多轮对话：AI 能够记住完整的对话上下文，实现连贯的多轮交流体验。
4. 会话管理：支持创建新会话、加载历史会话、删除会话等功能，所有会话数据以 JSON 格式持久化存储，方便用
5. 系统提示词模板：通过预设的系统提示词（System Prompt）约束 AI 的行为规则，如每次只回复一条消息、禁止场景描述、匹配用户语言、回复简短等，使对话更贴近真实的聊天风格。
"""

import os
import streamlit as st
from openai import OpenAI
import json
from datetime import datetime

print("------------重新启动Python文件")
# 系统提示词
system_prompt = """
        你叫%s，现在是用户的真实伴侣，请完全代入伴侣角色。：
        规则：
            1. 每次只回1条消息
            2. 禁止任何场景或状态描述性文字
            3. 匹配用户的语言
            4. 回复简短，像微信聊天一样
            5. 有需要的话可以用❤️🌸等emoji表情
            6. 用符合伴侣性格的方式对话
            7. 回复的内容, 要充分体现伴侣的性格特征
        伴侣性格：
            - %s
        你必须严格遵守上述规则来回复用户。
    """
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🥰",
    layout="wide",
    # 侧边栏的菜单
    initial_sidebar_state="expanded",
    # 菜单信息
    menu_items={
    }
)

def save_session():
    if st.session_state.current_session:
        # 构建会话对象
        session_data = {
            "nick_name": st.session_state.nick_name,
            "character": st.session_state.character,
            "messages": st.session_state.messages,
            "current_session": st.session_state.current_session
        }
        if not os.path.exists("sessions"):
            os.makedirs("sessions")
        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=4)

def generate_session_name():
    return datetime.now().strftime("%y-%m-%d_%H-%M-%S")

# 加载所有会话列表
def load_session_list():
    session_list = []
    # 加载Python目录下的所有json文件
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for file in file_list:
            if file.endswith(".json"):
                session_list.append(file[:-5])
    return session_list.sort(reverse=True)
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nick_name = session_data["nick_name"]
                st.session_state.character = session_data["character"]
                st.session_state.current_session = session_name
    except Exception as e:
        st.error("加载会话失败, 具体错误信息:",e)


def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception:
        st.error("删除会话失败")
# 初始化聊天消息
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'nick_name' not in st.session_state:
    st.session_state.nick_name = "小甜甜"
if 'character' not in st.session_state:
    st.session_state.character = "活泼可爱"
if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()
# 大标题
st.title("AI智能伴侣")
# 添加logo
# Cach 1:
# st.sidebar.subheader("AI智能伴侣")
# nick_name = st.sidebar.text_input("伴侣昵称")
# character = st.sidebar.text_input("伴侣性格")
# Cach 2: 创建侧边栏
with st.sidebar:
    st.subheader("AI智能伴侣控制板")
    # 创建新的对话
    if st.button("创建新的对话", width="stretch", icon="✏️"):
        if st.session_state.messages:
            # 1. 保存当前会话信息
            save_session()
            # 2. 创建新的会话
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun()
    # 会话列表
    st.text("会话历史")
    session_list = load_session_list()
    for session in session_list:
        col1, col2 = st.columns([4, 1])
        with col1:
            # 三元运算符, 语法
            # 语法: 条件为真时的值 if 条件 else 条件为假时的值
            if st.button(session, width="stretch",icon="📄",
                         key=f"load_{session}",
                         type="primary" if session == st.session_state.current_session else "secondary"):

                #加载会话
                load_session(session)
                st.rerun()

        with col2:
            if st.button("",icon="❌️", key=f"delete_{session}"):
                # 删除session
                delete_session(session)
                st.rerun()

    nick_name = st.text_input("伴侣昵称", placeholder="请输入伴侣昵称", value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name

    character = st.text_area("伴侣性格", placeholder="请输入伴侣性格", value=st.session_state.character)
    if character:
        st.session_state.character = character



client = OpenAI(
        api_key=os.environ.get('DEEPSEEK_API_KEY'),
        base_url="https://api.deepseek.com")

# 展示聊天信息--> 遍历展示
st.text(f"会话名称:{st.session_state.current_session}")
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# 输入框
prompt = st.chat_input("请输入您要问的问题")
if prompt: # 字符串自动转换为布尔值, 如果非空字符串则为True
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 调用AI大模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=
        [
            {"role": "system", "content": system_prompt % (st.session_state.nick_name, st.session_state.character)},
            *st.session_state.messages
        ],
        stream=True
    )
    #非流失输出
    # st.chat_message("assistant").write(response.choices[0].message.content)
    #流式输出
    response_message = st.empty() # 创建一个空容器, 用于展示大模型的结果
    full_response = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_response += content
            response_message.chat_message("assistant").write(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    #保存当前会话信息
    save_session()
