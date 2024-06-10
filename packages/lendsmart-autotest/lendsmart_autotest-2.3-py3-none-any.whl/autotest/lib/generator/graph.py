"""
    This module will build the graph
"""
from dataclasses import dataclass
import networkx as nx
from autotest.lib.generator.intent.intent import Question, Option


@dataclass
class SimpleBranch:
    """
    Hold the branch nodes
    """

    child_nodes: list[any]

    def __str__(self) -> str:
        child_text = ""
        for child_node in self.child_nodes:
            child_text += " △ " + f"{child_node}"
        return child_text


@dataclass
class SimpleNode:
    """
    Hold the node
    """

    parent: Question
    childrens: list[SimpleBranch]

    def __str__(self) -> str:
        parent_text = "» " + str(self.parent.question_text)
        for idx, childs in enumerate(self.childrens):
            parent_text += "\n" + f"{childs}"
        return parent_text


class AdjacentQuestions:
    """
    This class will get the related questions for key field
    """

    def __init__(self, sparse_questions: list[Question]) -> None:
        self.sparse_questions = sparse_questions

    def get(self, key_field: str, index: int):
        """
        This function will loop the questions and find the related question
        """
        res = []
        sub_index = index
        for quest in self.sparse_questions[index:]:
            sub_index += 1
            related = quest.is_related_to(key_field=key_field)
            if related:
                res.append(quest)

        return res


class QuestionCategorizer:
    """
    This class will categorize the question based on the options
    """

    def __init__(self, realted_questions: list[Question]) -> None:
        self.related_questions = realted_questions

    def __is_deactivated(self, deactivated_upons: list, option: Option):
        """
        This function will check
        """
        for dau in deactivated_upons:
            if dau.operation == "equals" and dau.target_value == option.update_it_as:
                return True
            if (
                dau.operation == "not_equals"
                and dau.target_value != option.update_it_as
            ):
                return True
            if dau.operation == "gte" and int(option.update_it_as) >= int(dau.target_value):
                return True
            if dau.operation == "rule_context":
                return False
        return False

    def get_questions_by_options(self, option: Option):
        """
        This function will find the question by options
        """
        res = []
        for question in self.related_questions:
            deactivated_upons = question.de_activated_upon_objs()
            is_deactivated = self.__is_deactivated(
                deactivated_upons=deactivated_upons, option=option
            )
            if is_deactivated:
                continue
            res.append(question)
            question.set_option(option)
        return res

    def categorize(self, question: Question) -> SimpleNode:
        """
        This function will categorize based on the options of question
        """
        matched_quests = []
        for opt in question.options:
            if not opt.update_it_as:
                continue
            matched_questions = self.get_questions_by_options(option=opt)
            matched_quests.append(matched_questions)
        return matched_quests


class Edge:
    """
    Hold the edges
    """

    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node


class Graph:
    """
    graph
    """

    def __init__(self):
        self.nodes = []
        self.edges = []
        self.graph = nx.DiGraph()

    def add_node(self, node):
        """
        Add nodes
        """
        self.nodes.append(node)
        self.graph.add_node(node)

    def add_edge(self, from_node, to_node):
        """
        Add edges
        """
        edge = Edge(from_node, to_node)
        self.edges.append(edge)
        self.graph.add_edge(from_node, to_node)

    def bfs(self, start_node, end_node):
        """
        BFS search
        """
        queue = [(start_node, [start_node])]
        possible_paths = []
        while queue:
            (current_node, path) = queue.pop(0)
            if current_node == end_node:
                possible_paths.append(path)
            else:
                for next_node in self.graph.neighbors(current_node):
                    if next_node not in path:
                        new_path = list(path)
                        new_path.append(next_node)
                        queue.append((next_node, new_path))
        return possible_paths


class SimpleNodeTraversor:
    """
    This class will traverse each node and its child to find the possibe ways
    """

    def __init__(self, nodes: list[SimpleNode]) -> None:
        self.nodes = nodes
        self.graph = Graph()

    def add_childrens(
        self,
        parent_node: SimpleNode,
        exit_node: SimpleNode,
        childrens: list[SimpleBranch],
    ):
        """
        test
        """
        for simple_branch in childrens:
            total_child_nodes = len(simple_branch.child_nodes)
            if not simple_branch.child_nodes:
                self.__add_edges(
                    from_node=parent_node, to_node=exit_node, skip_childs=True
                )
                continue
            if total_child_nodes == 1:
                from_node = parent_node
                to_node = simple_branch.child_nodes[0]
                self.__add_edges(from_node=from_node, to_node=to_node, skip_childs=True)
                from_node = simple_branch.child_nodes[0]
                to_node = exit_node
                self.__add_edges(from_node=from_node, to_node=to_node)
                continue

            for idx, child_node in enumerate(simple_branch.child_nodes):
                if idx == 0:
                    from_node = parent_node
                    to_node = child_node
                    self.__add_edges(
                        from_node=from_node, to_node=to_node, skip_childs=True
                    )
                    from_node = child_node
                    to_node = simple_branch.child_nodes[idx + 1]
                    self.__add_edges(from_node=from_node, to_node=to_node)
                    continue
                if idx + 1 == total_child_nodes:
                    from_node = child_node
                    to_node = exit_node
                    self.__add_edges(from_node=from_node, to_node=to_node)
                    continue
                else:
                    from_node = child_node
                    to_node = simple_branch.child_nodes[idx + 1]
                    self.__add_edges(from_node=from_node, to_node=to_node)
                    continue

    def __add_edges(
        self, from_node: SimpleNode, to_node: SimpleNode, skip_childs=False
    ):
        """
        ADD edges recursively
        """
        from_node_childrens = from_node.childrens
        if not from_node_childrens or skip_childs:
            self.graph.add_edge(from_node=from_node.parent, to_node=to_node.parent)
        else:
            self.add_childrens(
                parent_node=from_node, exit_node=to_node, childrens=from_node_childrens
            )

    def traverse(self):
        """
        This function will traverse and return the directed graph
        """
        for idx, node in enumerate(self.nodes):
            if idx + 1 == len(self.nodes):
                # self.__add_edges(from_node=node, to_node=self.nodes[-1])
                continue
            self.__add_edges(from_node=node, to_node=self.nodes[idx + 1])

        return self.graph


class DirectedGraphBuilder:
    """
    This class will build the directed graph
    """

    def __init__(self, sparse_questions: list[Question]) -> None:
        self.sparse_questions = sparse_questions
        self.adjacent_finder = AdjacentQuestions(sparse_questions=self.sparse_questions)

    def mk_simple_node(self, question: Question, index: int):
        """
        Recursivly build the simple node
        """
        adjacent_questions = self.adjacent_finder.get(
            key_field=question.key_field, index=index
        )
        if not adjacent_questions:
            question.visited = True
            return SimpleNode(parent=question, childrens=[])
        else:
            categorized_question = QuestionCategorizer(
                realted_questions=adjacent_questions
            ).categorize(question=question)
            simple_branches = []
            for quest in categorized_question:
                simple_nodes = []
                for qts in quest:
                    qts_index = self.sparse_questions.index(qts)
                    simple_node = self.mk_simple_node(question=qts, index=qts_index)
                    simple_nodes.append(simple_node)
                    qts.visited = True
                simple_branches.append(SimpleBranch(child_nodes=simple_nodes))
            return SimpleNode(parent=question, childrens=simple_branches)

    def get_directed_graph(self, simple_nodes):
        """
        This function will return the directed graph
        """
        return SimpleNodeTraversor(nodes=simple_nodes).traverse()

    def get_simple_nodes(self):
        """
        This function will return the simple nodes
        """
        simple_nodes = []
        for idx, quest in enumerate(self.sparse_questions):
            if quest.visited:
                continue
            simple_node = self.mk_simple_node(question=quest, index=idx)
            simple_nodes.append(simple_node)
        return simple_nodes

    def get_combinations(self, bfs_graph):
        """
        This function will find the combination in ordered way
        """
        combinations = []
        for idx, comb in enumerate(bfs_graph):
            ordered_b = sorted(comb, key=lambda x: self.sparse_questions.index(x))
            combinations.append(ordered_b)
            print("=========================================", idx)
            for quest in ordered_b:
                print("===quest", quest.question_text, "option", quest.selected_option)
            print("===================================================================")
            print("===================================================================")
        return combinations

    def build(self):
        """
        Graph builder started
        """
        simple_nodes = self.get_simple_nodes()

        directed_graph = self.get_directed_graph(simple_nodes=simple_nodes)

        bfs_graph = directed_graph.bfs(
            start_node=simple_nodes[0].parent, end_node=simple_nodes[-1].parent
        )

        print("The total combinations is ->", len(bfs_graph))
        return self.get_combinations(bfs_graph=bfs_graph)
