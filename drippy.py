import json
from uuid import UUID
import discord

import logging
import datetime

from punishment import Punishment
from command import Command


intents = discord.Intents.all()
client = discord.Client(intents=intents)


class EmbedType:
    def __init__(self, type: str):
        self.type = type
        # info, warning, error, punishment, other

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

    async def kick(self, c: Command):
        await self.logging(c, c.message.mentions[0])
        
    async def logging(self, c: Command, punished: discord.Member | None):
        channelid = self.getConfig("logging")
        channel = discord.utils.get(c.message.guild.text_channels, id=channelid)

        if c.info['name'] == "kick":
            reason = c.args
            reason.pop(0)
            reason = " ".join(reason)

            p = Punishment(c, punished, "perm", reason=reason)

            self.addToCase(p.uuid, p.punished)

            embed = discord.Embed(color=0xd30d0d)
            embed.set_author(name=punished.name, icon_url=punished.display_avatar.url)
            embed.add_field(name =f"Punishment nr. {p.uuid}",
            value=f"""**Type**: Kick
            **Duration**: {p.duration}
            **Moderator**: {p.moderator.mention}
            **Time**: {p.time}
            **Reason**: {p.reason}
            """)

            await channel.send(embed=embed)
    
    def getCase(self, u: discord.Member):
        data = json.load(open('cases.json', 'r'))

        try:
            return data[u.name]        
        except KeyError:
            return None

    def addToCase(self, uuid: UUID, u: discord.Member):
        data = json.load(open('cases.json', 'r'))
        
        try:
            data[u.name][str(len(data[u.name]) + 1)] = str(uuid)
        except KeyError:
            data[u.name] = {}
            data[u.name][str(len(data[u.name]) + 1)] = str(uuid)

        json.dump(data, open('cases.json', 'w'), sort_keys=True, indent=4)


    def getConfig(self, value: str):
        data = json.load(open('config.json', 'r'))

        try:
            return data[value]
        except KeyError:
            return None



d = Drippy()

@client.event
async def on_message(message):
    if message.author.bot:
        return

    c = Command(message)
    if not c.getCommand():
        return

    await eval(f"d.{c.info['name']}(c)")


client.run(d.getToken())