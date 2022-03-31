from discord.ext import commands
from cogs.utils.Designs import SetupView, RequestView, ResponseEmbed
from cogs.utils.Cache import cache
import discord
from typing import Union


class CreateRequest(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.dm_only()
    async def request(self, ctx, *, request):
        ticket = cache.cache["Guild"]["ticket_number"]
        new_channel = await cache.category.create_text_channel(name=f'{ticket} - {ctx.author}')
        await new_channel.set_permissions(ctx.author, read_messages=True, send_messages=False)
        view = RequestView(self.client)
        msg = await new_channel.send(f'{ctx.author.mention} said: "{request}"', view=view)
        embed = ResponseEmbed(title='Your Request', url=msg.jump_url, color=0xDF61B5, description='Status - Not Received')
        msg = await ctx.reply(content=None, embed=embed)
        cache.cache["Guild"]["ticket_number"] += 1
        content_dict = {
            'channel': new_channel.id,
            'id': ctx.author.id,
            'embed': msg.id
        }
        cache.cache['Guild']["open_tickets"].append(content_dict)
        cache.tickets.append(new_channel.id)

    @commands.command()
    async def ping(self, ctx):
        await ctx.reply(f'Pong: {round(self.client.latency*1000)}')


class AdminSetup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def setup(self, ctx):
        cache.category = new_category = await ctx.guild.create_category(name='ModMail', position=0)
        await new_category.set_permissions(ctx.guild.default_role, view_channel=False)
        cache.channel = channel = await new_category.create_text_channel(name='Introduction', position=0)
        cache.archive_channel = archive_channel = await new_category.create_text_channel(name='Archive', position=1)
        view = SetupView()

        await channel.send('Hi', view=view)  # TODO maybe change the message content?
        cache.cache['Guild']['setup'] = True
        cache.cache['Guild']['category_request'] = new_category.id
        cache.cache['Guild']['archive_channel'] = archive_channel.id
        cache.cache['Guild']['introduction_channel'] = channel.id

    @commands.command()
    async def add_mod(self, ctx, role: Union[discord.Role, discord.Member]):
        cache.cache['Guild']['mods'].append(role.id)
        await cache.category.set_permissions(role, view_channel=True)


async def setup(client):
    await client.add_cog(AdminSetup(client))
    await client.add_cog(CreateRequest(client))