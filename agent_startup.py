# agent_startup.py
import logging
import datetime
from typing import List
from dotenv import load_dotenv
import os

from qwen_agent.agents import Assistant
from qwen_agent.tools import BaseTool

# ========================
# 环境变量
# ========================
load_dotenv()
api_key = os.getenv("qianwen_apikey")

# ========================
# 日志配置
# ========================
logging.basicConfig(
    filename='agent_startup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# ========================
# 工具1：获取时间
# ========================
class GetTimeTool(BaseTool):
    name = "get_time"
    description = "获取当前系统时间"

    def call(self, params=None, **kwargs):
        logging.info("调用当前时间工具")
        now = datetime.datetime.now()
        return now.strftime("当前时间是：%Y年%m月%d日 %H:%M:%S")

# ========================
# 工具2：启动检查
# ========================
class StartupCheckTool(BaseTool):
    name = "startup_check"
    description = "执行智能体启动时的系统检查任务"

    def call(self, params=None, **kwargs):
        logging.info("调用系统初始化检查工具")
        checks = ["模型加载完成", "工具已注册", "记忆注入成功", "上下文初始化完成"]
        return "系统初始化检查通过：" + ",".join(checks)

# ========================
# 构建 Agent
# ========================
def build_agent() -> Assistant:
    logging.info("启用Agent构建流程")
    tools: List[BaseTool] = [GetTimeTool(), StartupCheckTool()]

    llm_config = {
        "model": "qwen-turbo",
        #"api_key": api_key,#这两个apikey和url都可以不要
        #"base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "temperature": 0.2
    }

    agent = Assistant(
        llm=llm_config,
        function_list=tools,
        system_message="你是一位系统智能体助手，负责初始化流程，工具检查与运行日志监控"
    )
    return agent

# ========================
# 万能提取文字（修复版）
# ========================
# ========================
# 【核心】获取最终完整消息（不显示流式）
# ========================
def get_full_response(agent, prompt):
    messages = [{"role": "user", "content": prompt}]
    
    # 遍历流式，但不输出！只收集最后结果
    full_response = None
    for msg in agent.run(messages):
        full_response = msg  # 只保留最后一条完整数据
    
    # 从结果里找 function 的返回值（你要的文字）
    for item in full_response:
        if item.get("role") == "function":#这里的还可以改成助手
            return item["content"]
    return ""

# ========================
# 启动流程
# ========================
def run_startup_sequence():
    agent = build_agent()

    # 系统检查
    messages = [{"role": "user", "content": "请执行一次系统检查"}]
    #res = agent.run(messages)
#     res = agent.run(messages)

# for msg in res:
#     print(msg) 想知道全部的结果用这个
    res1 = get_full_response(agent, "请执行一次系统检查")
    print(">> 系统检查响应：", res1)

    #获取时间
    messages1 = [{"role": "user", "content": "请告诉我现在几点"}]
    #res2 = agent.run(messages1)
    res2 = get_full_response(agent, "请告诉我现在几点")
    print(">> 当前时间响应：", res2)
    print("\n🎉 智能体启动成功！全程使用 agent.run()！")

# ========================
# 主入口
# ========================
if __name__ == "__main__":
    run_startup_sequence()