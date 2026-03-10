from fastapi import FastAPI
from pydantic import BaseModel
import random

from state_machine import PlannerStateMachine
from logger import RunLogger

from agents.prerequisite_agent import PrerequisiteAgent
from agents.scheduler_agent import SchedulerAgent
from agents.validator_agent import ValidatorAgent

from metrics.evaluator import Evaluator

app = FastAPI()


# -------------------------
# Request Model
# -------------------------

class CourseInput(BaseModel):
    course: str
    prerequisite: str | None = None


class PlannerRequest(BaseModel):
    courses: list[CourseInput]
    max_courses_per_semester: int = 3
    seed: int = 42


# -------------------------
# API
# -------------------------

@app.post("/run_planner")
def run_planner(request: PlannerRequest):

    random.seed(request.seed)

    logger = RunLogger()
    sm = PlannerStateMachine()

    prereq_agent = PrerequisiteAgent()
    scheduler = SchedulerAgent()
    validator = ValidatorAgent()
    evaluator = Evaluator()

    sm.load_data()

    graph = prereq_agent.run(request.courses)
    logger.log("PrerequisiteAgent", "user_input", "graph_created")

    sm.build_graph()

    plan = scheduler.run(graph, request.max_courses_per_semester)
    logger.log("SchedulerAgent", "graph_input", plan)

    sm.schedule()

    validation = validator.run(plan)
    logger.log("ValidatorAgent", plan, validation)

    sm.validate()

    metrics = evaluator.evaluate(plan)

    sm.finish()

    return {
        "run_id": logger.run_id,
        "state": sm.state,
        "plan": plan,
        "metrics": metrics,
        "logs": logger.get_logs()
    }