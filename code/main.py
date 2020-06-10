import os
import json
import time
import subprocess
from azureml.core import Workspace, Experiment
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.pipeline.core import PipelineRun
from azureml.exceptions import AuthenticationException, ProjectSystemException, AzureMLException, UserErrorException
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError
from json import JSONDecodeError
from utils import AMLConfigurationException, ActionDeploymentError, AMLExperimentConfigurationException, required_parameters_provided, mask_parameter, convert_to_markdown, load_pipeline_yaml, load_runconfig_yaml, load_runconfig_python

    
def main():
    azure_credentials = os.environ.get("INPUT_AZURE_CREDENTIALS", default="{}")
    try:
        azure_credentials = json.loads(azure_credentials)
        print(azure_credentials)
    except JSONDecodeError:
        print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS")
        raise AMLConfigurationException(f"Incorrect or poorly formed output from azure credentials saved in AZURE_CREDENTIALS secret. See setup in https://github.com/Azure/aml-workspace/blob/master/README.md")
    required_parameters_provided(
        parameters=azure_credentials,
        keys=["tenantId", "clientId", "clientSecret"],
        message="Required parameter(s) not found in your azure credentials saved in AZURE_CREDENTIALS secret for logging in to the workspace. Please provide a value for the following key(s): "
    )
    print("::debug::Masking parameters")
    mask_parameter(parameter=azure_credentials.get("tenantId", ""))
    mask_parameter(parameter=azure_credentials.get("clientId", ""))
    mask_parameter(parameter=azure_credentials.get("clientSecret", ""))
    mask_parameter(parameter=azure_credentials.get("subscriptionId", ""))
    print("::debug::Loading parameters file")
    print("4--------------------------------------")

    tenant_id=azure_credentials.get("tenantId", "")
    service_principal_id=azure_credentials.get("clientId", "")
    service_principal_password=azure_credentials.get("clientSecret", "")
    print(service_principal_password)
    command = ('az login --service-principal --username {APP_ID} --password {PASSWORD} --tenant {TENANT_ID}').format(
           APP_ID=service_principal_id, PASSWORD=service_principal_password, TENANT_ID=tenant_id)    
    #command='az login --service-principal --username "ab96606e-49a7-45d3-a575-5172e11fdb7f" --password "^s:e6b4uCMXxN168t+i?[f](\\`E~8YeAP" --tenant "2d1aba9c-5938-402b-90b9-72a284a4bced"'
    try:
        app_create = subprocess.check_output(command, shell=True)
        print(app_create)
    except Exception as ex:
        print(ex) 

if __name__ == "__main__":
    main()
