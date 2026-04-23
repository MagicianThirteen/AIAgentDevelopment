#实现一个基于Qwen智能体框架的智能体启动过程，涵盖模型加载、工具注册、
#系统提示词配置、初始化记忆注入、多轮日志追踪、并通过函数调用能力实现工具调度
#agent_startup.py
import logging
import datetime
from typing import List
from qwen_agent import Agent,Tool,ChatMessage
from qwen_agent.llm import QwenLLM
from qwen_agent.tools.base import BaseTool
from qwen_agent.utils import CompletionConfig

#配置日志
logging.basicConfig(
    filename='agent_startup.log',
    level=logging.INFO,
    format='%(asctime)s-%(levelname)s-%(message)s'
)

#初始化工具：当前时间工具
class GetTimeTool(BaseTool):
