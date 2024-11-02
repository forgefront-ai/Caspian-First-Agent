# agent.py
import openai
from config import API_KEY, MODEL, Assist_ID
from openai import OpenAI
import time



class CaspianAgent:
    def __init__(self):
        self.client = OpenAI(api_key=API_KEY)
        self.chat_id = None

    def start_conversation(self, user_message):
        """Inicia una conversación con el assistant preconfigurado en OpenAI."""
        # Crear un nuevo hilo de conversación con el primer mensaje del usuario
        # Si es la primera vez, crea un nuevo hilo de conversación y guarda el ID
        if not self.chat_id:
            chat = self.client.beta.threads.create(
                messages=[{'role': 'user', 'content': user_message}]
            )
            self.chat_id = chat.id
            print(f"Chat ID inicializado: {self.chat_id}")
        else:
            # Si ya existe un chat, simplemente añade el mensaje del usuario al hilo actual
            self.client.beta.threads.messages.create(
                thread_id=self.chat_id,
                role="user",
                content=user_message
            )
            print(f'Chat ID utilizado: {self.chat_id}')

        # Ejecutar el assistant con el run_id del assistant configurado
        run = self.client.beta.threads.runs.create(
            thread_id=self.chat_id,
            assistant_id=Assist_ID
        )
        print(f'Run Created: {run.id}')

        # Verificar el estado hasta que el run esté completo
        while run.status != 'completed':
            run = self.client.beta.threads.runs.retrieve(thread_id=self.chat_id, run_id=run.id)
            print(f'Run Status: {run.status}')
            time.sleep(0.5)

        # Obtener la respuesta del assistant
        message_response = self.client.beta.threads.messages.list(thread_id=self.chat_id)
        messages = message_response.data
        latest_message = messages[0]
        print(f'Response: {latest_message.content[0].text.value}')
        return latest_message.content[0].text.value




    def interactive_chat(self):
        """Permite una conversación interactiva con el usuario."""
        print("Inicia la conversación con el agent (escribe 'salir' para terminar).")
        while True:
            # Obtener el input del usuario
            user_message = input("Tú: ")
            if user_message.lower() in ["salir", "exit"]:
                print("Finalizando la conversación. ¡Hasta luego!")
                break

            # Generar la respuesta del agent y mostrarla
            response = self.start_conversation(user_message)
            print(f"Agent: {response}")


# Ejemplo de uso interactivo
if __name__ == "__main__":
    agent = CaspianAgent()
    agent.interactive_chat()
