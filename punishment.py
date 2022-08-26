from datetime import datetime

from command import Command

import discord
import json

import uuid

class Punishment:
    def __init__(self, c: Command, punished: discord.Member, duration: str, reason: str):
        self.punished = punished
        self.moderator = c.message.author

        self.type = c.name
        self.uuid = str(uuid.uuid4())

        self.duration = duration

        self.reason = reason
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        self.addToPunishments()

    def addToPunishments(self):
        """
        Saves the info set in the '__init__' to the punishments.json
        """
        data = json.load(open('json/punishments.json', 'r'))

        uuid = self.uuid

        data[str(self.uuid)] = self.__dict__.copy()

        data[str(uuid)]['moderator'] = self.moderator.id
        data[str(uuid)]['punished'] = self.punished.id


        json.dump(data, open('json/punishments.json', 'w'), sort_keys=True, indent=4)