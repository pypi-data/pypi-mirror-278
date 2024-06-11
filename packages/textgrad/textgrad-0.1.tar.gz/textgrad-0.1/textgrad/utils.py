import pickle
from typing import List
from copy import deepcopy


class DebugVariable:

    def __init__(self, filepath: str):
        self.steps: List = []
        self.filepath: str = filepath

    def add_debug_step(self, variable):
        self.steps.append(deepcopy(variable))


    def save(self):
        """
        This function simply exports the variable and its ancestors to a pickle file.
        Pickle can be loaded for a streamlit app

        :param variables:
        :param filepath:
        :return:
        """

        list_of_states = []

        # Leetcoding at best
        # This should traverse the graph and store nodes and edges
        for v in self.steps:
            queue = [v]
            nodes = {}
            edges = []

            while queue:
                current = queue.pop()

                for item in current.prev:
                    current_name = f"{current.get_role_description()} {id(current)}"
                    item_name = f"{item.get_role_description()} {id(item)}"

                    edges.append({"source": current_name, "target": item_name})
                    nodes[current_name] = {
                        "size": 25,
                        "value": str(current.value),
                        "gradient": str(current.gradients),
                    }
                    nodes[item_name] = {
                        "size": 25,
                        "value": str(item.value),
                        "gradient": str(item.gradients),
                    }

                    queue.append(item)
            list_of_states.append({"nodes": nodes, "edges": edges})

        with open(f"{self.filepath}", "wb") as f:
            pickle.dump(list_of_states, f)
