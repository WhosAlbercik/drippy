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
        """"
        Returns the token
        """
        try:
            data = json.load(open('token.json', 'r'))

            self.token = data['token']
            return self.token
        except:
            data['token'] = ""

            json.dump(data, open('token.json', 'w'))

    
    
    async def kick(self, c: Command):
        await self.logging(c, c.message.mentions[0])

        await c.message.mentions[0].kick()

    async def case(self, c: Command):
        case = self.getCase(c.message.mentions[0])

        if case == None:
            await c.message.channel.send(f"{c.message.mentions[0].mention} Does not Have any Case History.")
            return

        embed = discord.Embed(color=0x0ee1a2)
        embed.set_author(name=c.message.mentions[0].name, icon_url=c.message.mentions[0].avatar.url)

        str = ""
        for x in case:
            str += f"{x}) " + case[x] + "\n"
        
        embed.add_field(name=f"{c.message.mentions[0].name} Case History", value=str)

        await c.message.channel.send(embed=embed)



    async def logging(self, c: Command, punished: discord.Member):
        """
        Logs a command on the #logs channel and in the punishments.json and cases.json files
        """

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

            dm = await punished.create_dm()
            await dm.send(embed=embed)
            
            await channel.send(embed=embed)
    
    def getCase(self, u: discord.Member):
        """"
        returns the case history as a dictionary, of the given member (u)
        """
        data = json.load(open('json/cases.json', 'r'))

        try:
            return data[u.name]        
        except KeyError:
            return None

    def addToCase(self, uuid: UUID, u: discord.Member):
        """
        Adds the given UUID to the case history of the given user
        """
        data = json.load(open('json/cases.json', 'r'))
        
        try:
            data[u.name][str(len(data[u.name]) + 1)] = str(uuid)
        except KeyError:
            data[u.name] = {}
            data[u.name][str(len(data[u.name]) + 1)] = str(uuid)

        json.dump(data, open('json/cases.json', 'w'), sort_keys=True, indent=4)


    def getConfig(self, value: str):
        """
        returns a value from the config
        """
        data = json.load(open('config.json', 'r'))

        try:
            return data[value]
        except KeyError:
            return None



d = Drippy()

@client.event
async def on_message(message):
    """
    Triggered when a message is sent, anywhere from to the bot, to any channel on the server
    """
    if message.author.bot:
        return

    c = Command(message)
    if c.checkCommand() == None:
        return
    
    elif not c.checkCommand():
        embed = discord.Embed(color=0xd30d0d)
        embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
        embed.add_field(name="Something Went Wrong :x:", value="Check the amount of arguments and your permissions.\nIf that doesn't help try contacting one of the bot developers.")
        await message.channel.send(embed=embed)
        return

    await eval(f"d.{c.info['name']}(c)")


client.run(d.getToken())