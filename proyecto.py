import streamlit as st  # Importa la librería Streamlit para crear la app web
from groq import Groq

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mi chat de Inteligencia Artificial", page_icon="⚽")
st.title("Mi primera aplicación con Streamlit jeje. BOCA MORISTE EN MADRID ⚰️")

# --- SALUDO INICIAL ---
nombre = st.text_input("¿Cuál es tu nombre?")  # Crea una caja de texto donde el usuario escribe su nombre
if st.button("Saludar"):  # Crea un botón que dice "Saludar"
    st.write(f"¡Hola, {nombre}! gracias por venir a Talento Tech 👋")  # Muestra un mensaje personalizado

# --- LISTA DE MODELOS ---
MODELOS = ['llama-3.1-8b-instant', 'llama-3.3-70b-versatile', 'deepseek-r1-distill-llama-70b']

# --- FUNCIONES DEL CHATBOT ---

def configurar_pagina():
    """Configura la página principal y la barra lateral"""
    st.sidebar.title("Configuración de la IA")
    elegirModelo = st.sidebar.selectbox('Elegí un Modelo', options=MODELOS, index=0)
    return elegirModelo


def crear_usuario_groq():
    """Crea el cliente con la API Key guardada en Streamlit Secrets"""
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)


def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    """Envía el mensaje del usuario al modelo y devuelve la respuesta en stream"""
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True
    )


def inicializar_estado():
    """Inicializa el historial de mensajes si no existe"""
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


def actualizar_historial(rol, contenido, emoji):
    """Guarda los mensajes del usuario y del asistente"""
    st.session_state.mensajes.append({"role": rol, "content": contenido, "emoji": emoji})


def area_chat():
    """Muestra el historial de mensajes en pantalla"""
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["emoji"]):
            st.write(mensaje["content"])


def generar_respuesta(chat_completo):
    """Genera la respuesta del modelo palabra por palabra"""
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa


# --- FUNCIÓN PRINCIPAL ---
def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    inicializar_estado()

    # Área de chat
    mensaje = st.chat_input("Escribí tu mensaje:")
    area_chat()

    if mensaje:
        actualizar_historial("user", mensaje, "🧑")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)

        if chat_completo:
            with st.chat_message("assistant", avatar="👻"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "👻")

            st.rerun()


# --- BLOQUE PRINCIPAL PARA EJECUCIÓN ---
if __name__ == "__main__":
    main()
