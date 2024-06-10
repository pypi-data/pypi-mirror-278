"""
    This module will send trigger to lambda
"""
import json
import boto3


class LambdaObj:
    """
    invoke the lambda
    """

    def __init__(self) -> None:
        self.__lambda_client = boto3.client("lambda")

    def invoke(self, payload : dict, function_name : str, trigger_type=None):
        """
        invoke the lambda
        """
        if trigger_type is None:
            trigger_type = "Event"
        return self.__lambda_client.invoke(
            FunctionName=function_name,
            InvocationType=trigger_type,
            Payload=json.dumps(payload),
        )
