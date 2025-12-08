import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder, FileSearchTool, FilePurpose

PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
FILE_PATH = "./data/product_info_1.md"


project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

# Upload file and create vector store
file = project.agents.files.upload(file_path=FILE_PATH, purpose=FilePurpose.AGENTS)
vector_store = project.agents.vector_stores.create_and_poll(file_ids=[file.id], name="my_vectorstore")

# Create file search tool and agent
file_search = FileSearchTool(vector_store_ids=[vector_store.id])
agent = project.agents.create_agent(
    model="gpt-4o",
    name="my-assistant",
    instructions="You are a helpful assistant and can search information from uploaded files",
    tools=file_search.definitions,
    tool_resources=file_search.resources,
)

# Create thread and process user message
thread = project.agents.threads.create()
project.agents.messages.create(thread_id=thread.id, role="user", content="Please describe the B77 tape recorder.")
run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

# Handle run status
if run.status == "failed":
    print(f"Run failed: {run.last_error}")

# Print thread messages
messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
for message in messages:
    if message.run_id == run.id and message.text_messages:
        print(f"{message.role}: {message.text_messages[-1].text.value}")

# Cleanup resources
project.agents.vector_stores.delete(vector_store.id)
project.agents.files.delete(file_id=file.id)
project.agents.delete_agent(agent.id)