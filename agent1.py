# Copyright (c) Microsoft. All rights reserved.

import os

import asyncio
from random import randint
from typing import Annotated

from agent_framework import AgentThread, ChatAgent
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from pydantic import Field

from agent_framework.observability import setup_observability

"""
Azure AI Agent with Memory Thread Example

This sample demonstrates Azure AI Agent with persistent memory using threads.
Shows both streaming and non-streaming responses with function tools and memory.
Includes OpenTelemetry tracing for observability.
"""


def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


async def streaming_with_thread_example() -> None:
    """Example of streaming response with persistent thread memory."""
    print("=== Streaming Response with Thread Memory Example ===")
    print("Using streaming output with persistent memory across multiple conversations.\n")

    # For authentication, run `az login` command in terminal or replace AzureCliCredential with preferred
    # authentication option.
    async with (
        AzureCliCredential() as credential,
        ChatAgent(
            chat_client=AzureAIAgentClient(async_credential=credential),
            instructions="You are a helpful weather agent with memory.",
            tools=get_weather,
        ) as agent,
    ):
        # Create a persistent thread for memory
        thread = agent.get_new_thread()
        
        # First streaming conversation
        first_query = "What's the weather like in Portland?"
        print(f"User: {first_query}")
        print("Agent: ", end="", flush=True)
        async for chunk in agent.run_stream(first_query, thread=thread):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print("\n")
        
        # Second streaming conversation - should remember Portland
        second_query = "How about comparing that to Tokyo?"
        print(f"User: {second_query}")
        print("Agent: ", end="", flush=True)
        async for chunk in agent.run_stream(second_query, thread=thread):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print("\n")
        
        # Third streaming conversation - test memory of both cities
        third_query = "Which of these two cities has better weather?"
        print(f"User: {third_query}")
        print("Agent: ", end="", flush=True)
        async for chunk in agent.run_stream(third_query, thread=thread):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print("\n")
        
        print("=== Example completed successfully! ===")


async def main() -> None:
    print("=== Azure AI Chat Client Agent with Memory Thread Examples ===")
    
    # Initialize observability for VS Code AI Toolkit only (no console output)
    try:
        # Check if VS Code AI Toolkit is available by testing the endpoint
        import urllib.request
        urllib.request.urlopen("http://localhost:3000", timeout=1)
        
        # Only setup observability if AI Toolkit is running
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:3000"
        os.environ["OTEL_TRACES_EXPORTER"] = "otlp"
        os.environ["OTEL_METRICS_EXPORTER"] = "none"
        os.environ["OTEL_LOGS_EXPORTER"] = "none"
        
        setup_observability()
    except Exception:
        # AI Toolkit not available - completely skip telemetry
        pass
    
    await streaming_with_thread_example()


if __name__ == "__main__":
    asyncio.run(main())