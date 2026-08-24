import streamlit as st
import plotly.express as px
import pandas as pd
from api_client import APIClient

st.title(
    "Dashboard General",
    text_alignment='center'
)

cliente_api = APIClient()
with st.spinner("Cargando dashboard..."):
    metricas = cliente_api.traer_metricas()
    if not metricas:
        st.error("Ha ocurrido un problema con el servidor")
        st.stop()

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    kpi_pedidos = metricas.get("pedidos",0)
    st.metric(
        label="Pedidos",
        value=kpi_pedidos,
        border=True,
        width='stretch'
    )

with kpi2:
    kpi_ingresos = metricas.get("Ingresos",0)
    st.metric(
        label="Ingresos",
        value=kpi_ingresos,
        border=True,
        width='stretch',
        format='dollar'
    )


with kpi3:
    kpi_adelantos = metricas.get("adelantos",0)
    st.metric(
        label="Adelantos",
        value=kpi_adelantos,
        border=True,
        width='stretch',
        format='dollar'
    )

with kpi4:
    kpi_deudas = metricas.get("deudas",0)
    st.metric(
        label="Deudas",
        value=kpi_deudas,
        border=True,
        width='stretch',
        format='dollar'
    )

with kpi5:
    kpi_utilidad = metricas.get("utilidad neta",0)
    st.metric(
        label="Utilidad Neta",
        value=kpi_utilidad,
        border=True,
        width='stretch',
        format='dollar'
    )

with kpi6:
    kpi_costos = metricas.get("costos",0)
    st.metric(
        label="Costos",
        value=kpi_costos,
        border=True,
        width='stretch',
        format='dollar'
    )

tabla1, grafico1 = st.columns(2)
with tabla1:
    pedidos_proximos = pd.DataFrame(columns=["Nombre","Fecha de Entrega"])
    with st.container():
        st.write("Trabajando!")
        st.dataframe(
            data=pedidos_proximos,
            width='content',
            use_container_width=True,
            hide_index=True
            )

with grafico1:
    pedidos_cubiertos = metricas.get("Pedidos cubiertos",{})

    data_pedidos_cubiertos = pd.DataFrame(
        list(pedidos_cubiertos.items()),
        columns=["Estado","Valor"])

    if not data_pedidos_cubiertos.empty:
        graph_pedidos_cubiertos = px.pie(
            data_frame=data_pedidos_cubiertos,
            names=data_pedidos_cubiertos["Estado"],
            values=data_pedidos_cubiertos["Valor"]
        )
        st.plotly_chart(
            figure_or_data=graph_pedidos_cubiertos,
            use_container_width=True,
            width='content'
        )
    else:
        st.info("Cuando haya pedidos próximos aparecerán aquí")

st.write("Otro gráfico próximamente!")