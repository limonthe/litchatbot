import streamlit as st
import sounddevice as sd
import portaudio
import numpy as np
import speech_recognition as sr
from zhipuai import ZhipuAI
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)

# 创建一个自定义的麦克风类，使用 sounddevice
class SoundDeviceMicrophone(sr.Microphone):
    def __init__(self, device_index=None, samplerate=None, channels=None, chunk_size=1024):
        self.device_index = device_index
        self.samplerate = samplerate
        self.channels = channels
        self.chunk_size = chunk_size
        self.device = sd.default.device = self.device_index
        self.samplerate = self.samplerate or sd.query_devices(self.device_index, 'input')['default_samplerate']
        self.channels = self.channels or sd.query_devices(self.device_index, 'input')['max_input_channels']

    def listen(self, source):
        # 使用 SoundDevice 录音
        audio_data = sd.rec(int(self.samplerate * 5), samplerate=self.samplerate, channels=self.channels)
        sd.wait()
        return np.array(audio_data)

# 创建一个SpeechRecognition对象
recognizer = sr.Recognizer()

# 设置页面标题和图标
st.set_page_config(
    page_title="俄罗斯文学工具人",
    page_icon="🤖💬",
    layout="wide",  # 页面布局为宽模式
)

# 预置的API Key
predefined_api_key = "5f4378d13fb14e9caf3374bc01b3fe4f.rDBXwfdNDp1OJ7h1"

def zhipu_chat(api_key, model, temperature, top_p, max_tokens, do_sample):
    """初始化ZhipuAI客户端"""
    client = ZhipuAI(api_key=api_key)
    return client

def render_sidebar():
    """渲染设置区域并返回设置的参数"""
    st.sidebar.title("参数设置")   

    # 选择是否使用预置API Key
    use_predefined_key = st.sidebar.radio(
        "选择API Key方式：", 
        ("使用预置API Key", "自定义API Key")
    )
    
    api_key = predefined_api_key if use_predefined_key == "使用预置API Key" else st.sidebar.text_input(
        "请输入您的API Key：", value=st.session_state.get("api_key", ""), type="password", placeholder="例如：xxxxxxxxxxxxx.xxxxxxxxxxxx"
    )

    model = st.sidebar.selectbox(
        "选择模型：",
        ("glm-4-flash", "glm-4-long", "glm-4-plus"),
        index=("glm-4-flash", "glm-4-long").index(st.session_state.get("model", "glm-4-flash")),
    )

    # 选择是否启用采样
    do_sample = st.sidebar.checkbox(
        "启用采样策略 (Do Sample)",
        value=st.session_state.get("do_sample")
    )
    
    temperature = st.sidebar.slider(
        "选择采样温度 (Temperature)：",
        min_value=0.0, max_value=1.0, value=st.session_state.get("temperature", 0.95), step=0.01,
    )

    top_p = st.sidebar.slider(
        "选择核采样 (Top P)：",
        min_value=0.0, max_value=1.0, value=st.session_state.get("top_p", 0.70), step=0.01,
    )

    max_tokens = st.sidebar.number_input(
        "选择最大Token数量 (Max Tokens)：",
        min_value=1, max_value=4095, value=st.session_state.get("max_tokens", 4095), step=1,
    )
     
    # 保存设置到session_state
    st.session_state.api_key = api_key
    st.session_state.model = model
    st.session_state.temperature = temperature
    st.session_state.top_p = top_p
    st.session_state.max_tokens = max_tokens
    st.session_state.do_sample = do_sample

    # 根据采样设置输出对应的参数
    def get_sampling_params(do_sample, temperature, top_p):
        if do_sample:
            return {'采样温度temperature': temperature, '核采样top_p': top_p}
        else:
            return {'采样温度temperature': 1.0, '核采样top_p': 1.0}

    sampling_params = get_sampling_params(do_sample, temperature, top_p)
    st.write(f"采样参数: {sampling_params}")

    return api_key, model, temperature, top_p, max_tokens, do_sample

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

def chat_with_bot(client, conversation, user_input, model, temperature, top_p, max_tokens, do_sample):
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
                do_sample=do_sample,
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
    st.title("尽情提问，即刻咏来！٩(•̤̀ᵕ•̤́๑)")
    st.markdown(
        """
        这是一个基于ChatGLM模型的ai助手，主要针对于俄罗斯文艺、国情、俄语知识等。权且一试，待其回答。
        """
    )

    # 渲染设置区域
    api_key, model, temperature, top_p, max_tokens, do_sample = render_sidebar()

    # 检查并初始化ZhipuAI客户端
    if api_key and model:
        client = zhipu_chat(api_key, model, temperature, top_p, max_tokens, do_sample)
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

    # 语音输入按钮
    if st.button("点击开始语音输入"):
         # 使用麦克风进行语音识别
         with sr.Microphone() as source:
             st.text("正在听你说话，请讲...")
             audio = recognizer.listen(source)

         try:
             # 识别音频并转换为文本
             voice_text = recognizer.recognize_google(audio, language="zh-CN")
             st.write(f"你说的是: {voice_text}")
             # 将识别的语音内容设置为文本框的输入
             user_input = voice_text
         except sr.UnknownValueError:
             st.error("未能理解语音内容，请再试一次。")
         except sr.RequestError:
             st.error("请求错误，请检查网络连接。")

    # 显示最终的用户输入（无论是文本输入还是语音输入）
    st.write(f"你输入的内容是: {user_input}")   

    # 发送按钮
    send_button = st.button("发送")

    # 控制按钮点击或回车触发聊天
    if send_button or (user_input and st.session_state.get("input_key", False)):
        if not user_input.strip() and not send_button:
            st.error("请输入有效的内容。")
        else:
            # 调用与机器人聊天的函数
            chat_with_bot(client, st.session_state.conversation_history, user_input, model, temperature, top_p, max_tokens, do_sample)

    # 页面底部说明
    st.markdown(
        """
        ----
        提示：如遇问题，请确保API Key正确且可正常访问ZhipuAI服务。
        """
    )
    "[![在GitHub代码仓库中查看](https://github.com/codespaces/badge.svg)](https://github.com/limonthe/litchatbot)"
    "[获取 API key](https://bigmodel.cn/?faitai.com)"
    "[回到平台页面](https://limonthe.github.io/rebornlL/surface.html)"

# 页面底部添加说明
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
            font-size: 12px;
        }
    </style>
    <div class="footer">
        仍处开发调试中，望不吝赐教！ 525976102@qq.com。Ciallo～(∠・ω< )⌒★ 
    </div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
