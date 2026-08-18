import streamlit as st

st.set_page_config(
    page_title="Dashboard del Negocio",
    layout='wide',
    initial_sidebar_state='expanded'
)

def iniciar_sesion():
    st.title("Acceso a la app")
    with st.form("Login"):
        usuario = st.text_input(
            label="Ingresa tu usuario",
            key="usuario_login"
        )
        password = st.text_input(
            label="Ingresa tu contraseña",
            key="usuario_password")
        submit = st.form_submit_button("Acceder")

        if submit:
            if (usuario == "Chirris" or usuario == "Chiji") and password == "170123":
                st.session_state['autenticado'] = True
                st.session_state['usuario'] = usuario
                st.rerun()
            else:
                st.error("Credenciales incorrectas")

if 'autenticado' not in st.session_state or not st.session_state['autenticado']:
    iniciar_sesion()
else:
    st.sidebar.title(f"Hola, {st.session_state['usuario']}")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state['autenticado'] = False
        st.rerun()

    paginas = [
        st.Page("views/principalui.py", title="Resumen General"),
        st.Page("views/pedidosui.py", title="Gestión de Pedidos"),
        st.Page("views/inventariosui.py", title="Gestión de Inventarios")
    ]
    navegador = st.navigation(pages=paginas,
                              position='top')
    navegador.run()