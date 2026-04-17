from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()
api_key =os.getenv("API_KEY")
llm = OpenAI(
    api_key=api_key,
    base_url="https://poloai.top/v1")

#构建任务Prompt
instruction="文本：浙江橙龙科技有限公司位于杭州市余杭区五常街道五常大道100号" 
prompt1=f"""
任务说明：从文本中识别并提取公司名称与地址信息。
输出格式：
{{
    "company_name": "公司名称",
    "address": "地址信息"
}}
请处理如下文本：
{instruction}
"""

result=llm.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt1}
    ]
)

print(result.choices[0].message.content)