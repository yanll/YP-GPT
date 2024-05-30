from dbgpt.extra.dag.buildin_awel.monitor.monitor2 import Monitor2
from dbgpt.extra.dag.buildin_awel.monitor.monitor3 import monitor3
from dbgpt.extra.dag.buildin_awel.monitor.monitor4 import monitor4
from dbgpt.extra.dag.buildin_awel.monitor.monitor1bystat import Monitor1ByStat
from dbgpt.extra.dag.buildin_awel.monitor.monitor1bypayer import Monitor1ByPayer

def main():
    alert_list = []
    try:
        monitor = Monitor1ByStat()
        alert_list += monitor.run()
    except Exception as e:
        print('监控一(商户签约名维度)运行失败')
    try:
        monitor = Monitor1ByPayer()
        alert_list += monitor.run()
    except Exception as e:
        print('监控一(付方签约名维度)运行失败')

    try:
        monitor = Monitor2()
        alert_list += monitor.run()
    except Exception as e:
        print('监控二运行失败')
    alert_list += monitor3()
    alert_list += monitor4()
    return alert_list


# def main1():
#     return monitor1()
# def main2():
#     return monitor2()
def main3():
    return monitor3()
def main4():
    return monitor4()


# data = main()
# print("数据",data)