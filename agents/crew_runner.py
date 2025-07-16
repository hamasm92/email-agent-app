import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from gmail_fetcher import fetch_unread_emails
from calendar_fetcher import fetch_today_events
from utils.google_auth import get_credentials

# 1. Load environment variables
load_dotenv()

# Ensure OPENAI_API_KEY is set
if not os.environ.get("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable not set in Replit Secrets.")
    exit()

# 2. Fetch credentials and Gmail/Calendar data
try:
    print("🔄 Fetching emails and calendar events...")
    creds = get_credentials()

    emails = fetch_unread_emails(creds)
    events = fetch_today_events(creds)

    email_text = "\n".join([f"- {e}" for e in emails]) if emails else "No unread emails found."
    event_text = "\n".join([f"- {e}" for e in events]) if events else "No events found for today."

except Exception as e:
    print(f"❌ Error fetching Gmail/Calendar data: {e}")
    email_text = "Error fetching emails."
    event_text = "Error fetching calendar."

# 3. Create prompt
task_prompt = f"""
You are a virtual executive assistant. Your job is to prepare a daily report for your user.

Unread Emails:
{email_text}

Calendar Events Today:
{event_text}

Please create a structured, clear 3-paragraph report summarizing today's updates, key tasks, and any action items.
"""

# 4. Set up LLM and agent
openai_llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

daily_reporter = Agent(
    role='Executive Assistant',
    goal='Write daily status reports based on Gmail and Calendar.',
    backstory='You are a sharp, reliable AI assistant that writes clean, clear summaries.',
    verbose=True,
    llm=openai_llm
)

# 5. Define the task
task = Task(
    description=task_prompt,
    expected_output="A well-structured 3-paragraph report for the day.",
    agent=daily_reporter
)

# 6. Run the crew
crew = Crew(
    agents=[daily_reporter],
    tasks=[task],
    verbose=True,
    process=Process.sequential
)

print("\n🚀 Running Daily Report Crew...\n")
result = crew.kickoff()
print("\n✅ Crew Finished.\n")
print(result)
