"""
    This module will generate the test data for each question
"""
from ramda import path_or
from autotest.lib.generator.intent.intent import Question
from autotest.lib.generator.question_type import QuestionTypeFinder, QuestionType


class GenerateTestData:
    """
    This class will generate test data
    Args :
        single_combination : A single flow of questions
    """

    def __init__(
        self, single_combination: list[Question], all_questions, test_case_data
    ) -> None:
        self.single_combination = single_combination
        self.all_questions = all_questions
        self.test_case_data = test_case_data

    def start(self):
        """
        This function will generate the test data for a flow
        """
        test_data = []
        for idx, question in enumerate(self.single_combination):
            data = QuestionDataGenerator(
                question=question,
                single_combination=self.single_combination[idx - 1 :],
                all_questions=self.all_questions,
                test_case_data=self.test_case_data,
            ).generate_data()
            test_data.append(data)
        return test_data


class QuestionDataGenerator:
    """
    A class that generate test data for single question
    """

    def __init__(
        self,
        question: Question,
        single_combination: list,
        all_questions,
        test_case_data,
    ):
        self.question = question
        self.single_combination = single_combination
        self.all_questions = all_questions
        self.test_case_data = test_case_data

    def generate_data(self):
        """
        Generate test data based on option
        """
        try:
            actions = self.question_type_map()(
                question=self.question,
                sparsed_questions=self.single_combination,
                all_questions=self.all_questions,
                test_data_set=self.test_case_data,
            ).get()
            data = {"actions": [i.__dict__ for i in actions], "intent_data": self.question.question}
            return data
        except Exception as err:
            print("error happened ===>", err)
            return {}

    def question_type_map(self) -> QuestionType:
        """
        Hold the map of question types
        """
        question_type_or_intent_type = path_or("", ["question_type"], self.question.question) \
            or path_or("",["intent_type"], self.question.question)
        return QuestionTypeFinder().get_type_obj(
            question_type=question_type_or_intent_type
        )
