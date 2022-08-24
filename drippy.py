import json
import discord

import logging

from command import Command

client = discord.Client(intents=discord.Intents.default())


class Drippy:
    def __init__(self):
        pass

    def getToken(self):
        try:
            data = json.load(open('token.json', 'r'))

            self.token = data['token']
            return self.token
        except:
            data['token'] = ""

            json.dump(data, open('token.json', 'w'))


    @client.event
    async def on_message(message):
        if message.author.bot:
            return

        c = Command(message)
        if not c.getCommand():
            return

        

d = Drippy()

client.run(d.getToken())