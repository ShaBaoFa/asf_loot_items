import json
from typing import List, Any

from ASF import IPC
import asyncio
import time


async def command(asf, cmd):
    print(f'running command: {cmd}')
    return await asf.Api.Command.post(body={
        'Command': cmd
    })


async def get_bot(asf, bot):
    return await asf.Api.Bot['botNames'].get(botNames=bot)

def read_config(filename):
    with open(filename, 'r') as f:
        config = json.load(f)
    return config

async def main(bots=None):
    config = input('请输入 config 名称:')
    config_data = read_config(f'{config}.json')
    while True:
        async with IPC(ipc=config_data['ipc'], password=config_data['password'], timeout=60) as asf:
            # 读取 TradeOfferFailedList.txt 文件，获取失败的 Bot 列表
            with open('bananaFailList.txt', 'r') as f:
                bots = [line.strip() for line in f.readlines()]
            if not bots:
                return
            # 遍历每个 Bot
            for bot_name in bots:
                try:
                    result = await command(asf, '!loot^ ' + bot_name + config_data['items'])
                    if result.success:
                        # 打印 当前时间
                        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] result: {result.result}')
                        if 'failed' in result.result:
                            with open(f'{config}FailList.txt', 'a') as f:
                                f.write(bot_name + '\n')
                            time.sleep(600)
                    else:
                        print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] Error: {result.message}')
                        with open(f'{config}FailList.txt', 'a') as f:
                            f.write(bot_name + '\n')
                        time.sleep(600)
                except Exception as e:
                    print(f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] Error: {e}')
                    with open(f'{config}FailList.txt', 'a') as f:
                        f.write(bot_name + '\n')
                    time.sleep(600)
            return


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
