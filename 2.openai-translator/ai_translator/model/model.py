from book import ContentType

class Model:
    def make_text_prompt(self, text: str, src_language: str,target_language: str) -> str:
        return f"你是一位优秀的翻译专家，请将文本从{src_language}翻译为{target_language}，保留换行符不变。确保以下所有的文本内容均被翻译：{text}"

    def make_table_prompt(self, table: str, src_language: str,target_language: str) -> str:
        return f'''你是一位优秀的翻译专家，请将表格从{src_language}翻译为{target_language},以相同的格式输出翻译结果，保持行、列、间距不变，逗号不要改变为其他符号(请不要将,转换为，或者、)，每一行用'\n'换行。Think step by step.
        例如:
        [Fruit, Color, Price (USD)] [Apple, Red, 1.20] [Banana, Yellow, 0.50]
        翻译为俄文：
        [Фрукт, Цвет, Цена (USD)] 
        [Яблоко, Красный, 1.20]
        [Банан, Жёлтый, 0.50] 
        请翻译：\n{table}'''

    def translate_prompt(self, content, src_language: str,target_language: str) -> str:
        if content.content_type == ContentType.TEXT:
            return self.make_text_prompt(content.original, src_language,target_language)
        elif content.content_type == ContentType.TABLE:
            return self.make_table_prompt(content.get_original_as_str(), src_language,target_language)

    def make_request(self, prompt):
        raise NotImplementedError("子类必须实现 make_request 方法")
