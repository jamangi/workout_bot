from workout_backend import (read_json, edit_value, add_user, add_scheduled_workout,
                             add_unscheduled_workout, add_report, get_all_reports, delete_from_dict)


def schedule_routine_main(user, workout_name, muscle_group, weights_used, tutorial_url, image_url, workout_day_1,
                          workout_day_2, workout_day_3, workout_day_4, workout_day_5, workout_day_6, workout_day_7):
    """Adds a scheduled workout to the json under the user's id.

    :param user: (object) a Discord object containing information about the person who used the slash command
    :param workout_name: (str) the name of the workout being added
    :param muscle_group: (str) a brief statement or description of the muscle groups used
    :param weights_used: (str) a brief statement or description of the weights used
    :param tutorial_url: (str) the url for a tutorial that can be accessed for aid
    :param image_url: (str) the url for an image that represents the workout
    :param workout_day_1: (str) a day of the week during which the workout should be regularly done
    :param workout_day_2: (str) a day of the week during which the workout should be regularly done
    :param workout_day_3: (str) a day of the week during which the workout should be regularly done
    :param workout_day_4: (str) a day of the week during which the workout should be regularly done
    :param workout_day_5: (str) a day of the week during which the workout should be regularly done
    :param workout_day_6: (str) a day of the week during which the workout should be regularly done
    :param workout_day_7: (str) a day of the week during which the workout should be regularly done
    :return: (str) a message that can be sent to Discord regarding the success of the operation
    """
    # Get the user id and compile the workout days into a list
    user_id = int(user.id)
    workout_days = [workout_day_1, workout_day_2, workout_day_3,
                    workout_day_4, workout_day_5, workout_day_6, workout_day_7]
    days_scheduled = [day for day in workout_days if day is not None]

    # If the user isn't already in the json, add them
    json_data = read_json()
    if str(user_id) not in json_data['users']:
        add_user(user_id, user.display_name)

    # Add the workout to the json
    add_scheduled_workout(user_id=user_id,
                          workout_name=workout_name,
                          days_scheduled=days_scheduled,
                          muscle_group=muscle_group,
                          weights_used=weights_used,
                          tutorial_url=tutorial_url,
                          img_url=image_url)

    # Create a sentence about the workout's schedule if one was entered
    sched_msg = ''
    if len(days_scheduled) > 0:
        if len(days_scheduled) > 1:
            workout_schedule_string = ', '.join(days_scheduled[:-1]) + f" and {days_scheduled[-1]}"
        else:
            workout_schedule_string = days_scheduled[0]
        sched_msg = f"It should be done every {workout_schedule_string}."

    # Create sentences about the muscle groups and weights used
    muscles_msg = ''
    if muscle_group:
        muscles_msg = f"Muscle group(s) used: {muscle_group}"
    weights_msg = ''
    if weights_used:
        weights_msg = f"Weights used: {weights_used}"

    # Create sentences about the tutorial and image urls
    tutorial_msg = ''
    if tutorial_url:
        tutorial_msg = f"A tutorial can be found at `{tutorial_url}`"
    image_msg = ''
    if image_url:
        image_msg = image_url

    # Add the message up into one big message
    message = (f"The workout {workout_name} has been scheduled. " + '\n' + sched_msg + '\n'
               + muscles_msg + '\n' + weights_msg + '\n' + tutorial_msg + '\n' + image_msg)

    return message


def report_scheduled_main(user, workout_id, completion, comment):
    """Create a report for the specified scheduled workout, then send a confirmation message back to Discord.

    :param user: (object) a Discord object containing information about the person who used the slash command
    :param workout_id: (str) the id (also unix time of creation) of the scheduled workout that was completed
    :param completion: (str) how much of the workout was finished. Either "complete", "partially complete", or "skipped"
    :param comment: (str) any comments about how the workout went
    :return: (str) a confirmation message to be sent back to Discord
    """
    user_id = int(user.id)
    # Add the report to the json database
    add_report(user_id, completion, comment=comment, workout_id=workout_id)

    # Get the workout's name
    json_data = read_json()
    workout_name = json_data['users'][str(user_id)]['scheduled_workout'][workout_id]['workout_name']

    # Create the message to be sent back to Discord
    message = (f"Your report for this scheduled workout, {workout_name}, has been logged:\n"
               f"Completion: {completion}\n"
               f"Comment: {comment}")

    return message


def report_unscheduled_main(user, workout_name, muscle_group, weights_used, tutorial_url, image_url, comment):
    """Create a report for an unscheduled workout, then send a confirmation message back to Discord.

    :param user: (object) a Discord object containing information about the person who used the slash command
    :param workout_name: (str) the name of the workout being added
    :param muscle_group: (str) a brief statement or description of the muscle groups used
    :param weights_used: (str) a brief statement or description of the weights used
    :param tutorial_url: (str) the url for a tutorial that can be accessed for aid
    :param image_url: (str) the url for an image that represents the workout
    :param comment: (str) any comment optionally left by the user
    :return: (str) a message to be returned to Discord reporting the success of the operation
    """
    user_id = int(user.id)

    # If the user isn't already in the json, add them
    json_data = read_json()
    if str(user_id) not in json_data['users']:
        add_user(user_id, user.display_name)

    # Add the report to the json database
    add_unscheduled_workout(user_id, workout_name, muscle_group, weights_used, tutorial_url, image_url, comment=comment)

    message = (f"Your report for this unscheduled workout has been logged:\n"
               f"Workout name: {workout_name}\n"
               f"Muscle group(s) used: {muscle_group}\n"
               f"Comment: {comment}\n"
               f"Link to tutorial: {tutorial_url}\n"
               f"Image: {image_url}")

    return message


def edit_workout_main(user, workout_id, field, new_value,
                      new_schedule_day_1, new_schedule_day_2, new_schedule_day_3, new_schedule_day_4,
                      new_schedule_day_5, new_schedule_day_6, new_schedule_day_7):
    """Edits a single field in a report, and/or changes the schedule. Can do both at the same time.

    :param user: (object) a Discord object containing information about the person who used the slash command
    :param workout_id: (str) the id (also the unix time of creation) of the workout to be edited
    :param field: (str) the name of the field whose value we're editing
    :param new_value: (str) the new value of the field that we're editing to
    :param new_schedule_day_1: (str) a day of the week during which the workout should be regularly done from now on
    :param new_schedule_day_2: (str) a day of the week during which the workout should be regularly done from now on
    :param new_schedule_day_3: (str) a day of the week during which the workout should be regularly done from now on
    :param new_schedule_day_4: (str) a day of the week during which the workout should be regularly done from now on
    :param new_schedule_day_5: (str) a day of the week during which the workout should be regularly done from now on
    :param new_schedule_day_6: (str) a day of the week during which the workout should be regularly done from now on
    :param new_schedule_day_7: (str) a day of the week during which the workout should be regularly done from now on
    :return: (str) a message to be returned to Discord reporting the success of the operation
    """
    user_id = int(user.id)
    workout_days = [new_schedule_day_1, new_schedule_day_2, new_schedule_day_3,
                    new_schedule_day_4, new_schedule_day_5, new_schedule_day_6, new_schedule_day_7]

    # Return an error if no changes were requested
    days_scheduled = [day for day in workout_days if day is not None]
    if len(days_scheduled) == 0 and not new_value:
        raise ValueError("You didn't actually request any changes to the workout... Make sure to specify them!")

    # If what's being changed is the workout name, make sure it's not too long
    if field == 'workout_name' and len(new_value) > 79:
        raise ValueError("Your new workout name is too long. The maximum length is 79 characters.")

    # Make the requested change
    if new_value:
        edit_value(user_id, field, new_value, scheduled_or_unscheduled='scheduled_workout', workout_unixid=workout_id)

    # Change the schedule, too, if requested
    if len(days_scheduled) > 0:
        edit_value(user_id, 'days_scheduled', days_scheduled, 'scheduled_workout', workout_unixid=workout_id)

    # Create a sentence about the workout's new schedule if it was changed
    json_data = read_json()
    workout_name = json_data['users'][str(user_id)]['scheduled_workout'][workout_id]['workout_name']
    sched_msg = ''
    if len(days_scheduled) > 0:
        if len(days_scheduled) > 1:
            workout_schedule_string = ', '.join(days_scheduled[:-1]) + f" and {days_scheduled[-1]}"
        else:
            workout_schedule_string = days_scheduled[0]
        sched_msg = (f" The schedule has been changed. The workout will now be done every week "
                     f"on {workout_schedule_string}.")

    # Generate a message to be sent back to Discord
    message = (f"The requested change has been made to your scheduled workout, {workout_name}, which was created "
               f"on <t:{int(float(workout_id))}:f>.")
    if new_value:
        message += f" {field} has been changed to {new_value}."
    message += sched_msg

    return message


def edit_report_main(user, report_id, field, new_value):
    """Edits a single field in a report, whether it's scheduled or unscheduled.

    :param user: (object) a Discord object containing information about the person who used the slash command
    :param report_id: (str) the id (also the unix time of creation) of the report to be edited
    :param field: (str) the name of the field whose value we're editing
    :param new_value: (str) the new value of the field that we're editing to
    :return: (str) a message to be returned to Discord reporting the success of the operation
    """
    user_id = int(user.id)
    # If what's being changed is the workout name, make sure it's not too long
    if field == 'workout_name' and len(new_value) > 79:
        raise ValueError("Your new workout name is too long. The maximum length is 79 characters.")

    # If what's being changed is the completion, make sure it's one of the three accepted values
    if (field == 'completion' and new_value != "complete"
            and new_value != "partially complete" and new_value != "skipped"):
        raise ValueError("Completion can only be one of 'complete', 'partially complete', or 'skipped'.")

    # Figure out if it's scheduled or unscheduled, then edit the value
    all_reports = get_all_reports(user_id)
    full_report = all_reports[report_id]
    if 'completion' in full_report:
        workout_id = full_report['workout_id']
        edit_value(user_id, field, new_value, 'scheduled_workout',
                   workout_unixid=workout_id, report_unixid=report_id)
        scheduled_or_unscheduled = 'scheduled'
    else:
        edit_value(user_id, field, new_value, 'unscheduled_workout', report_unixid=report_id)
        scheduled_or_unscheduled = 'unscheduled'

    # Gather the information necessary to make the message we'll send back to Discord, then make the message
    timestamp = f'<t:{int(float(report_id))}:f>'
    workout_name = full_report['workout_name']
    message = (f"The report for the {scheduled_or_unscheduled} workout {workout_name} made at {timestamp} has been "
               f"edited. The value for {field} has been changed to {new_value}")

    return message


def view_report_main(user, report_id):
    """Given a specific report, gathers all the information about that report and returns it to Discord.

    :param user: (object) a Discord object containing information about the person who used the slash command
    :param report_id: (str) the id (also the unix time of creation) of the report to be viewed
    :return: (str) a message to be returned to Discord containing info about the specified report
    """
    # Get the report
    report = get_all_reports(str(user.id))[report_id]

    # Generate info needed to finish the message:
    workout_name = report['workout_name']
    if 'completion' in report:
        scheduled_or_unscheduled = 'scheduled'
    else:
        scheduled_or_unscheduled = 'unscheduled'
    user_nick = user.display_name
    timestamp = f"<t:{int(float(report_id))}:f>"

    image_str = ''
    if scheduled_or_unscheduled == 'scheduled':
        image = read_json()['users'][str(user.id)]['scheduled_workout'][report['workout_id']]['img_url']
        if image:
            image_str = image

    # Compile the report data into strings
    report_data = [f"{field}: {value}" for field, value in report.items()]

    message = ((f"Here is all the data from the report on the {scheduled_or_unscheduled} workout session "
               f"'{workout_name}' which was done by {user_nick} on {timestamp}:\n")
               + '\n'.join(report_data)
               + '\n' + image_str)

    return message


def view_workout_main(user, workout_id):
    """Given a specific report, gathers all the information about that report and returns it to Discord.

    :param user: (object) a Discord object containing information about the person who used the slash command
    :param workout_id: (str) the id (also the unix time of creation) of the workout to be viewed
    :return: (str) a message to be returned to Discord containing info about the specified workout and its reports
    """
    # Get the workout and extract its reports and days scheduled
    workout = read_json()['users'][str(user.id)]['scheduled_workout'][workout_id]
    reports = workout['reports']
    del workout['reports']
    days_scheduled = workout['days_scheduled']

    # Create a sentence about the workout's schedule if one was entered
    if len(days_scheduled) > 0:
        if len(days_scheduled) > 1:
            workout_schedule_string = ', '.join(days_scheduled[:-1]) + f" and {days_scheduled[-1]}"
        else:
            workout_schedule_string = days_scheduled[0]
    else:
        workout_schedule_string = 'None'

    # Compile the workout data into strings
    if workout['tutorial_url']:
        workout['tutorial_url'] = f"`{workout['tutorial_url']}`"
    workout['days_scheduled'] = workout_schedule_string
    workout_data = [f"{field}: {value}" for field, value in workout.items()]

    # Compile the reports into strings, too
    reports_list = [f"<t:{int(float(report))}:f>:\n"
                    + '\n'.join([f"{field}: {value}" for field, value in reports[report].items()])
                    for report in reports]

    # Generate info needed to finish the message:
    workout_name = workout['workout_name']
    user_nick = user.display_name
    timestamp = f"<t:{int(float(workout_id))}:f>"
    num_reports = len(reports)

    message = ((f"Here is everything there is to know about the workout routine "
               f"'{workout_name}' which was designed by {user_nick} on {timestamp}:\n") + '\n'.join(workout_data)
               + f"\n\n**{num_reports}** Reports:\n" + '\n\n'.join(reports_list))

    return message


def delete_report_main(user, report_id):
    """Deletes the specified report from the json file

    :param user: (object) a Discord object containing information about the person who used the slash command
    :param report_id: (str) the id (also the unix time of creation) of the report to be deleted
    :return: (str) a confirmation message to be sent to Discord
    """
    user_id = str(user.id)
    # Get the report info so we can decide what to delete and how
    report = get_all_reports(str(user.id))[report_id]

    # Generate info:
    workout_name = report['workout_name']
    workout_id = report['workout_id']
    if 'completion' in report:
        scheduled_or_unscheduled = 'scheduled'
    else:
        scheduled_or_unscheduled = 'unscheduled'
    user_nick = user.display_name
    timestamp = f"<t:{int(float(report_id))}:f>"

    if scheduled_or_unscheduled == 'unscheduled':
        delete_from_dict(user_id, report_unixid=report_id)
    elif scheduled_or_unscheduled == 'scheduled':
        delete_from_dict(user_id, workout_unixid=workout_id, report_unixid=report_id)
    else:
        raise ValueError("Something went wrong. Make sure 'scheduled_or_unscheduled is either 'scheduled' or "
                         "'unscheduled'.")

    message = (f"The report for the {scheduled_or_unscheduled} workout session "
               f"'{workout_name}', which was done by {user_nick} on {timestamp}, has been successfully deleted.")

    return message


def delete_workout_main(user, workout_id, save):
    """Deletes the specified workout from the json file. The user can specify through the 'save' variable whether
    they want the reports to be deleted, too, or whether they should be listed as unscheduled workouts, instead.

    :param user: (object) a Discord object containing information about the person who used the slash command
    :param workout_id: (str) the id (also the unix time of creation) of the workout to be deleted
    :param save: (str) If 'True', save all reports for the specified workout as unscheduled workouts after
    the workout has been deleted. If 'False', just delete all the workout's reports.
    :return: (str) a confirmation message to be sent to Discord
    """
    user_id = str(user.id)
    # Get the workout and all its data
    workout = read_json()['users'][str(user.id)]['scheduled_workout'][workout_id]
    reports = workout['reports']

    # Generate info
    workout_name = workout['workout_name']
    user_nick = user.display_name
    timestamp = f"<t:{int(float(workout_id))}:f>"

    if save == 'True':
        # Collect all the reports from the workout and save them as unscheduled workouts
        for report_id in reports:
            add_unscheduled_workout(user_id,
                                    workout_name,
                                    muscle_group=reports[report_id]['muscle_group'],
                                    weights_used=reports[report_id]['weights_used'],
                                    tutorial_url=reports[report_id]['tutorial_url'],
                                    img_url=reports[report_id]['img_url'],
                                    preset_report_id=report_id)

    # Delete the workout from the json file
    delete_from_dict(user_id, workout_unixid=workout_id)

    message = (f"The workout routine called '{workout_name}', which was designed by {user_nick} on {timestamp}, "
               f"has been successfully deleted.\n")
    if save:
        message += "The workout reports have been saved as unscheduled reports."

    return message
