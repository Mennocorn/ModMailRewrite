import json
import cogs.utils.checks as check
import config


class Cache:
    def __init__(self, file: str):
        self.cache = None
        self.initial = None
        self.category = None
        self.archive_channel = None
        self.guild = None
        self.channel = None
        self.tickets = []
        check.is_json(file)
        self.file = file

    def load_cache(self):
        print('loaded cache')
        with open(self.file) as data_file:
            self.cache = json.load(data_file)
            self.initial = self.cache

    def make_save(self):
        with open(self.file, 'w') as save_file:
            json.dump(self.cache, save_file, indent=4)

    def get_channel_index(self, channel):
        return self.tickets.index(channel.id)


cache = Cache(config.data)