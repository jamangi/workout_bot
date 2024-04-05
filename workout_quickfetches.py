from workout_backend import read_json, get_all_reports
from datetime import datetime


def reports_years_quickfetch(userid):
    """Returns a list (in quickfetch form ready for autocomplete, so {'name': year, 'value': year}) of every year in
    which the user has submitted a report, whether scheduled or unscheduled.

    :param userid: (int) the Discord ID of the person who used the slash command
    :return: (list of dicts) {'name': year, 'value': year} for every year in which there is a report
    """
    # Get all the reports the user has submitted
    all_reports = get_all_reports(userid)
    report_dates = [float(report_id) for report_id in all_reports]

    # Create a list of years that have reports in them
    valid_years = []
    year = 2024
    year_start = datetime(year, 1, 1).timestamp()
    for unixtime in report_dates:
        while unixtime > year_start:
            year += 1
            year_start = datetime(year, 1, 1).timestamp()
        if year not in valid_years:
            valid_years.append(year)

    # Format the list of years the way autocomplete likes -- a list of dicts like so: {'name': name, 'value': value}
    years_strings = [str(year) for year in valid_years]
    years_list = [{'name': 'latest', 'value': 'latest'}] + [{'name': year, 'value': year} for year in years_strings]
    return years_list


def reports_months_quickfetch(userid, year):
    pass


def reports_days_quickfetch(userid, year, month):
    pass


def reports_by_day_quickfetch(userid, year, month, day):
    pass


def fields_in_report_quickfetch(userid, report_name):
    pass


def workouts_quickfetch(userid):
    pass



# choices = [SlashCommandChoice(name='latest', value='latest'),
#            SlashCommandChoice(name='1 - January', value='1'),
#            SlashCommandChoice(name='2 - February', value='2'),
#            SlashCommandChoice(name='3 - March', value='3'),
#            SlashCommandChoice(name='4 - April', value='4'),
#            SlashCommandChoice(name='5 - May', value='5'),
#            SlashCommandChoice(name='6 - June', value='6'),
#            SlashCommandChoice(name='7 - July', value='7'),
#            SlashCommandChoice(name='8 - August', value='8'),
#            SlashCommandChoice(name='9 - September', value='9'),
#            SlashCommandChoice(name='10 - October', value='10'),
#            SlashCommandChoice(name='11 - November', value='11'),
#            SlashCommandChoice(name='12 - December', value='12')])