import json
import discord

import logging

from command import Command


intents = discord.Intents.all()
client = discord.Client(intents=intents)


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

    def kick(self, command: Command):
        return
        
         

d = Drippy()

@client.event
async def on_message(message):
    if message.author.bot:
        return

    c = Command(message)
    if not c.getCommand():
        return

    eval(f"d.{c.info['name']}(c)")


client.run(d.getToken())