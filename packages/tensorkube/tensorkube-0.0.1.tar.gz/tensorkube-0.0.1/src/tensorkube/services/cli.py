import pprint
import os
import time

import click
from pkg_resources import resource_filename

from tensorkube.services.aws_service import get_aws_account_id, get_cluster_name, get_credentials, get_bucket_name, \
    get_aws_user_arn, are_credentials_valid
from tensorkube.services.cloudformation_service import create_cloudformation_stack, stream_stack_events, \
    delete_cloudformation_stack, delete_launch_templates, cloudformation
from tensorkube.services.eks_service import get_current_clusters, install_karpenter, apply_karpenter_nodepool, \
    describe_cluster, apply_knative_crds, apply_knative_core, delete_knative_crds, delete_knative_core, \
    delete_karpenter_from_cluster, delete_karpenter_nodepool, apply_nvidia_plugin, create_eks_addon, delete_eks_addon, \
    update_eks_kubeconfig
from tensorkube.services.eksctl_service import create_base_tensorkube_cluster_eksctl, delete_cluster, \
    check_and_install_eksctl
from tensorkube.services.istio import check_and_install_istioctl, install_istio_on_cluster, install_net_istio, \
    install_default_domain, remove_domain_server, uninstall_istio_from_cluster
from tensorkube.services.knative_service import apply_knative_service, enable_node_selector_feature, \
    list_deployed_services, cleanup_knative_resources
from tensorkube.services.kubectl_utils import check_and_install_kubectl, check_and_install_helm
from tensorkube.services.local_service import check_and_install_cli_tools
from tensorkube.services.s3_service import create_s3_bucket, delete_s3_bucket, upload_files_in_parallel
from tensorkube.services.iam_service import create_mountpoint_iam_policy, detach_role_policy, delete_role, delete_policy
from tensorkube.services.ecr_service import get_or_create_ecr_repository, delete_all_tensorkube_ecr_repositories
from tensorkube.services.k8s_service import apply_k8s_kaniko_configs, create_aws_secret, create_kaniko_pv_and_pvc, \
    find_and_delete_old_kaniko_pod, check_pod_status, delete_aws_secret
from tensorkube.helpers import create_mountpoint_driver_role_with_policy, sanitise_name, \
    sanitise_assumed_role_arn
from tensorkube.constants import SERVICE_ACCOUNT_NAME, MOUNTPOINT_POLICY_NAME, MOUNTPOINT_DRIVER_ROLE_NAME, ADDON_NAME, \
    REGION, NAMESPACE


@click.group()
def tensorkube():
    pass


@tensorkube.group()
def list():
    pass


@list.command()
def deployments():
    list_deployed_services()


@tensorkube.command()
def init():
    click.echo("Initializing Tensorfuse runtime for your cloud...")
    # create cloudformation stack
    cloudformation()


@tensorkube.command()
def configure():
    click.echo("Configuring the Tensorfuse runtime for your cloud...")
    check_and_install_cli_tools()

    #check if tensorkube cluster already exists
    if get_cluster_name() in get_current_clusters():
        click.echo("Tensorkube cluster already exists. Skipping cluster creation.")
        return

    # create cloudformation stack
    cloudformation()
    # create eks cluster
    response = create_base_tensorkube_cluster_eksctl()
    click.echo(response)
    # install karpenter
    install_karpenter()
    # apply karpenter nodepool
    apply_karpenter_nodepool()

    # install istio networking plane
    check_and_install_istioctl()
    install_istio_on_cluster()

    # install knative crds
    apply_knative_crds()
    # install knative core
    apply_knative_core()

    # install nvidia plugin
    apply_nvidia_plugin()

    # install net istio
    install_net_istio()
    # install default domain
    install_default_domain()

    # create s3 bucket for kaniko
    bucket_name = get_bucket_name()
    create_s3_bucket(bucket_name)

    # create mountpoint policy to mount bucket to eks cluster
    create_mountpoint_iam_policy(MOUNTPOINT_POLICY_NAME, bucket_name)

    # create s3 csi driver role and attach mountpoint policy to it
    create_mountpoint_driver_role_with_policy(cluster_name=get_cluster_name(), account_no=get_aws_account_id(),
                                              role_name=MOUNTPOINT_DRIVER_ROLE_NAME, policy_name=MOUNTPOINT_POLICY_NAME)

    # create eks addon to mount s3 bucket to eks cluster
    create_eks_addon(get_cluster_name(), ADDON_NAME, get_aws_account_id(), MOUNTPOINT_DRIVER_ROLE_NAME)

    # create aws credentials cluster secret
    # TODO!: figure out how to update credentials in case of token expiry
    create_aws_secret(get_credentials())

    # create pv and pvc claims for kaniko
    create_kaniko_pv_and_pvc(bucket_name)

    # update knative to use pod labels
    enable_node_selector_feature()

    click.echo("Your tensorfuse cluster is ready and you are good to go.")




@tensorkube.command()
def account():
    """Get the AWS account ID."""
    click.echo(get_aws_account_id())


# The following commands can tear down all the resources that you have created and configured using the CLI.

# uninstall knative
# uninstall istio
# uninstall karpenter
# delete cluster

@tensorkube.command()
def teardown():
    click.echo("Tearing down all resources...")

    # TODO?: add logic to delete any other resources
    click.echo("Deleting all ECR repositories...")
    delete_all_tensorkube_ecr_repositories()

    # EKS addon
    try:
        click.echo("Deleting EKS addon...")
        delete_eks_addon(get_cluster_name(), ADDON_NAME)
    except Exception as e:
        click.echo(f"Error while deleting EKS addon: {e}")

    # Detach policy from role, delete role, delete policy
    click.echo("Deleting mountpoint driver role and policy...")
    click.echo("Detaching policy from role...")
    try:
        detach_role_policy(get_aws_account_id(), MOUNTPOINT_DRIVER_ROLE_NAME, MOUNTPOINT_POLICY_NAME)
        click.echo("Deleting role...")
        delete_role(MOUNTPOINT_DRIVER_ROLE_NAME)
        click.echo("Deleting policy...")
        delete_policy(get_aws_account_id(), MOUNTPOINT_POLICY_NAME)
    except Exception as e:
        click.echo(f"Error while deleting role and policy: {e}")

    # delete s3 bucket
    click.echo("Deleting S3 bucket...")
    try:
        delete_s3_bucket(get_bucket_name())
    except Exception as e:
        click.echo(f"Error while deleting S3 bucket: {e}")

    click.echo("Uninstalling domain server...")
    try:
        remove_domain_server()
    except Exception as e:
        click.echo(f"Error while uninstalling domain server: {e}")

    click.echo("Uninstalling Knative resources")
    try:
        cleanup_knative_resources()
    except Exception as e:
        click.echo(f"Error while cleaning up Knative resources: {e}")

    click.echo("Uninstalling and deleting Istio resources")
    try:
        uninstall_istio_from_cluster()
    except Exception as e:
        click.echo(f"Error while uninstalling Istio: {e}")
    click.echo("Uninstalling Knative core")
    try:
        delete_knative_core()
        click.echo("Uninstalling Knative CRDs")
        delete_knative_crds()
        click.echo("Successfully uninstalled Knative and Istio.")
    except Exception as e:
        click.echo(f"Error while uninstalling Knative: {e}")

    ## remove karpenter
    click.echo("Uninstalling Karpenter...")
    try:
        delete_karpenter_from_cluster()
        click.echo("Successfully uninstalled Karpenter.")
    except Exception as e:
        click.echo(f"Error while uninstalling Karpenter: {e}")
    # delete cluster
    try:
        click.echo("Deleting cluster...")
        delete_cluster()
        click.echo("Successfully deleted cluster.")
    except:
        click.echo("Error while deleting cluster.")
    try:
        # delete cloudformation stack
        click.echo("Deleting cloudformation stack...")
        delete_cloudformation_stack(get_cluster_name())
        click.echo("Successfully deleted cloudformation stack.")
    except:
        click.echo("Error while deleting cloudformation stack.")

    # delete launch templates
    click.echo("Deleting launch templates...")
    delete_launch_templates()
    click.echo("Successfully deleted launch templates.")
    click.echo("Tensorfuse has been successfully disconnected from your cluster.")


@tensorkube.command()
def clear():
    print(delete_cloudformation_stack(get_cluster_name()))


@tensorkube.command()
def test():
    print('Test command executed successfully')


@tensorkube.command()
@click.option('--gpus', default=0, help='Number of GPUs needed for the service.')
@click.option('--gpu-type', type=click.Choice(['V100', 'A10G'], case_sensitive=False), help='Type of GPU.')
def deploy(gpus, gpu_type):
    if gpus not in [0, 1, 4, 8]:
        click.echo('Error: Invalid number of GPUs. Only supported values are 0, 1, 4, and 8.')
        return
    cwd = os.getcwd()
    is_dockerfile_present = False
    for root, dirs, files in os.walk(cwd):
        for file in files:
            local_file = os.path.join(root, file)
            if local_file == cwd + "/Dockerfile":
                is_dockerfile_present = True
    if not is_dockerfile_present:
        click.echo("No Dockerfile found in current directory.")
        return
    else:
        bucket_name = get_bucket_name()
        project_name = os.path.basename(cwd)
        sanitised_project_name = sanitise_name(project_name)
        status = find_and_delete_old_kaniko_pod(sanitised_project_name)
        if not status:
            click.echo("Another deployment is already in progress. Please wait for the build to complete.")
            return

        # TODO!: add logic to update the aws-secret only if IAM Identity Center User
        credentials = get_credentials()
        if are_credentials_valid(credentials):
            click.echo("Updating aws-secret with the latest credentials...")
            delete_aws_secret()
            create_aws_secret(get_credentials())
        else:
            click.echo("The AWS credentials have expired. Please update the credentials.")
            return

        # TODO!: figure out how to upload only the updated files to the s3 bucket
        click.echo("Uploading the current directory to the S3 bucket...")
        upload_files_in_parallel(bucket_name=bucket_name, folder_path=cwd, s3_path="build/" + project_name + "/")

        click.echo("Building the Docker image and pushing to ECR...")
        ecr_repo_url = get_or_create_ecr_repository(sanitised_project_name)
        args = ["--context=dir:///data/build/" + project_name,
                "--dockerfile=/data/build/" + project_name + "/Dockerfile", "--destination=" + ecr_repo_url + ":latest"]

        apply_k8s_kaniko_configs(sanitised_project_name, SERVICE_ACCOUNT_NAME, args)
        # check for Kaniko pod to succeed
        while True:
            pod_status = check_pod_status("kaniko-{}".format(sanitised_project_name), NAMESPACE)
            if pod_status in ["Succeeded", "Failed"]:
                break
            print("Waiting for the image to be built...")
            time.sleep(10)
        if pod_status == 'Succeeded':
            click.echo("Successfully built and pushed the Docker image to ECR.")
            yaml_file_path = resource_filename('tensorkube',
                                               'configurations/kaniko_build_configs/knative_base_config.yaml')
            apply_knative_service(service_name=f"{sanitised_project_name}-gpus-{gpus}-{str(gpu_type).lower()}",
                                  image_url=ecr_repo_url, yaml_file_path=yaml_file_path, gpus=gpus, gpu_type=gpu_type)
        else:
            click.echo(
                "Failed to build the Docker image. Please check the logs for more details. Pod status: {}".format(
                    pod_status))


@tensorkube.command()
def delete_project():
    click.echo("Deleting the project resources...")
    # TODO!: add logic to delete the ecr repository, s3 folder, kaniko pod, and any other resources
    click.echo("Successfully deleted the project resources.")


@tensorkube.command()
def get_permissions_command():
    # TODO: give details of cluster user as well
    click.echo(
        "Ask the initial user to run this command to grant you the necessary permissions to the Tensorkube EKS cluster:")

    user_arn = get_aws_user_arn()
    final_arn = None
    if 'assumed-role' in user_arn:
        final_arn = sanitise_assumed_role_arn(user_arn)
    else:
        final_arn = user_arn

    click.echo("""\
    eksctl create iamidentitymapping \\
    --cluster tensorkube \\
    --region {} \\
    --arn {} \\
    --group system:masters \\
    --username <USERNAME_OF_YOUR_CHOICE>""".format(REGION, final_arn))

    click.echo("Once you have access to the cluster, run the following command to sync the config files:")
    click.echo("tensorkube sync")

    # eksctl create iamidentitymapping --cluster $CLUSTER_NAME --region $AWS_DEFAULT_REGION --arn arn:aws:iam::<ACC NO>:role/<ROLE NAME>  --group system:masters --username <CLUSTER USERNAME>  # eksctl create iamidentitymapping --cluster $CLUSTER_NAME --region $AWS_DEFAULT_REGION --arn arn:aws:iam::<ACC NO>:user/<USERNAME> --group system:masters --username <CLUSTER USERNAME>


@tensorkube.command()
def sync():
    click.echo("Syncing config files for the tensorkube cluster...")
    click.echo("Updating kubeconfig...")
    update_eks_kubeconfig()
    click.echo("Successfully updated the kubeconfig file.")
