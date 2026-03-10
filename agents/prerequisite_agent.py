import networkx as nx

class PrerequisiteAgent:

    def run(self, courses):

        graph = nx.DiGraph()

        for item in courses:

            course = item.course
            prereq = item.prerequisite

            graph.add_node(course)

            if prereq:
                graph.add_edge(prereq, course)

        return graph