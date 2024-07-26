import streamlit as st
from openai import OpenAI
import os
import json
import time

# Create a chatbot UI with Streamlit and OpenAI
def chat_ui():
    state = st.session_state
    # Set the title of the app
    st.title("InternLM")

    # Create a client for the OpenAI API
    if "client" not in state:
        st.info("请配置Chatbot的基本设置，其中API Key和Base URL是必须的。")
        pass
    else:
        # if "message_history" not in state:
        #     state.message_history = []
        #     pass
        # if "system_prompt" in state:
        #     state.message_history.append({"role": "system", "content": state.system_prompt})
        user_input = st.chat_input("输入消息")
        if user_input:
            state.message_history.append({"role": "user", "content": user_input})
            # Generate a response from the chatbot
            if "max_tokens" in state:
                response = state.client.chat.completions.create(
                    model=state.client.models.list().data[0].id,
                    messages=state.message_history,
                    max_tokens=state.max_tokens,
                    temperature=state.temperature
                )
            else:
                response = state.client.chat.completions.create(
                    model=state.client.models.list().data[0].id,
                    messages=state.message_history,
                    temperature=state.temperature
                )
            state.message_history.append({"role": "assistant", "content": response.choices[0].message.content})
            pass
        for message in state.message_history:
            if message["role"] == "system":
                continue
            else:
                st.chat_message(message["role"]).write(message["content"])

    # Create a text input for the user to type their message

    pass
# define a side bar for the setting of the chatbot, such as the max token length, temperature, api_key, base_url, system prompt, etc.
def side_bar():
    st.sidebar.title("设置")
    state = st.session_state
    # Set a form of the settings
    with st.sidebar.form(key="settings"):
        # Set the max token length for the chatbot
        max_tokens = st.number_input("最大token长度", min_value=0, max_value=2048, value=100, step=1)
        # Set the temperature for the chatbot
        temperature = st.number_input("Temperature", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
        # Set the api key for the OpenAI API
        api_key = st.text_input("API Key", value="internlm2")
        # Set the base url for the OpenAI API
        base_url = st.text_input("Base URL",value="http://0.0.0.0:23333/v1")
        # Set the system prompt for the chatbot
        system_prompt = st.text_area("系统提示", value="")
        # Add a submit button to the form
        submit = st.form_submit_button("保存设置")
        # If the submit button is pressed, save the settings
        if submit:
            if max_tokens != 0:
                state.max_tokens = max_tokens
            state.temperature = temperature
            state.api_key = api_key
            state.base_url = base_url
            state.message_history = []
            if system_prompt != "":
                state.system_prompt = system_prompt
                state.message_history.append({"role": "system", "content": system_prompt})
            state.client = OpenAI(api_key=state.api_key, base_url=state.base_url)
            pass
    if st.sidebar.button("开启新对话"):
        if not os.path.exists("chat_history"):
            os.mkdir("chat_history")
            pass
        with open(f"chat_history/{time.time()}.json", "w") as f:
            json.dump(state.message_history, f, ensure_ascii=False)
            pass
        state.message_history = []
        st.rerun()

    pass

if __name__ == "__main__":
    side_bar()
    chat_ui()
    pass

    