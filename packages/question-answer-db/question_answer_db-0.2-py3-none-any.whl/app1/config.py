
def get_sagemaker_endpoint_name():
    endpoint_name = input("Enter the SageMaker endpoint name: ")
    return endpoint_name

SAGEMAKER_ENDPOINT_NAME = get_sagemaker_endpoint_name()
