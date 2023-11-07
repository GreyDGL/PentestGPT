import os
from datetime import datetime

# get keys for your project
os.environ[
    "LANGFUSE_PUBLIC_KEY"
] = "pk-lf-5655b061-3724-43ee-87bb-28fab0b5f676"  # do not modify
os.environ[
    "LANGFUSE_SECRET_KEY"
] = "sk-lf-c24b40ef-8157-44af-a840-6bae2c9358b0"  # do not modify
from langfuse import Langfuse

langfuse = Langfuse()

from langfuse.model import CreateTrace, CreateSpan, CreateGeneration, CreateEvent

trace = langfuse.trace(CreateTrace(name="llm-feature"))
retrieval = trace.span(CreateSpan(name="retrieval"))
retrieval.generation(CreateGeneration(name="query-creation"))
retrieval.span(CreateSpan(name="vector-db-search"))
retrieval.event(CreateEvent(name="db-summary"))
trace.generation(CreateGeneration(name="user-output"))
generationStartTime = datetime.now()

generation = trace.generation(
    CreateGeneration(
        name="summary-generation",
        startTime=generationStartTime,
        endTime=datetime.now(),
        model="gpt-3.5-turbo",
        modelParameters={"maxTokens": "1000", "temperature": "0.9"},
        prompt=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Please generate a summary of the following documents \nThe engineering department defined the following OKR goals...\nThe marketing department defined the following OKR goals...",
            },
        ],
        metadata={"interface": "whatsapp"},
    )
)
