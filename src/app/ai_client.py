import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
PROJECT_NAME = os.environ["AZURE_AI_PROJECT_NAME"]
AGENT_NAME = os.environ["AZURE_AI_AGENT_NAME"]

credential = DefaultAzureCredential()

project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=credential,
)

def run_agent(query: str, user_id: str):
    # 1) create a thread
    thread = project_client.agents.create_thread(
        metadata={"user_id": user_id}
    )

    # 2) add a user message
    project_client.agents.create_message(
        thread_id=thread["id"],
        role="user",
        content=query,
    )

    # 3) run the agent
    run = project_client.agents.create_and_run(
        agent_name=AGENT_NAME,
        thread_id=thread["id"],
    )

    # 4) poll until completion
    run = project_client.agents.poll_run(
        thread_id=thread["id"],
        run_id=run["id"],
        timeout=60,
    )

    # 5) read messages
    messages = project_client.agents.list_messages(
        thread_id=thread["id"]
    )

    # Get the latest assistant answer
    for msg in reversed(messages["data"]):
        if msg["role"] == "assistant":
            return msg["content"]

    return "No assistant response found."
