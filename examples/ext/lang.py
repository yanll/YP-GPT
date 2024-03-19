class NumberProducerOperator():
    async def streamify(self):
        print('hello')


task = NumberProducerOperator()
task.streamify()
