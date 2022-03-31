import discord
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from cogs.utils.Cache import cache
import config
import traceback
from cogs.utils.Logging import logger
from cogs.utils.Designs import SetupView, RequestView, ResponseEmbed
description = f"I am simple ModMail Bot created by {config.owner_name} for {config.guild_name} "

initial_extensions = (
    f'cogs.{"UserCommands"}',
    f'cogs.{"CacheCommands"}',
)


class ModMail(commands.Bot):

    def __init__(self):
        self.persistent_views_added = False
        allowed_mentions = discord.AllowedMentions(roles=True, users=True, replied_user=True)
        super().__init__(
            command_prefix=when_mentioned_or('m!'),
            allowed_mentions=allowed_mentions,
            case_insensitive=True,
            description=description,
            intents=discord.Intents.all(),
            owner_ids=config.owner_id,
        )


    # add error handling here # TODO error handling
    async def on_ready(self):
        print(f'I have gone online, as {self.user.name}#{self.user.discriminator} on {config.guild_name}')
        if not self.persistent_views_added:
            self.add_view(SetupView())
            self.add_view(RequestView(self))
            self.persistent_views_added = True

    async def setup_hook(self):
        for extension in initial_extensions:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load {extension}.')
                traceback.print_exc()

    async def on_message(self, message):

        if message.channel.id in cache.tickets:
            if not message.flags.ephemeral:
                print(message.content)
                channel_index = cache.get_channel_index(message.channel)
                my_user = self.get_user(cache.cache['Guild']['open_tickets'][channel_index]['id'])
                if not message.author.bot:
                    await my_user.create_dm()
                    msg = await my_user.dm_channel.fetch_message(cache.cache['Guild']['open_tickets'][channel_index]['embed'])
                    embed = msg.embeds[0]
                    if len(embed.fields) >= 25:
                        await message.channel.send('Dude what the fuck is wrong with you get a life bro it was one request, doesnt need more than 25 answers')  # TODO think of something better than victim blaming
                    else:
                        embed.add_field(name=f'{message.author.name}#{message.author.discriminator}', value=message.content, inline=False)
                        await msg.edit(embed=embed)
                    my_user = message.author
                logger.log_message(message, my_user)
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_guild_join(self, guild):
        if guild.id != config.guild_id:
            await guild.leave()

    async def invoke(self, ctx):
        if ctx.command is not None and 'setup' not in ctx.message.content and not cache.cache['Guild']['setup']:
            print('caught by setup check')
            await ctx.send('Please setup the bot first.')
            return
        await super().invoke(ctx)

    async def close(self):
        await super().close()

    def run(self):
        try:
            super().run(config.token, reconnect=True)
        except Exception as e:
            print(f'Running failed with: {e}')
            traceback.print_exc()





