from dotenv import dotenv_values
import os

env = dotenv_values(os.getenv("ENV_CONFIG_FILE"))


def getenv(name) -> str:
    v = env.get(name)
    print("获取变量：", "|", name, ":", v, "|")
    return v


print(getenv("TEST_KEY"))
