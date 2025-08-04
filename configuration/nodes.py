from .state import EmailAssistantState
from .model import watsonx_llm
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from mail.fetchMail import fetch_emails

def fetch_unread_emails(state: EmailAssistantState) -> EmailAssistantState:
    
    emails = fetch_emails()
    print(emails)
    print(state)
    return {**state, "emails": emails}


def summarize_email(state: EmailAssistantState) -> EmailAssistantState:
    email = state.get("current_email")
    if not email:
        raise ValueError("No current_email found in state.")
    formatted_email = f"""From: {email['sender']}
    Subject: {email['subject']}

    {email['body']}
    """
    prompt = f"""You are an AI assistant. Summarize the following email in 1-2 lines and if required for better understanding go for 2-3 lines:

    Email:
    {formatted_email}
    """
    response = watsonx_llm.invoke([HumanMessage(content=prompt)])
    summary = response.content.strip()
    return {
        **state,
        "summaries": state["summaries"] + [summary],
    }


def ask_to_reply(state: EmailAssistantState) -> EmailAssistantState:
    summary = state["summaries"][-1]
    # print(f"\n📨 Summary:\n{summary}")

    # Cover the voice part coding later.
    
    # speak("Here is the summary.")
    # speak(summary)

    # user_input = get_voice_input("Would you like to reply to this email? Please say yes or no.")
    user_input = "yes"
    
    return {
        **state,
        "user_wants_reply": user_input.startswith("y")  # Sab sambhalta hai yes, yeah, y
    }

def send_email(state: EmailAssistantState) -> EmailAssistantState:
    email = state["current_email"]
    prompt = f"""Draft a short, polite reply to the following email:

    From: {email['sender']}
    Subject: {email['subject']}

    {email['body']}
    """
    response = watsonx_llm.invoke([HumanMessage(content=prompt)])
    reply = response.content.strip()

    # Write smtp server here to send mail.

    return {**state, "replies": state["replies"] + [reply]}

def go_to_next_email(state: EmailAssistantState) -> EmailAssistantState:
    emails = state.get("emails", [])
    summaries = state.get("summaries", [])

    if len(summaries) >= len(emails):
        return {
            **state,
            "current_email": None,
        }

    next_email = emails[len(summaries)]
    return {
        **state,
        "current_email": next_email,
    }


def build_email_assistant_graph():
    builder = StateGraph(EmailAssistantState)

    builder.add_node("fetch_unread_emails", fetch_unread_emails)
    builder.add_node("summarize_email", summarize_email)
    builder.add_node("ask_to_reply", ask_to_reply)
    builder.add_node("send_email", send_email)
    builder.add_node("go_to_next_email", go_to_next_email)

    builder.set_entry_point("fetch_unread_emails")

    builder.add_edge("fetch_unread_emails", "go_to_next_email")
    builder.add_conditional_edges("go_to_next_email", lambda state: "summarize_email" if state.get("current_email") else END)

    builder.add_edge("summarize_email", "ask_to_reply")
    builder.add_conditional_edges("ask_to_reply", lambda state: "send_email" if state["user_wants_reply"] else "go_to_next_email")

    builder.add_conditional_edges("send_email", go_to_next_email)



    return builder.compile()