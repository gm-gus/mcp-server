# agent_service.py
import os
import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

load_dotenv(override=True)

# Configuración del proveedor
deepseek_provider = OpenAIProvider(
    base_url='https://api.deepseek.com',
    api_key=os.environ["DEEPSEEK_API_KEY"]
)
# Inicializar modelo
deepseek_chat_model = OpenAIModel(
    'deepseek-chat',
    provider=deepseek_provider
)

# Define the MCP Servers
exa_server = MCPServerStdio('python', ['mcp_tools/search.py'])
python_tools_server = MCPServerStdio('python', ['mcp_tools/python_tool.py'])

# Define the Agent
agent = Agent(
    deepseek_chat_model,
    mcp_servers=[exa_server, python_tools_server],
    retries=3
)

async def run_agent(prompt: str) -> str:
    async with agent.run_mcp_servers():
        result = await agent.run(prompt)
        return result.output
