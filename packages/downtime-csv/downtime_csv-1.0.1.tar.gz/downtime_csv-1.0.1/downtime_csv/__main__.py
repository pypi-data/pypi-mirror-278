#!env python

import aiohttp
import asyncio
import time
import sys

if len(sys.argv) != 2:
    print(f'invalid argument length: {sys.argv[0]} URL', file=sys.stderr)
    sys.exit(1)

url = sys.argv[1]

async def doQuery():
    async with aiohttp.ClientSession() as session:
        tat_start = time.time_ns()
        async with session.get(url) as resp:
            await resp.text()
            tat_end = time.time_ns()
            tat = tat_end - tat_start
            mlsec = int(tat_start % 1000000000 / 1000000)
            print(f'{time.strftime('%X', time.localtime(tat_start/1000000000))}.{str(mlsec).zfill(3)},{int(tat/1000000)},{resp.status}')

async def downtime():
    task_list = []
    for i in range(1500):
        task_list.append(asyncio.create_task(doQuery()))
        await asyncio.sleep(0.2)
    for j in task_list:
        await j

def main():
    asyncio.run(downtime())

if __name__ == '__main__':
    main()
