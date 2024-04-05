import json
from datetime import datetime
from decouple import config


def read_json():
    """Read all data from a JSON file.

    :return: (dict) all the data that was in the JSON file
    """
    filename = config("FILENAME")
    with open(filename, 'r') as file:
        json_data = json.load(file)

    return json_data


def edit_value(user_id, field, new_value,
               scheduled_or_unscheduled=None, workout_unixid=None, report_unixid=None):
    """Edit a value for a particular user in the JSON file.

    :param user_id: (int) the Discord ID of the person whose information is being updated
    :param field: (str) the name of the field containing the value that is to be updated
    :param new_value: (any) the new value will be placed in the desired field
    :param scheduled_or_unscheduled: (str) 'scheduled_workout' or 'unscheduled_workout' depending on which is needed
    :param workout_unixid: (float) if it's something inside a workout that needs to be changed, the workout's unix time
    :param report_unixid: (float) if it's something inside a report that needs to be changed, the report's unix time
    """
    filename = config("FILENAME")
    user_id = str(user_id)
    with open(filename, 'r') as file:
        json_data = json.load(file)
    if not scheduled_or_unscheduled:
        json_data['users'][user_id][field] = new_value
    else:
        if scheduled_or_unscheduled != 'scheduled_workout' and scheduled_or_unscheduled != 'unscheduled_workout':
            raise ValueError('In edit_value, scheduled_or_unscheduled must be either None or '
                             '"scheduled_workout" or "unscheduled_workout".')
        if not workout_unixid:
            raise ValueError('If scheduled_or_unscheduled is given as an argument, a workout_unixid must be '
                             'supplied to clarify which workout is being referred to.')
        if not report_unixid:
            json_data['users'][user_id][scheduled_or_unscheduled][workout_unixid][field] = new_value
        else:
            json_data['users'][user_id][scheduled_or_unscheduled][workout_unixid][report_unixid][field] = new_value

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


def add_user(user_id, user_nick):
    """Adds to the json a user that is reporting/scheduling their first workout.

    :param user_id: (int) the Discord ID of the new user
    :param user_nick: (str) the Discord display name of the new user
    """
    filename = config("FILENAME")
    with open(filename, 'r') as file:
        json_data = json.load(file)

    json_data['users'][str(user_id)] = {'username': user_nick, 'unscheduled_workout': {}, 'scheduled_workout': {}}

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


def add_scheduled_workout(user_id, workout_name, days_scheduled, muscle_group=None, weights_used=None,
                          tutorial_url=None, img_url=None):
    """Adds a scheduled workout to the scheduled_workout dict within the user's entry in the users dict in the json.

    :param user_id: (int) the Discord ID of the user creating the workout
    :param workout_name: (str) the name of the new workout
    :param days_scheduled: (list) a list of the days the workout should be done. ex: ["Monday", "Friday"]
    :param muscle_group: (str) a description of the muscle group(s) used in this workout
    :param weights_used: (str) a description of the weights used in this workout, if any
    :param tutorial_url: (str) a link to a tutorial that shows how to do this workout properly
    :param img_url: (str) a link to an image that can be used in messages about this workout
    """
    filename = config("FILENAME")
    time_now = datetime.now().timestamp()

    with open(filename, 'r') as file:
        json_data = json.load(file)

    json_data['users'][str(user_id)]['scheduled_workout'][time_now] = {'workout_name': workout_name,
                                                                  'days_scheduled': days_scheduled,
                                                                  'muscle_group': muscle_group,
                                                                  'weights_used': weights_used,
                                                                  'tutorial_url': tutorial_url,
                                                                  'img_url': img_url}

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


def add_unscheduled_workout(user_id, workout_name, muscle_group=None, weights_used=None,
                            tutorial_url=None, img_url=None):
    """Adds an impromptu workout to the unscheduled_workout dict within the user's entry in the users dict in the json.

    :param user_id: (int) the Discord ID of the user reporting the workout
    :param workout_name: (str) the name of the reported workout
    :param muscle_group: (str) a description of the muscle group(s) used in this workout
    :param weights_used: (str) a description of the weights used in this workout, if any
    :param tutorial_url: (str) a link to a tutorial that shows how to do this workout properly
    :param img_url: (str) a link to an image that can be used in messages about this workout
    """
    filename = config("FILENAME")
    time_now = datetime.now().timestamp()

    with open(filename, 'r') as file:
        json_data = json.load(file)

    json_data['users'][user_id]['unscheduled_workout'][time_now] = {'workout_name': workout_name,
                                                                    'muscle_group': muscle_group,
                                                                    'weights_used': weights_used,
                                                                    'tutorial_url': tutorial_url,
                                                                    'img_url': img_url}

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


def add_report(user_id, workout_name, completion, comment=None):
    """Adds an impromptu workout to the unscheduled_workout dict within the user's entry in the users dict in the json.

    :param user_id: (int) the Discord ID of the user reporting the workout
    :param workout_name: (str) the name of the reported workout
    :param completion: (str) whether the workout was skipped or completed, and to what degree. Options constrained
    :param comment: (str) a comment about how the workout went
    """
    filename = config("FILENAME")
    time_now = datetime.now().timestamp()

    with open(filename, 'r') as file:
        json_data = json.load(file)

    # Find the dict with the desired workout_name
    unscheduled = json_data['users'][str(user_id)]['unscheduled_workout']
    workout_unixid = [workout for workout in unscheduled if unscheduled[workout]['workout_name'] == workout_name][0]

    # Add the report to the reports dict
    json_data['users'][str(user_id)]['unscheduled_workout'][workout_unixid][time_now] = {'completion': completion,
                                                                                         'comment': comment}

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


def get_all_reports(userid):
    """Get a list of all the reports, both scheduled and unscheduled, for the given user

    :param userid: (int) the Discord id of the user who used the slash command
    :return: (dict of dicts) all the reports the user has ever submitted
    """
    json_data = read_json()
    userid = str(userid)

    # Get all unscheduled reports and put them into the reports dict
    reports = json_data[userid]['unscheduled']

    # Add all scheduled reports to the reports dict
    scheduled = json_data[userid]['scheduled']
    for workout_id in scheduled:
        for report_id, report_data in scheduled[workout_id]['reports']:
            reports[report_id] = report_data
            reports[report_id]['workout_id'] = workout_id  # add the workout id to report data for clarity

    return reports


