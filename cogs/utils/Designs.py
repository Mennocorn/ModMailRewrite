import discord

from cogs.utils.Cache import cache
import config
import os
from cogs.utils.Logging import logger
from datetime import timedelta


class Button(discord.ui.Button):

    async def callback(self, interaction):
        self.disabled = True
        await interaction.response.edit_message(view=self.view)
        await interaction.followup.send(f"You marked this ticket as '{self.custom_id}ED'", ephemeral=True)
        channel_index = cache.get_channel_index(interaction.channel)
        user = await self.view.bot.fetch_user(cache.cache['Guild']['open_tickets'][channel_index]['id'])
        await user.create_dm()
        msg = await user.dm_channel.fetch_message(cache.cache['Guild']['open_tickets'][channel_index]['embed'])
        print(self.label)
        if self.label == 'Receive':
            name = f'{self.label}d'
        elif self.label == 'Process':
            name = f'{self.label}ing'
        else:
            name = f'{self.label}ed'
        embed = msg.embeds[0]
        embed.description = "Status - " + name
        await msg.edit(embed=embed)
        logger.log_event(interaction, self)
        if self.label == 'Dismiss' or self.label == 'Finish':
            del cache.cache['Guild']['open_tickets'][channel_index]
            await interaction.channel.delete()
            await self.archive(interaction)

    @staticmethod
    async def archive(interaction):
        channel = interaction.channel
        path_to_log_file = f'{config.logs}/{channel.id}.txt'
        if not cache.cache['Guild']['archive']:
            os.remove(path_to_log_file)

            return

        await cache.archive_channel.send(f'Log file of {(channel.created_at + timedelta(hours=1)).strftime("%d/%m/%Y %H:%M:%S")}', file=discord.File(path_to_log_file))
        os.remove(path_to_log_file)


class RequestView(discord.ui.View):

    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)
        buttons = ['Receive', 'Process', 'Dismiss', 'Finish']
        types = [discord.ButtonStyle.blurple, discord.ButtonStyle.blurple, discord.ButtonStyle.red, discord.ButtonStyle.green]
        emojis = ['📩', '✏', '❌', '✅']
        for button in range(len(buttons)):
            new_button = Button(label=buttons[button], style=types[button], emoji=emojis[button], custom_id=buttons[button].upper())
            self.add_item(new_button)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        current_open_tickets = [user_id['id'] for user_id in list(cache.cache['Guild']['open_tickets'])]
        if interaction.user.id in current_open_tickets:
            if not interaction.channel.permissions_for(interaction.user).send_messages:
                return await interaction.response.send_message('You cannot do this', ephemeral=True)
            else:
                return True
        else:
            return True

class SetupView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Archive', style=discord.ButtonStyle.green, emoji='✅', custom_id='Archive')
    async def toggle_archive_button_callback(self, interaction, button):
        if button.style is discord.ButtonStyle.green:
            button.style = discord.ButtonStyle.danger
            button.emoji = '❌'
            cache.cache['Guild']['archive'] = False
            await interaction.response.edit_message(view=self)
        else:
            button.style = discord.ButtonStyle.green
            button.emoji = '✅'
            cache.cache['Guild']['archive'] = True
            await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Delete All', style=discord.ButtonStyle.blurple, emoji='👮‍♂️', custom_id='Delete')
    async def add_role_button_callback(self, interaction, button):
        for channel in cache.category.channels:
            await channel.delete()
        await cache.category.delete()
        cache.cache['Guild']['setup'] = False


class ResponseEmbed(discord.Embed):
    pass


