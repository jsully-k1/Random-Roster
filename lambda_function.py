import json
from datetime import datetime
import sys
import random
import urllib3
from os import getenv


def generate_roster(member_list):
    dt = datetime.now()
    random.seed(dt.microsecond)

    name_count = len(member_list)
    roster = []

    for i in range(0, name_count):
        name = member_list[random.randint(0, name_count - 1)]
        while name in roster:
            name = member_list[random.randint(0, name_count - 1)]
        roster.append(name)

    scrum_master = member_list[random.randint(0, name_count - 1)]

    return scrum_master, roster


def render_roster(master, roster):
    roster = [f'\t{name}\n' for name in roster]

    output = f'Today\'s Scrum Master: {master}\n\n' \
             f'Roster:\n' \
             f'{"".join(roster)}'
    return output


def get_slack_body(body_text):
    return {'text': body_text}


def get_rocket_body(body_text):
    return {"username": "Random-Roster",
            "icon_emoji": ":robot:",
            "text": body_text,
            }


def get_ms_teams_body(body_text):
    return {'text': body_text}


def post(webhook, body):
    http = urllib3.PoolManager()
    exit_code = {
        'statusCode': 200,
        'body': 'Success'
    }

    try:
        response = http.request('POST',
                                webhook,
                                body=json.dumps(body),
                                headers={'Content-Type': 'application/json'})
        if response.status != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status, response.data)
            )

    except Exception as e:
        exit_code['statusCode'] = 500
        exit_code['body'] = f'Other Exception: {str(e)}' \
                            f' (input arguement of --url_hook : {webhook})'

    return exit_code


def lambda_handler(event, context):
    exit_code = {
        'statusCode': 200,
        'body': 'Success'
    }

    members = getenv("TEAM_ROSTER", default=None)
    renders = [{'url': getenv('SLACK_WEBHOOK_URL', default=None), 'render': get_slack_body},
               {'url': getenv('ROCKET_WEBHOOK_URL', default=None), 'render': get_rocket_body},
               {'url': getenv('MS_TEAMS_WEBHOOK_URL', default=None), 'render': get_ms_teams_body}]

    if members:
        members = members.split(",")
    else:
        members = []

    if len(members):
        master, roster = generate_roster(members)
        roster_output = render_roster(master, roster)

        for render in renders:
            if render['url']:
                body = render['render'](roster_output)
                ec = post(render['url'], body)
                if ec['statusCode'] != 200:
                    exit_code['statusCode'] = 500
                    exit_code['body'] += ec['body']

    return exit_code


if __name__ == '__main__':
    lambda_handler('a', 'b')