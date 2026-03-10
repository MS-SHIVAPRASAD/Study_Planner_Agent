from transitions import Machine

class PlannerStateMachine:

    states = [
        "INIT",
        "LOAD_DATA",
        "BUILD_GRAPH",
        "GENERATE_SCHEDULE",
        "VALIDATE_PLAN",
        "COMPLETE"
    ]

    def __init__(self):

        self.machine = Machine(
            model=self,
            states=PlannerStateMachine.states,
            initial="INIT"
        )

        self.machine.add_transition("load_data", "INIT", "LOAD_DATA")
        self.machine.add_transition("build_graph", "LOAD_DATA", "BUILD_GRAPH")
        self.machine.add_transition("schedule", "BUILD_GRAPH", "GENERATE_SCHEDULE")
        self.machine.add_transition("validate", "GENERATE_SCHEDULE", "VALIDATE_PLAN")
        self.machine.add_transition("finish", "VALIDATE_PLAN", "COMPLETE")