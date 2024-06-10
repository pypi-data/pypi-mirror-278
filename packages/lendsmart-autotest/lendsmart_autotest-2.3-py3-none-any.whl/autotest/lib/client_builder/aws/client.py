"""
    This module hold the aws clients
"""

from dataclasses import dataclass
from autotest.lib.client_builder.aws.dynamodb import DynamodDBClient
from autotest.lib.client_builder.aws.lambda_obj import LambdaObj


@dataclass
class AwsClient:
    """
    hold the aws resource client
    """

    def dynamodb(self):
        """
        returns the dynamodb client
        """
        return DynamodDBClient()

    def lambda_obj(self):
        """
        this function returns the lambda obj
        """
        return LambdaObj()
