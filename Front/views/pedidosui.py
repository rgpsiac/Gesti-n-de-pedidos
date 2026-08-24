import streamlit as st
import pandas as pd
from api_client import APIClient
import plotly.express as px
import time

st.title("Gestión de Pedidos", text_alignment='center')
cliente_api = APIClient()
with st.spinner("Obteniendo Pedidos..."):
    ordenes = cliente_api.obtener_ordenes()
    metricas = cliente_api.traer_metricas()

kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    kpi_pedidos = metricas.get("pedidos",0)
    st.metric(
        label="Pedidos",
        value=kpi_pedidos,
        border=True,
        width='stretch'
    )

with kpi2:
    kpi_entregados = metricas.get("pedidos entregados",0)
    st.metric(
        label="Entregados",
        value=kpi_entregados,
        border=True,
        width='stretch'
    )

with kpi3:
    kpi_pendientes = metricas.get("pedidos pendientes")
    st.metric(
        label="Pendientes",
        value=kpi_pendientes,
        border=True,
        width='stretch'
    )


if len(ordenes) == 0:
    st.info("No hay órdenes registradas en el sistema")
else:

    st.subheader("Registro de Pedidos")
    df = pd.DataFrame(ordenes)

    columnas_editor_ordenes = ["Id Orden", "Id Cliente", "Cliente", "Teléfono", "Canal", "Tipo de Pedido", "Estatus", "Fecha de Entrega", "Total", "Pagado", "Deuda", "Asignacion Orden"]

    df_ordenes = df[columnas_editor_ordenes].drop_duplicates(subset="Id Orden").reset_index(drop=True)
    if "Explorar" not in df_ordenes.columns:
        df_ordenes.insert(0,"Explorar",False)
    df_ordenes = df_ordenes.sort_values("Id Orden").reset_index(drop=True)

    df_editado = st.data_editor(
        data=df_ordenes,
        use_container_width=True,
        hide_index=True,
        key="editor_ordenes",
        column_config={
            "Id Orden": None,
            "Cliente": st.column_config.TextColumn("Nombre del cliente", disabled=False),
            "Teléfono": st.column_config.NumberColumn("Celular"),
            "Canal": st.column_config.TextColumn("Canal de entrada"),
            "Tipo de Pedido": st.column_config.TextColumn("Tipo de Pedido"),
            "Total": st.column_config.NumberColumn("Precio", format="$%d"),
            "Fecha de Entrega": st.column_config.SelectboxColumn("Fecha de Entrega",disabled=False, help="Elige la fecha por la que quieras actualizar el pedido", options=["Lunes 24 de agosto", "Viernes 28 de agosto", "Lunes 31 de agosto", "Viernes 4 de septiembre", "Lunes 7 de septiembre", "Viernes 11 de septiembre"]),
            "Pagado": st.column_config.NumberColumn("Pagado", format="$%d", min_value=0, disabled=False),
            "Deuda": st.column_config.NumberColumn("Deuda", format="$%d", min_value=0),
            "Estatus": st.column_config.SelectboxColumn("Estatus", help="Cambia el Estatus según el avance del pedido", required=True, options=["Pendiente", "En proceso", "Empacado", "Entregado", "Devuelto por cambios"]),
            "Asignacion Orden": st.column_config.TextColumn("Asignacion"),
            "Explorar": st.column_config.CheckboxColumn(label="Ver detalles",width='small', pinned=True, default=False),
            "Id Cliente": None},
            disabled=["Id Orden","Teléfono","Tipo de Pedido","Total","Deuda", "Id Cliente", "Asignacion Orden"])

    if st.button("Guardar Cambios"):
        cambios = st.session_state["editor_ordenes"].get("edited_rows",{})
        if not cambios:
            st.warning("No hay cambios para guardar")
        else:
            with st.spinner("Guardando cambios..."):
                for idx_fila, cambio in cambios.items():
                    id_orden = df_ordenes.iloc[idx_fila]["Id Orden"]
                    if "Estatus" in cambio:
                        nuevo_estado = cambio["Estatus"]
                        cliente_api.actualizar_estado(id_orden=id_orden, nuevo_estado=nuevo_estado)
                    if "Cliente" in cambio:
                        nuevo_nombre = cambio["Cliente"]
                        cliente_api.actualizar_nombre(id_orden=id_orden, nuevo_nombre=nuevo_nombre)
                    if "Fecha de Entrega" in cambio:
                        nueva_fecha = cambio["Fecha de Entrega"]
                        cliente_api.actualizar_fecha_entrega(id_orden=id_orden, nueva_fecha=nueva_fecha)
                    if "Pagado" in cambio:
                        pago = cambio["Pagado"]
                        cliente_api.actualizar_pago(id_orden=id_orden, pago=pago)
                del st.session_state["editor_ordenes"]
            st.toast("Cambios hechos correctamente")
            time.sleep(1)
            st.rerun()

    st.divider()

    fila_marcada = df_editado[df_editado["Explorar"] == True]
    if not fila_marcada.empty:
        id_selected = fila_marcada.iloc[0]["Id Orden"]

        columnas_editor_detalles = ["Id Orden", "Id detalles", "Producto", "Detalle", "Cantidad", "Pertenencia", "Asignacion Detalles"]

        df_detalles = df[df["Id Orden"] == id_selected]
        df_detalles = df_detalles[columnas_editor_detalles]
        df_detalles = df_detalles.sort_values("Id detalles").reset_index(drop=True)
        opciones_disponbiles = df["Detalle"].unique().tolist()

        st.subheader(f"Detalles de la orden {id_selected}")

        fig_detalles_orden = px.sunburst(
            data_frame=df_detalles,
            path=["Pertenencia", "Producto", "Detalle"],
            values="Cantidad",
            title="Armado de Kits"
        )
        fig_detalles_orden.update_layout(
            height = 600,
            font = dict(size=18),
            margin=dict(t=30, l=10, r=10, b=10)
        )
        st.plotly_chart(figure_or_data=fig_detalles_orden, use_container_width=True)

        st.data_editor(
            data=df_detalles,
            use_container_width=True,
            hide_index=True,
            key="editor_detalles",
            column_config={
                "Id Orden": st.column_config.NumberColumn("Id Orden"),
                "Id detalles": None,
                "Producto": st.column_config.TextColumn("Producto"),
                "Detalle": st.column_config.SelectboxColumn("Detalle", help="Puedes cambiar el color o talla del producto si es necesario", options=opciones_disponbiles),
                "Cantidad": st.column_config.NumberColumn("Cantidad", help="Puedes cambiar la cantidad del producto si es necesario"),
                "Asignacion Detalles": st.column_config("Asignacion")
            },
            disabled=["Id Orden", "Id detalles", "Producto", "Pertenencia", "Asignacion Detalles"]
        )
        if st.button("Guardar cambios"):
            cambios = st.session_state["editor_detalles"].get("edited_rows",{})
            if not cambios:
                st.warning("No hay cambios por guardar")
            else:
                with st.spinner("Guardando cambios..."):
                    for idx_fila, cambio in cambios.items():
                        id_detalle_selected = df_detalles.iloc[idx_fila]["Id detalles"]
                        n_detalle = cambio.get("Detalle")
                        n_cantidad = cambio.get("Cantidad")
                        cliente_api.actualizar_detalle_orden(
                            id_detalle=id_detalle_selected,
                            nuevo_detalle=n_detalle,
                            nueva_cantidad=n_cantidad
                        )
                    del st.session_state["editor_detalles"]
                st.toast("Cambios hechos correctamente")
                time.sleep(1)
                st.rerun()

    else:
        st.subheader("Detalles de la orden")
        st.info("Selecciona una orden en la tabla de registros para ver sus detalles en esta sección")