import platform
import subprocess

import click

from tensorkube.configurations.configuration_urls import DOMAIN_SERVER_URL, KNATIVE_ISTIO_CONTROLLER_URL
from tensorkube.services.eks_service import get_pods_using_namespace, apply_yaml_from_url, delete_resources_from_url


def check_and_install_istioctl():
    """Check if istioctl is installed."""
    try:
        subprocess.run(["istioctl", "version"], check=True)
    except Exception as e:
        # check if the operating system is mac and install istioctl
        if platform.system() == "Darwin":
            try:
                subprocess.run(["brew", "install", "istioctl"])
            except Exception as e:
                print("Unable to install istioctl. Please install istioctl manually.")


def install_istio_on_cluster():
    """Install Istio with the default profile."""
    try:
        subprocess.run(["istioctl", "install", "--set", "profile=default", "-y"])
        print("Istio installed successfully.")
    except Exception as e:
        print(f"Error installing Istio: {e}")
    # finally using the kubeconfi
    pods = get_pods_using_namespace("istio-system")
    for pod in pods.items:
        click.echo(f"Pod name: {pod.metadata.name}, Pod status: {pod.status.phase}")


def remove_domain_server():
    delete_resources_from_url(DOMAIN_SERVER_URL, "removing Knative Default Domain")


def uninstall_istio_from_cluster():
    """Uninstall Istio from the cluster."""
    # remove knative istion controller
    delete_resources_from_url(KNATIVE_ISTIO_CONTROLLER_URL, "uninstalling Knative Net Istio")
    # remove istio
    try:
        subprocess.run(["istioctl", "x", "uninstall", "--purge", "-y"])
        click.echo("Istio uninstalled successfully.")
    except Exception as e:
        click.echo(f"Error uninstalling Istio: {e}")


def install_net_istio():
    apply_yaml_from_url(KNATIVE_ISTIO_CONTROLLER_URL, "installing Knative Net Istio")


def install_default_domain():
    apply_yaml_from_url(DOMAIN_SERVER_URL, "installing Knative Default Domain")
