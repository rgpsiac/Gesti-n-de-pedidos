import streamlit as st
import plotly.express as px
from datetime import date
from api_client import APIClient
import pandas as pd

st.title("Gestión del Inventario")
cliente_api = APIClient()
datos = cliente_api.traer_productos()
if datos.empty:
    datos["producto"] = "sin productos"
    datos["detalle"] = "sin detalles"
def agregar_fila():
    st.session_state.datos_formulario += 1


col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="Pedidos",
        value=0,
        border=True,
        width='stretch',
        delta_description="Trabajando!"
        )
with col2:
    st.metric(
        label="Costos",
        value=0,
        border=True,
        height='stretch',
        delta_description="Trabajando!"
    )
with col3:
    st.metric(
        label="Items faltantes",
        value=0,
        border=True,
        width='stretch',
        delta_description="Trabajando!"
    )

with st.popover(label="Agregar stock",
                type='primary',
                disabled=False,
                use_container_width=True,
                width='content',
                key="popover_forms_stock"):
    if "datos_formulario" not in st.session_state:
        st.session_state.datos_formulario = 1
    for i in range(st.session_state.datos_formulario):
        colp, cold, colc, colcu = st.columns(4)
        with colp:
            producto = st.selectbox(label=f"Producto {i}", options=["Mandil", "Cuchillo", "Guantes de plástico", "Guantes de nitrilo", "Bolsa", "Pijama quirúrgica antifluidos", "Gorro quirúrgico antifluidos"], key=f"producto_{i}")
            detalles = datos[datos["producto"] == producto]["detalle"]
        with cold:
            st.selectbox(label=f"Detalle {i}", options=detalles, key=f"detalle_{i}")
        with colc:
            st.number_input(label=f"Cantidad {i}", min_value=1, value='min',key=f"cantidad_{i}")
        with colcu:
            st.number_input(label=f"Costo Unitario {i}", min_value=0, step=0.10, format="$%d", key=f"costou_{i}")

    fila, guardado = st.columns(2)
    with fila:
        st.button("+ Agregar fila", on_click=agregar_fila, use_container_width=True)
    with guardado:
        if st.button("Agregar stock", type='primary', use_container_width=True):
            payload = []
            for i in range(st.session_state.datos_formulario):
                registro = {
                    "Producto": st.session_state.get(f"producto_{i}"),
                    "Detalle": st.session_state.get(f"detalle_{i}"),
                    "Cantidad": st.session_state.get(f"cantidad_{i}"),
                    "Costo Unitario": st.session_state.get(f"costou_{i}"),
                    "Fecha de registro": str(date.today())
                }
                payload.append(registro)
            cliente_api.agregar_stock(datos=payload)
            st.toast("Stock agregado exitosamente")