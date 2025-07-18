from fastapi import FastAPI
from configuration.state import EmailAssistantState
from configuration.nodes import build_email_assistant_graph

# http://127.0.0.1:8000/docs
app = FastAPI()


email_assistant_app = build_email_assistant_graph()

@app.get("/")
def root():
    return {"message": "Email Assistant is running!"}


@app.post("/run-email-assistant")
def run_email_assistant():
    initial_state: EmailAssistantState = {
        "user_input": "Read my emails",
        "emails": [],
        "current_email": None,
        "summaries": [],
        "replies": [],
        "messages": [],
        "user_wants_reply": None
    }

    final_state = email_assistant_app.invoke(initial_state)

    return {
        "summaries": final_state["summaries"],
        "replies": final_state["replies"]
    }


