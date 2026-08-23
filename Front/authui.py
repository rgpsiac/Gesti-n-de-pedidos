import streamlit as st

st.set_page_config(
    page_title="Dashboard del Negocio",
    layout='wide',
    initial_sidebar_state='expanded'
)
admin1 = st.secrets["ADMIN1"]
admin2 = st.secrets["ADMIN2"]
psswrd = st.secrets["KEY"]

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
            if (usuario == admin1 or usuario == admin2) and password == psswrd:
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
        st.Page("views/pedidosui.py", title="Pedidos"),
        st.Page("views/inventariosui.py", title="Inventarios")
    ]
    navegador = st.navigation(pages=paginas, position='top')
    navegador.run()