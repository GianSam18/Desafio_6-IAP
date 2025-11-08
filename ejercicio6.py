import streamlit as st
from groq import Groq

# -------------------------------------------------------------
# CONFIGURACIÓN GENERAL DE LA APP
# -------------------------------------------------------------
st.set_page_config(page_title="Mi chat de IA - Samanez", page_icon="🐶")
st.title("Mi primera aplicación con Streamlit - Samanez")  

# Entrada del nombre + botón para saludar 
nombre = st.text_input("¿Cuál es tu nombre?")
if st.button("Saludar"):
    st.write(f"¡Hola, {nombre}! Gracias por venir a Talento Tech 😊")

# -------------------------------------------------------------
# CONFIGURACIÓN DE MODELOS
# -------------------------------------------------------------
MODELOS = [
    'llama-3.1-8b-instant',
    'llama-3.3-70b-versatile',
    'deepseek-r1-distill-llama-70b'
]

def configurar_pagina():
    st.title("Mi chat de IA 🤖")  # <-- Título dentro del chat
    st.sidebar.title("Configuración de la IA")
    elegirModelo = st.sidebar.selectbox("Elegí un modelo", options=MODELOS, index=0)
    return elegirModelo


# -------------------------------------------------------------
# CREAR CLIENTE DE GROQ (USA LA API KEY DE secrets.toml)
# -------------------------------------------------------------
def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

clienteUsuario = crear_usuario_groq()


# -------------------------------------------------------------
# MANEJO DEL CHAT
# -------------------------------------------------------------
def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})


def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])


def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat:
        mostrar_historial()


# -------------------------------------------------------------
# FUNCIÓN PARA ENVIAR MENSAJE A GROQ
# -------------------------------------------------------------
def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    respuesta = cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True
    )

    texto_final = ""
    for chunk in respuesta:  # el streaming devuelve pedacitos
        parte = chunk.choices[0].delta.content or ""
        texto_final += parte

    return texto_final


# -------------------------------------------------------------
# EJECUCIÓN
# -------------------------------------------------------------
modelo = configurar_pagina()
inicializar_estado()
area_chat()

mensaje = st.chat_input("Escribí tu mensaje:")

if mensaje:
    actualizar_historial("user", mensaje, "🧑‍💻")  # guardamos el mensaje del usuario

    # respuesta de la IA
    respuesta = configurar_modelo(clienteUsuario, modelo, mensaje)

    actualizar_historial("assistant", respuesta, "🤖")

    # Refrescar el chat para que la respuesta aparezca
    st.rerun()
