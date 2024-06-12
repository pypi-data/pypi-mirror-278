```js
(async () => {
  const robsdk = require('robusdk')
  const {Coroutine, Sequence, Logger, Awaitable} = require('robusdk')

  const Client = await robsdk({
    url: 'http://192.168.192.168:6680/',
    username: 'admin',
    password: 'elite2014'
  })
  const rpc = Client('RPC')
  const pipeline = Client('PIPELINE')
  const options = {
    repeat: 4,
    delay: 1000
  }

  Logger.info(await rpc.get_joint_pos().next())

  Logger.info(await pipeline.machinePos().next())

  for await (const result of rpc.get_joint_pos()) {
    Logger.info(result)
  }

  for await (const result of pipeline.machinePos()) {
    Logger.info(result)
  }

  Logger.info(await new Coroutine([
    new Sequence(() => rpc.get_joint_pos(), Logger.debug, Logger.error, options),
    new Sequence(() => pipeline.machinePos(), Logger.debug, Logger.error, options),
    new Sequence(() => pipeline.motorSpeed(), Logger.debug, Logger.error, options),
  ]))

  Logger.info(await new Coroutine([
    ...[...Array(4).keys()].map((addr) => new Sequence(() => rpc.getSysVarP({addr}), Logger.debug, Logger.error, options)),
    ...[...Array(4).keys()].map((addr) => new Sequence(() => rpc.getSysVarB({addr}), Logger.debug, Logger.error, options)),
  ]))

  Logger.info(await new Coroutine([
    new Awaitable(() => pipeline(['machinePos', 'machinePose']), Logger.info, Logger.error),
    new Awaitable(() => pipeline(), Logger.info, Logger.error),
  ]))
})()
```

```python
async def future():
  from robusdk import robusdk, Logger, Sequence, Coroutine, Awaitable
  Client = await robusdk(
    url='http://192.168.192.168:6680/',
    username='admin',
    password='elite2014',
  )
  rpc = Client('RPC')
  pipeline = Client('PIPELINE')
  options = {'repeat': 4, 'delay': 1000}

  Logger.info(await anext(rpc.get_joint_pos()))

  Logger.info(await anext(pipeline.machinePos()))

  async for result in rpc.get_joint_pos():
      Logger.info(result)

  async for result in pipeline.machinePos():
      Logger.info(result)

  Logger.info(await Coroutine([
    Sequence(lambda: rpc.get_joint_pos(), Logger.debug, Logger.error, options),
    Sequence(lambda: pipeline.machinePos(), Logger.debug, Logger.error, options),
    Sequence(lambda: pipeline.motorSpeed(), Logger.debug, Logger.error, options),
  ]))

  Logger.info(await Coroutine([
    *list(map(lambda addr: Sequence(lambda: rpc.getSysVarP(addr=addr), Logger.debug, Logger.error, options), range(4))),
    *list(map(lambda addr: Sequence(lambda: rpc.getSysVarB(addr=addr), Logger.debug, Logger.error, options), range(4))),
  ]))

  Logger.info(await Coroutine([
      Awaitable(lambda: pipeline(['machinePos', 'machinePose']), Logger.info, Logger.error),
  ]))

from asyncio import run
run(future())
```
