import streamlit as st
import pandas as pd
import time
import random
import requests
from datetime import datetime

st.set_page_config(page_title="Personal Study Planner", layout="wide")

# -------------------------
# Session State
# -------------------------

if "state_history" not in st.session_state:
    st.session_state.state_history = []

if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_agent" not in st.session_state:
    st.session_state.active_agent = None

if "run_id" not in st.session_state:
    st.session_state.run_id = None

if "metrics" not in st.session_state:
    st.session_state.metrics = {
        "courses_planned": 0,
        "semesters_used": 0,
        "agent_calls": 0
    }

# -------------------------
# Functions
# -------------------------

def log_state(state):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.state_history.append((timestamp, state))

def log_message(agent, msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append((timestamp, agent, msg))
    st.session_state.metrics["agent_calls"] += 1


# -------------------------
# Layout
# -------------------------

st.title("📚 Personal Study Planner - Multi Agent System")

col1, col2, col3 = st.columns([1,2,1])

# -------------------------
# Agent Panel
# -------------------------

with col1:
    st.subheader("Agents")

    agents = [
        "InputAgent",
        "PrerequisiteAgent",
        "SchedulerAgent",
        "ValidatorAgent"
    ]

    for agent in agents:
        if agent == st.session_state.active_agent:
            st.success(agent)
        else:
            st.write(agent)

# -------------------------
# Interaction Panel
# -------------------------

with col2:
    st.subheader("Agent Interaction Log")

    if len(st.session_state.messages) == 0:
        st.info("No interactions yet")

    for msg in st.session_state.messages:
        st.write(f"[{msg[0]}] **{msg[1]}** → {msg[2]}")

# -------------------------
# State Panel
# -------------------------

with col3:
    st.subheader("State Machine")

    if len(st.session_state.state_history) == 0:
        st.info("No state transitions")

    for state in st.session_state.state_history:
        st.write(f"{state[0]} → {state[1]}")


st.divider()

# -------------------------
# Metrics Dashboard
# -------------------------

st.subheader("Metrics Dashboard")

metric1, metric2, metric3 = st.columns(3)

metric1.metric(
    "Courses Planned",
    st.session_state.metrics["courses_planned"]
)

metric2.metric(
    "Semesters Used",
    st.session_state.metrics["semesters_used"]
)

metric3.metric(
    "Agent Calls",
    st.session_state.metrics["agent_calls"]
)

st.divider()

# -------------------------
# User Input
# -------------------------

st.subheader("Enter Courses")

num_courses = st.number_input("Number of Courses", 1, 20, 5)

courses = []

for i in range(num_courses):

    colA, colB = st.columns(2)

    course = colA.text_input(f"Course {i+1}", key=f"course{i}")
    prereq = colB.text_input(f"Prerequisite {i+1}", key=f"prereq{i}")

    if course:
        courses.append({
            "course": course,
            "prerequisite": prereq if prereq else None
        })


# -------------------------
# Run Planner
# -------------------------

if st.button("Start"):

    from agents.prerequisite_agent import PrerequisiteAgent
    from agents.scheduler_agent import SchedulerAgent
    from agents.validator_agent import ValidatorAgent
    from metrics.evaluator import Evaluator

    prereq_agent = PrerequisiteAgent()
    scheduler = SchedulerAgent()
    validator = ValidatorAgent()
    evaluator = Evaluator()

    # Build graph
    graph = prereq_agent.run(courses)

    # Generate plan
    plan = scheduler.run(graph, 3)

    # Validate
    validation = validator.run(plan)

    # Metrics
    metrics = evaluator.evaluate(plan)

    # Display Study Plan
    st.subheader("📚 Generated Study Plan")

    for i, semester in enumerate(plan, start=1):

        st.markdown(f"### Semester {i}")

        for course in semester:
            st.markdown(f"- {course}")

    # Update metrics
    st.session_state.metrics["courses_planned"] = metrics["courses_planned"]
    st.session_state.metrics["semesters_used"] = metrics["semesters_used"]
    st.session_state.metrics["agent_calls"] = 3

    # Update logs
    log_message("PrerequisiteAgent", "Graph built")
    log_message("SchedulerAgent", "Schedule generated")
    log_message("ValidatorAgent", "Plan validated")

    log_state("COMPLETE")

    st.success("Study Plan Generated")
