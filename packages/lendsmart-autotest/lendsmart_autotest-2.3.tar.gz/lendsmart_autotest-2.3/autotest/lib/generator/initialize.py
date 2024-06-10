"""
    This module will generate the test flows from intent json
"""
import random
import asyncio
from ramda import path_or
from autotest.lib.lib.lend_event import LendEvent
from autotest.lib.generator.intent.intent import Questions
from autotest.lib.generator.graph import DirectedGraphBuilder
from autotest.lib.generator.generate_test_data import GenerateTestData
from autotest.lib.generator.test_data import TEST_DATA_SETS
from autotest.lib.client_builder.aws.client import AwsClient
from autotest.lib.utilities.random_email import get_random_string


class FlowGeneratorInitializer:
    """
    This class will generate the test flows
    """

    def __init__(self, lend_event: LendEvent):
        self.__lend_event = lend_event
        self.__event_data = path_or({}, ["event_data"], self.__lend_event.event_data)

    def get_intent(self):
        """
        This function returns the intent
        """
        return path_or({}, ["intent_data", "data", 0], self.__event_data)

    def get_product_name(self):
        """
        This function returns the product name
        """
        return path_or("", ["product_name"], self.__event_data)

    def get_loan_role(self):
        """
        This function retuen the loan role
        """
        return path_or("", ["loan_role"], self.__event_data)

    def get_namespace(self):
        """
        This function return the namespace of the intent
        """
        return path_or("", ["object_meta", "namespace"], self.get_intent())

    def get_test_case_stub_datas(self):
        """
        This function will get the stub data to feed into the test action
        generator
        """
        test_datas_requested = path_or([], ["test_datas"], self.__event_data)
        namespace = self.get_namespace()
        stub_datas = []
        for stub_data in TEST_DATA_SETS:
            if (
                namespace in path_or([], ["namespaces"], stub_data)
                and stub_data["use_case_name"] in test_datas_requested
            ):
                stub_datas.append(stub_data)
        return stub_datas

    def get_role_question_groups(self, intent):
        """
        This will return the question groups by loan role
        """
        role_groups = []
        product_section = intent.get_section_by_product(
            product_name=self.get_product_name()
        )

        for group in product_section.groups:
            role_question_group = group.get_role_question_group_by_loan_role(
                loan_role=self.get_loan_role()
            )
            # print("========>Role question groups==>", role_question_group)
            if not role_question_group:
                continue
            role_groups.extend(role_question_group)
        return [element for sublist in role_groups for element in sublist.items]

    def get_question_ids(self, role_question_groups: list, all_question_groups: list):
        """
        This function will return the list of questions
        """
        res = []

        def get_matched_question_group(rqg):
            for que_group in all_question_groups:
                if que_group.name == rqg:
                    return que_group
            return None

        for rqg in role_question_groups:
            match_qg = get_matched_question_group(rqg)
            if not match_qg:
                continue
            res.extend(match_qg.question_ids)

        return res

    def get_question_objs(self, intent):
        """
        This function will get the matched question
        """
        res = []
        role_question_groups = self.get_role_question_groups(intent=intent)
        all_question_groups = intent.question_groups

        matched_question_ids = self.get_question_ids(
            role_question_groups=role_question_groups,
            all_question_groups=all_question_groups,
        )
        for question_id in matched_question_ids:
            question = intent.get_question_by_id(question_id=question_id)
            if question is None:
                continue
            res.append(question)
        return res

    def get_matched_questions(self):
        """
        This function will return the matched questions
        """
        intent = Questions(intent=self.get_intent())
        return self.get_question_objs(intent=intent)

    def get_directed_graph_builder(self):
        """
        This function will return the directed graph builder
        """
        return DirectedGraphBuilder(sparse_questions=self.get_matched_questions())

    def get_random_combinations(self, combinations: list[list]):
        """
        This function will select random combinations
        """
        selected_combination_index = path_or(
            "", ["selected_combination_index"], self.__event_data
        )
        if selected_combination_index:
            selected_combination_index = int(selected_combination_index)
            return [path_or([], [selected_combination_index], combinations)]
        combination_samples = (
            path_or(5, ["combination_samples"], self.__event_data) or 5
        )
        return random.sample(combinations, int(combination_samples))

    def generate_test_actions(self, combo, all_questions, test_case_data):
        """
        This function will generate the test actions
        """
        return GenerateTestData(
            single_combination=combo,
            all_questions=all_questions,
            test_case_data=test_case_data,
        ).start()

    def get_generated_actions(
        self,
        test_case_data,
        rand_combinations: list[list],
        all_questions,
        all_combos: list,
    ):
        """
        This function will generate test actions
        """
        test_data = []
        for combo in rand_combinations:
            random_combo_index = all_combos.index(combo)
            print(
                "------------------------------------------------", random_combo_index
            )
            data = self.generate_test_actions(
                combo=combo, all_questions=all_questions, test_case_data=test_case_data
            )
            test_data.append(
                {
                    "name": path_or("", ["use_case_name"], test_case_data),
                    "data": data,
                    "combination": [
                        {
                            "question": path_or("", ["question"], i.question)
                            or path_or("", ["question_id"], i.question),
                            "option": i.selected_option.__dict__
                            if i.selected_option
                            else "",
                        }
                        for i in combo
                    ],
                }
            )
        return test_data

    def get_test_datas(self, combinations: list[list]):
        """
        This function will generate the test data
        """
        random_combo = self.get_random_combinations(combinations)
        test_case_stub = self.get_test_case_stub_datas()
        all_questions = self.get_matched_questions()
        test_data = []
        for test_case_data in test_case_stub:
            test_data.extend(
                self.get_generated_actions(
                    test_case_data=test_case_data,
                    rand_combinations=random_combo,
                    all_questions=all_questions,
                    all_combos=combinations,
                )
            )
        return test_data

    async def send_trigger(self, payload):
        """
        This function will send trigger to runner lambda
        """
        lambda_obj = AwsClient().lambda_obj()
        return lambda_obj.invoke(payload, "autotest_test")

    async def create_async_invoke(self, test_data_list: list):
        """
        This function create async invokes
        """
        results = await asyncio.gather(
            *[
                asyncio.create_task(self.send_trigger(payload))
                for payload in test_data_list
            ]
        )
        return results

    async def trigger_runner(self, test_data_list: list):
        """
        This function will trigger the runner
        """
        return await self.create_async_invoke(test_data_list)

    def form_payload(self, test_data: dict):
        """
        This function will form the payload
        """
        res = []
        combination_group_id = get_random_string()
        for data in test_data:
            res.append(
                {"event_data" :{
                    "test_data": { 
                        "chrome_driver_path": path_or(
                            "", ["chrome_driver_path"], self.__event_data
                        ),
                        "headless_chromium_path": path_or(
                            "", ["headless_chromium_path"], self.__event_data
                        ),
                        "browser_type" : path_or(
                            "", ["browser_type"], self.__event_data
                        ),
                        "test_type": "APPLICATION_WORKFLOW",
                        "combination_group_id": combination_group_id,
                        "combination_unique_id": get_random_string(),
                        "namespace": self.get_namespace(),
                        "entry_url": path_or("", ["entry_url"], self.__event_data),
                        "product_name": path_or(
                            "", ["product_name"], self.__event_data
                        ),
                        "loan_role": path_or("", ["loan_role"], self.__event_data),
                        "test_case_name": path_or("", ["name"], data),
                        "nodes": path_or([], ["data"], data),
                        "combinations": path_or([], ["combination"], data),
                    }
                }}
            )
        return res

    def generate_test_data(self):
        """
        Return the test datas
        """
        graph_builder = self.get_directed_graph_builder()
        possible_combinations = graph_builder.build()
        return self.get_test_datas(combinations=possible_combinations)

    def get_payload(self):
        """
        This function return the payload
        """
        return self.form_payload(test_data=self.generate_test_data())

    def start(self):
        """
        starts the generator
        """
        payload = self.get_payload()
        import json

        print(json.dumps(payload))
        return asyncio.run(self.trigger_runner(payload))
