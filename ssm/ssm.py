import boto3



if __name__ == '__main__':
    session = boto3.session.Session(profile_name='saml', region_name='us-east-1')
    ssm = session.client('ssm', region_name='us-east-1')
    x = ssm.get_parameter(Name='/fraud/artifacts/IAB_files/bots')['Parameter']['Value']
    print(x)
