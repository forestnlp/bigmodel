# from langchain.chat_models import ChatOpenAI
# 1.0 from langchain_community.chat_models import ChatOpenAI
# from langchain_openai import ChatOpenAI
# from langchain_community.chat_models import ChatOpenAI

# conda activate homework & cd d:\xuexi\llm-homework\openai-quickstart\langchain\openai-translator\ & d: 
# python ai_translator/gradio_server.py
# python ai_translator/gradio_gui.py

from langchain_openai import ChatOpenAI
from langchain_core.prompts import (ChatPromptTemplate,SystemMessagePromptTemplate,HumanMessagePromptTemplate)
from langchain_community.llms.chatglm3 import ChatGLM3
from langchain.chains import LLMChain

# from langchain.prompts.chat import (
#     ChatPromptTemplate,
#     SystemMessagePromptTemplate,
#     HumanMessagePromptTemplate,
# )

from utils import LOG


class TranslationChain:
    def __init__(self, model_name: str = "gpt-3.5-turbo", verbose: bool = True):
        
        # 翻译任务指令始终由 System 角色承担
        template = (
            """You are a translation expert, proficient in various languages. \n
            Translates {source_language} to {target_language} with translation style of {styles}."""
        )
        system_message_prompt = SystemMessagePromptTemplate.from_template(template)

        # 待翻译文本由 Human 角色输入
        human_template = "{text}"
        human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

        # 使用 System 和 Human 角色的提示模板构造 ChatPromptTemplate
        chat_prompt_template = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt]
        )

        # 为了翻译结果的稳定性，将 temperature 设置为 0
        if(model_name=="gpt-3.5-turbo"):
            chat = ChatOpenAI(model_name=model_name, temperature=0, verbose=verbose)
        else:
            chat = ChatGLM3(endpoint_url="http://127.0.0.1:6006/v1/chat/completions",max_tokens=80000,top_p=0.9, temperature=0, verbose=verbose)


        self.chain = LLMChain(llm=chat, prompt=chat_prompt_template, verbose=verbose)

    def run(self, text: str, source_language: str, target_language: str,styles:str) -> (str, bool):
        import os
        import socket
        import socks

        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 10808)
        socket.socket = socks.socksocket
        os.environ['SERPAPI_API_KEY'] = 'YOUR SERPAPI_API_KEY'
        os.environ['OPENAI_API_KEY'] = 'YOUR_OPENAI_API_KEY'
        
        result = ""
        try:
            result = self.chain.run({
                "text": text,
                "source_language": source_language,
                "target_language": target_language,
                "styles":styles
            })
        except Exception as e:
            LOG.error(f"An error occurred during translation: {e}")
            return result, False

        return result, True