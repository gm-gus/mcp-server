# ui_gradio.py
import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/run"  # Asegúrate de que FastAPI esté corriendo

def consultar_agente(prompt):
    try:
        response = requests.post(API_URL, json={"prompt": prompt})
        if response.status_code == 200:
            return response.json().get("result", "")
        else:
            return f"Error {response.status_code}: {response.text}"
    except requests.exceptions.ConnectionError:
        return "❌ No se pudo conectar con la API. Asegúrate de que FastAPI está en ejecución."

with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>Asistente IA con MCP</h1>")

    with gr.Row():
        entrada = gr.Textbox(
            label="Prompt del usuario",
            placeholder="Escribe tu consulta aquí...",
            lines=5
        )

        salida = gr.Markdown(
            label="Respuesta del agente"
        )

    boton = gr.Button("Enviar")
    boton.click(fn=consultar_agente, inputs=entrada, outputs=salida)

if __name__ == "__main__":
    demo.launch()
