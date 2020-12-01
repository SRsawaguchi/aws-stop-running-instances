import boto3

def get_ec2_client():
    return boto3.client('ec2')

def find_running_instances(ec2client):
    resp = ec2client.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            },
    ])

    instances = list()
    for resv in resp['Reservations']:
        instances.append(resv["Instances"][0])

    return instances

def stop_instances(ec2client, ids):
    resp = ec2client.stop_instances(InstanceIds=ids)
    return resp['StoppingInstances']


def stop_running_instances(ec2client):
    instances = find_running_instances(ec2client)

    instance = [i['InstanceId'] for i in instances]

    stoppingInstances = stop_instances(
        ec2client,
        ids=[i['InstanceId'] for i in instances]
    )

    for instance in stoppingInstances:
        print('stopping: ' + instance['InstanceId'])


stop_running_instances(get_ec2_client())
