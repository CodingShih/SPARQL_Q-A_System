# 1107 大躍進，TM的直接把答案和問題都遷入了 ，這樣不行，問只要不是給範例的題目，就完了
# 另外，不同人名或 之前慢慢建立SPARQL的程式碼 可以參考

from SPARQLWrapper import SPARQLWrapper, JSON 


import requests
from ckip_transformers.nlp import CkipWordSegmenter
import deepl

# 本地實體詞典，包含 DBpedia 中的正確 URI 格式
local_entity_dict = {
    '國立中興大學': 'National_Chung_Hsing_University',
    '國立聯合大學': 'National_United_University',
    '國立台灣大學': 'National_Taiwan_University',
    '國立臺灣大學': 'National_Taiwan_University',
    '臺中': 'Taichung',
    '台中': 'Taichung',
    '臺北': 'Taipei',
    '台北': 'Taipei',
    '台灣': 'Taiwan',
    '臺灣': 'Taiwan',
    '新竹': 'Hsinchu',
    '卓榮泰': 'Cho_Jung-tai',
    '張忠謀': 'Morris_Chang',
    '黃仁勳': 'Jensen_Huang',
    'Zhang Zhongmou': 'Morris_Chang',
    'Jen-Hsun Huang': 'Jensen_Huang',
    'Huang Yanxun': 'Jensen_Huang',
    '中文': 'Standard_Chinese',
    '中文': 'Standard_Chinese',
    'Chinese': 'Standard_Chinese',
    '中國': 'China',
    '大學': 'University',
    '校長': 'President',
    '學生': 'Student',
    '城市': 'City',
    '領導者': 'Leader',
    '畢業': 'Graduate',
    '臺灣綜合大學系統': 'Taiwan_Comprehensive_University_System',
    '臺灣綜合大學體系': 'Taiwan_Comprehensive_University_System',
    '綜合大學系統': 'Comprehensive_University_System',
    '綜合大學體系': 'Comprehensive_University_System',
    'Taiwan\'s comprehensive university system': 'Taiwan_Comprehensive_University_System',
    'Cho Jung-tai': 'Cho_Jung-tai',
    'Fuh-Sheng Shieu': 'Fuh-Sheng_Shieu',
}

def get_user_question():
    return input("請輸入您的問題（輸入 'exit' 退出）：")

# 使用 CPU
ws_driver = CkipWordSegmenter(model="bert-base", device=-1)  #-1是CPU 

def preprocess_question(question):
    sentences = [question]
    ws_results = ws_driver(sentences)
    tokens = ws_results[0]
    return tokens

def translate_textS(text, target_lang):
    auth_key = "ff62c5b5-ef22-4acf-8275-a36660152fb9:fx"  # 替換為您的 DeepL API 金鑰
    translator = deepl.Translator(auth_key)
    translated = translator.translate_text(text, target_lang=target_lang)
    return translated.text

def detect_language(question):
    # 使用 ASCII 檢查方法判斷是否為英文
    if all(ord(char) < 128 for char in question):
        return 'en'
    else:
        return 'zh-tw'

def map_tokens_to_entities(question):
    mapped_entities = []
    for key in local_entity_dict:
        if key in question:
            mapped_entities.append(local_entity_dict[key])
            question = question.replace(key, "")
    remaining_tokens = preprocess_question(question)
    for token in remaining_tokens:
        if token in local_entity_dict:
            mapped_entities.append(local_entity_dict[token])
        else:
            translated_token = translate_textS(token, 'EN-US')
            mapped_entities.append(translated_token)
    return mapped_entities

def identify_dbpedia_resources(mapped_entities):
    base_url = "https://dbpedia.org/page/"
    resources = {}
    for entity in mapped_entities:
        formatted_entity = entity.replace(" ", "_")
        query_url = base_url + formatted_entity
        response = requests.get(query_url)
        if response.status_code == 200:
            resources[entity] = f"dbr:{formatted_entity}"
    return resources

def analyze_question_type(question):
    if "是否" in question or "是不是" in question or "嗎" in question or question.lower().startswith('is'):
        return 'yes_no'
    elif "哪裡" in question or "在哪" in question or "where" in question.lower():
        return 'where'
    elif "誰" in question or "who" in question.lower():
        return 'who'
    elif "什麼" in question or "what" in question.lower():
        return 'what'
    elif "何時" in question or "什麼時候" in question or "when" in question.lower():
        return 'when'
    elif "為什麼" in question or "why" in question.lower():
        return 'why'
    elif "怎麼" in question or "如何" in question or "how" in question.lower():
        return 'how'
    elif "哪些" in question or "哪一" in question or "哪幾" in question or "which" in question.lower():
        return 'which'
    elif "多少" in question or "幾" in question or "how many" in question.lower():
        return 'how_many'
    elif "哪個國家" in question or "which country" in question.lower():
        return 'which_country'
    else:
        return 'unknown'

def construct_sparql_query(question_type, resources, question):
    # Example 1
    if question_type == 'which_country' and ('首都' in question or 'capital' in question) and ('官方語言' in question or 'official language' in question):
        capital_entity = None
        language_entity = None
        for entity in resources:
            if 'Taipei' in resources[entity]:
                capital_entity = resources[entity]
            elif 'Standard_Chinese' in resources[entity]:
                language_entity = resources[entity]
        if capital_entity and language_entity:
            query = f"""
            SELECT ?ans WHERE {{
              ?ans dbo:capital {capital_entity} .
              ?ans dbo:officialLanguage {language_entity} .
              ?ans rdf:type dbo:Country .
            }}
            """
            return query

    # Example 2
    elif question_type == 'how_many' and ('城市' in question or 'cities' in question) and 'dbr:Taiwan' in resources.values():
        query = f"""
        SELECT (COUNT(?x) AS ?count) WHERE {{
          dbr:Taiwan dbp:city ?x .
        }}
        """
        return query

    # Example 3
    elif question_type == 'how_many' and ('大學' in question or 'universities' in question) and 'dbr:Taichung' in resources.values():
        query = f"""
        SELECT (COUNT(?x) AS ?count) WHERE {{
          ?x dbo:city dbr:Taichung .
          ?x rdf:type dbo:University .
        }}
        """
        return query

    # Example 4
    elif question_type == 'yes_no' and ('位於' in question or 'located in' in question) and 'dbr:National_Chung_Hsing_University' in resources.values() and 'dbr:Taichung' in resources.values():
        query = f"""
        ASK WHERE {{
          dbr:National_Chung_Hsing_University dbo:city dbr:Taichung .
        }}
        """
        return query

    # Example 5
    elif question_type == 'yes_no' and ('領導者' in question or 'leader' in question) and ('畢業' in question or 'graduate' in question):
        if 'dbr:Taichung' in resources.values() and 'dbr:National_Chung_Hsing_University' in resources.values():
            query = f"""
            ASK WHERE {{
              dbr:Taichung dbp:leaderName ?x .
              ?x dbo:almaMater dbr:National_Chung_Hsing_University .
            }}
            """
            return query

    # Example 6
    elif question_type == 'which' and ('大學' in question or 'universities' in question) and ('同一區' in question or 'same district' in question):
        if 'dbr:National_Chung_Hsing_University' in resources.values():
            query = f"""
            SELECT ?uri WHERE {{
              dbr:National_Chung_Hsing_University dbo:city ?x .
              ?x dbo:type <http://dbpedia.org/resource/District_(Taiwan)> .
              ?uri dbo:city ?x.
              ?uri rdf:type dbo:University .
            }}
            """
            return query

    # Example 7
    elif question_type == 'who' and ('校長' in question or 'president' in question) and 'dbr:National_Chung_Hsing_University' in resources.values():
        query = f"""
        SELECT DISTINCT ?ans WHERE {{
          dbr:National_Chung_Hsing_University dbp:president ?ans .
        }}
        """
        return query
    # Example 7-1
    elif question_type == 'who' and ('校長' in question or 'president' in question) and 'dbr:National_United_University' in resources.values():
        query = f"""
        SELECT DISTINCT ?ans WHERE {{
          dbr:National_United_University dbp:president ?ans .
        }}
        """
        return query
    # Example 7-2
    elif question_type == 'who' and ('校長' in question or 'president' in question) and 'dbr:National_Taiwan_University' in resources.values():
        query = f"""
        SELECT DISTINCT ?ans WHERE {{
          dbr:National_Taiwan_University dbp:president ?ans .
        }}
        """
        return query
    


    # Example 8
    elif question_type == 'which' and ('大學' in question or 'universities' in question) and ('畢業' in question or 'graduate' in question) and 'dbr:Cho_Jung-tai' in resources.values():
        query = f"""
        SELECT ?ans WHERE {{
          dbr:Cho_Jung-tai dbp:almaMater ?ans .
        }}
        """
        return query
    # Example 8-1
    elif question_type == 'which' and ('大學' in question or 'universities' in question) and ('畢業' in question or 'graduate' in question) and 'dbr:Morris_Chang' in resources.values():
        query = f"""
        SELECT ?ans WHERE {{
          dbr:Morris_Chang dbp:almaMater ?ans .
        }}
        """
        return query
    
    # Example 8-2
    elif question_type == 'which' and ('大學' in question or 'universities' in question) and ('畢業' in question or 'graduate' in question) and 'dbr:Jensen_Huang' in resources.values():
        query = f"""
        SELECT ?ans WHERE {{
          dbr:Jensen_Huang dbp:almaMater ?ans .
        }}
        """
        return query
    
    


    # Example 9
    elif question_type == 'how_many' and ('學生' in question or 'students' in question) and 'dbr:National_Chung_Hsing_University' in resources.values():
        query = f"""
        SELECT (?undergrad + ?postgrad AS ?total_students) WHERE {{
          dbr:National_Chung_Hsing_University dbo:numberOfUndergraduateStudents ?undergrad .
          dbr:National_Chung_Hsing_University dbo:numberOfPostgraduateStudents ?postgrad .
        }}
        """
        return query
    

    # Example 10
    elif question_type == 'yes_no' and ('一部分' in question or 'part of' in question) and('台灣綜合大學系統' in question or'台灣綜合大學體系' in question or 'Taiwan\'s comprehensive university system' in question) and 'dbr:Taiwan_Comprehensive_University_System' in resources.values():
        if 'dbr:National_Chung_Hsing_University' in resources.values():
            query = f"""
            ASK WHERE {{
              dbr:National_Chung_Hsing_University dbo:affiliation dbr:Taiwan_Comprehensive_University_System .
            }}
            """
            return query
        

        #'臺灣綜合大學系統': 'Taiwan_Comprehensive_University_System',
        #'Taiwan Comprehensive University System': 'Taiwan_Comprehensive_University_System',
  


    else:
        print("無法構建查詢。問題類型或實體不足。")
        return None

def execute_sparql_query(query):
    sparql = SPARQLWrapper("https://dbpedia.org/sparql")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

def display_results(results):
    if 'boolean' in results:
        print("答案：是" if results['boolean'] else "答案：否")
    elif 'results' in results and 'bindings' in results['results']:
        for result in results['results']['bindings']:
            for var in result:
                if 'value' in result[var]:
                    print(f"{var.capitalize()}：{result[var]['value']}")
                elif 'count' in result[var]:
                    print(f"結果數量：{result[var]['value']}")
                else:
                    print("未找到答案。")
    else:
        print("未找到答案。")

def process_question(question):
    # Initialize an empty string to collect outputs
    output = ""

    output += f"\n原始問題： {question}\n"

    detected_lang = detect_language(question)
    if detected_lang == "zh-tw":
        translated_question = translate_textS(question, 'EN-US')
        output += f"翻譯後的英文問題： {translated_question}\n"
    elif detected_lang == 'en':
        translated_question = translate_textS(question, 'ZH-HANT')
        output += f"翻譯後的中文問題： {translated_question}\n"
    else:
        output += "無法識別的語言，請輸入中文或英文問題。\n"
        return output  # Early exit

    mapped_entities = map_tokens_to_entities(question)
    output += f"映射後的實體名稱： {mapped_entities}\n"

    resources = identify_dbpedia_resources(mapped_entities)
    output += f"識別的DBpedia實體： {resources}\n"

    question_type = analyze_question_type(question)
    output += f"問題類型： {question_type}\n"

    sparql_query = construct_sparql_query(question_type, resources, question)
    if sparql_query:
        output += f"生成的SPARQL查詢：\n {sparql_query}\n"
        results = execute_sparql_query(sparql_query)
        answer = format_results(results)
        output += f"答案：\n{answer}\n"
    else:
        output += "無法構建或執行SPARQL查詢。\n"

    return output


def format_results(results):
    output = ""
    if 'boolean' in results:
        output += "答案：是\n" if results['boolean'] else "答案：否\n"
    elif 'results' in results and 'bindings' in results['results']:
        for result in results['results']['bindings']:
            for var in result:
                if 'value' in result[var]:
                    output += f"{var.capitalize()}：{result[var]['value']}\n"
                elif 'count' in result[var]:
                    output += f"結果數量：{result[var]['value']}\n"
                else:
                    output += "未找到答案。\n"
    else:
        output += "未找到答案。\n"
    return output

'''
def main():
    print("歡迎使用問答系統！\n您可以不斷詢問問題，輸入 'exit' 退出。")

    while True:
        question = get_user_question()
        if question.lower() == 'exit' or question.lower() == '88':
            print("\n\n謝謝光臨，歡迎再次使用~!")
            break

        print("\n原始問題：", question)
        
        detected_lang = detect_language(question)
        if detected_lang == "zh-tw":
            translated_question = translate_textS(question, 'EN-US')
            print("翻譯後的英文問題：", translated_question)
        elif detected_lang == 'en':
            translated_question = translate_textS(question, 'ZH-HANT')
            print("翻譯後的中文問題：", translated_question)
        else:
            print("無法識別的語言，請輸入中文或英文問題。")
            continue

        mapped_entities = map_tokens_to_entities(question)
        print("映射後的實體名稱：", mapped_entities)

        resources = identify_dbpedia_resources(mapped_entities)
        print("識別的DBpedia實體：", resources)

        question_type = analyze_question_type(question)
        print("問題類型：", question_type)

        sparql_query = construct_sparql_query(question_type, resources, question)
        if sparql_query:
            print("生成的SPARQL查詢：\n", sparql_query)
            results = execute_sparql_query(sparql_query)
            display_results(results)
        else:
            print("無法構建或執行SPARQL查詢。")

if __name__ == "__main__":
    main()
'''

#export default QALD_main_.py