import boto3


def get_ec2_client():
    return boto3.client('ec2')


def get_rds_client():
    return boto3.client('rds')


def contains_tag(tags, key, value):
    for tag in tags:
        if tag['Key'] == key and tag['Value'] == value:
            return True
    return False


def find_running_db_instances(rds_client):
    resp = rds_client.describe_db_instances()
    running_instance_ids = list()
    for instance in resp['DBInstances']:
        if instance['DBInstanceStatus'] != 'available':
            continue

        arn = instance['DBInstanceArn']
        tags = rds_client.list_tags_for_resource(ResourceName=arn)['TagList']
        if contains_tag(tags, 'Env', 'dev'):
            running_instance_ids.append(instance['DBInstanceIdentifier'])

    return running_instance_ids


def stop_db_instances(rds_client, ids):
    for db_identifier in ids:
        rds_client.stop_db_instance(DBInstanceIdentifier=db_identifier)
        print('[rds] stopping: ' + db_identifier)


def find_running_instances(ec2_client):
    resp = ec2_client.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['running']
            },
            {
                'Name': 'tag:Env',
                'Values': ['dev']
            }
        ])
    instances = list()
    for resv in resp['Reservations']:
        instances.append(resv["Instances"][0])

    return instances


def stop_running_db_instances(rds_client):
    ids = find_running_db_instances(rds_client)
    if len(ids) == 0:
        print('[rds] There is no running db instances.')
        return
    stop_db_instances(rds_client, ids)


def stop_ec2_instances(ec2_client, ids):
    resp = ec2_client.stop_instances(InstanceIds=ids)
    return resp['StoppingInstances']


def stop_running_ec2_instances(ec2_client):
    instances = find_running_instances(ec2_client)
    if len(instances) == 0:
        print('[ec2] There is no running ec2 instances.')
        return

    stoppingInstances = stop_ec2_instances(
        ec2_client,
        ids=[i['InstanceId'] for i in instances]
    )
    for instance in stoppingInstances:
        print('[ec2] stopping: ' + instance['InstanceId'])


stop_running_ec2_instances(get_ec2_client())
stop_running_db_instances(get_rds_client())
