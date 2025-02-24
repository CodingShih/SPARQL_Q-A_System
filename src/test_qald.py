# 創建一個簡單的測試文件 test_qald.py
from QALD_main_7112029008 import *

def test_basic_functions():
    # 測試基本功能
    question = "國立中興大學位於台中市嗎?"
    
    # 測試語言檢測
    lang = detect_language(question)
    print(f"Detected language: {lang}")
    
    # 測試翻譯
    trans = translate_textS(question, 'EN-US')
    print(f"Translation: {trans}")
    
    # 測試實體映射
    entities = map_tokens_to_entities(question)
    print(f"Mapped entities: {entities}")

if __name__ == "__main__":
    test_basic_functions()
    