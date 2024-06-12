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
