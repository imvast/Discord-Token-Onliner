import aiohttp
import random
import json
import os
import sys
import asyncio
from pystyle import Colors, Colorate, Center

DISCORD_URL = "wss://gateway.discord.gg/?encoding=json&v=8"
DEFAULT_GAME_NAME = "discord.gg/vast"
DEFAULT_GAME_DETAILS = "discord.gg/vast"
DEFAULT_GAME_STATE = "discord.gg/vast"

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
                async with session.ws_connect(DISCORD_URL) as ws:
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
                                            "name": DEFAULT_GAME_NAME,
                                            "type": 0,
                                            "details": DEFAULT_GAME_DETAILS,
                                            "state": DEFAULT_GAME_STATE,
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

                        while True:
                            heartbeatJSON = {"op": 1, "token": self.token, "d": 0}
                            await ws.send_json(heartbeatJSON)
                            await asyncio.sleep(heartbeat_interval)
        except Exception as e:
            print(f"An error occurred: {e}")

async def banner_thread():
    while True:
        if Stats.online == Stats.total:
            break
        
        os.system("cls||clear")
        banner = f"""
            ┬  ┬┌─┐┌─┐┌┬┐  ┌─┐┌┐┌┬  ┬┌┐┌┌─┐┬─┐
            └┐┌┘├─┤└─┐ │   │ │││││  ││││├┤ ├┬┘
             └┘ ┴ ┴└─┘ ┴   └─┘┘└┘┴─┘┴┘└┘└─┘┴└─
            
          ╭───────────────────────────╮
          │      Online: {Stats.online:<5}        │
          │       Total: {Stats.total:<5}        │
          ╰───────────────────────────╯
        """
        print(Center.XCenter(Colorate.Vertical(Colors.purple_to_blue, banner)))
        await asyncio.sleep(0.1)

async def main():
    os.system("cls||clear")
    tasks = []

    with open("./tokens.txt", "r") as tokens_file:
        tokens = [line.strip() for line in tokens_file]

    Stats.total = len(tokens)

    asyncio.create_task(banner_thread())
    async with aiohttp.ClientSession() as session:
        for token in tokens:
            onliner = Onliner(token)
            task = asyncio.create_task(onliner.start())
            tasks.append(task)

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
