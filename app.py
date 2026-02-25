import requests
import json
import gradio as gr

url = "http://localhost:11434/api/generate" # use http unless SSL configured

headers = {
    "Content-Type": "application/json"
}

history = []

def generate_response(prompt):
    history.append(prompt)
    final_prompt = "\n".join(history)

    payload = {
        "model": "CodeGuru",
        "prompt": final_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            response_json = response.json()
            actual_response = response_json.get("response", "No response field found.")
            return actual_response
        else:
            return f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Connection error: {e}"

# Frontend using Gradio
interface = gr.Interface(
    fn=generate_response,
    inputs=gr.Textbox(lines=4, label="Enter your prompt"),
    outputs="text",
    title="CodeGuru - Your AI Coding Companion"
)

interface.launch()