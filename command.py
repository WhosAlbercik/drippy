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
        """
        Checks if the command exists and is used in a proper way
        """

        if not self.getCommand():
            return None

        if self.checkPerms() < self.info['permissions'] or not self.checkArgs() or not self.checkMentions():
            return False
        else:
            return True

    def checkArgs(self):
        """
        Checks if the amount of arguments is correct
        """
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
        """
        Checks if the command exists and returns it
        """
        data = json.load(open('commands.json', 'r'))

        if not self.message.content.startswith(self.prefix):
            return False

        try:
            self.info = data[self.name]
            return True
        except:
            for x in data:
                if self.name in data[x]['alias']:
                    self.info = data[x]
                    return True
            else:
                self.info = None
                return False

    def checkPerms(self):
        """
        checks if the command sender has the right permissions
        0 = everyone
        1 = moderator
        2 = admin
        3 = owner
        """
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

    def checkMentions(self):
        """
        Checks if the sent command contains enough mentions
        """
        if self.info['mentions'] == str(len(self.message.mentions)) or self.info['mentions'] == "False":
            return True
        elif "to" in self.info['mentions'] and int(self.info['mentions'][0]) <= len(self.message.mentions) and int(self.info['mentions'][-1]) >= len(self.message.mentions):
            return True
        else:
            return False

    def getConfig(self, value: str):
        """
        Returns the config value (copied from Drippy)
        """
        data = json.load(open('config.json', 'r'))

        try:
            return data[value]
        except KeyError:
            return None