import aiohttp
import random
import json
import os
import sys
import asyncio
from pystyle import Colors, Colorate, Center


config = {
    "details": "discord.gg/vast",
    "state": "discord.gg/vast",
    "name": "discord.gg/vast",
}
class Stats:
    online = 0
    total = 0


class Onliner:
    def __init__(self, token) -> None:
        self.token = token
        self.statuses = ["online", "idle", "do not disturb"]

    async def start(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.ws_connect("wss://gateway.discord.gg/?encoding=json&v=8") as ws:
                    async for msg in ws:
                        response = msg.data
                        event = json.loads(response)
                        heartbeat_interval = int(event["d"]["heartbeat_interval"]) / 1000

                        await ws.send_json(
                            {
                                "op": 2,
                                "d": {
                                    "token": self.token,
                                    "properties": {
                                        "$os": sys.platform,
                                        "$browser": "Discord iOS",
                                        "$device": f"{sys.platform} Device",
                                    },
                                    "presence": {
                                        "game": {
                                            "name": config["name"],
                                            "type": 0,
                                            "details": config["details"],
                                            "state": config["state"],
                                        },
                                        "status": random.choice(self.statuses),
                                        "since": 0,
                                        "activities": [],
                                        "afk": False,
                                    },
                                },
                                "s": None,
                                "t": None,
                            }
                        )
                        Stats.online += 1
                        # print("\033[32mOnline\033[0m |", self.token, end="\r")

                        while True:
                            heartbeatJSON = {"op": 1, "token": self.token, "d": 0}
                            await ws.send_json(heartbeatJSON)
                            await asyncio.sleep(heartbeat_interval)
        except Exception as e:
            pass

async def BannerThread(b=False):
    while True:
        if Stats.online == Stats.total: break
        
        os.system("cls||clear")
        print(
            Center.XCenter(
                Colorate.Vertical(
                    Colors.purple_to_blue,
                    """
                        ┬  ┬┌─┐┌─┐┌┬┐  ┌─┐┌┐┌┬  ┬┌┐┌┌─┐┬─┐
                        └┐┌┘├─┤└─┐ │   │ │││││  ││││├┤ ├┬┘
                         └┘ ┴ ┴└─┘ ┴   └─┘┘└┘┴─┘┴┘└┘└─┘┴└─
                            
                          ╭───────────────────────────╮
                          │      Online: %s        │
                          │       Total: %s        │
                          ╰───────────────────────────╯
                """ % (f'{Stats.online:<5}', f'{Stats.total:<5}'),
                )
            )
        )
        await asyncio.sleep(0.1)
    
async def main():
    os.system("cls||clear")
    tasks = []
    Stats.total = len(open("./tokens.txt", "r").readlines())

    asyncio.create_task(BannerThread())
    async with aiohttp.ClientSession() as session:
        for token in open("./tokens.txt", "r").readlines():
            onliner = Onliner(token)
            task = asyncio.create_task(onliner.start())
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
