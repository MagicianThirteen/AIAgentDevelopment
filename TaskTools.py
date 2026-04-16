#案例一：生成SQL语句的任务建模
#目标：用户描述一个查询目标，由模型生成对应的SQL语句，并返回结构化输出
from openai import OpenAI #这里先要导入OpenAI的库，
from dotenv import load_dotenv
import os
load_dotenv() #加载环境变量
api_key =os.getenv("API_KEY") #从环境变量中获取API密钥
llm = OpenAI(
    api_key=api_key,
    base_url="https://poloai.top/v1"
    )
     #创建一个OpenAI对象实例


#构建任务Prompt
user_instruction="我想查询所有注册时间在2023年之后的用户姓名和邮箱"
prompt=f"""
你是一位数据库专家，请根据以下用户指令生成SQL语句。
要求：
1.表名为users;
2.字段包括name和email;
3.使用标准的SQL语法;
4.输出格式为JSON,字段包括sql和explanation。
指令：{user_instruction}
"""

#调用大模型
response=llm.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0,#这个值越高，ai越有想象力，容易乱来
)

#输出结果
print(response.choices[0].message.content)