# chatbot_app.py
import streamlit as st
from agent import CaspianAgent  # Asegúrate de que agent.py esté en el mismo directorio

# Inicializa el agent solo una vez
if "agent" not in st.session_state:
    st.session_state.agent = CaspianAgent()

# Configuración de la conversación y el chat_id
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None  # Se mantendrá constante en la sesión

# Historial de conversación
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Función para manejar el envío de mensajes
def send_message():
    # Agrega el mensaje del usuario al historial
    user_input = st.session_state.user_input  # Captura el texto ingresado
    st.session_state.chat_history.append(f"Tú: {user_input}")

    # Llama al agent y obtiene la respuesta, manteniendo el chat_id existente
    response = st.session_state.agent.start_conversation(user_input)
    st.session_state.chat_history.append(f"Agent: {response}")

    # Limpia el campo de entrada después de enviar
    st.session_state.user_input = ""  # Restablece el cuadro de texto

# Título de la aplicación
st.title("Conversación con el Agent")

# Mostrar el historial de la conversación
for message in st.session_state.chat_history:
    st.write(message)

# Caja de texto para el input del usuario
st.text_input(
    "Escribe tu mensaje aquí",
    key="user_input",  # Clave única en session_state
    placeholder="Escribe aquí y presiona Enter para enviar",
    label_visibility="hidden",
    on_change=send_message  # Ejecuta send_message al cambiar el texto
)