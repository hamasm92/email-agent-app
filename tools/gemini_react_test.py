
# gemini_react_test.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# Ensure your GOOGLE_API_KEY is set in your environment
if not os.environ.get("GOOGLE_API_KEY"):
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest",
    temperature=0.3, # Match the temperature from the CrewAI test
    google_api_key=os.environ.get("GOOGLE_API_KEY")
)

system_prompt = """You are a helpful AI assistant.
To give your best complete final answer, respond using the exact following format:

Thought: I now can give a great answer
Final Answer: Your final answer must be the great and the most complete as possible, it must be outcome described.

I MUST use these formats, my job depends on it!
"""

user_question = "What is the capital of France?"

messages = [
    SystemMessage(content=system_prompt),
    HumanMessage(content=f"Current Task: {user_question}\n\nThought:") # Mimic CrewAI's initial 'Thought:'
]

print("--- Sending direct prompt to Gemini via LangChain ---")
print("System Prompt:\n", system_prompt)
print("\nUser Message:\n", messages[-1].content)
print("-" * 50)

try:
    response = llm.invoke(messages, stop=["\nObservation:"]) # Keep the stop sequence as CrewAI uses it
    print("\n--- Raw Gemini Response ---")
    print(response.content)
    print("\n--- Test Complete ---")

except Exception as e:
    print(f"An error occurred: {e}")