import json

class Command:
    def __init__(self, message):
        self.message = message
        self.prefix = '$'
        
        if not self.message.content.startswith(self.prefix):
            return

        self.name = self.message.content.split('$')[1].split(' ')[0]
        self.args = self.message.content.split('$')[1].split(' ')
        self.args.pop(0)

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