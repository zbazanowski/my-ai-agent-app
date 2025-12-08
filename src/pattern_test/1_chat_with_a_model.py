import os

from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

PROJECT_ENDPOINT = os.environ["AZURE_AI_PROJECT_ENDPOINT"]
MODEL_DEPLOYMENT_NAME = os.environ['AZURE_AI_FOUNDRY_MODEL_DEPLOYMENT_NAME']
           
print(f"Using AZURE_AI_FOUNDRY_PROJECT_ENDPOINT: {PROJECT_ENDPOINT}")
print(f"Using AZURE_AI_FOUNDRY_MODEL_DEPLOYMENT_NAME: {MODEL_DEPLOYMENT_NAME}")


project = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

models = project.get_openai_client(api_version="2024-10-21")
response = models.chat.completions.create(
    model=MODEL_DEPLOYMENT_NAME,
    messages=[
        {"role": "system", "content": "You are a helpful writing assistant"},
        {"role": "user", "content": "Write me a poem about flowers"},
    ],
)

print(response.choices[0].message.content)
