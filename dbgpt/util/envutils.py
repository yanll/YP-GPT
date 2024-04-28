from dotenv import dotenv_values

env = dotenv_values('../../../config.env')


def getenv(name) -> str:
    v = env.get(name)
    print("获取变量：", "|", name, ":", v, "|")
    return v


print(getenv("TEST_KEY"))
