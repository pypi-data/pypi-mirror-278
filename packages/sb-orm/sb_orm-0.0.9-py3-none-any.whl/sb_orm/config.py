import os
from os import getenv
from dotenv import load_dotenv

load_dotenv()


# 获取环境变量
def env(key):
    return getenv(key)
