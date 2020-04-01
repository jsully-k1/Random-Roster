import json
from datetime import datetime
import sys
import random
import urllib3
from os import environ

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
    
def slack_post(webhook, body_text):
    http = urllib3.PoolManager()
    exit_code = {
        'statusCode': 200,
        'body': 'Success'
    }

    try:
        slack_data = {'text': body_text}
        response = http.request('POST',
                                webhook,
                                body=json.dumps(slack_data),
                                headers={'Content-Type': 'application/json'})
        if response.status != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status, response.data)
            )

    except Exception as e:
        exit_code['statusCode'] = 500
        exit_code['body'] = f'Other Exception: {str(e)}' \
                            f' (input arguement of --slack_hook : {webhook})'
                            
    return exit_code
    
def lambda_handler(event, context):
    
    members = environ["TEAM_ROSTER"]
    slack_url = environ['SLACK_WEBHOOK_URL']
    members = members.split(",")
    
    if len(members):
        master, roster = generate_roster(members)
        roster_output = render_roster(master, roster)
        return slack_post(slack_url, roster_output)
