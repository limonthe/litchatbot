import streamlit as st
from zhipuai import ZhipuAI
from datetime import datetime 
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)

# 设置页面标题和图标
st.set_page_config(
    page_title="俄罗斯文学工具人",
    page_icon="🤖",
    layout="wide",  # 页面布局为宽模式
)

# 预置的API Key
predefined_api_key = "5f4378d13fb14e9caf3374bc01b3fe4f.rDBXwfdNDp1OJ7h1"

def zhipu_chat(api_key, model, temperature, top_p, max_tokens):
    """初始化ZhipuAI客户端"""
    client = ZhipuAI(api_key=api_key)
    return client

# 获取当前日期
current_date = datetime.now().strftime("%Y-%m-%d")

def render_sidebar():
    """渲染设置区域并返回设置的参数"""
    st.sidebar.title("参数设置")

# 默认值
DEFAULT_API_KEY = "5f4378d13fb14e9caf3374bc01b3fe4f.rDBXwfdNDp1OJ7h1"  # 你可以自定义默认API Key
DEFAULT_MODEL = "glm-4-flash"
DEFAULT_TEMPERATURE = 0.95
DEFAULT_TOP_P = 0.70
DEFAULT_MAX_TOKENS = 4095
DEFAULT_WEB_SEARCH = False  # 默认关闭联网搜索

# 在侧边栏中设置标题
st.sidebar.title("设置区域")

# 选择API Key方式
use_predefined_key = st.sidebar.radio(
    "选择API Key方式：", 
    ("使用预置API Key", "自定义API Key")
)

# 输入API Key
api_key = predefined_api_key if use_predefined_key == "使用预置API Key" else st.sidebar.text_input(
    "请输入您的API Key：", value=st.session_state.get("api_key", ""), type="password", placeholder="例如：xxxxxxxxxxxxxxxxx"
)

# 选择模型
model = st.sidebar.selectbox(
    "选择模型：",
    ("glm-4-flash", "glm-4-long"),
    index=("glm-4-flash", "glm-4-long").index(st.session_state.get("model", DEFAULT_MODEL)),
)

# 选择采样温度 (Temperature)
temperature = st.sidebar.slider(
    "选择采样温度 (Temperature)：",
    min_value=0.0, max_value=1.0, value=st.session_state.get("temperature", DEFAULT_TEMPERATURE), step=0.01,
)

# 选择核采样 (Top P)
top_p = st.sidebar.slider(
    "选择核采样 (Top P)：",
    min_value=0.0, max_value=1.0, value=st.session_state.get("top_p", DEFAULT_TOP_P), step=0.01,
)

# 选择最大Token数量 (Max Tokens)
max_tokens = st.sidebar.number_input(
    "选择最大Token数量 (Max Tokens)：",
    min_value=1, max_value=4095, value=st.session_state.get("max_tokens", DEFAULT_MAX_TOKENS), step=1,
)

# 联网搜索开关
web_search = st.sidebar.checkbox(
    "启用联网搜索（默认关闭）", value=st.session_state.get("web_search", DEFAULT_WEB_SEARCH)
)

# 设置工具（启用网络搜索）
tools = [{
    "type": "web_search",
    "web_search": {
        "enable": web_search  # 根据复选框的值启用或禁用联网搜索
    }
}]

# 恢复默认设置按钮
if st.sidebar.button("恢复默认设置"):
    # 重置所有设置为默认值
    st.session_state.api_key = DEFAULT_API_KEY
    st.session_state.model = DEFAULT_MODEL
    st.session_state.temperature = DEFAULT_TEMPERATURE
    st.session_state.top_p = DEFAULT_TOP_P
    st.session_state.max_tokens = DEFAULT_MAX_TOKENS
    st.session_state.web_search = DEFAULT_WEB_SEARCH

    # 更新界面上显示的内容
    st.sidebar.text("设置已恢复为默认值")

# 保存设置到 session_state
st.session_state.api_key = api_key
st.session_state.model = model
st.session_state.temperature = temperature
st.session_state.top_p = top_p
st.session_state.max_tokens = max_tokens
st.session_state.web_search = web_search

# 返回设置的参数
return api_key, model, temperature, top_p, max_tokens, tools

def display_conversation():
    """显示对话历史"""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    # 显示所有的问答历史
    for chat in st.session_state.conversation_history:
        if chat['role'] == 'user':
            st.markdown(f"**用户：** {chat['content']}")
        else:
            st.markdown(f"**工具人：** {chat['content']}")

def chat_with_bot(client, conversation, user_input, model, temperature, top_p, max_tokens):
    """与机器人聊天，并返回机器人的回答"""
    with st.spinner("工具人正在翻小抄..."):
        try:
            # 添加用户输入到对话历史
            conversation.append({"role": "user", "content": user_input})

            # 进行API调用，获取机器人响应
            response = client.chat.completions.create(
                model=model,
                messages=conversation,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens,
            )

            assistant_response = response.choices[0].message.content
            # 添加机器人的回答到历史记录
            conversation.append({"role": "assistant", "content": assistant_response})

            # 显示机器人回答
            st.markdown(f"**工具人回答：** {assistant_response}")

        except Exception as e:
            logging.error(f"发生错误：{e}")
            st.error("发生错误，请重试。")

def main():
    # 页面标题
    st.title("尽情提问，即刻咏来！")
    st.markdown(
        """
        这是一个基于ChatGLM模型的ai助手，主要针对于俄罗斯文艺、国情、俄语知识等。请输入您的问题，它会尽快回答。
        """
    )

    # 渲染设置区域
    api_key, model, temperature, top_p, max_tokens = render_sidebar()

    # 检查并初始化ZhipuAI客户端
    if api_key and model:
        client = zhipu_chat(api_key, model, temperature, top_p, max_tokens)
    else:
        st.warning("请确保您已设置API Key和模型。")
        return

    # 如果对话历史不存在，初始化空对话历史
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    # 显示对话历史
    display_conversation()

    # 设置默认提示文本
    prompt_options = [
        "介绍俄罗斯文学概况",
        "介绍一部俄罗斯文学作品",
        "托尔斯泰的创作理念",
        "聊一聊陀思妥耶夫斯基的主要作品",
        "介绍俄国文学与西方文学的关系",
        "分析普希金的文学贡献"
    ]

    # 提供选择框让用户选择预设的提示
    selected_prompt = st.selectbox(
        "选择一个提示：",
        prompt_options,
        index=0
    )

    # 用户输入框，默认填充选择的提示
    user_input = st.text_input("用户输入：", value=selected_prompt, placeholder="在这里输入您的问题...")

    # 发送按钮
    send_button = st.button("发送")

    # 控制按钮点击或回车触发聊天
    if send_button or (user_input and st.session_state.get("input_key", False)):
        if not user_input.strip() and not send_button:
            st.error("请输入有效的内容。")
        else:
            # 调用与机器人聊天的函数
            chat_with_bot(client, st.session_state.conversation_history, user_input, model, temperature, top_p, max_tokens)

    # 页面底部说明
    st.markdown(
        """
        ----
        提示：如果遇到任何问题，请确保API Key输入正确并且可以正常访问ZhipuAI服务。
        """
    )

if __name__ == "__main__":
    main()
