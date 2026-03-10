class Evaluator:

    def evaluate(self, plan):

        semesters = len(plan)
        courses = sum(len(s) for s in plan)

        efficiency = courses / semesters if semesters > 0 else 0

        return {
            "courses_planned": courses,
            "semesters_used": semesters,
            "schedule_efficiency": efficiency
        }