import os
import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv

load_dotenv(override=True)

# Inicializar proveedor DeepSeek
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
exa_server = MCPServerStdio(
    'python', # Intérprete
    ['search.py'] # Archivo a ejecutar con el interprete
)

python_tools_server = MCPServerStdio(
    'python',
    ['python_tool.py']
)

actas_server = MCPServerStdio(
    'python',
    ['generar_acta.py']
)

agent = Agent(
    deepseek_chat_model,
    mcp_servers=[exa_server, python_tools_server, actas_server],
    retries=3
)

async def main():
    transcripcion = """
    La reunión comenzó el 8 de agosto de 2025 con la presencia de Ana, Luis y Marta.
    Se discutió la campaña de marketing para el próximo trimestre y la necesidad de mejorar la web.
    Se acordó contratar un diseñador freelance y aumentar el presupuesto en redes sociales.
    """

    async with agent.run_mcp_servers():
        result = await agent.run(f"""
            Usa la herramienta generar_acta_desde_transcripcion con esta transcripción:
            {transcripcion}
        """)
        print(result.data)
# async def main():
#     async with agent.run_mcp_servers():
#         result = await agent.run("""
#             Busca las últimas noticias sobre inteligencia artificial de Openai
#                                  """)
        
#         ##Crear un gráfico de barras que muestre la población de las cinco ciudades más grandes del mundo
#         print(result.data)

if __name__ == "__main__":
    asyncio.run(main())
