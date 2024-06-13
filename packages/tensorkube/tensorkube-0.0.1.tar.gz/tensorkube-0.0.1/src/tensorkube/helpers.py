from tensorkube.services.eks_service import get_cluster_oidc_issuer_url
from tensorkube.services.iam_service import create_s3_csi_driver_role, attach_role_policy
from tensorkube.constants import NAMESPACE, SERVICE_ACCOUNT_NAME, REGION
import base64
import json
import os

def create_mountpoint_driver_role_with_policy(cluster_name, account_no, role_name, policy_name, 
                                              service_account_name=SERVICE_ACCOUNT_NAME, 
                                              namespace=NAMESPACE, region=REGION):
    oidc_issuer_url = get_cluster_oidc_issuer_url(cluster_name)
    create_s3_csi_driver_role(account_no, role_name, oidc_issuer_url,
                              namespace, service_account_name)
    attach_role_policy(account_no, policy_name, role_name, region)


def get_base64_encoded_docker_config(username: str, password: str, email: str):
    auth = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
        
    docker_config_dict = {
        "auths": {
            "https://index.docker.io/v1/": {
                "username": username,
                "password": password,
                "email": email,
                "auth": auth,
            }
        }
    }


    base64_encoded_docker_config = base64.b64encode(
            json.dumps(docker_config_dict).encode("utf-8")
        ).decode("utf-8")
    return base64_encoded_docker_config


def sanitise_name(name: str):
    return name\
        .replace("_", "-")\
        .replace(" ", "-")\
        .lower()


def sanitise_assumed_role_arn(arn: str):
    arn = arn.replace('assumed-role', 'role')
    last_slash_index = arn.rfind('/')
    if last_slash_index != -1:
        arn = arn[:last_slash_index]
    return arn
