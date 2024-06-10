"""
    Hold the differnt type of questions
"""
import random
from dataclasses import dataclass
from abc import ABC, abstractmethod
from ramda import path_or
from autotest.lib.generator.intent.intent import Question
from autotest.lib.generator.graph import QuestionCategorizer, AdjacentQuestions
from autotest.lib.utilities.random_email import generate_email


@dataclass
class QuestionType(ABC):
    """
    ANSWER
    """

    question: Question
    sparsed_questions: list[Question]
    all_questions: list[Question]
    test_data_set: dict

    @abstractmethod
    def get(self):
        """
        get the answer
        """

    def get_data_for_category(self, category: str):
        """
        This function will return the stub data
        for the question category
        """
        for data in self.test_data_set["data"]:
            if category == path_or("", ["category"], data):
                return data
        return {}

    def get_data_for_key_fields(self, key_field: str, sub_categories):
        """
        This function will find the test data from key fields
        """
        for sub_cat in sub_categories:
            if key_field in path_or("", ["key_fields"], sub_cat):
                return sub_cat
        return sub_categories[0]

    def get_test_data(self, category: str, key_field):
        """
        This function return the test data
        """
        return self.get_data_for_key_fields(
            key_field=key_field,
            sub_categories=path_or(
                [], ["sub_categories"], self.get_data_for_category(category=category)
            ),
        )


@dataclass
class SingleOptionSelect(QuestionType):
    """
    Option based class
    """

    def get_adjacent_questions(self, all_questions_include=True):
        """
        This function will return the adjacent questions
        """
        if all_questions_include:
            return AdjacentQuestions(self.all_questions).get(self.question.key_field, 0)
        return AdjacentQuestions(self.sparsed_questions).get(self.question.key_field, 0)

    def get_question_categorizer(self, adjcent_questions):
        """
        This function will return the question categorizer
        """
        return QuestionCategorizer(adjcent_questions)

    def get_option_without_followups(self):
        """
        This function will return the option which does not have any folowups
        """
        qts_categorizer = self.get_question_categorizer(self.get_adjacent_questions())
        mapper = {}
        for opt in self.question.options:
            mapped = qts_categorizer.get_questions_by_options(opt)
            mapper[opt] = mapped
        for opt, mapped_qts in mapper.items():
            if not mapped_qts:
                return opt

        return self.question.options[-1]

    def get_option(self):
        """
        This function will find the option
        """
        qts_categorizer = self.get_question_categorizer(
            self.get_adjacent_questions(all_questions_include=False)
        )
        for opt in self.question.options:
            matched_qts = qts_categorizer.get_questions_by_options(opt)
            if matched_qts:
                return opt

        return self.get_option_without_followups()

    def get(self):
        """
        Get the answer
        """
        return [
            Action(
                find_by="element_text",
                action_type="click",
                data={"element_text": self.get_option().display_it_as},
            )
        ]


@dataclass
class DOBType(QuestionType):
    """
    DOB
    """


@dataclass
class WorkFlowNextButtonAction:
    """
    This class will provide the action for
    workflow next button
    """

    def get(self):
        """
        Return the actions
        """
        return Action(
            find_by="element_id",
            action_type="click",
            data={"element_id": "workflow-next-button"},
        )


@dataclass
class NameTextType(QuestionType):
    """
    Name
    """

    def get(self):
        """
        get the answers
        """
        test_data = self.get_test_data(
            category="NAME_TEXT", key_field=self.question.key_field
        )
        actions = []
        for option in path_or([], ["options"], self.question.question):
            act = Action(
                find_by="data_test_id",
                action_type="input_text",
                data={
                    "data_test_id": path_or("", ["name"], option),
                    "input_text": path_or(
                        "", ["first_name"], random.choice(test_data["valid"]["datas"])
                    ),
                },
            )
            actions.append(act)
        actions.append(WorkFlowNextButtonAction().get())
        return actions


@dataclass
class AddressType(QuestionType):
    """
    address
    """

    def get(self):
        """
        get the address
        """
        test_data = self.get_test_data(
            category="ADDRESS", key_field=self.question.key_field
        )
        address = random.choice(test_data["valid"]["datas"])
        return [
            Action(
                find_by="data_test_id",
                action_type="input_text",
                data={
                    "data_test_id": self.question.key_field,
                    "input_text": address,
                },
            ),
            Action(
                find_by="element_text",
                action_type="click",
                data={
                    "element_text": address,
                },
            ),
            Action(
                find_by="element_text",
                action_type="click",
                data={
                    "element_text": "Save",
                },
            ),
        ]


@dataclass
class SSNType(QuestionType):
    """
    Handles the ssn
    """

    def get(self):
        """
        This function will return the ssn
        """
        test_data = self.get_test_data(
            category="SSN_QUESTION", key_field=self.question.key_field
        )
        return [
            Action(
                find_by="data_test_id",
                action_type="input_text",
                data={
                    "data_test_id": self.question.key_field,
                    "input_text": random.choice(test_data["valid"]["datas"]),
                },
            ),
            WorkFlowNextButtonAction().get(),
        ]


@dataclass
class TextDate(QuestionType):
    """
    This class will get the text date
    """

    def get(self):
        """
        This function return the action for text date
        """
        test_data = self.get_test_data(
            category="TEXT_DATE", key_field=self.question.key_field
        )
        return [
            Action(
                find_by="element_placeholder",
                action_type="input_text",
                data={
                    "element_placeholder": path_or(
                        "mm/dd/yyyy", ["placeholder"], self.question.question
                    )
                    or "mm/dd/yyyy",
                    "input_text": random.choice(test_data["valid"]["datas"]),
                },
            ),
            WorkFlowNextButtonAction().get(),
        ]


@dataclass
class PhoneNumberType(QuestionType):
    """
    This class will enter the phone number
    """

    def get(self):
        """
        Get the phone number
        """
        test_data = self.get_test_data(
            category="PHONE_NUMBER", key_field=self.question.key_field
        )
        actions = []
        for option in path_or([], ["options"], self.question.question):
            act = Action(
                find_by="data_test_id",
                action_type="input_text",
                data={
                    "data_test_id": path_or("", ["name"], option),
                    "input_text": random.choice(test_data["valid"]["datas"]),
                },
            )
            actions.append(act)
        actions.append(WorkFlowNextButtonAction().get())
        return actions


@dataclass
class SignupType(QuestionType):
    """
    THis class will give the signup
    """

    def get(self):
        """
        Returns the actions for signup
        """
        return [
            Action(
                find_by="element_placeholder",
                action_type="input_text",
                data={
                    "element_placeholder": "your@email.com",
                    "input_text": generate_email(),
                },
            ),
            Action(
                find_by="element_placeholder",
                action_type="input_text",
                data={"element_placeholder": "*******", "input_text": "Speed#123"},
            ),
            Action(
                find_by="element_type",
                action_type="click",
                data={"element_type": "checkbox"},
            ),
            Action(
                find_by="element_text",
                action_type="click",
                data={"element_text": "Continue", "wait_time": 20},
            ),
        ]


@dataclass
class MultiAccountInputs(QuestionType):
    """
    This class will get the actions for
    multi account inputs
    """

    def get(self):
        """
        get the actions
        """
        return [
            Action(
                find_by="element_text",
                action_type="click",
                data={"element_text": "Skip and proceed"},
            )
        ]


@dataclass
class TextInputAmountType(QuestionType):
    """
    This class will get the amount
    """

    def get(self):
        """
        Return the text amount
        """
        test_data = self.get_test_data(
            category="SLIDER_AMOUNT", key_field=self.question.key_field
        )
        return [
            Action(
                find_by="data_test_id",
                action_type="input_text",
                data={
                    "data_test_id": self.question.key_field,
                    "input_text": random.choice(test_data["valid"]["datas"]),
                },
            ),
            WorkFlowNextButtonAction().get(),
        ]


@dataclass
class TextType(QuestionType):
    """
    Return the text
    """

    def get(self):
        """
        random text
        """
        test_data = self.get_test_data(
            category="TEXT", key_field=self.question.key_field
        )
        actions = []
        for option in path_or([], ["options"], self.question.question):
            act = Action(
                find_by="data_test_id",
                action_type="input_text",
                data={
                    "data_test_id": path_or("", ["name"], option),
                    "input_text": random.choice(test_data["valid"]["datas"]),
                },
            )
            actions.append(act)
        actions.append(WorkFlowNextButtonAction().get())
        return actions


@dataclass
class CreditSubmitType(QuestionType):
    """
    This class will click the submit button at credit step
    """

    def get(self):
        """
        Return the action to click the submit at credit
        """
        return [
            Action(
                find_by="element_text",
                action_type="click",
                data={"element_text": "Submit", "wait_time": 20, "ignore_error": True},
            ),
            Action(
                find_by="element_text",
                action_type="click",
                data={"element_text": "Log Out", "wait_time": 10, "ignore_error": True},
            ),
            Action(
                find_by="element_text",
                action_type="click",
                data={"element_text": "Accept", "wait_time": 10, "ignore_error": True},
            ),
            Action(
                find_by="element_text",
                action_type="click",
                data={"element_text": "Submit", "wait_time": 10, "ignore_error": True},
            ),
        ]


@dataclass
class QuestionTypeFinder:
    """
    This class will find the question type class
    """

    def get_type_obj(self, question_type: str) -> QuestionType:
        """
        This function will return the matched question type
        """
        question_type_map = {
            "PRODUCT_TILE": SingleOptionSelect,
            "MULTIPLE_LONG": SingleOptionSelect,
            "MULTIPLE": SingleOptionSelect,
            "MULTI_INPUT_SAVE_NAME": NameTextType,
            "dob_type": DOBType,
            "ADDRESS": AddressType,
            "EMPLOYER_INTENT_ADDRESS": AddressType,
            "SSN_QUESTION": SSNType,
            "TEXT_DATE": TextDate,
            "PHONE_NUMBER": PhoneNumberType,
            "SIGN_UP": SignupType,
            "MULTI_ACCOUNT_INPUTS": MultiAccountInputs,
            "SLIDER_AMOUNT": TextInputAmountType,
            "TEXT": TextType,
            "CREDIT_REPORT_INTENT": CreditSubmitType,
        }
        matched = path_or(None, [question_type], question_type_map)
        if not matched:
            raise Exception("Unknow question type " + question_type)
        return matched


@dataclass
class Action:
    """
    Hold the action
    """

    find_by: str
    action_type: str
    data: dict


def get_id_action(id_name: str, action_type: str, action_data: str = ""):
    """
    THis function will return the action for id
    """
    return Action(
        find_by="element_id",
        action_type=action_type,
        data={"element_id": id_name, action_type: action_data},
    )
