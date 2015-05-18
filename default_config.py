config = {

    # AWS credentials for the IAM user (alternatively can be set up as environment variables)
    'aws_access_key': '',
    'aws_secret_key': '',

    # EC2 info about your server's region
    'ec2_region_name': 'eu-central-1',
    'ec2_region_endpoint': 'ec2.eu-central-1.amazonaws.com',

    # Tag of the EBS volume you want to take the snapshots of
    'tag_name': 'tag:NeedSnapshotting',
    'tag_value': 'True',

    # Number of snapshots to keep (the older ones are going to be deleted,
    # since they cost money).
    'keep': 5,

    # Path to the log for this script
    'log_file': '/tmp/makesnapshots.log',

}