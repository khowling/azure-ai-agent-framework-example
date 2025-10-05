# Azure AI Agent Framework Example

A demonstration of the new Microsoft Agent Framework using Azure AI Foundry agents with persistent memory threads.

## Features

- **Streaming Responses**: Real-time text generation with memory persistence
- **Thread Memory**: Maintains conversation context across multiple interactions  
- **Function Tools**: Weather function tool integration
- **Azure AI Foundry**: Built on Microsoft's new agent framework
- **Observability**: OpenTelemetry tracing for monitoring and debugging

## Prerequisites

- Azure CLI (`az login`)
- Azure AI project with deployed model
- Environment variables:
  - `AZURE_AI_PROJECT_ENDPOINT`
  - `AZURE_AI_MODEL_DEPLOYMENT_NAME`

## Usage

```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export AZURE_AI_PROJECT_ENDPOINT="https://your-project.openai.azure.com/"
export AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-4"

# Run the example
python agent1.py
```

## Example Output

The agent demonstrates memory by remembering previous cities mentioned in the conversation and can compare weather between multiple locations using persistent thread context.

## Observability & Tracing

This example includes OpenTelemetry tracing for monitoring agent interactions:

### Quick Setup (VS Code AI Toolkit)
1. Install the AI Toolkit extension in VS Code
2. Run the agent - traces automatically appear in the AI Toolkit tracing view
3. View traces at: Extensions → AI Toolkit → Tracing

### Manual Setup
```bash
# Install with tracing dependencies
pip install agent-framework[telemetry]

# Run with Docker (Jaeger)
docker run -d -p 16686:16686 -p 4317:4317 -p 4318:4318 jaegertracing/all-in-one:latest

# View traces at: http://localhost:16686
```

### What You'll See
- Agent conversation flows and timing
- Function tool invocations (weather API calls)
- Memory thread operations
- Token usage and model interactions
- Error traces and performance metrics

## Agent Lifecycle

**Important Note**: This example creates **ephemeral agents** that are automatically managed:
- Agents are created temporarily when the script runs
- Agents are automatically deleted when the script completes
- Agents do **not** persist in the Azure AI Foundry portal

The agents exist only during script execution and use automatic lifecycle management for quick prototyping and development.

## About

This example showcases the Microsoft Agent Framework's capabilities for building conversational AI agents with memory and tool integration using Azure AI Foundry services.

## References

- [Microsoft Agent Framework Documentation](https://github.com/microsoft/agent-framework)
- [Azure AI Foundry Agent Examples](https://github.com/microsoft/agent-framework/tree/main/python/samples/getting_started/agents/azure_ai)