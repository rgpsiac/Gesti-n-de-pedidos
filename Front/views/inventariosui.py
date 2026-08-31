import streamlit as st
import plotly.express as px
from datetime import date
from api_client import APIClient
import pandas as pd

st.title("Gestión del Inventario", text_alignment='center')
with st.spinner("Cargando..."):
    cliente_api = APIClient()
    datos = cliente_api.traer_productos()
    metricas = cliente_api.traer_metricas()

    if datos.empty:
        datos["producto"] = "sin productos"
        datos["detalle"] = "sin detalles"
    def agregar_fila():
        st.session_state.datos_formulario += 1
    def eliminar_fila():
        if st.session_state.datos_formulario > 1:
            st.session_state.datos_formulario -= 1


    productos_cubiertos = metricas.get("Items faltantes",{})
    data_productos_cubiertos = pd.DataFrame(productos_cubiertos)
    stock_actual = metricas.get("Stock actual", {})
    data_stock_actual = pd.DataFrame(stock_actual)

col1, col2, col3 = st.columns(3)
with col1:
    kpi_pedidos = metricas.get("pedidos",0)
    st.metric(
        label="Pedidos",
        value=kpi_pedidos,
        border=True,
        width='stretch'
        )
    
with col2:
    kpi_costos = metricas.get("costos",0)
    st.metric(
        label="Costos",
        value=kpi_costos,
        border=True,
        height='stretch',
        format='dollar'
    )

with col3:
    faltantes = metricas.get("Items",0)
    kpi_items_faltantes = faltantes.get("Pendiente",0)
    st.metric(
        label="Items faltantes",
        value=kpi_items_faltantes,
        border=True,
        width='stretch'
    )

if not data_productos_cubiertos.empty:
    graph_productos_cubiertos = px.treemap(
        data_frame=data_productos_cubiertos,
        path=["Producto", "Detalle"],
        values="Cantidad",
        title="Items Faltantes",
        color="Producto"
    )
    graph_productos_cubiertos.update_traces(textinfo='label+value')
    st.plotly_chart(
        figure_or_data=graph_productos_cubiertos,
        use_container_width=True
    )
else:
    st.info("Aquí aparecerán los items faltantes")

if not data_stock_actual.empty:
    graph_stock_actual = px.treemap(
        data_frame=data_stock_actual,
        path=["Producto", "Detalle"],
        values="Disponibles",
        title="Stock actual",
        color="Producto"
    )
    graph_stock_actual.update_traces(textinfo='label+value')
    st.plotly_chart(
        figure_or_data=graph_stock_actual,
        use_container_width=True
    )

with st.popover(label="Agregar stock",
                type='primary',
                disabled=False,
                use_container_width=False,
                width='stretch',
                key="popover_forms_stock"):
    if "datos_formulario" not in st.session_state:
        st.session_state.datos_formulario = 1
    with st.container(height=300):
        for i in range(st.session_state.datos_formulario):
            colp, cold, colc, colcu = st.columns(4)
            with colp:
                producto = st.selectbox(label=f"Producto {i}", options=datos["producto"].unique(), key=f"producto_{i}")
                detalles = datos[datos["producto"] == producto]["detalle"].tolist()
            with cold:
                st.selectbox(label=f"Detalle {i}", options=detalles, key=f"detalle_{i}")
            with colc:
                st.number_input(label=f"Cantidad {i}", min_value=1, value='min',key=f"cantidad_{i}")
            with colcu:
                st.number_input(label=f"Costo Unitario ($) {i}", min_value=0.0, value='min', step=0.10, format="%.2f", key=f"costou_{i}")

    fila, guardado, fila_del = st.columns(3)
    with fila:
        st.button("+ Agregar fila", on_click=agregar_fila, use_container_width=True)
    with fila_del:
        st.button("- Eliminar fila", on_click=eliminar_fila, use_container_width=True)
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
            st.session_state.datos_formulario = 1
            st.rerun()