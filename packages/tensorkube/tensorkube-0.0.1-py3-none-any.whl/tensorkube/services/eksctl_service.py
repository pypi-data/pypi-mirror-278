import os
import platform
import subprocess
from string import Template

import click
from pkg_resources import resource_filename

from tensorkube.services.aws_service import get_aws_account_id, get_karpenter_namespace, get_cluster_name


# create base cluster using eksctl

def create_base_tensorkube_cluster_eksctl(cluster_name: str = 'tensorkube'):
    yaml_file_path = resource_filename('tensorkube', 'configurations/base_cluster.yaml')
    # variables
    variables = {"CLUSTER_NAME": cluster_name, "AWS_DEFAULT_REGION": "us-east-1", "K8S_VERSION": "1.29",
                 "AWS_ACCOUNT_ID": get_aws_account_id(), "KARPENTER_NAMESPACE": get_karpenter_namespace(),
                 "AWS_PARTITION": "aws", }

    with open(yaml_file_path) as file:
        template = file.read()
    yaml_content = Template(template).substitute(variables)

    temp_yaml_file_path = "/tmp/temp_cluster.yaml"
    with open(temp_yaml_file_path, 'w') as file:
        file.write(yaml_content)

        # Run the eksctl create cluster command
    command = ["eksctl", "create", "cluster", "-f", temp_yaml_file_path]
    subprocess.run(command, check=True)

    # Remove the temporary file
    os.remove(temp_yaml_file_path)


def delete_cluster():
    command = ["eksctl", "delete", "cluster", "--name", get_cluster_name()]
    subprocess.run(command)


def check_and_install_eksctl():
    """Check if eksctl is installed and if not isntall it."""
    try:
        subprocess.run(["eksctl", "version"], check=True)
    except Exception as e:
        # check if the operating system is mac and install eksctl
        if platform.system() == "Darwin":
            try:
                subprocess.run(["brew", "install", "eksctl"])
            except Exception as e:
                print("Unable to install eksctl. Please install eksctl manually.")
