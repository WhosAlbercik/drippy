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
        
        if c.args[0].startswith('<'):
            case = self.getCase(c.message.mentions[0])

            if case == None:
                await c.message.channel.send(f"{c.message.mentions[0].mention} Does not Have any Case History.")
                return

            embed = discord.Embed(color=0x0ee1a2)
            embed.set_thumbnail(url=c.message.mentions[0].avatar.url)
            embed.set_author(name=c.message.mentions[0].name, icon_url=c.message.mentions[0].avatar.url)

            str = ""
            count = 1
            for x in case:
                str += f"{count}) **{self.getPunishment(x)['type']}** {x} \n"
                count += 1

            if str == "":
                str = "User has no Case History"

            embed.add_field(name=f"{c.message.mentions[0].name} Case History", value=str)
            
            await c.message.channel.send(embed=embed)
            return
        
        else:
            punishment = self.getPunishment(c.args[0])

            if punishment == None:
                await c.message.channel.send("The uuid provided is not in the database :x:. Please make sure you provided the correct uuid")
                return
            
            punished = discord.utils.get(c.message.guild.members, id=punishment['punished'])
            moderator = discord.utils.get(c.message.guild.members, id=punishment['moderator'])


            embed = discord.Embed(color=0x0ee1a2)
            embed.set_thumbnail(url=punished.avatar.url)
            embed.set_author(name=punished.name, icon_url=punished.avatar.url)
            embed.add_field(name=f"Punishment nr. {c.args[0]}",
            value=f"""**duration:** {punishment['duration']}
        **moderator:** {moderator.mention}
        **punished:** {punished.mention}
        **reason:** {punishment['reason']}
        **time** {punishment['time']}
        **type** {punishment['type']}
        **uuid** {punishment['uuid']}""")

            await c.message.channel.send(embed=embed)
            return

    async def warn(self, c: Command):
        await self.logging(c, c.message.mentions[0])



    async def delpunishment(self, c: Command):
        punishment = self.getPunishment(c.args[0])

        if punishment == None:
            await c.message.channel.send("The uuid provided is not in the database :x:\nPlease make sure you provided the correct uuid")
            return

        self.delPunishment(punishment['uuid'])

        punished = discord.utils.get(c.message.guild.members, id=punishment['punished'])

        

        case = self.getCase(punished)

        embed = discord.Embed(title="Punishment has been deleted", color=0x26ed83)
        embed.set_thumbnail(url=punished.avatar.url)
        embed.set_author(name=punished.name, icon_url=punished.avatar.url)

        str = ""
        count = 1
        try:
            for x in case:
                str += f"{count}) **{self.getPunishment(x)['type']}** {x} \n"
                count += 1  

        except TypeError or case == []:
            str = "User Has no Case History"
    
        embed.add_field(name=f"{punished.name} new Case History", value=str)
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
            embed = discord.Embed(color=0xd30d0d)

    
        elif c.info['name'] == "warn":
            reason = c.args
            reason.pop(0)
            reason = " ".join(reason)

            p = Punishment(c, punished, "perm", reason=reason)

            embed = discord.Embed(color=0xedea26)


        self.addToCase(p.uuid, p.punished)

        embed.set_thumbnail(url=punished.display_avatar.url)
        embed.set_author(name=punished.name, icon_url=punished.display_avatar.url)
        embed.add_field(name =f"Punishment nr. {p.uuid}",
        value=f"""**Type**: {p.type}
            **Duration**: {p.duration}
            **Moderator**: {p.moderator.mention}
            **Time**: {p.time}
            **Reason**: {p.reason}""")

        try:
            dm = await punished.create_dm()
            await dm.send(embed=embed)
        except:
            pass

        await channel.send(embed=embed)
        await c.message.channel.send(embed=embed)
        return

    def getCase(self, u: discord.Member):
        """"
        returns the case history as a dictionary, of the given member (u)
        """
        data = json.load(open('json/cases.json', 'r'))

        try:
            return data[str(u.id)]        
        except KeyError:
            return None

    def addToCase(self, uuid: UUID, u: discord.Member):
        """
        Adds the given UUID to the case history of the given user
        """
        data = json.load(open('json/cases.json', 'r'))
        
        try:
            data[str(u.id)].append(str(uuid))
        except KeyError:
            data[str(u.id)] = []
            data[str(u.id)].append(str(uuid))

        json.dump(data, open('json/cases.json', 'w'), sort_keys=True, indent=4)

    def getPunishment(self, uuid: UUID):
        """
        Returns the punishment data labeled with the given uuid
        """

        data = json.load(open('json/punishments.json', 'r'))
        try:
            return data[str(uuid)]
        except KeyError:
            return None

    def delPunishment(self, uuid: UUID):
        """
        Deletes the punishment data labeled with the given uuid
        """
        datap = json.load(open('json/punishments.json', 'r'))
       
        datac = json.load(open('json/cases.json', 'r'))

        try:
            if uuid in datac[str(datap[uuid]['punished'])]:
                datac[str(datap[uuid]['punished'])].remove(uuid)
            else:
                raise KeyError
        except KeyError:
            return False
        
        
        if datac[str(datap[uuid]['punished'])] == []:
            del datac[str(datap[uuid]['punished'])]

        try:
            del datap[str(uuid)]
        except KeyError:
            return False

        json.dump(datap, open('json/punishments.json', 'w'), sort_keys=True, indent=4)
        json.dump(datac, open('json/cases.json', 'w'), sort_keys=True, indent=4)

       
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