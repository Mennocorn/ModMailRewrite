from cogs.utils.errors.cache import NotAJsonFile
from discord.ext import commands


def is_json(file: str):
    if file.endswith('.json'):
        return True
    else:
        raise NotAJsonFile