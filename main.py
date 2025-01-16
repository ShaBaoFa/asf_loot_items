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


async def handle_retry(asf, bot_name, retry_count, current_time, error_message):
    print(f'[{current_time}] Error: {error_message}')
    print(f'Retry attempt {retry_count}/5 for {bot_name}')
    if retry_count < 5:
        wait_time = (10 - retry_count * 2) * 60  # 从8分钟开始，每次减2分钟
        print(f'\n等待重试中... (等待{wait_time//60}分钟)')
        for remaining in range(wait_time, 0, -1):
            print(f'\r剩余等待时间: {remaining} 秒', end='', flush=True)
            time.sleep(1)
        print('\n')


async def main(bots=None):
    config = input('请输入 config 名称:')
    config_data = read_config(config + '.json')
    
    while True:
        async with IPC(ipc=config_data['ipc'], password=config_data['password'], timeout=60) as asf:
            if not bots:
                bot = input('请输入 Bot 名称:')
                resp = await get_bot(asf, bot)
                if resp.success:
                    bots = resp.result
                    
            for bot_name, bot_data in bots.items():
                retry_count = 0
                success = False
                
                while retry_count < 5 and not success:
                    try:
                        result = await command(asf, '!loot^ ' + bot_name +' ' +config_data['items'])
                        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        
                        if result.success and 'failed' not in result.result:
                            print(f'[{current_time}] result: {result.result}')
                            success = True
                        else:
                            retry_count += 1
                            error_msg = result.message if not result.success else result.result
                            await handle_retry(asf, bot_name, retry_count, current_time, error_msg)
                    
                    except Exception as e:
                        retry_count += 1
                        await handle_retry(asf, bot_name, retry_count, current_time, str(e))
                
                if not success:
                    with open(f'{config}FailList.txt', 'a') as f:
                        f.write(bot_name + '\n')
            return


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
