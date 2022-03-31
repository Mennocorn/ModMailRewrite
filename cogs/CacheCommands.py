from discord.ext import commands
from discord.ext import tasks
from cogs.utils.Cache import cache
import asyncio
import config


class CacheFunction(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.wait_for_check.start()
        self.i = True

    @tasks.loop(minutes=5)
    async def wait_for_check(self):
        self.check_for_save()
        if self.i:
            await self.client.wait_until_ready()
            await self.load_channels()
            self.i = False

    def check_for_save(self):
        # if cache.initial == cache.cache:
        cache.initial = cache.cache
        cache.make_save()

    async def load_channels(self):
        if cache.cache['Guild']['setup']:
            cache.guild = self.client.get_guild(config.guild_id)
            cache.category = cache.guild.get_channel(cache.cache['Guild']['category_request'])
            cache.archive_channel = cache.guild.get_channel(cache.cache['Guild']['archive_channel'])
            cache.channel = cache.guild.get_channel(cache.cache['Guild']['introduction_channel'])
            for ticket in cache.cache['Guild']["open_tickets"]:
                cache.tickets.append(ticket['channel'])

    @commands.command()
    async def save(self, ctx):
        self.check_for_save()
        await ctx.reply('Saved.', delete_after=5)
        await ctx.message.delete()


async def setup(client):
    await client.add_cog(CacheFunction(client))