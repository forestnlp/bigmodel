import gradio as gr

from model import OpenAIModel, GLMModel
from translator import PDFTranslator
from utils import ConfigLoader

import socket
import socks



def translate(pdf_file_path: str, file_format: str, src_language: str, target_language: str, model_type: str) -> tuple:
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 10808)
    socket.socket = socks.socksocket

    config_loader = ConfigLoader("config.yaml")
    config = config_loader.load_config()
    try:
        if model_type == "OpenAIModel":
            model_name = config['OpenAIModel']['model']
            api_key = config['OpenAIModel']['api_key']
            model = OpenAIModel(model=model_name,api_key=None)
        else:
            timeout = config['GLMModel']['timeout']
            model_url = config['GLMModel']['model_url']
            model = GLMModel(model_url=model_url, timeout=timeout)

        translator = PDFTranslator(model)
        translator.translate_pdf(pdf_file_path, file_format, src_language ,target_language)

        if(file_format=='markdown'):
            translated_file_name = pdf_file_path.replace('.pdf', f'_translated.md')
        else:
            translated_file_name = pdf_file_path.replace('.pdf', f'_translated.pdf')
        return  translated_file_name

    except Exception as e:
        return  str(e)

# Create input components

pdf_file = gr.File(label="Upload PDF file")
src_language = gr.Textbox(label="Source Language",placeholder="英文", value="英文")
target_language = gr.Textbox(label="Target Language",placeholder="中文", value="中文")
model_type = gr.Radio(["OpenAIModel", "GLMModel"], label="Model Type ")
file_format = gr.Radio(["pdf", "markdown"], label="Output Format")

# Create output component
output = gr.File(label="Translated File")

# Create interface
gr.Interface(
    fn=translate,
    inputs=[pdf_file,file_format,src_language, target_language,model_type],
    outputs=[output],
    title="PDF Translation",
    description="Translate PDF files to the desired language and format.",
    allow_flagging="never"
).launch(share=True, server_name="0.0.0.0", debug=True)