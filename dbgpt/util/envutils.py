from dotenv import dotenv_values

env = dotenv_values('../../../config.env')


def getenv(name) -> str:
    return env.get(name)


print(getenv("TEST_KEY"))
