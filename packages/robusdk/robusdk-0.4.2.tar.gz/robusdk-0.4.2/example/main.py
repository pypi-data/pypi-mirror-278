async def main():
    Logger.info(await anext(cobot('rpc').get_joint_pos()))
    async for event in stream(Channel.pipeline):
        Logger.info(event.message.root['machine_pos'])
        break
