# Before executing the script, let's define a safe execution environment
# We will import the required modules and define the function to capture any exceptions that might occur

import socket
import re
import gradio as gr

# Define the function from the script
def get_hostname():
    hostname = socket.gethostname()
    match = re.search(r'-(\d+)$', hostname)
    if match:  # Added a check to avoid AttributeError if no match is found
        name = match.group(1)
    else:
        name = "user"  # Default name if no match
    return name

# We will define a separate function to launch the Gradio demo
def launch_gradio_demo():
    with gr.Blocks(gr.themes.Soft()) as demo:
        html_code = """
                <p align="center">
                <a href="https://intern-ai.org.org.cn/home">
                    <img src="https://intern-ai.org.cn/assets/headerLogo-4ea34f23.svg" alt="Logo" width="20%" style="border-radius: 5px;">
                </a>
                </p>
                <h1 style="text-align: center;">☁️ Welcome {get_hostname()} user, welcome to the ShuSheng LLM Practical Camp Course!</h1>
                <h2 style="text-align: center;">😀 Let’s go on a journey through ShuSheng Island together.</h2>
                <p align="center">
                    <a href="https://github.com/InternLM/Tutorial/blob/camp3">
                        <img src="https://oss.lingkongstudy.com.cn/blog/202410081252022.png" alt="Logo" width="50%" style="border-radius: 5px;">
                    </a>
                </p>
                """
        gr.Markdown(html_code)
    return demo.launch()

# Execute the Gradio demo and capture any exceptions
error_message = None
try:
    launch_gradio_demo()
except Exception as e:
    error_message = str(e)

error_message