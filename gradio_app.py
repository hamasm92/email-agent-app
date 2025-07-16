import os
from dotenv import load_dotenv
load_dotenv()

import gradio as grimport gradio as gr
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from agents.gmail_fetcher import fetch_unread_emails
from agents.calendar_fetcher import fetch_today_events
from utils.google_auth import generate_auth_url, exchange_code_for_credentials

# Step 1: Generate the auth link from your own logic
def get_auth_link():
    try:
        url = generate_auth_url()
        return f"🔗 [Click here to authorize access]({url})\n\nThen paste the code below 👇"
    except Exception as e:
        return f"❌ Error generating auth link: {str(e)}"

# Step 2: Accept auth code, fetch tokens, and generate the report
def generate_report_with_code(auth_code):
    try:
        creds = exchange_code_for_credentials(auth_code)

        emails = fetch_unread_emails(creds)
        events = fetch_today_events(creds)

        email_text = "\n".join([f"- {e}" for e in emails]) or "No unread emails."
        event_text = "\n".join([f"- {e}" for e in events]) or "No calendar events today."

        task_prompt = f"""
        You are a virtual executive assistant. Your job is to prepare a daily report for your user.

        Unread Emails:
        {email_text}

        Calendar Events Today:
        {event_text}

        Please create a structured, clear 3-paragraph report summarizing today's updates, key tasks, and any action items.
        """

        openai_llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
        agent = Agent(
            role="Executive Assistant",
            goal="Write daily status reports based on Gmail and Calendar.",
            backstory="You are a sharp, reliable AI assistant.",
            verbose=True,
            llm=openai_llm
        )

        task = Task(description=task_prompt, expected_output="3-paragraph structured report", agent=agent)
        crew = Crew(agents=[agent], tasks=[task], process=Process.sequential)

        result = crew.kickoff()
        return result

    except Exception as e:
        return f"❌ Error: {str(e)}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 📬 Gmail + Calendar Daily Report Agent")

    gr.Markdown("### Step 1: Authorize Access")
    with gr.Row():
        auth_btn = gr.Button("🔑 Get Google Auth Link")
        auth_link_output = gr.Textbox(label="Authorization Link", lines=2)

    gr.Markdown("### Step 2: Paste Authorization Code")
    with gr.Row():
        code_input = gr.Textbox(label="Paste Auth Code Here")
        generate_btn = gr.Button("📝 Generate Report")

    gr.Markdown("### 📄 AI Assistant Report")
    report_output = gr.Textbox(lines=15, label="", show_copy_button=True)

    auth_btn.click(fn=get_auth_link, outputs=auth_link_output)
    generate_btn.click(fn=generate_report_with_code, inputs=code_input, outputs=report_output)

# Launch the app
demo.launch(server_name="0.0.0.0", share=True)
