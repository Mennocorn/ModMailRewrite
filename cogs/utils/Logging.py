import config
import discord
import datetime as dt


class Logger:

    def __init__(self):
        self.dt = dt
        self.dt.timezone(dt.timedelta(hours=1))

    @staticmethod
    def get_file(channel_id: int) -> str:
        return f'{config.logs}/{channel_id}.txt'

    def get_format(self, user: discord.User):
        return f'{self.dt.datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - {user.name}#{user.discriminator}: '

    def log_message(self, message: discord.Message, user: discord.User):

        with open(self.get_file(message.channel.id), 'a') as log_f:
            log_f.write(f'{self.get_format(user)} "{message.content}"\n')

    def log_event(self, interaction, button):
        with open(self.get_file(interaction.channel.id), 'a') as log_f:
            log_f.write(f'{self.get_format(interaction.user)}{button.custom_id}\n')


logger = Logger()