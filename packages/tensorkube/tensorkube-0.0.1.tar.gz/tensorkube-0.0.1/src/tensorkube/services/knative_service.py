import subprocess

import click
import yaml
from kubernetes import config, client, utils

from tensorkube.constants import KNATIVE_SERVING_NAMESPACE, CONFIG_FEATURES

def get_instance_family_from_gpu_type(gpu_type):
    gpu_type = gpu_type.lower()
    if gpu_type == 'v100':
        return 'p3'
    elif gpu_type == 'a10g':
        return 'g5'
    else:
        raise ValueError(f"Unsupported GPU type: {gpu_type}")


def apply_knative_service(service_name: str, image_url: str, yaml_file_path: str, gpus: int, gpu_type: str):
    # Load kube config
    config.load_kube_config()

    # Read the YAML file
    with open(yaml_file_path, 'r') as f:
        yaml_content = f.read()

    # Replace the placeholders with the actual values
    yaml_content = yaml_content.replace('${SERVICE_NAME}', service_name)
    yaml_content = yaml_content.replace('${IMAGE_URL}', image_url)
    yaml_content = yaml_content.replace('${GPUS}', str(gpus))

    # Load the YAML content
    yaml_dict = yaml.safe_load(yaml_content)
    if gpus > 0:
        yaml_dict['spec']['template']['spec']['nodeSelector'] = {
            'karpenter.k8s.aws/instance-family': get_instance_family_from_gpu_type(gpu_type)
        }

    # Create a Kubernetes API client
    k8s_client = client.CustomObjectsApi()

    # Apply the configuration
    group = "serving.knative.dev"
    version = "v1"
    namespace = "default"
    plural = "services"

    k8s_client.create_namespaced_custom_object(group, version, namespace, plural, yaml_dict)

def enable_node_selector_feature(namespace=KNATIVE_SERVING_NAMESPACE):
    """
    Enable the nodeSelector feature in the config-features ConfigMap.

    Args:
        namespace (str): The namespace where the ConfigMap is located. Defaults to 'knative-serving'.
    """
    # Load the kubeconfig
    config.load_kube_config()

    # Create an instance of the API class
    v1 = client.CoreV1Api()

    try:
        # Get the existing config-features ConfigMap
        config_map = v1.read_namespaced_config_map(name=CONFIG_FEATURES, namespace=namespace)

        # Update the ConfigMap data
        if config_map.data is None:
            config_map.data = {}
        config_map.data['kubernetes.podspec-nodeselector'] = 'enabled'

        # Update the ConfigMap
        v1.patch_namespaced_config_map(name=CONFIG_FEATURES, namespace=namespace, body=config_map)
        print(f"Successfully enabled node selector feature in {CONFIG_FEATURES} ConfigMap.")
    except client.exceptions.ApiException as e:
        print(f"Exception when updating ConfigMap: {e}")
        raise

def list_deployed_services():
    # kubectl get ksvc
    command = ["kubectl", "get", "ksvc"]
    subprocess.run(command, check=True)


def cleanup_knative_resources():
    try:
        # kubectl delete ksvc --all -n <your-namespace>
        command = ["kubectl", "delete", "ksvc", "--all", "-n", "default"]
        subprocess.run(command, check=True)
    except Exception as e:
        click.echo(f"Error while cleaning up Knative services: {e}")
    try:
        # kubectl delete gateway --all -n istio-system
        command = ["kubectl", "delete", "gateway", "--all", "-n", "istio-system"]
        subprocess.run(command, check=True)
        #  kubectl delete gateway --all -n knative-serving
        command = ["kubectl", "delete", "gateway", "--all", "-n", "knative-serving"]
        subprocess.run(command, check=True)
    except Exception as e:
        click.echo(f"Error while cleaning up Istio gateways: {e}")


