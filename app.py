import requests

from flask import Flask

from exceptions import InitialDataException
from settings import * # This is the only case when import * is allowed

app = Flask(__name__)

# Env configurations
organization_id = ENVIRONMENT_CONF["HUBSTAFF_ORGANIZATION_ID"]
api_url = ENVIRONMENT_CONF["HUBSTAFF_API_URL"]
app_token = ENVIRONMENT_CONF["HUBSTAFF_APP_TOKEN"]
api_token = ENVIRONMENT_CONF["HUBSTAFF_AUTH_TOKEN"]

# Hubstaff API urls
organization_memebers_url = api_url + "/organizations/{organization_id}/members"
organization_projects_url = api_url + "/organizations/{organization_id}/projects"
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
        employees = req_response.content
    else:
        raise InitialDataException


def load_organization_projects_data():
    global projects

    projects_url = organization_projects_url.format(organization_id=organization_id)
    req_response = requests.get(projects_url, headers=hubstaff_headers)

    if req_response.status_code == 200:
        projects = req_response.content
    else:
        raise InitialDataException()


def load_initial_data():
    load_organization_members_data()
    load_organization_projects_data()


def get_day_activity():


@app.route('/')
def dashboard():
    load_initial_data()
    return str(employees + projects)


if __name__ == '__main__':
    app.run()
