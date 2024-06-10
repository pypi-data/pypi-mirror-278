"""
    HANDLE THE utility
"""


class DAUValidator:
    """
        Validate the deactivated upon
    """

    def __init__(self, from_node, to_node) -> None:
        self.from_node = from_node
        self.to_node = to_node

    def lenth_compare(self) -> bool:
        """
            Compares the length
        """
        len_of_from_node = len(self.from_node.de_activated_upon)
        len_of_to_node = len(self.to_node.de_activated_upon)
        return len_of_from_node == len_of_to_node

    def have_same_conditions(self):
        """
            This function will check does both dau has same condition
        """
        for dau in self.from_node.de_activated_upon:
            if dau not in self.to_node.de_activated_upon:
                return False
        return True

    def match(self) -> bool:
        """
            This function will compare the 2 nodes dau and checks 2 are belongs to same trunk
        """
        length_match = self.lenth_compare()
        if length_match:
            return self.have_same_conditions()
        return False
