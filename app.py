import json
from datetime import datetime, timedelta, time

import requests

from flask import Flask, render_template, request

from exceptions import InitialDataException
from settings import ENVIRONMENT_CONF, DATE_FORMAT

app = Flask(__name__)

# Env configurations
organization_id = ENVIRONMENT_CONF["HUBSTAFF_ORGANIZATION_ID"]
api_url = ENVIRONMENT_CONF["HUBSTAFF_API_URL"]
app_token = ENVIRONMENT_CONF["HUBSTAFF_APP_TOKEN"]
api_token = ENVIRONMENT_CONF["HUBSTAFF_AUTH_TOKEN"]

# Hubstaff API urls
organization_memebers_url = api_url + "/organizations/{organization_id}/members"
organization_projects_url = api_url + "/organizations/{organization_id}/projects"
custom_bydate_team = api_url + "custom/by_date/team"

hubstaff_headers = {
    "App-Token": app_token,
    "Auth-Token": api_token
}

# Initial data global vars
employees = []
projects = []


def load_organization_members_data():
    global employees
    members_url = organization_memebers_url.format(organization_id=organization_id)
    req_response = requests.get(members_url, headers=hubstaff_headers)

    if req_response.status_code == 200:
        employees = json.loads(req_response.content)["users"]
    else:
        raise InitialDataException


def load_organization_projects_data():
    global projects

    projects_url = organization_projects_url.format(organization_id=organization_id)
    req_response = requests.get(projects_url, headers=hubstaff_headers)

    if req_response.status_code == 200:
        projects = json.loads(req_response.content)["projects"]
    else:
        raise InitialDataException()


def load_initial_data():
    load_organization_members_data()
    load_organization_projects_data()


def format_data(hours):
    """
        Get the data in the format gived by custom/bydate/team and returns a JSON with the format
        {"Juan Pablo": {"1234": "time_hours", "2313": "time hours2"}, "pedro":{}} to process in the Template easily
    :type hours: dict
    :return: dict
    """
    try:
        formated_data_return = {}
        by_day_data = hours["organizations"][0]["dates"]  # Just because I'm working in an organization, I take the 0 index
        for days in by_day_data:
            for employee in days["users"]:
                # formated_data_return[employee["name"]] = {}

                for project in employee["projects"]:
                    # formated_data_return[employee["project"]] = {}
                    if project["name"] not in formated_data_return:
                        formated_data_return[project["name"]] = {employee["name"]: project["duration"]}
                    else:
                        old_time = 0 if employee["name"] not in formated_data_return[project["name"]] \
                                     else formated_data_return[project["name"]][employee["name"]]
                        new_time = project["duration"]
                        formated_data_return[project["name"]][employee["name"]] = old_time + new_time

        return formated_data_return
    except (IndexError, KeyError):
        return []


@app.route('/')
def dashboard():
    date = request.args.get('date')
    if not date:
        date_start = datetime.combine(datetime.today() - timedelta(days=1), time.min)
        date_end = datetime.combine(datetime.today(), time.min)
    else:
        date = date_start = datetime.strptime(date, DATE_FORMAT)
        date_end = datetime.combine(date + timedelta(days=1), time.min)

    req_response = requests.get(
        custom_bydate_team, headers=hubstaff_headers, params={"start_date": date_start.isoformat(),
                                                              "end_date": date_end.isoformat()}
                 )
    content = format_data(json.loads(req_response.text))
    return render_template('dashboard.html', content=content, employees=employees, projects=projects)


# In order to have this data updated, this should be in a shell command, saved in a database and resync
load_initial_data()
