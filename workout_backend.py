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
        if not report_unixid:
            json_data['users'][user_id][scheduled_or_unscheduled][workout_unixid][field] = new_value
        elif not workout_unixid:
            json_data['users'][user_id][scheduled_or_unscheduled][report_unixid][field] = new_value
        else:
            json_data['users'][user_id][scheduled_or_unscheduled][workout_unixid]['reports'][report_unixid][field] \
                = new_value

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
                                                                       'img_url': img_url,
                                                                       'reports': {}}

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


def add_unscheduled_workout(user_id, workout_name, muscle_group=None, weights_used=None,
                            tutorial_url=None, img_url=None, preset_report_id=None, comment=None):
    """Adds an impromptu workout to the unscheduled_workout dict within the user's entry in the users dict in the json.

    :param user_id: (int) the Discord ID of the user reporting the workout
    :param workout_name: (str) the name of the reported workout
    :param muscle_group: (str) a description of the muscle group(s) used in this workout
    :param weights_used: (str) a description of the weights used in this workout, if any
    :param tutorial_url: (str) a link to a tutorial that shows how to do this workout properly
    :param img_url: (str) a link to an image that can be used in messages about this workout
    :param preset_report_id: (str) if this is not None, use this value as the report_id
    :param comment: (str) any comment about the workout optionally left by the user
    """
    filename = config("FILENAME")
    if preset_report_id:
        time_now = preset_report_id
    else:
        time_now = datetime.now().timestamp()

    with open(filename, 'r') as file:
        json_data = json.load(file)

    json_data['users'][str(user_id)]['unscheduled_workout'][time_now] = {'workout_name': workout_name,
                                                                         'muscle_group': muscle_group,
                                                                         'weights_used': weights_used,
                                                                         'tutorial_url': tutorial_url,
                                                                         'img_url': img_url,
                                                                         'comment': comment}

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


def add_report(user_id, completion, workout_name=None, workout_id=None, comment=None):
    """Adds a report for a scheduled workout in the users dict in the json.
    Workout can be accessed by referring to either its name or its id.

    :param user_id: (int) the Discord ID of the user reporting the workout
    :param completion: (str) whether the workout was skipped or completed, and to what degree. Options constrained
    :param workout_name: (str) the name of the reported workout
    :param workout_id: (str) the id (also unix time of creation) for the specified workout
    :param comment: (str) a comment about how the workout went
    """
    filename = config("FILENAME")
    time_now = datetime.now().timestamp()

    with open(filename, 'r') as file:
        json_data = json.load(file)

    if workout_name:
        # Find the dict with the desired workout_name
        scheduled = json_data['users'][str(user_id)]['scheduled_workout']
        workout_id = [workout for workout in scheduled if scheduled[workout]['workout_name'] == workout_name][0]

    # Add the report to the reports dict
    json_data['users'][str(user_id)]['scheduled_workout'][workout_id]["reports"][time_now] = {'completion': completion,
                                                                                              'comment': comment}

    if not workout_name and not workout_id:
        raise ValueError("add_report must be provided either workout_id or workout_name, but got neither.")

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


def delete_from_dict(user_id, workout_unixid=None, report_unixid=None):
    """Delete a workout or report from the json file. If workout_unixid is given but not report_unixid, the selected
    scheduled workout will be deleted. If report_unixid is given but not workout_unixid, the selected unscheduled
    workout report will be deleted. If both are given, the selected scheduled workout report will be deleted.

    :param user_id: (int) the Discord ID of the person whose information is being updated
    :param workout_unixid: (float) the scheduled workout's unix time
    :param report_unixid: (float) the report's unix time
    """
    filename = config("FILENAME")
    user_id = str(user_id)
    with open(filename, 'r') as file:
        json_data = json.load(file)

    # Make sure enough info is given to make specifying a key to remove possible
    if not workout_unixid and not report_unixid:
        raise ValueError("Please provide at least one of workout_unixid or report_unixid to specify what to delete.")

    # Remove unscheduled workout report if only report id is provided
    elif not workout_unixid:
        del json_data['users'][user_id]['unscheduled_workout'][report_unixid]

    # Remove scheduled workout routine if only workout id is provided
    elif not report_unixid:
        del json_data['users'][user_id]['scheduled_workout'][workout_unixid]

    # Remove scheduled workout report if both report id and workout id are provided
    else:
        del json_data['users'][user_id]['scheduled_workout'][workout_unixid][report_unixid]

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
    reports = json_data['users'][userid]['unscheduled_workout']

    # Add all scheduled reports to the reports dict
    scheduled = json_data['users'][userid]['scheduled_workout']
    for workout_id in scheduled:
        for report_id, report_data in scheduled[workout_id]['reports'].items():
            reports[report_id] = report_data
            reports[report_id]['workout_id'] = workout_id  # add the workout id to report data for clarity
            reports[report_id]['workout_name'] = scheduled[workout_id]['workout_name']  # the workout's name, too

    return reports


