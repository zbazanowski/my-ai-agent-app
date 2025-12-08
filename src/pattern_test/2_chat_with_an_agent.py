import os
from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder, FilePurpose

load_dotenv()

PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]

project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

agent = project.agents.create_agent(
    model="gpt-4o",
    name="my-agent",
    instructions="You are a helpful writing assistant")

thread = project.agents.threads.create()
message = project.agents.messages.create(
    thread_id=thread.id, 
    role="user", 
    content="Write me a poem about flowers")

run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
if run.status == "failed":
    # Check if you got "Rate limit is exceeded.", then you want to get more quota
    print(f"Run failed: {run.last_error}")

# Get messages from the thread
messages = project.agents.messages.list(thread_id=thread.id)

# Get the last message from the sender
messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
for message in messages:
    if message.run_id == run.id and message.text_messages:
        print(f"{message.role}: {message.text_messages[-1].text.value}")

# Delete the agent once done
project.agents.delete_agent(agent.id)
print("Deleted agent")
