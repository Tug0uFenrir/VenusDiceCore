import requests
from bs4 import BeautifulSoup


def baidu_baike_search(query):
    url = f"https://baike.baidu.com/search/word?word={requests.utils.quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }

    # 发送请求
    response = requests.get(url, headers=headers)
    result=''''''
    if response.status_code == 200:
        # 获取页面内容
        html_content = response.text

        # 提取内容摘要
        summaries = extract_summaries(html_content)
        print("内容摘要：\n", summaries)
        result+="内容摘要:\n"+summaries

        # 提取具体介绍内容
        detailed_introduction = extract_detailed_introduction(html_content)
        print("详细介绍内容:\n", detailed_introduction)
        result+="详细内容介绍:\n"+detailed_introduction

        # 提取表格内容
        markdown_table = extract_table_content(html_content)
        print("表格内容:\n", markdown_table)
        result+="表格内容\n"+markdown_table

        return result

    else:
        print(f"请求失败，状态码：{response.status_code}")
        return response.status_code


def extract_summaries(html_content):
    """提取内容摘要部分"""
    soup = BeautifulSoup(html_content, 'html.parser')
    summaries = soup.find_all("div", class_="para_G3_Os summary_oSgaA MARK_MODULE")

    full_summary = ''
    for summary in summaries:
        text = summary.get_text(separator=' ', strip=True)
        if "播报" not in text and "编辑" not in text:
            full_summary += text + ' '

    return full_summary.strip() if full_summary else "未找到相关摘要内容。"


def extract_detailed_introduction(html_content):
    """提取具体介绍内容"""
    soup = BeautifulSoup(html_content, 'html.parser')
    content_div = soup.find("div", class_=["J-lemma-content","paraTitle_igGmY level-1_utOLc","anchorList_kqLvv"])

    if content_div:
        introduction = content_div.get_text(separator=' ', strip=True)
        introduction = ' '.join([text for text in introduction.split() if "播报" not in text and "编辑" not in text])
        return introduction
    return "未找到相关详细介绍内容。"


def extract_table_content(html_content):
    """提取表格内容并转换为Markdown格式"""
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all("div", class_="moduleTable_J_MrI")

    markdown_tables = []

    for table in tables:
        table_data = table.find("table")
        if table_data:
            rows = table_data.find_all("tr")
            markdown_table = []
            for row in rows:
                cells = row.find_all("td")
                row_data = []
                for cell in cells:
                    # 获取文本内容并去除多余的空格
                    cell_text = cell.get_text(separator=' ', strip=True)
                    row_data.append(cell_text)
                markdown_table.append(row_data)

            # 格式化Markdown表格
            if markdown_table:
                markdown_tables.append(convert_to_markdown(markdown_table))

    return "\n\n".join(markdown_tables) if markdown_tables else "未找到表格内容。"


def convert_to_markdown(table_data):
    """将表格数据转换为Markdown格式字符串"""
    markdown = []
    for row in table_data:
        markdown.append("| " + " | ".join(row) + " |")

    # 添加分隔行
    header_length = len(table_data[0])
    separator = "| " + " | ".join(['---'] * header_length) + " |"
    markdown.insert(1, separator)

    return "\n".join(markdown)



