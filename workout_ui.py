from decouple import config
from interactions import (SlashContext, OptionType, Client, SlashCommand, slash_option, AutocompleteContext, listen)
import traceback
from interactions.api.events import CommandError
import os
from json import dump as json_dump


@listen()
async def on_ready():
    """Lets the console know when the bot is online."""
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

    # Make sure the database file is already there. If it's not, create it
    if not os.path.isfile(config("FILENAME")) or not os.path.isfile(config("FILENAME")):
        with open(config("FILENAME"), 'w') as new_json:
            json_dump({}, new_json)


@listen(CommandError, disable_default_listeners=True)  # tell the dispatcher that this replaces the default listener
async def on_command_error(event: CommandError):
    """Listens for any errors in slash commands. If an error is raised, this listener will catch it and store all the
    error messages in event.error. These errors are sent to the person who used the slash command as an ephemeral msg.

    :param event: (object) contains information about the interaction
    """
    traceback.print_exception(event.error)
    if not event.ctx.responded:
        errors = ''
        if event.error.args[0]:
            errors = '\nAlso! '.join(event.error.args)
        await event.ctx.send('Error! ' + errors, ephemeral=True)


base_command = SlashCommand(
    name="workout",
    description="Tracks workout data for server members"
)

# -------------------------------------------------------------------------------------------------------------------- #


@base_command.subcommand(sub_cmd_name="schedule_routine",
                         sub_cmd_description="Create a workout and schedule out which days you'll do it")
@slash_option(name="workout_name", description="What should this workout routine be called?",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="workout_day_1", description="Schedule a workout for this day every week",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="workout_day_2", description="Schedule a workout for this day every week",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="workout_day_3", description="Schedule a workout for this day every week",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="workout_day_4", description="Schedule a workout for this day every week",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="workout_day_5", description="Schedule a workout for this day every week",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="workout_day_6", description="Schedule a workout for this day every week",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="workout_day_7", description="Schedule a workout for this day every week",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="muscle_groups", description="Which muscle group(s) will the workout work out?",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="weights_used", description="Which weights will the workout use?",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="tutorial_url", description="A link to a tutorial that explains how to do the workout",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="image_url", description="A link to an image or gif to be shown with relevant messages",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="show_everyone", description="Want the post to be visible to everyone?",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
async def schedule_routine(ctx: SlashContext, workout_name,
                           workout_day_1=None, workout_day_2=None, workout_day_3=None,
                           workout_day_4=None, workout_day_5=None, workout_day_6=None, workout_day_7=None,
                           muscle_groups=None, weights_used=None, tutorial_url=None, image_url=None,
                           show_everyone=False):
    msg = schedule_routine_main(user=ctx.author,
                                workout_name=workout_name,
                                workout_day_1=workout_day_1,
                                workout_day_2=workout_day_2,
                                workout_day_3=workout_day_3,
                                workout_day_4=workout_day_4,
                                workout_day_5=workout_day_5,
                                workout_day_6=workout_day_6,
                                workout_day_7=workout_day_7,
                                muscle_groups=muscle_groups,
                                weights_used=weights_used,
                                tutorial_url=tutorial_url,
                                image_url=image_url)

    await ctx.send(msg, ephemeral=not show_everyone)


@schedule_routine.autocomplete("workout_day_1")
@schedule_routine.autocomplete("workout_day_2")
@schedule_routine.autocomplete("workout_day_3")
@schedule_routine.autocomplete("workout_day_4")
@schedule_routine.autocomplete("workout_day_5")
@schedule_routine.autocomplete("workout_day_6")
@schedule_routine.autocomplete("workout_day_7")
async def days_of_the_week_autocomplete(ctx: AutocompleteContext):
    """Fetches a list of days from Monday to Friday so you can pick which days you want to schedule your workout for.

    :param ctx: (object) contains information about the interaction
    """
    # Fetch the days of the week. Make sure you respond within three seconds
    days_of_the_week = [{'name': 'Mondays', 'value': 'Monday'},
                        {'name': 'Tuesdays', 'value': 'Tuesday'},
                        {'name': 'Wednesdays', 'value': 'Wednesday'},
                        {'name': 'Thursdays', 'value': 'Thursday'},
                        {'name': 'Fridays', 'value': 'Friday'},
                        {'name': 'Saturdays', 'value': 'Saturday'},
                        {'name': 'Sundays', 'value': 'Sunday'}]
    await ctx.send(choices=days_of_the_week)

# -------------------------------------------------------------------------------------------------------------------- #


@base_command.subcommand(sub_cmd_name="report_unscheduled",
                         sub_cmd_description="Report a workout routine you didn't schedule ahead of time")
@slash_option(name="workout_name", description="What should this workout routine be called?",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="show_everyone", description="Want the post to be visible to everyone?",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="muscle_groups", description="Which muscle group(s) did the workout work out?",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="weights_used", description="Which weights did the workout use?",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="tutorial_url", description="A link to a tutorial that explains how to do the workout",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="image_url", description="A link to an image or gif to be shown with relevant messages",
              opt_type=OptionType.STRING, required=False)
async def report_unscheduled(ctx: SlashContext, workout_name,
                             muscle_groups=None, weights_used=None, tutorial_url=None, image_url=None,
                             show_everyone=False):
    msg = report_unscheduled_main(user=ctx.author,
                                  workout_name=workout_name,
                                  muscle_groups=muscle_groups,
                                  weights_used=weights_used,
                                  tutorial_url=tutorial_url,
                                  image_url=image_url)

    await ctx.send(msg, ephemeral=not show_everyone)


if __name__ == "__main__":
    # Set the cwd to the directory where this file lives
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Define and start the bot
    bot = Client(token=config("BOT_TOKEN"))
    bot.start()
