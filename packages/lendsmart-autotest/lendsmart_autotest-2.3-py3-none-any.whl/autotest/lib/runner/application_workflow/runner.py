"""
    Workflow tester
"""
import json
import time
import datetime
from dataclasses import dataclass, field
from ramda import path_or
from selenium.webdriver.chrome.webdriver import WebDriver
from autotest.lib.lib.node.node import NodeBuilder
from autotest.lib.lib.node.action import Action
from autotest.lib.client_builder.aws.client import AwsClient


@dataclass
class ApplicationWorkflowTest:
    """
    Test the application workflow
    """

    driver: WebDriver
    data: dict
    errors: list = field(default_factory=list)

    def load_initail_page(self):
        """
        start the initial page
        """
        url = path_or("", ["test_data", "entry_url"], self.data)
        return self.driver.get(url)

    def get_object_meta(self):
        """
        This function returns the object meta
        """
        return {
            "namespace": path_or("", ["test_data", "namespace"], self.data),
            "labels": {
                "product_name": path_or("", ["test_data", "product_name"], self.data),
            },
        }

    @staticmethod
    def get_current_time():
        """
        This function returns the current time
        """
        return str(datetime.datetime.now())

    def get_payload(self, results):
        """
        This function form the payload
        """
        return {
            "result": results,
            "object_meta": self.get_object_meta(),
            "metadata": {},
            "combination_group_id": path_or(
                "", ["test_data", "combination_group_id"], self.data
            ),
            "combination_unique_id": path_or(
                "", ["test_data", "combination_unique_id"], self.data
            ),
            "test_data": path_or({}, ["test_data"], self.data),
            "created_at": self.get_current_time(),
            "updated_at": self.get_current_time(),
        }

    def upload_report(self, report: dict):
        """
        This function will upload the report in database dynamodb
        """
        dynamodb_client = AwsClient().dynamodb()
        upload_result = dynamodb_client.upload("test_results", report)
        print("=======db upoad result", upload_result)
        return upload_result

    def run(self):
        """
        This function eill
        """
        print("=========Test started====", self.data)
        nodes = NodeBuilder().convert_json_to_obj(
            json_nodes=path_or([], ["test_data", "nodes"], self.data)
        )
        self.load_initail_page()
        time.sleep(10)
        results = Action(driver=self.driver, nodes=nodes).start()
        print("-------------results------------------", results)
        report = self.get_payload(results=results)
        print(json.dumps(report))
        return self.upload_report(report=report)
