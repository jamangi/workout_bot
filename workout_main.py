from workout_backend import (read_json, edit_value, add_user, add_scheduled_workout, add_unscheduled_workout,
                             add_report)


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

    # Create a sentence about the message's schedule if one was entered
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
        tutorial_msg = f"A tutorial can be found at {tutorial_url}"
    image_msg = ''
    if image_url:
        image_msg = image_url

    # Add the message up into one big message
    message = (f"The workout {workout_name} has been scheduled. " + '\n' + sched_msg + '\n'
               + muscles_msg + '\n' + weights_msg + '\n' + tutorial_msg + '\n' + image_msg)

    return message


def report_scheduled_main():
    pass


def report_unscheduled_main():
    pass


def edit_workout_main():
    pass


def edit_report_main():
    pass