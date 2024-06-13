import json
import boto3
from pkg_resources import resource_filename
from tensorkube.constants import REGION

def create_mountpoint_iam_policy(policy_name, bucket_name, region=REGION):
    policy_file_path = resource_filename('tensorkube', 'configurations/aws_configs/mountpoint_policy.json')
    with open(policy_file_path, 'r') as f:
        policy = json.load(f)
    for statement in policy['Statement']:
        statement['Resource'] = [r.replace('USER_BUCKET', bucket_name) for r in statement['Resource']]

    iam = boto3.client('iam', region_name=region)
    response = iam.create_policy(
        PolicyName=policy_name,
        PolicyDocument=json.dumps(policy)
    )
    return response


def create_s3_csi_driver_role(account_no: str, role_name: str, oidc_issuer_url: str, 
                              namespace: str, service_account_name: str):
    oidc_issuer = oidc_issuer_url[8:]
    region = oidc_issuer.split('.')[2]
    trust_policy_file_path = resource_filename('tensorkube', 
                                               'configurations/aws_configs/aws_s3_csi_driver_trust_policy.json')
    with open(trust_policy_file_path, 'r') as f:
        trust_policy = json.load(f)
    trust_policy['Statement'][0]['Principal']['Federated'] \
        = 'arn:aws:iam::{}:oidc-provider/{}'.format(account_no, oidc_issuer)
    trust_policy['Statement'][0]['Condition']['StringEquals'] = {
          "{}:sub".format(oidc_issuer): "system:serviceaccount:{}:{}".format(namespace, service_account_name),
          "{}:aud".format(oidc_issuer): "sts.amazonaws.com"
        }

    iam = boto3.client('iam', region_name=region)
    response = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=json.dumps(trust_policy),
    )
    return response


def attach_role_policy(account_no, policy_name, role_name, region=REGION):
    client = boto3.client('iam', region_name=region)
    response = client.attach_role_policy(
        PolicyArn='arn:aws:iam::{}:policy/{}'.format(account_no, policy_name),
        RoleName=role_name,
    )
    return response


def detach_role_policy(account_no, role_name, policy_name, region=REGION):
    client = boto3.client('iam', region_name=region)
    response = client.detach_role_policy(
        PolicyArn='arn:aws:iam::{}:policy/{}'.format(account_no, policy_name),
        RoleName=role_name,
    )
    return response


def delete_role(role_name, region=REGION):
    client = boto3.client('iam', region_name=region)
    response = client.delete_role(RoleName=role_name)
    return response


def delete_policy(account_no, policy_name, region=REGION):
    client = boto3.client('iam', region_name=region)
    response = client.delete_policy(
        PolicyArn='arn:aws:iam::{}:policy/{}'.format(account_no, policy_name)
    )
    return response
