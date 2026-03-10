import networkx as nx

class SchedulerAgent:

    def run(self, graph, max_per_sem=3):

        order = list(nx.topological_sort(graph))

        semesters = []
        semester = []

        for course in order:

            semester.append(course)

            if len(semester) == max_per_sem:
                semesters.append(semester)
                semester = []

        if semester:
            semesters.append(semester)

        return semesters