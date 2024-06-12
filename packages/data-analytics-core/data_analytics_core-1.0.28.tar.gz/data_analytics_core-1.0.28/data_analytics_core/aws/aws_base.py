import os
from abc import ABC
import boto3
# custom imports
from data_analytics_core.localstack.boto_client_moks.localstack_clients import boto3_client_localstack, \
    boto3_resource_localstack


class AmazonWebServicesInterface(ABC):
    def __call__(self, client: str, region_name: str = "eu-central-1", needs_resource_init: bool = False):
        self.region = region_name
        if os.getenv("LOCALSTACK_ENDPOINT_URL"):
            self.client = boto3_client_localstack(service_name=client, region_name=self.region)
        else:
            self.client = boto3.client(client, region_name=self.region)
        if needs_resource_init:
            if os.getenv("LOCALSTACK_ENDPOINT_URL"):
                self.resource = boto3_resource_localstack(service_name=client, region_name=self.region)
            else:
                self.resource = boto3.resource(client, region_name=self.region)

