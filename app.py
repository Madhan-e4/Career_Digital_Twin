from openai import OpenAI
from tools import handle_tool_calls, tools
from system_prompt import system_prompt
import gradio as gr
from dotenv import load_dotenv
from styles import EXAMPLES, CSS, JS

load_dotenv(override = True)

openai = OpenAI()

system = [{"role":"system", "content":system_prompt}]

def chat(message, history):
    messages = system + history + [{"role":"user", "content": message}]
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages,
        tools = tools
    )
    while response.choices[0].finish_reason == "tool_calls":
        tool_calls = response.choices[0].message.tool_calls
        results = handle_tool_calls(tool_calls)
        messages.append(response.choices[0].message)
        messages.extend(results)
        response = openai.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messages,
            tools = tools
        )
    return response.choices[0].message.content


if __name__ == "__main__":
    gr.ChatInterface(
        fn = chat, type="messages",
        examples=EXAMPLES,
        title="Hello I'm Madhan",
        description="You're currently talking to my digital twin.",
        chatbot=gr.Chatbot(show_label=False),
        css=CSS, js=JS, theme=gr.themes.Base()).launch()