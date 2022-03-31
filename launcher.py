from cogs.utils.Cache import cache
from bot import ModMail
import traceback
import click
import atexit
import asyncio
bot = ModMail()


def run_bot():
    try:
        cache.load_cache()
    except Exception as e:
        click.echo(f'Starting Cache failed!')
        traceback.print_exc()
        return

    bot.run()


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        run_bot()


async def stop_bot():
    await bot.close()


@atexit.register
def exited():
    print('exit')
    cache.make_save()

if __name__ == '__main__':
    main()



