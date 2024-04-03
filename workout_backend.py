import json


def read_json(filename):
    """Read all data from a JSON file.

    :param filename: (str) the JSON file where the data is stored (ends with .json)
    :return: (dict) all the data that was in the JSON file
    """
    with open(filename, 'r') as file:
        json_data = json.load(file)

    return json_data


def edit_value(filename, user_id, field, new_value,
               scheduled_or_unscheduled=None, workout_unixid=None, report_unixid=None):
    """Edit a value for a particular user in the JSON file.

    :param filename: (str) the JSON file where the data is stored (ends with .json)
    :param user_id: (int) the Discord ID of the person whose information is being updated
    :param field: (str) the name of the field containing the value that is to be updated
    :param new_value: (any) the new value will be placed in the desired field
    :param scheduled_or_unscheduled: (str) 'scheduled_workout' or 'unscheduled_workout' depending on which is needed
    :param workout_unixid: (float) if it's something inside a workout that needs to be changed, the workout's unix time
    :param report_unixid: (float) if it's something inside a report that needs to be changed, the report's unix time
    """
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
        else: json_data['users'][user_id][scheduled_or_unscheduled][workout_unixid][report_unixid][field] = new_value

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)


def add_user(filename, user_id, user_nick):
    """Adds to the json a user that is reporting/scheduling their first workout.

    :param filename: (str) the JSON file where the data is stored (ends with .json)
    :param user_id: (int) the Discord ID of the new user
    :param user_nick: (str) the Discord display name of the new user
    """
    with open(filename, 'r') as file:
        json_data = json.load(file)

    json_data['users'][user_id] = {'username': user_nick, 'unscheduled_workout': {}, 'scheduled_workout': {}}

    with open(filename, 'w') as file:
        json.dump(json_data, file, indent=4)
