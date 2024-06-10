"""
    Hold the node data
"""
from dataclasses import dataclass
from ramda import path_or


@dataclass
class NodeAction:
    """
    hold the actions of node
    """

    find_by: str
    action_type: str
    data: dict
    validations: dict


@dataclass
class Node:
    """
    Hold the node data
    """

    name: str
    intent_data: dict
    actions: list


@dataclass
class Nodes:
    """
    Hold the list of nodes
    """

    nodes: list


@dataclass
class NodeBuilder:
    """
    Build the node data
    """

    def get_node_actions(self, actions: list) -> list:
        """
        This function will return the node actions
        """
        res = []
        for action in actions:
            res.append(
                NodeAction(
                    find_by=path_or("", ["find_by"], action),
                    action_type=path_or("", ["action_type"], action),
                    data=path_or({}, ["data"], action),
                    validations=path_or({}, ["validations"], action),
                )
            )
        return res

    def convert_json_to_obj(self, json_nodes: list) -> Node:
        """
        This function will convert the nodes json to obj
        """
        result = []
        for json_node in json_nodes:
            result.append(
                Node(
                    name=path_or("", ["name"], json_node),
                    intent_data=path_or({}, ["intent_data"], json_node),
                    actions=self.get_node_actions(path_or([], ["actions"], json_node)),
                )
            )
        return Nodes(nodes=result)
