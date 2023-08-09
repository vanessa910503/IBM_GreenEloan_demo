from Original import data_processing, selected_questions_list, chat_chain
import os


### ========== Original ====================================================================================================================================
'''
REQUIRED INFORMATION:
- api_key: OpenAI API key
- pdf_file_path: the path of the pdf file
- csv_file_path: the path of the csv file
- selected_questions: the list of selected questions
'''
def main():
    # Please fill in all the required information
    api_key = "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"
    pdf_file_path = "IBM_GreenEloan_demo/data/pdf/CTBC_2022_Sustainability_Report_zh3.pdf"
    csv_file_path = "IBM_GreenEloan_demo/data/csv/中國信託_ViolationItems.csv"
    selected_questions = [
                # 第一部分：E/S/G 違規項目
                '請根據資料中 <裁處書發文日期> 判斷近二年該公司是否發生洗錢或資助資恐活動情節重大或導致停工 / 停業者',
                # 第二部分：E/S/G 關鍵作為
                '近一年該公司是否曾獲得外部永續相關獎項',
                # 第三部分：Environmental
                '該公司是否投資於節能或綠色能源相關環保永續之機器設備，或投資於我國綠能產業（如:再生能源電廠）等，或有發行或投資其資金運用於綠色或社會效益投資計畫並具實質效益之永續發展金融商品，並揭露其投資情形及具體效益？',
                # 第三部分：Social
                '該公司是否揭露員工福利政策？（如：保險、育嬰假、退休制度、員工持股、工作者健康促進、在職訓練…等）',
                # 第三部分：Governancce
                '該公司是否已將「股利政策」、「董監事及經理人績效評估與酬金制度」、「員工權益」，揭露於公司網路、年報或永續報告書？']

    # Processing
    os.environ["OPENAI_API_KEY"] = f"{api_key}"
    vectorstore = data_processing(pdf_file_path, csv_file_path)
    questions = selected_questions_list(selected_questions)
    chat_history = chat_chain(vectorstore, questions)

    return chat_history

if __name__ == "__main__":
    main()