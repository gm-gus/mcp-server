import os
import asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModel

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

# Crear agente
agent = Agent(deepseek_chat_model)

# Prompt de prueba
async def main():
    result = await agent.run("¿Qué es la inteligencia artificial en pocas palabras?")
    print("\n🧠 Respuesta de DeepSeek:")
    print(result.output)

if __name__ == "__main__":
    asyncio.run(main())
