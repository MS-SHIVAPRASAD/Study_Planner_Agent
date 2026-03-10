class ValidatorAgent:

    def run(self, plan):

        valid = True
        total_courses = sum(len(s) for s in plan)

        if total_courses == 0:
            valid = False

        return {
            "valid": valid,
            "courses": total_courses
        }