"""
    Hold the intent data
"""

from dataclasses import dataclass
from ramda import path_or

# pylint: disable=C0103,R0903


@dataclass
class Initializer:
    """
    Hold the inializer
    """

    initializer: dict


@dataclass
class RoleQuestionGroup:
    """
    hold the role questiongroup
    """

    role_question_group: dict

    @property
    def loan_role(self) -> str:
        """
        Returns the loan role
        """
        return path_or("", ["loan_role"], self.role_question_group)

    @property
    def items(self) -> list:
        """
        This function return the items
        """
        return self.role_question_group["items"]


@dataclass
class Group:
    """
    Hold the groups
    """

    group: dict

    @property
    def role_question_groups(self) -> list[RoleQuestionGroup]:
        """
        Returns the role question froup
        """
        res = []
        for role_question_group in path_or([], ["role_question_groups"], self.group):
            res.append(RoleQuestionGroup(role_question_group=role_question_group))
        return res

    def get_role_question_group_by_loan_role(self, loan_role: str):
        """
        This function return the matched items
        """
        res = []
        for role_question_group in self.role_question_groups:
            if role_question_group.loan_role == loan_role:
                res.append(role_question_group)
        return res


@dataclass
class Section:
    """
    Hold the section
    """

    section: dict

    @property
    def product(self):
        """
        Returns the product
        """
        return path_or("", ["product"], self.section)

    @property
    def groups(self) -> list[Group]:
        """
        This function returns the groups
        """
        res = []
        for group in path_or([], ["groups"], self.section):
            res.append(Group(group=group))
        return res


@dataclass
class QuestionGroup:
    """
    hold the question group
    """

    question_group: dict

    @property
    def name(self):
        """
        Returns the name
        """
        return path_or("", ["name"], self.question_group)

    @property
    def question_ids(self):
        """
        Return the question ids
        """
        return path_or([], ["question_ids"], self.question_group)


@dataclass
class DeactivatedUpon:
    """
    Handle the deactivated upon
    """

    deactivated_upon: dict

    @property
    def key_field(self):
        """
        This function returns the key field
        """
        for key, value in self.deactivated_upon.items():
            if isinstance(value, dict) and "key_field" in value:
                key_field_value = value["key_field"]
                return key_field_value
        return ""

    @property
    def target_value(self):
        """
        This function returns the target_value
        """
        for key, value in self.deactivated_upon.items():
            if isinstance(value, dict) and "key_field" in value:
                target_value = value["target_value"]
                return target_value
        return ""

    @property
    def operation(self):
        """
        This function returns the operation
        """
        for key, value in self.deactivated_upon.items():
            if isinstance(value, dict) and "key_field" in value:
                return key
        return ""


@dataclass
class Option:
    """
    This class hold the option
    """

    display_it_as: str
    update_it_as: str

    def __hash__(self):
        return hash((self.display_it_as, self.update_it_as))


@dataclass
class Question:
    """
    Hold the single question
    """

    question: dict
    _visited: bool = False
    selected_option = None

    def set_option(self, option: Option):
        """
        this function will store the selected option
        """
        if self.selected_option is None:
            self.selected_option = option

    @property
    def visited(self):
        """
        store is it visited
        """
        return self._visited

    @visited.setter
    def visited(self, value):
        """
        Property to set the visited status
        """
        self._visited = value

    @property
    def question_id(self) -> str:
        """
        Returns the question id
        """
        return path_or("", ["question_id"], self.question)

    @property
    def question_text(self) -> str:
        """
        Returns the question id
        """
        return path_or("", ["question"], self.question) or self.question_id

    @property
    def key_field(self) -> str:
        """
        Returns the key field
        """
        return path_or("", ["key_field"], self.question)

    @property
    def de_activated_upon(self):
        """
        Returns the de_activated_upon
        """
        return path_or([], ["de_activated_upon"], self.question)

    @property
    def options(self) -> list[Option]:
        """
        This function return the list of options
        """
        res = []
        opts = path_or([], ["options"], self.question)
        for opt in opts:
            res.append(
                Option(
                    display_it_as=path_or("", ["display_it_as"], opt),
                    update_it_as=path_or("", ["update_it_as"], opt),
                )
            )
        return res

    def is_option_based(self):
        """
            This function will return True if the question answer
            is option based select
        """
        for opt in self.options:
            if not opt.update_it_as:
                return False
        return True

    def de_activated_upon_objs(self):
        """
        This function returns the de activated upon objs
        """
        res = []
        for dau in self.de_activated_upon:
            res.append(DeactivatedUpon(deactivated_upon=dau))
        return res

    def is_related_to(self, key_field: str):
        """
        This function will find is this question related to this key field
        """
        for dau in self.de_activated_upon_objs():
            if dau.key_field == key_field:
                return True
        return False

    def __hash__(self):
        return hash(self.get_hashable())

    def get_hashable(self):
        """
        get hasable
        """

        def convert_to_hashable(item):
            if isinstance(item, dict):
                return tuple((k, convert_to_hashable(v)) for k, v in item.items())
            if isinstance(item, list):
                return tuple(convert_to_hashable(e) for e in item)
            return item

        return (
            self.question_id,
            self.key_field,
            convert_to_hashable(self.de_activated_upon),
        )

    @property
    def have_deactivated_upon(self):
        """
        This function will have bool
        """
        if self.de_activated_upon:
            return True
        return False


@dataclass
class Questions:
    """
    Hold the intent data
    """

    intent: dict

    @property
    def sections(self) -> list[Section]:
        """
        returns the sections
        """
        res = []
        for section in path_or([], ["sections"], self.intent):
            res.append(Section(section=section))
        return res

    @property
    def question_groups(self) -> list[QuestionGroup]:
        """
        returns the question groups
        """
        res = []
        for question_group in path_or([], ["question_groups"], self.intent):
            res.append(QuestionGroup(question_group=question_group))
        return res

    @property
    def intents(self) -> list[Question]:
        """
        Return the intents
        """
        res = []
        for question in path_or([], ["intents", "questions"], self.intent):
            res.append(Question(question=question))
        return res

    def get_section_by_product(self, product_name: str) -> Section:
        """
        This function return the product section
        """
        for section in self.sections:
            if section.product == product_name:
                return section
        return None

    def get_question_group_by_name(self, question_group_name: str) -> QuestionGroup:
        """
        THis function return the question qroup
        """
        for question_group in self.question_groups:
            if question_group.name == question_group_name:
                return question_group
        return None

    def get_question_by_id(self, question_id: str):
        """
        This function will return the question
        """
        for question in self.intents:
            if question.question_id == question_id:
                return question
        return None
