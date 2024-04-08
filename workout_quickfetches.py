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
    year_strings = [str(year) for year in valid_years]
    years_list = [{'name': 'latest', 'value': 'latest'}] + [{'name': year, 'value': year} for year in year_strings]

    return years_list


def reports_months_quickfetch(userid, year):
    """Returns a list (in quickfetch form ready for autocomplete) of every month within the selected year in which the
    user submitted a report, whether scheduled or unscheduled.

    :param userid: (int) the Discord ID of the person who used the slash command
    :param year: (str) the year that is being queried to check for workouts
    :return: (list of dicts) dict for every month in which there is a report. ex: {'name': '1 - January', 'value': '1''}
    """
    months_hash = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                   9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    # Get bounds of this year
    year = int(year)
    year_start = datetime(year, 1, 1).timestamp()
    year_end = datetime(year+1, 1, 1).timestamp()

    # Get all the reports the user has submitted this year
    all_reports = get_all_reports(userid)
    report_dates = [float(report_id) for report_id in all_reports if year_start <= float(report_id) < year_end]

    # Create a list of months in that year that have reports in them
    valid_months = []
    month = 1
    month_start = datetime(year, month, 1).timestamp()
    for unixtime in report_dates:
        while unixtime > month_start:
            month += 1
            month_start = datetime(year, month, 1).timestamp()
        if month not in valid_months:
            valid_months.append(month)

    # Format the list of months the way autocomplete likes -- a list of dicts like so: {'name': name, 'value': value}
    months_list = ([{'name': 'latest', 'value': 'latest'}]
                   + [{'name': f"{month} - {months_hash[month]}", 'value': str(month)} for month in valid_months])

    return months_list


def reports_days_quickfetch(userid, year, month):
    """Returns a list (in quickfetch form ready for autocomplete) of every day within the selected month in which the
    user submitted a report, whether scheduled or unscheduled.

    :param userid: (int) the Discord ID of the person who used the slash command
    :param year: (str) the year that is being queried to check for workouts
    :param month: (str) the month that is being queried to check for workouts
    :return: (list of dicts) dict for every month in which there is a report. ex: {'name': '1 - January', 'value': '1''}
    """
    months_hash = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
                   9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    # Get bounds of this month
    year = int(year)
    month = int(month)
    month_start = datetime(year, month, 1).timestamp()
    month_end = datetime(year, month+1, 1).timestamp()

    # Get all the reports the user has submitted this month
    all_reports = get_all_reports(userid)
    report_dates = [float(report_id) for report_id in all_reports if month_start <= float(report_id) < month_end]

    # Create a list of days in that month that have reports in them
    valid_days = []
    day = 1
    day_start = datetime(year, month, 1).timestamp()
    for unixtime in report_dates:
        while unixtime > day_start:
            day += 1
            day_start = datetime(year, month, day).timestamp()
        if day not in valid_days:
            valid_days.append(month)

    # Format the list of months the way autocomplete likes -- a list of dicts like so: {'name': name, 'value': value}
    days_list = ([{'name': 'latest', 'value': 'latest'}]
                   + [{'name': f"{day} - {months_hash[month]} {day}, {year}", 'value': str(day)}
                      for day in valid_days])

    return days_list


def reports_by_day_quickfetch(userid, year, month, day):
    pass


def fields_in_report_quickfetch(userid, report_name):
    pass


def workouts_quickfetch(userid):
    pass
