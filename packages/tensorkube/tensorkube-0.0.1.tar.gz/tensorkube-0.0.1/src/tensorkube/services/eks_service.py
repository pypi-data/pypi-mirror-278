import subprocess


from kubernetes import config, client, utils
import boto3
from pkg_resources import resource_filename

from tensorkube.constants import REGION

from tensorkube.configurations.configuration_urls import KNATIVE_CRD_URL, KNATIVE_CORE_URL
from tensorkube.services.aws_service import get_eks_client, get_karpenter_version, get_karpenter_namespace, \
    get_cluster_name, get_kubernetes_context_name


def get_current_clusters():
    """Get all the clusters in the current AWS account."""
    eks_client = get_eks_client()
    response = eks_client.list_clusters()
    if response.get("clusters"):
        return response.get("clusters")
    return []


def get_pods_using_namespace(namespace):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace=namespace)
    return pods


def describe_cluster(cluster_name):
    eks_client = get_eks_client()
    response = eks_client.describe_cluster(name=cluster_name)
    return response


def install_karpenter():
    # Logout from helm registry
    logout_command = ["helm", "registry", "logout", "public.ecr.aws"]
    try:
        subprocess.run(logout_command, check=True)
    except Exception as e:
        pass

    # Install/upgrade karpenter
    install_command = ["helm", "upgrade", "--install", "karpenter", "oci://public.ecr.aws/karpenter/karpenter",
                       "--version", get_karpenter_version(), "--namespace", get_karpenter_namespace(),
                       "--create-namespace", "--set", f"settings.clusterName={get_cluster_name()}", "--set",
                       f"settings.interruptionQueue={get_cluster_name()}", "--set",
                       "controller.resources.requests.cpu=1", "--set", "controller.resources.requests.memory=1Gi",
                       "--set", "controller.resources.limits.cpu=1", "--set", "controller.resources.limits.memory=1Gi",
                       "--wait"]
    try:
        subprocess.run(install_command, check=True)
    except Exception as e:
        print(f"Error while installing karpenter: {e}")
        # now try running by logging into ecr
        # aws ecr get-login-password --region your-region | helm registry login --username AWS --password-stdin public.ecr.aws
        login_command = ["aws", "ecr", "get-login-password", "--region", REGION, "|", "helm", "registry", "login",
                         "--username", "AWS", "--password-stdin", "public.ecr.aws"]
        try:
            subprocess.run(login_command, check=True)
            subprocess.run(install_command, check=True)
        except Exception as e:
            print(f"Error while installing karpenter: {e}")



def delete_karpenter_from_cluster():
    # helm uninstall karpenter --namespace "${KARPENTER_NAMESPACE}"
    command = ["helm", "uninstall", "karpenter", "--namespace", get_karpenter_namespace()]
    subprocess.run(command, check=True)


def apply_karpenter_nodepool():
    file_name = resource_filename('tensorkube', 'configurations/karpenter_nodepool_deploy.yaml')
    command = ["kubectl", "apply", "-f", f"{file_name}"]
    subprocess.run(command, check=True)


def update_eks_kubeconfig(region: str=REGION):
    command = ["aws", "eks", "update-kubeconfig", "--name", get_cluster_name(), "--region", region]
    subprocess.run(command, check=True)


def delete_karpenter_nodepool():
    file_name = resource_filename('tensorkube', 'configurations/karpenter_nodepool_deploy.yaml')
    command = ["kubectl", "delete", "-f", f"{file_name}", "-v=10"]
    subprocess.run(command, check=True)


def apply_nvidia_plugin():
    # kubectl create -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.9.0/nvidia-device-plugin.yml
    # using k8s python client
    command = ["kubectl", "create", "-f",
               "https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.9.0/nvidia-device-plugin.yml"]
    subprocess.run(command, check=True)



def apply_yaml_from_url(url, error_context):
    command = ["kubectl", "apply", "-f", url]
    try:
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"Error while {error_context}: {e}")


def delete_resources_from_url(url, error_context):
    command = ["kubectl", "delete", "-f", url]
    try:
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"Error while {error_context}: {e}")


def apply_knative_crds():
    apply_yaml_from_url(KNATIVE_CRD_URL, "installing Knative CRDs")


def delete_knative_crds():
    delete_resources_from_url(KNATIVE_CRD_URL, "deleting Knative CRDs")


def apply_knative_core():
    apply_yaml_from_url(KNATIVE_CORE_URL, "installing Knative core")


def delete_knative_core():
    delete_resources_from_url(KNATIVE_CORE_URL, "deleting Knative core")


def get_cluster_oidc_issuer_url(cluster_name):
    client = boto3.client('eks')
    response = client.describe_cluster(name=cluster_name)
    return response['cluster']['identity']['oidc']['issuer']



def create_eks_addon(cluster_name, addon_name, account_no, 
                     mountpoint_driver_role_name, region=REGION):
    client = boto3.client('eks', region_name=region)
    response = client.create_addon(
        addonName=addon_name,
        clusterName=cluster_name,
        serviceAccountRoleArn='arn:aws:iam::{}:role/{}'.format(account_no, mountpoint_driver_role_name),
    )
    return response

def delete_eks_addon(cluster_name, addon_name, region=REGION):
    client = boto3.client('eks', region_name=region)
    response = client.delete_addon(
        addonName=addon_name,
        clusterName=cluster_name,
    )
    return response
