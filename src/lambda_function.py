import json
import os
import urllib.request
import stop_instances


def post_to_slack(webhook_url, channel, username, text, icon_emoji):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'channel': channel,
        'username': username,
        'text': text,
        'icon_emoji': icon_emoji
    }
    req = urllib.request.Request(
        webhook_url, json.dumps(data).encode(), headers)
    with urllib.request.urlopen(req) as res:
        return {'message': res.read().decode('utf-8')}

    return {'message': 'error'}


def main():
    webhook_url = os.environ['WEBHOOK_URL']
    channel = os.environ['SLACK_CHANNEL']
    username = os.environ['SLACK_USERNAME']
    icon_emoji = os.environ['SLACK_ICON_EMOJI']

    ec2 = stop_instances.get_ec2_client()
    rds = stop_instances.get_rds_client()
    stopped_ec2_instances = stop_instances.stop_running_ec2_instances(ec2)
    stopped_rds_instances = stop_instances.stop_running_db_instances(rds)

    text = ''
    if len(stopped_ec2_instances) > 0:
        text += '*' + str(len(stopped_ec2_instances)) + \
            '個のEC2インスタンスを停止させました*\n'
        for i in stopped_ec2_instances:
            text += ' - *' + i + '*\n'
        text += '\n'

    if len(stopped_rds_instances) > 0:
        text += '*' + str(len(stopped_rds_instances)) + \
            '個のRDSインスタンスを停止させました*\n'
        for i in stopped_rds_instances:
            text += ' - *' + i + '*\n'
        text += '\n'

    if len(stopped_ec2_instances) == 0 and len(stopped_rds_instances) == 0:
        text += '停止するインスタンスはありませんでした。:tada:'

    return post_to_slack(
        webhook_url=webhook_url,
        username=username,
        channel=channel,
        icon_emoji=icon_emoji,
        text=text
    )


def lambda_handler(event, context):
    return main()
