async def main(rpc, sleep):
    print(1)
    print('step1', await anext(rpc.get_joint_pos()))
    # print(await anext(rpc.run_forward(speed=90, targetPos=[90, -81, 113, -122, 89, 33])))
    # await sleep(10)
    print('step2', await anext(rpc.load(filename='python1.jbi')))
    await sleep(1)
    print('step3', await anext(rpc.run(line=0)))
    await sleep(10)
