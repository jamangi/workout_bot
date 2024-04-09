from decouple import config
from interactions import (SlashContext, OptionType, Client, SlashCommand,
                          slash_option, SlashCommandChoice, AutocompleteContext, listen)
import traceback
from interactions.api.events import CommandError
import os
from json import dump as json_dump

from workout_main import (schedule_routine_main, report_scheduled_main, report_unscheduled_main, edit_workout_main,
                          edit_report_main)
from workout_quickfetches import (reports_years_quickfetch, reports_months_quickfetch, reports_days_quickfetch,
                                  reports_by_day_quickfetch, fields_in_report_quickfetch, workouts_quickfetch)


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
"""schedule_routine"""


@base_command.subcommand(sub_cmd_name="schedule_routine",
                         sub_cmd_description="Create a workout and schedule out which days you'll do it")
@slash_option(name="workout_name", description="What should this workout routine be called?",
              opt_type=OptionType.STRING, required=True, max_length=79)
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
@slash_option(name="muscle_group", description="Which muscle group(s) will the workout work out?",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="weights_used", description="Which weights will the workout use?",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="tutorial_url", description="A link to a tutorial that explains how to do the workout",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="image_url", description="A link to an image or gif to be shown with relevant messages",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="show_everyone", description="Want the post to be visible to everyone?",
              opt_type=OptionType.BOOLEAN, required=False)
async def schedule_routine(ctx: SlashContext, workout_name,
                           muscle_group=None, weights_used=None, tutorial_url=None, image_url=None,
                           workout_day_1=None, workout_day_2=None, workout_day_3=None,
                           workout_day_4=None, workout_day_5=None, workout_day_6=None, workout_day_7=None,
                           show_everyone=False):
    msg = schedule_routine_main(user=ctx.author,
                                workout_name=workout_name,
                                muscle_group=muscle_group,
                                weights_used=weights_used,
                                tutorial_url=tutorial_url,
                                image_url=image_url,
                                workout_day_1=workout_day_1,
                                workout_day_2=workout_day_2,
                                workout_day_3=workout_day_3,
                                workout_day_4=workout_day_4,
                                workout_day_5=workout_day_5,
                                workout_day_6=workout_day_6,
                                workout_day_7=workout_day_7,)

    await ctx.send(msg, ephemeral=not show_everyone)

# -------------------------------------------------------------------------------------------------------------------- #
"""report_scheduled"""


@base_command.subcommand(sub_cmd_name="report_scheduled",
                         sub_cmd_description="Report a workout routine you've followed according to schedule")
@slash_option(name="workout_name", description="Which scheduled workout would you like to submit a report for?",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
@slash_option(name="completion", description="What should this unscheduled workout be called?",
              opt_type=OptionType.STRING, required=True,
              choices=[SlashCommandChoice(name='complete', value='complete'),
                       SlashCommandChoice(name='partially complete', value='partially_complete'),
                       SlashCommandChoice(name='skipped', value='skipped')])
@slash_option(name="comment", description="Is there anything you'd like to note about how the workout session went?",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="show_everyone", description="Want the post to be visible to everyone?",
              opt_type=OptionType.BOOLEAN, required=False)
async def report_scheduled(ctx: SlashContext, workout_name, completion, comment=None, show_everyone=False):
    msg = report_scheduled_main(user=ctx.author,
                                workout_id=workout_name,
                                completion=completion,
                                comment=comment)

    await ctx.send(msg, ephemeral=not show_everyone)

# -------------------------------------------------------------------------------------------------------------------- #
"""report_unscheduled"""


@base_command.subcommand(sub_cmd_name="report_unscheduled",
                         sub_cmd_description="Report a workout routine you didn't schedule ahead of time")
@slash_option(name="workout_name", description="What should this unscheduled workout be called?",
              opt_type=OptionType.STRING, required=True, max_length=79)
@slash_option(name="muscle_group", description="Which muscle group(s) did the workout work out?",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="weights_used", description="Which weights did the workout use?",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="tutorial_url", description="A link to a tutorial that explains how to do the workout",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="image_url", description="A link to an image or gif to be shown with relevant messages",
              opt_type=OptionType.STRING, required=False)
@slash_option(name="show_everyone", description="Want the post to be visible to everyone?",
              opt_type=OptionType.BOOLEAN, required=False)
async def report_unscheduled(ctx: SlashContext, workout_name,
                             muscle_group=None, weights_used=None, tutorial_url=None, image_url=None,
                             show_everyone=False):
    msg = report_unscheduled_main(user=ctx.author,
                                  workout_name=workout_name,
                                  muscle_group=muscle_group,
                                  weights_used=weights_used,
                                  tutorial_url=tutorial_url,
                                  image_url=image_url)

    await ctx.send(msg, ephemeral=not show_everyone)

# -------------------------------------------------------------------------------------------------------------------- #
"""edit_workout"""


@base_command.subcommand(sub_cmd_name="edit_workout",
                         sub_cmd_description="Edit a scheduled workout routine")
@slash_option(name="workout_name", description="Which workout would you like to edit?",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
@slash_option(name="field_to_change", description="Which field within the report would you like to change?",
              opt_type=OptionType.STRING, required=True,
              choices=[SlashCommandChoice(name='workout name', value='workout_name'),
                       SlashCommandChoice(name='muscle groups', value='muscle_groups'),
                       SlashCommandChoice(name='weights used', value='weights_used'),
                       SlashCommandChoice(name='tutorial url', value='tutorial_url'),
                       SlashCommandChoice(name='image url', value='img_url')])
@slash_option(name="new_value", description="What should the field be changed to? (leave blank if you only want to "
                                            "change the date)", opt_type=OptionType.STRING, required=False)
@slash_option(name="new_schedule_day_1", description="Want to change the schedule? Input it here, or leave this "
                                                     "unfilled to keep the same schedule.",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="new_schedule_day_2", description="Want to change the schedule? Input it here, or leave this "
                                                     "unfilled to keep the same schedule.",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="new_schedule_day_3", description="Want to change the schedule? Input it here, or leave this "
                                                     "unfilled to keep the same schedule.",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="new_schedule_day_4", description="Want to change the schedule? Input it here, or leave this "
                                                     "unfilled to keep the same schedule.",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="new_schedule_day_5", description="Want to change the schedule? Input it here, or leave this "
                                                     "unfilled to keep the same schedule.",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="new_schedule_day_6", description="Want to change the schedule? Input it here, or leave this "
                                                     "unfilled to keep the same schedule.",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="new_schedule_day_7", description="Want to change the schedule? Input it here, or leave this "
                                                     "unfilled to keep the same schedule.",
              opt_type=OptionType.STRING, required=False, autocomplete=True)
@slash_option(name="show_everyone", description="Want the post to be visible to everyone?",
              opt_type=OptionType.BOOLEAN, required=False)
async def edit_workout(ctx: SlashContext, workout_name, field_to_change, new_value=None, new_schedule_day_1=None,
                       new_schedule_day_2=None, new_schedule_day_3=None, new_schedule_day_4=None,
                       new_schedule_day_5=None, new_schedule_day_6=None, new_schedule_day_7=None,
                       show_everyone=False):
    msg = edit_workout_main(user=ctx.author,
                            workout_name=workout_name,
                            field_to_change=field_to_change,
                            new_value=new_value,
                            new_schedule_day_1=new_schedule_day_1,
                            new_schedule_day_2=new_schedule_day_2,
                            new_schedule_day_3=new_schedule_day_3,
                            new_schedule_day_4=new_schedule_day_4,
                            new_schedule_day_5=new_schedule_day_5,
                            new_schedule_day_6=new_schedule_day_6,
                            new_schedule_day_7=new_schedule_day_7,)

    await ctx.send(msg, ephemeral=not show_everyone)

# -------------------------------------------------------------------------------------------------------------------- #
"""edit_report"""


@base_command.subcommand(sub_cmd_name="edit_report",
                         sub_cmd_description="Edit the report for a past workout session")
@slash_option(name="year", description="What year did this session take place? (or input the word latest)",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
@slash_option(name="month", description="What month did this session take place?",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
@slash_option(name="day", description="What day did this session take place?",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
@slash_option(name="report_to_edit", description="What report would you like to edit?",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
@slash_option(name="field_to_change", description="Which field within the report would you like to change?",
              opt_type=OptionType.STRING, required=True, autocomplete=True)
@slash_option(name="new_value", description="What should it be changed to?",
              opt_type=OptionType.STRING, required=True)
@slash_option(name="show_everyone", description="Want the post to be visible to everyone?",
              opt_type=OptionType.BOOLEAN, required=False)
async def edit_report(ctx: SlashContext, report_to_edit, field_to_change, new_value,
                      show_everyone=False):
    # Remember to constrain the date within the autocomplete so that future dates default to latest and dates before
    # the first recorded report are default to the oldest reports
    msg = edit_report_main(user=ctx.author,
                           report_id=report_to_edit,
                           field=field_to_change,
                           new_value=new_value)

    await ctx.send(msg, ephemeral=not show_everyone)


@edit_report.autocomplete("year")
async def reports_years_autocomplete(ctx: AutocompleteContext):
    """Fetches a list of years in which the user has completed workout sessions.

    :param ctx: (object) contains information about the interaction
    """
    # Fetch a list of years in which the user has submitted reports
    try:
        years_list = reports_years_quickfetch(userid=int(ctx.author_id))
    except KeyError:
        years_list = [{'name': 'There are no workouts reported under your name. Get swole, then try again',
                       'value': 'error'}]

    await ctx.send(choices=years_list)


@edit_report.autocomplete("month")
async def reports_months_autocomplete(ctx: AutocompleteContext):
    """Fetches a list of months within the selected year in which the user has completed workout sessions.

    :param ctx: (object) contains information about the interaction
    """
    # Fetch a list of months in the selected year in which the user has submitted reports
    try:
        int(ctx.args[0])
        months_list = reports_months_quickfetch(userid=int(ctx.author_id),
                                                year=ctx.args[0])
    except:
        months_list = [{'name': 'Error: Please delete the command and try again. '
                                'Make sure you fill in all fields in order.',
                        'value': 'error'}]

    await ctx.send(choices=months_list)


@edit_report.autocomplete("day")
async def reports_days_autocomplete(ctx: AutocompleteContext):
    """Fetches a list of days within the selected year and month in which the user has completed workout sessions.

    :param ctx: (object) contains information about the interaction
    """
    # Fetch a list of days in the selected month of the selected year in which the user has submitted reports
    try:
        int(ctx.args[1])
        days_list = reports_days_quickfetch(userid=int(ctx.author_id),
                                            year=ctx.args[0],
                                            month=ctx.args[1])
    except:
        days_list = [{'name': 'Error: Please delete the command and try again. '
                              'Make sure you fill in all fields in order.',
                      'value': 'error'}]

    await ctx.send(choices=days_list)


@edit_report.autocomplete("report_to_edit")
async def reports_by_day_autocomplete(ctx: AutocompleteContext):
    """Fetches a list of reports made by the user around the specified day. Includes the day before and the day
    after to smooth out any memory/time zone issues.

    :param ctx: (object) contains information about the interaction
    """
    # Fetch a list of all the reports the user has made on the selected day, and on surrounding days if convenient
    try:
        int(ctx.args[2])
        reports = reports_by_day_quickfetch(userid=int(ctx.author_id),
                                            year=ctx.args[0],
                                            month=ctx.args[1],
                                            day=ctx.args[2])
    except:
        reports = [{'name': 'Error: Please delete the command and try again. '
                            'Make sure you fill in all fields in order.',
                    'value': 'error'}]
    await ctx.send(choices=reports)


@edit_report.autocomplete("field_to_change")
async def fields_in_report_autocomplete(ctx: AutocompleteContext):
    """Fetches the fields of information contained within the selected report.

    :param ctx: (object) contains information about the interaction
    """
    # Fetch a list of fields in the selected report that the user might be able to change
    try:
        float(ctx.args[3])
        fields = fields_in_report_quickfetch(userid=int(ctx.author_id),
                                             report_id=ctx.args[3])
    except:
        fields = [{'name': 'Error: Please delete the command and try again. Make sure you fill in all fields in order.',
                   'value': 'error'}]

    await ctx.send(choices=fields)

# -------------------------------------------------------------------------------------------------------------------- #
"""Common-use autocompletes"""


@schedule_routine.autocomplete("workout_day_1")
@schedule_routine.autocomplete("workout_day_2")
@schedule_routine.autocomplete("workout_day_3")
@schedule_routine.autocomplete("workout_day_4")
@schedule_routine.autocomplete("workout_day_5")
@schedule_routine.autocomplete("workout_day_6")
@schedule_routine.autocomplete("workout_day_7")
@edit_workout.autocomplete("new_schedule_day_1")
@edit_workout.autocomplete("new_schedule_day_2")
@edit_workout.autocomplete("new_schedule_day_3")
@edit_workout.autocomplete("new_schedule_day_4")
@edit_workout.autocomplete("new_schedule_day_5")
@edit_workout.autocomplete("new_schedule_day_6")
@edit_workout.autocomplete("new_schedule_day_7")
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


@report_scheduled.autocomplete("workout_name")
@edit_workout.autocomplete("workout_name")
async def user_workouts_autocomplete(ctx: AutocompleteContext):
    """Fetches a list of all of a user's scheduled workouts.

    :param ctx: (object) contains information about the interaction
    """
    # Fetch a list of the user's workouts
    workouts = workouts_quickfetch(userid=int(ctx.author_id))
    await ctx.send(choices=workouts)

# -------------------------------------------------------------------------------------------------------------------- #


if __name__ == "__main__":
    # Set the cwd to the directory where this file lives
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    # Define and start the bot
    bot = Client(token=config("BOT_TOKEN"))
    bot.start()
