import json

import discord

class Command:
    def __init__(self, message):
        self.message = message
        self.prefix = '$'
        
        if not self.message.content.startswith(self.prefix):
            return

        self.name = self.message.content.split('$')[1].split(' ')[0]
        self.args = self.message.content.split('$')[1].split(' ')
        self.args.pop(0)

    def checkCommand(self):
        if not self.getCommand():
            return None

        if self.checkPerms() < self.info['permissions'] or not self.checkArgs():
            return False
        else:
            return True

    def checkArgs(self):
        if "min" in self.info['args']:
            argCount = int(self.info['args'][0])

            if len(self.args) < argCount:
                return False
            else:
                return True

        elif "maks" in self.info['args']:
            argCount = int(self.info['args'][0])

            if len(self.args) > argCount:
                return False
            else:
                return True

        else:
            argCount = int(self.info['args'])

            if len(self.args) != argCount:
                return False
            else:
                return True

    def getCommand(self):
        data = json.load(open('commands.json', 'r'))

        if not self.message.content.startswith(self.prefix):
            return False

        try:
            self.info = data[self.name]
            return True
        except KeyError:
            self.info = None
            return False

    def checkPerms(self):
        moderator = discord.utils.get(self.message.guild.roles, id=self.getConfig("moderator"))
        admin = discord.utils.get(self.message.guild.roles, id=self.getConfig("admin"))

        if moderator in self.message.author.roles:
            return 1
        elif admin in self.message.author.roles:
            return 2
        elif self.message.author.id == self.message.guild.owner_id:
            return 3
        else:
            return 0

    def getConfig(self, value: str):
        data = json.load(open('config.json', 'r'))

        try:
            return data[value]
        except KeyError:
            return None