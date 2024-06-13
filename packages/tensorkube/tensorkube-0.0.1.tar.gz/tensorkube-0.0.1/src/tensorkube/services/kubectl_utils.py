import platform
import subprocess


def check_and_install_kubectl():
    """Check if kubectl is installed."""
    try:
        subprocess.run(["kubectl", "version"], check=True)
    except Exception as e:
        # check if the operating system is mac and install kubectl
        if platform.system() == "Darwin":
            try:
                subprocess.run(["brew", "install", "kubectl"])
            except Exception as e:
                print("Unable to install kubectl. Please install kubectl manually.")

def check_and_install_helm():
    """Check if helm is installed."""
    try:
        subprocess.run(["helm", "version"], check=True)
    except Exception as e:
        # check if the operating system is mac and install helm
        if platform.system() == "Darwin":
            try:
                subprocess.run(["brew", "install", "helm"])
            except Exception as e:
                print("Unable to install helm. Please install helm manually.")

