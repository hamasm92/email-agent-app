from fastapi import FastAPI
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# ✅ Update import paths based on actual folder structure
from agents.gmail_fetcher import fetch_unread_emails
from agents.calendar_fetcher import fetch_today_events
from utils.google_auth import get_credentials
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "✅ Email Agent API is running. Visit /docs to test."}

@app.post("/generate_report")
def generate_daily_report():
    try:
        # 1. Authorize and fetch Google data
        creds = get_credentials()
        emails = fetch_unread_emails(creds)
        events = fetch_today_events(creds)

        email_text = "\n".join([f"- {e}" for e in emails]) or "No unread emails."
        event_text = "\n".join([f"- {e}" for e in events]) or "No events today."

        # 2. Build the task prompt
        task_prompt = f"""
        You are a virtual executive assistant. Your job is to prepare a daily report for your user.

        Unread Emails:
        {email_text}

        Calendar Events Today:
        {event_text}

        Please create a structured, clear 3-paragraph report summarizing today's updates, key tasks, and any action items.
        """

        # 3. Create LLM and agent
        openai_llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
        daily_reporter = Agent(
            role='Executive Assistant',
            goal='Write daily status reports based on Gmail and Calendar.',
            backstory='You are a sharp, reliable AI assistant that writes clean, clear summaries.',
            verbose=True,
            llm=openai_llm
        )

        # 4. Define task and crew
        task = Task(description=task_prompt, expected_output="3-paragraph structured report", agent=daily_reporter)
        crew = Crew(agents=[daily_reporter], tasks=[task], process=Process.sequential)

        print("\n🚀 Running Daily Report Crew...\n")
        result = crew.kickoff()

        return {"status": "success", "summary": result}

    except Exception as e:
        return {"status": "error", "message": str(e)}
