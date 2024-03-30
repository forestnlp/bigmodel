from flask import Flask, request, jsonify,send_file,render_template
from model import Model

from model import OpenAIModel, GLMModel
from translator import PDFTranslator
from utils import ConfigLoader
import os

import socket
import socks

socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 10808)
socket.socket = socks.socksocket

app = Flask(__name__)


@app.route('/api/translate', methods=['POST'])
def api_translate_pdf():
    try:
        config_loader = ConfigLoader("config.yaml")
        config = config_loader.load_config()

        pdf_file = request.files.get('file')
        src_language = request.form.get('src_language', '英文')  # 设置默认值
        target_language = request.form.get('target_language', '中文')  # 设置默认值
        output_format = request.form.get('output_format', 'pdf')
        model_type = request.form.get('model_type', 'OpenAIModel')


        if pdf_file is None:
            return jsonify({'error': 'No file provided'}), 400

        pdf_file_path = 'uploaded_file.pdf'
        pdf_file.save(pdf_file_path)

        if model_type == "OpenAIModel":
            model_name = config['OpenAIModel']['model']
            api_key = config['OpenAIModel']['api_key']
            model = OpenAIModel(model=model_name, api_key=api_key)
        else:
            timeout = config['GLMModel']['timeout']
            model_url = config['GLMModel']['model_url']
            model = GLMModel(model_url=model_url, timeout=timeout)

        success, translated_file_name = translate(pdf_file_path, output_format, src_language, target_language, model)

        if success:
            return send_file(os.getcwd() + "/" +translated_file_name,as_attachment=True)
        else:
            return jsonify({'result': 'error', 'message': str(translated_file_name)})

    except Exception as e:
        return jsonify({'result': 'error', 'message': str(e)})


def translate(pdf_file_path: str, file_format: str, src_language: str, target_language: str, model: Model) -> tuple:

    try:

        translator = PDFTranslator(model)
        translator.translate_pdf(pdf_file_path, file_format, src_language ,target_language)
        if(file_format=='markdown'):
            translated_file_name = pdf_file_path.replace('.pdf', f'_translated.md')
        else:
            translated_file_name = pdf_file_path.replace('.pdf', f'_translated.pdf')
        return True, translated_file_name

    except Exception as e:
        return False, str(e)

@app.route('/test')
def test_page():
    return render_template('api_test.html')

if __name__ == '__main__':
    app.run(debug=True)