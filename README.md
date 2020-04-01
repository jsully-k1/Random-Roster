# Random-Roster
AWS Lamda function for generating a random standup order and scrum master.

To run this code as an AWS lambda simply follow the Hello World tutorial to create a basic lambda function written in python.

1. Copy the code from python_lambda.py into your function.

    https://aws.amazon.com/getting-started/hands-on/run-serverless-code/

2. Add a Cloudwatch Events trigger from the Lambda configuration console with your desired schedule.

3. add a slack Web-Hooks integration on your slack account for the channel where you'd like the roster posted.

    https://my.slack.com/services/new/incoming-webhook/

4. create two environment variables in the lambda configuration.
    * "TEAM_ROSTER" containing the comma separated list of team members.
    * "SLACK_WEBHOOK_URL" containing the URL you received when you created the webhook integration on your slack channel.