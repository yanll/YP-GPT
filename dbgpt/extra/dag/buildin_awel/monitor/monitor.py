from dbgpt.extra.dag.buildin_awel.monitor.monitor2 import monitor2
from dbgpt.extra.dag.buildin_awel.monitor.monitor4 import monitor4


def main():
    alert_list = []
    alert_list += monitor2()
    alert_list += monitor4()
    return alert_list

def main2():
    return monitor2()

# data = main()
# print("数据",data)