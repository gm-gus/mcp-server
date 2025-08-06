import os
import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

load_dotenv(override=True)

deepseek_provider = OpenAIProvider(
    base_url='https://api.deepseek.com',
    api_key=os.environ["DEEPSEEK_API_KEY"]
)

deepseek_chat_model = OpenAIModel(
    'deepseek-chat',
    provider=deepseek_provider
)

# Define the MCP Servers
exa_server = MCPServerStdio(
    'python', # Intérprete
    ['search.py'] # Archivo a ejecutar con el interprete
)

python_tools_server = MCPServerStdio(
    'python',
    ['python_tool.py']
)

# Define the Agent
agent = Agent(
    deepseek_chat_model,
    mcp_servers=[exa_server, python_tools_server],
    retries=3
)

async def main():
    async with agent.run_mcp_servers():
        result = await agent.run("""
            Crear un gráfico de barras que muestre la población de las cinco ciudades más grandes del mundo
                                 """)
        
        ##Busca las últimas noticias sobre inteligencia artificial
        print(result.data)

if __name__ == "__main__":
    asyncio.run(main())
